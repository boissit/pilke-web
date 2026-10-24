"""Pilke's print kit: every file in the Drive folder "Pilke – painotuotteet", rebuilt.

    tools/print-kit/build.sh            # makes the venv on first run, then this

Reads the brand and pictures of both repositories and writes `tools/print-kit/out/`
(gitignored), one directory per Drive folder, with the same names:

    out/Brändi/   wordmarks (PNG + SVG), the app icon, sparkles, the palette
    out/Kuvat/    the site's photographs, the app's screens unframed and framed
    out/QR/       QR codes, ink and white on transparency, PNG + SVG
    out/drive/    the copies that go into Drive as files (small enough for the connector)
    out/slides/   the one-slide .pptx each Slides file is first made from
    out/manifest.json   every file, its size and SHA-256, for the upload step

The same inputs give the same bytes, so a rerun with nothing changed changes nothing,
and `manifest.json` is what says which files a re-upload has to replace.

`docs/print-kit.md` says what each file is for and how the Drive folder and the two
Slides files are refreshed from here.
"""
import argparse
import hashlib
import io
import json
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import qrcode
import resvg_py
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.dirname(os.path.dirname(HERE))
APP = os.environ.get('PILKE_APP', os.path.join(os.path.dirname(WEB), 'pilke-app'))
OUT = os.environ.get('PRINT_KIT_OUT', os.path.join(HERE, 'out'))
CACHE = os.path.join(HERE, '.cache')

BRAND = os.path.join(WEB, 'src', 'assets', 'brand')
PHOTOS = os.path.join(WEB, 'src', 'assets', 'photos')
SCREENS = os.path.join(WEB, 'src', 'assets', 'screens')
FONTS = os.path.join(WEB, 'public', 'fonts')
STORE = os.path.join(APP, 'tools', 'store-assets')

# The site's tokens (src/styles/global.css) and the app's spark colours
# (src/components/sparkleArtwork.ts). Names are the ones the palette sheet prints.
PALETTE = [
    # (name on the sheet, hex, where it comes from)
    ('Pohja', '#FFF8F4', '--ground'),
    ('Persikka', '#FFE3DA', '--brand-background'),
    ('Koralli', '#FFA98C', '--brand-main'),
    ('Ruusu', '#F4504F', 'kipinä, sytytetty'),
    ('Teksti', '#3A2E2B', '--text'),
    ('Pehmeä teksti', '#6E5F5A', '--text-soft'),
    ('Muste', '#3C3C3C', '--ink, wordmark'),
    ('Valkoinen', '#FFFFFF', '--surface'),
    ('Kipinä persikalla', '#FCD1C3', '--sparkle-on-peach'),
    ('Kipinä korallilla', '#FFBDA6', '--sparkle-on-coral'),
    ('Minttu', '#A8DACB', '--success'),
    ('Minttupohja', '#E4F3EE', '--mint-ground'),
    ('Kortti sininen', '#DCFBFF', '--card-sent'),
    ('Kortti pinkki', '#FFEAFC', '--card-received'),
    ('Kortti keltainen', '#FFF8C2', '--card-feedback'),
    ('Viiva', '#F0DDD5', '--rule'),
]
HEX = {name: hx for name, hx, _ in PALETTE}

SPARKLES = [
    ('ruusu', '#F4504F'),
    ('koralli', '#FFA98C'),
    ('persikka', '#FCD1C3'),
    ('vaalea-koralli', '#FFBDA6'),
    ('harmaa', '#D9D2D4'),
    ('teksti', '#3A2E2B'),
    ('valkoinen', '#FFFFFF'),
]

WORDMARKS = [
    # (file suffix, letter colour); the sparkle stays rose in every variant
    ('muste', '#3C3C3C'),
    ('valkoinen', '#FFFFFF'),
    ('koralli', '#FFA98C'),
]

QR = [
    ('pilke-app', 'https://pilke.app'),
    ('pilke-app-beta', 'https://pilke.app/#beta'),
    # From pilke-app/eas.json (ascAppId) and app.config.ts (the Android package).
    # Neither listing is public yet: both URLs answer 404 until the apps are released.
    ('app-store', 'https://apps.apple.com/fi/app/id6806932833'),
    ('google-play', 'https://play.google.com/store/apps/details?id=com.boissit.pilkeapp'),
]
QR_COLOURS = [('muste', '#3A2E2B'), ('valkoinen', '#FFFFFF')]

# The iPhone captures the store images are built from, and their Finnish names.
IPHONE_SHOTS = [
    ('treffit', 'treffit'),
    ('invitation', 'treffikutsu'),
    ('invitation-chosen', 'treffikutsu-valittu'),
    ('date', 'sovitut-treffit'),
    ('kalenteri', 'kalenteri'),
    ('kipinat', 'kipinat'),
    ('platter', 'ehdokkaat'),
]
# Site screens that have no iPhone capture: Android stills, navigation bar cut off as
# `Phone.astro` cuts it.
SITE_SHOTS = [
    ('story', 'persoonallisuuskysely'),
    ('feedback', 'palaute'),
    ('asetukset', 'asetukset-turvallisuus'),
]
ANDROID_NAV_ROWS = 136

SPARKLE_PATH = None  # read from src/components/sparkleArtwork.ts
SPARKLE_BOX = None

written = []


def out(*parts):
    path = os.path.join(OUT, *parts)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    written.append(path)
    return path


def rgb(hx):
    hx = hx.lstrip('#')
    return tuple(int(hx[i:i + 2], 16) for i in (0, 2, 4))


def bleed(im):
    """The colour under a transparent pixel, filled in from the nearest drawn pixels.

    A transparent pixel's colour is invisible in the PNG, but Google's PDF export
    re-encodes every picture as a JPEG plus a separate mask, and a JPEG smears that
    hidden colour, black by default, into the antialiased edge: a thin dark rim round
    every sparkle on a printed card. Filled with the edge's own colour, the rim is
    the drawing's colour again. The alpha, and every visible pixel, stay as they are."""
    import numpy as np
    if im.mode != 'RGBA':
        return im
    arr = np.asarray(im).astype(np.float32)
    a = arr[..., 3] / 255
    if a.min() > 0 or a.max() == 0:
        return im
    rgb = arr[..., :3]
    h, w = a.shape
    planes = [rgb[..., c] * a for c in range(3)] + [a]
    fill = rgb.copy()
    known = a > 0
    k = 1
    while not known.all() and (w >> k) >= 1 and (h >> k) >= 1:
        small = (max(1, w >> k), max(1, h >> k))
        up = [np.asarray(Image.fromarray(pl, 'F').resize(small, Image.BOX).resize((w, h), Image.BILINEAR))
              for pl in planes]
        ok = (up[3] > 1e-4) & ~known
        for c in range(3):
            fill[..., c][ok] = up[c][ok] / up[3][ok]
        known |= ok
        k += 1
    out = np.dstack([np.clip(fill, 0, 255), arr[..., 3]]).round().astype(np.uint8)
    return Image.fromarray(out, 'RGBA')


def save_png(im, path):
    # No timestamps or other metadata, so the bytes depend on the pixels alone.
    bleed(im).save(path, format='PNG', optimize=True)


def save_jpeg(im, path, quality=90):
    im.convert('RGB').save(path, format='JPEG', quality=quality, optimize=True, progressive=True,
                           subsampling=0)


def render_svg(svg_text, width):
    png = resvg_py.svg_to_bytes(svg_string=svg_text, width=width)
    return Image.open(io.BytesIO(bytes(png))).convert('RGBA')


# ───────────────────────────── fonts ─────────────────────────────

def font(face, size, weight):
    """The site's own variable woff2, as a TTF PIL can read, at a weight."""
    os.makedirs(CACHE, exist_ok=True)
    ttf = os.path.join(CACHE, f'{face}-latin.ttf')
    if not os.path.exists(ttf):
        f = TTFont(os.path.join(FONTS, f'{face}-latin.woff2'))
        f.flavor = None
        f.save(ttf)
    ft = ImageFont.truetype(ttf, size)
    try:
        ft.set_variation_by_axes([weight])
    except OSError:
        pass
    return ft


# ───────────────────────────── brand ─────────────────────────────

def read_sparkle():
    global SPARKLE_PATH, SPARKLE_BOX
    src = open(os.path.join(WEB, 'src', 'components', 'sparkleArtwork.ts')).read()
    SPARKLE_PATH = re.search(r"SPARKLE_PATH =\s*'([^']+)'", src).group(1)
    m = re.search(r'SPARKLE_BOX = \{ x: ([\d.]+), y: ([\d.]+), width: ([\d.]+), height: ([\d.]+)', src)
    SPARKLE_BOX = tuple(float(v) for v in m.groups())


def sparkle_svg(fill):
    x, y, w, h = SPARKLE_BOX
    # Square box, the path centred in it, as `Sparkle.astro` draws it.
    side = max(w, h)
    x -= (side - w) / 2
    y -= (side - h) / 2
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x:.3f} {y:.3f} {side:.3f} {side:.3f}">'
            f'<path fill="{fill}" d="{SPARKLE_PATH}"/></svg>\n')


def wordmarks():
    ink = open(os.path.join(BRAND, 'pilke-wordmark.svg')).read()
    white = open(os.path.join(BRAND, 'pilke-wordmark-white.svg')).read()
    for suffix, colour in WORDMARKS:
        if suffix == 'muste':
            svg = ink
        elif suffix == 'valkoinen':
            svg = white
        else:
            svg = ink.replace('fill="#3C3C3C"', f'fill="{colour}"', 1)
        assert 'fill="#F4504F"' in svg, 'the wordmark lost its rose sparkle'
        with open(out('Brändi', f'pilke-wordmark-{suffix}.svg'), 'w') as f:
            f.write(svg)
        # 4000 px wide is 34 cm at 300 dpi: a wordmark as wide as an A3 sheet.
        save_png(render_svg(svg, 4000), out('Brändi', f'pilke-wordmark-{suffix}.png'))
        # A small one for the Slides library, and for anything printed at badge size.
        save_png(render_svg(svg, 1200), out('Brändi', 'pienet', f'pilke-wordmark-{suffix}-1200.png'))


def app_icon():
    svg = open(os.path.join(APP, 'assets', 'brand', 'icon.svg')).read()
    im = render_svg(svg, 1024)
    save_png(im.convert('RGB'), out('Brändi', 'pilke-sovelluskuvake.png'))
    # The icon as a phone shows it: corners rounded at iOS's 22.37 %.
    big = render_svg(svg, 4096)
    mask = Image.new('L', big.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, big.width - 1, big.height - 1), radius=int(4096 * 0.2237), fill=255)
    big.putalpha(mask)
    save_png(big.resize((1024, 1024), Image.LANCZOS), out('Brändi', 'pilke-sovelluskuvake-pyorea.png'))


def sparkles():
    for name, colour in SPARKLES:
        svg = sparkle_svg(colour)
        with open(out('Brändi', 'kipinat', f'kipina-{name}.svg'), 'w') as f:
            f.write(svg)
        save_png(render_svg(svg, 1200), out('Brändi', 'kipinat', f'kipina-{name}.png'))
    # The counter's row: three sparkles, two lit and one on its way, as the app draws
    # `Kipinät:` beside them.
    row = sparkle_row()
    save_png(row, out('Brändi', 'kipinat', 'kipinarivi.png'))
    # A scatter for a background, the hero's placements in its peach and on coral.
    for name, colour in [('persikka', '#FCD1C3'), ('vaalea-koralli', '#FFBDA6'), ('valkoinen', '#FFFFFF')]:
        save_png(scatter(colour), out('Brändi', 'kipinat', f'kipinaparvi-{name}.png'))


def sparkle_im(colour, px, rotate=0):
    im = render_svg(sparkle_svg(colour), px * 2)
    if rotate:
        im = im.rotate(-rotate, resample=Image.BICUBIC, expand=False)
    return im.resize((px, px), Image.LANCZOS)


def sparkle_row():
    s = 600
    gap = -40
    im = Image.new('RGBA', (3 * s + 2 * gap, s), (0, 0, 0, 0))
    grey = sparkle_im('#D9D2D4', s)
    core = sparkle_im('#F4504F', int(s * 0.44))
    grey.alpha_composite(core, ((s - core.width) // 2, (s - core.height) // 2))
    for k, piece in enumerate([grey, sparkle_im('#F4504F', s), sparkle_im('#F4504F', s)]):
        im.alpha_composite(piece, (k * (s + gap), 0))
    return im


def scatter(colour):
    # The hero card's wide placements (index.astro), in a 1600 x 1000 card.
    W, H = 3200, 2000
    k = 2.0
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    placements = [
        (100, 14, 0.36 * 1600, 40), (38, -26, 0.36 * 1600 + 116, 120), (132, -18, 40, 1000 - 30 - 132),
        (44, 30, 190, 1000 - 130 - 44), (76, 36, 0.415 * 1600, 1000 - 90 - 76), (90, 10, 1600 - 40 - 90, 30),
        (34, -32, 1600 - 150 - 34, 56), (66, -38, 1600 - 40 - 66, 1000 - 30 - 66),
    ]
    for size, rot, x, y in placements:
        px = int(size * k * 1.6)
        im.alpha_composite(sparkle_im(colour, px, rot), (int(x * k), int(y * k)))
    return im


def palette_sheet():
    cols, chip_w, chip_h, pad = 4, 900, 620, 80
    rows = (len(PALETTE) + cols - 1) // cols
    W = cols * chip_w + (cols + 1) * pad
    H = rows * (chip_h + 300) + pad * 2 + 260
    im = Image.new('RGB', (W, H), rgb('#FFFFFF'))
    d = ImageDraw.Draw(im)
    title = font('Fredoka', 140, 600)
    name_f = font('Figtree', 64, 700)
    hex_f = font('Figtree', 58, 500)
    note_f = font('Figtree', 40, 500)
    d.text((pad, pad), 'Pilke – värit', font=title, fill=rgb(HEX['Teksti']))
    for i, (name, hx, src) in enumerate(PALETTE):
        r, c = divmod(i, cols)
        x = pad + c * (chip_w + pad)
        y = pad + 260 + r * (chip_h + 300)
        d.rounded_rectangle((x, y, x + chip_w, y + chip_h), radius=64, fill=rgb(hx),
                            outline=rgb(HEX['Viiva']), width=4)
        d.text((x + 8, y + chip_h + 30), name, font=name_f, fill=rgb(HEX['Teksti']))
        R, G, B = rgb(hx)
        d.text((x + 8, y + chip_h + 112), f'{hx}   RGB {R} {G} {B}', font=hex_f, fill=rgb(HEX['Pehmeä teksti']))
        d.text((x + 8, y + chip_h + 190), src, font=note_f, fill=rgb(HEX['Pehmeä teksti']))
    save_png(im, out('Brändi', 'paletti.png'))
    # The same sheet as vector, set in the site's faces where they are installed.
    cw, ch, gap = 180, 120, 20
    rows_svg = []
    for i, (name, hx, src) in enumerate(PALETTE):
        r, c = divmod(i, cols)
        x, y = gap + c * (cw + gap), 80 + r * (ch + 90)
        rows_svg.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="14" fill="{hx}" stroke="#F0DDD5" stroke-width="1.5"/>'
                        f'<text x="{x + 2}" y="{y + ch + 24}" class="n">{name}</text>'
                        f'<text x="{x + 2}" y="{y + ch + 46}" class="h">{hx} · RGB {" ".join(str(v) for v in rgb(hx))}</text>'
                        f'<text x="{x + 2}" y="{y + ch + 64}" class="s">{src}</text>')
    svg_w, svg_h = gap + cols * (cw + gap), 80 + rows * (ch + 90)
    with open(out('Brändi', 'paletti.svg'), 'w') as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}" width="{svg_w * 4}" height="{svg_h * 4}">'
                '<style>text{font-family:Figtree,Arial,sans-serif;fill:#3A2E2B}.t{font-family:Fredoka,Arial,sans-serif;'
                'font-weight:600;font-size:30px}.n{font-weight:700;font-size:15px}.h{font-size:13px;fill:#6E5F5A}'
                '.s{font-size:10px;fill:#6E5F5A}</style><rect width="100%" height="100%" fill="#FFFFFF"/>'
                f'<text x="{gap}" y="50" class="t">Pilke – värit</text>{"".join(rows_svg)}</svg>\n')
    with open(out('Brändi', 'paletti.txt'), 'w') as f:
        f.write('Pilke – värit (pilke-web/src/styles/global.css)\n\n')
        for name, hx, src in PALETTE:
            R, G, B = rgb(hx)
            f.write(f'{name:<20} {hx}   RGB {R:>3} {G:>3} {B:>3}   {src}\n')
        f.write('\nFontit: Fredoka 600 (otsikot), Figtree 400–700 (leipäteksti). Molemmat ovat Google Fonts -fontteja.\n')


# ───────────────────────────── QR ─────────────────────────────

def qr_codes():
    for name, url in QR:
        q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=4, box_size=1)
        q.add_data(url)
        q.make(fit=True)
        m = q.get_matrix()
        n = len(m)
        for cname, colour in QR_COLOURS:
            s = max(1, 1600 // n)
            im = Image.new('P', (n * s, n * s), 0)
            # The transparent entry carries the modules' own colour: see bleed().
            im.putpalette(list(rgb(colour)) * 2)
            d = ImageDraw.Draw(im)
            for y, row in enumerate(m):
                for x, v in enumerate(row):
                    if v:
                        d.rectangle((x * s, y * s, x * s + s - 1, y * s + s - 1), fill=1)
            im.save(out('QR', f'qr-{name}-{cname}.png'), format='PNG', optimize=True, transparency=0)
            rects = ''.join(f'M{x} {y}h1v1h-1z' for y, row in enumerate(m) for x, v in enumerate(row) if v)
            with open(out('QR', f'qr-{name}-{cname}.svg'), 'w') as f:
                f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {n} {n}" shape-rendering="crispEdges">'
                        f'<title>{url}</title><path fill="{colour}" d="{rects}"/></svg>\n')
    with open(out('QR', 'osoitteet.txt'), 'w') as f:
        for name, url in QR:
            f.write(f'qr-{name}-*: {url}\n')
        f.write('\napp-store ja google-play: kaupan sivut avautuvat sovelluksen julkaisun myötä (nyt 404). '
                'Painata nämä koodit julkaisun jälkeen.\n')


# ───────────────────────────── store badges ─────────────────────────────

# The stores' own Finnish badges, from their official badge pages: Apple's marketing
# toolbox (developer.apple.com/app-store/marketing/guidelines links to it) and Google
# Play's badge generator. Fetched once into .cache/, so later builds run offline.
# Both stores allow a badge only beside a working link to the listing, and neither
# listing is public yet: these are for after the release.
BADGES = [
    ('app-store-musta.svg', 'https://toolbox.marketingtools.apple.com/api/v2/badges/download-on-the-app-store/black/fi-fi'),
    ('app-store-valkoinen.svg', 'https://toolbox.marketingtools.apple.com/api/v2/badges/download-on-the-app-store/white/fi-fi'),
    ('google-play.png', 'https://play.google.com/intl/en_us/badges/static/images/badges/fi_badge_web_generic.png'),
]


def badges():
    import urllib.request
    os.makedirs(os.path.join(CACHE, 'badges'), exist_ok=True)
    for name, src in BADGES:
        cached = os.path.join(CACHE, 'badges', name)
        if not os.path.exists(cached):
            with urllib.request.urlopen(src, timeout=30) as r, open(cached + '.part', 'wb') as f:
                f.write(r.read())
            os.replace(cached + '.part', cached)
        shutil.copyfile(cached, out('Brändi', 'kauppamerkit', name))
        if name.endswith('.svg'):
            save_png(render_svg(open(cached).read(), 1200), out('Brändi', 'kauppamerkit', name.replace('.svg', '.png')))
        shutil.copyfile(cached, out('drive', 'Brändi', 'Kauppamerkit', name))


# ───────────────────────────── pictures ─────────────────────────────

def photographs():
    shutil.copyfile(os.path.join(PHOTOS, 'beta-invitation-fi.jpg'), out('Kuvat', 'valokuvat', 'kasi-ja-puhelin-talon-edessa.jpg'))
    hero = Image.open(os.path.join(PHOTOS, 'hero-cutout-fi.png')).convert('RGBA')
    save_png(hero, out('Kuvat', 'valokuvat', 'kasi-ja-puhelin-irrotettu.png'))
    save_png(hero_on_disc(hero), out('Kuvat', 'valokuvat', 'kasi-ja-puhelin-korallilevylla.png'))
    beta = Image.open(os.path.join(PHOTOS, 'beta-invitation-fi.jpg')).convert('RGB')
    # Crops for a flyer: a square from the phone's middle, and a circle of the same.
    w, h = beta.size
    sq = beta.crop((0, (h - w) // 2 + 40, w, (h - w) // 2 + 40 + w))
    save_jpeg(sq, out('Kuvat', 'valokuvat', 'rajaus-nelio-talon-edessa.jpg'))
    save_png(circle(sq), out('Kuvat', 'valokuvat', 'rajaus-ympyra-talon-edessa.png'))
    save_png(rounded(beta, 0.08), out('Kuvat', 'valokuvat', 'rajaus-pyorea-talon-edessa.png'))


def hero_on_disc(hero):
    """The front page's hero: the hand on the coral disc, the disc clipping the arm and
    the phone standing over its edge (index.astro, `.hero-art`)."""
    phone = Image.open(os.path.join(PHOTOS, 'hero-cutout-phone.png')).convert('RGBA').getchannel('A')
    W, H = hero.size
    unit = W / 118.89                      # one cqi of the art box, in the cut-out's pixels
    cx, cy, r = 72.89 * unit, 64.17 * unit, 50 * unit
    k = 2
    cw, ch = int(max(W, cx + r) + 8), int(max(H, cy + r) + 8)
    disc = Image.new('L', (cw * k, ch * k), 0)
    ImageDraw.Draw(disc).ellipse(((cx - r) * k, (cy - r) * k, (cx + r) * k, (cy + r) * k), fill=255)
    disc = disc.resize((cw, ch), Image.LANCZOS)
    canvas = Image.new('RGBA', (cw, ch), (0, 0, 0, 0))
    coral = Image.new('RGBA', (cw, ch), rgb(HEX['Koralli']) + (255,))
    canvas.paste(coral, (0, 0), disc)
    circle_in_cut = disc.crop((0, 0, W, H))
    keep = Image.composite(Image.new('L', (W, H), 255), circle_in_cut, phone)  # circle OR phone
    a = hero.getchannel('A')
    a = Image.composite(a, Image.new('L', (W, H), 0), keep)
    cut = hero.copy()
    cut.putalpha(a)
    canvas.alpha_composite(cut, (0, 0))
    return canvas.crop(canvas.getbbox())


def circle(im):
    k = 4
    w, h = im.size
    mask = Image.new('L', (w * k, h * k), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, w * k - 1, h * k - 1), fill=255)
    out_im = im.convert('RGBA')
    out_im.putalpha(mask.resize((w, h), Image.LANCZOS))
    return out_im


def rounded(im, frac):
    k = 4
    w, h = im.size
    mask = Image.new('L', (w * k, h * k), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, w * k - 1, h * k - 1), radius=int(min(w, h) * frac * k), fill=255)
    out_im = im.convert('RGBA')
    out_im.putalpha(mask.resize((w, h), Image.LANCZOS))
    return out_im


def phone_frame(screen, shadow=True):
    """The store images' white shell (pilke-app tools/store-assets/render/build.py):
    padding 3.3 % of the device's width, outer corners 16 %, the glass 12.9 %, and
    two soft shadows. Transparent outside the phone and its shadow."""
    sw, sh = screen.size
    W = sw / (1 - 2 * 0.033)
    pad = 0.033 * W
    H = sh + 2 * pad
    margin = int(0.16 * W) if shadow else 0
    k = 2
    cw, ch = int(W + 2 * margin), int(H + 2 * margin)
    canvas = Image.new('RGBA', (cw, ch), (0, 0, 0, 0))
    if shadow:
        # The store's two shadows, the deep one drawn tighter so that it fades out
        # inside the margin: cut off at the picture's edge it reads as a pale box.
        for dy, blur, alpha in [(0.007, 0.014, 0.10), (0.035, 0.07, 0.16)]:
            m = Image.new('L', (cw, ch), 0)
            ImageDraw.Draw(m).rounded_rectangle((margin, margin + dy * W, margin + W, margin + H + dy * W),
                                                radius=0.16 * W, fill=int(255 * alpha))
            m = m.filter(ImageFilter.GaussianBlur(blur * W / 2))
            layer = Image.new('RGBA', (cw, ch), (58, 46, 43, 0))
            layer.putalpha(m)
            canvas = Image.alpha_composite(canvas, layer)
    shell = Image.new('L', (cw * k, ch * k), 0)
    ImageDraw.Draw(shell).rounded_rectangle((margin * k, margin * k, (margin + W) * k, (margin + H) * k),
                                            radius=0.16 * W * k, fill=255)
    shell = shell.resize((cw, ch), Image.LANCZOS)
    canvas.paste(Image.new('RGBA', (cw, ch), (255, 255, 255, 255)), (0, 0), shell)
    glass = Image.new('L', (sw * k, sh * k), 0)
    ImageDraw.Draw(glass).rounded_rectangle((0, 0, sw * k - 1, sh * k - 1), radius=0.129 * W * k, fill=255)
    glass = glass.resize((sw, sh), Image.LANCZOS)
    canvas.paste(screen.convert('RGBA'), (int(margin + pad), int(margin + pad)), glass)
    return canvas


def screens():
    iphone = os.path.join(STORE, 'captures', 'iphone', 'fi')
    for shot, name in IPHONE_SHOTS:
        im = Image.open(os.path.join(iphone, f'{shot}.png')).convert('RGB')
        save_png(im, out('Kuvat', 'nayttokuvat', f'naytto-{name}.png'))
        save_png(phone_frame(im), out('Kuvat', 'puhelimet', f'puhelin-{name}.png'))
    for shot, name in SITE_SHOTS:
        im = Image.open(os.path.join(SCREENS, f'{shot}.png')).convert('RGB')
        im = im.crop((0, 0, im.width, im.height - ANDROID_NAV_ROWS))
        save_png(im, out('Kuvat', 'nayttokuvat', f'naytto-{name}.png'))
        save_png(phone_frame(im), out('Kuvat', 'puhelimet', f'puhelin-{name}.png'))
    store = os.path.join(STORE, 'out', 'fi', 'app-store', 'iphone-6.9')
    for f in sorted(os.listdir(store)):
        if f.endswith('.png'):
            save_jpeg(Image.open(os.path.join(store, f)), out('Kuvat', 'kauppakuvat', f.replace('.png', '.jpg')), 92)


# ───────────────────────────── the Drive copies ─────────────────────────────

def quantized(im, colours):
    """A palette PNG of a flat drawing: the same picture to the eye at a fifth of the
    bytes, which is what lets it travel through the Drive connector (see the doc)."""
    # Resampling leaves transparent pixels black, so the colour is bled in again first.
    return bleed(im).quantize(colours, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE)


def drive_set():
    """out/drive/: the files that go into the Drive folder as files. The Drive connector
    carries every upload's bytes inside one tool call, so these are kept under about
    15 KB each: the connector's uploads are typed out as base64, and past that they
    stop arriving intact. Text files and the QR codes are copied as they are, the
    drawings are palette PNGs at a size that fits, the full-size PNGs and every
    picture are placed in the Slides files instead (docs/print-kit.md)."""
    def copy(src, *dst):
        shutil.copyfile(os.path.join(OUT, src), out('drive', *dst))

    for suffix, _ in WORDMARKS:
        copy(f'Brändi/pilke-wordmark-{suffix}.svg', 'Brändi', f'pilke-wordmark-{suffix}.svg')
        im = Image.open(os.path.join(OUT, 'Brändi', f'pilke-wordmark-{suffix}.png'))
        im = im.resize((1000, round(im.height * 1000 / im.width)), Image.LANCZOS)
        quantized(im, 16).save(out('drive', 'Brändi', f'pilke-wordmark-{suffix}-1000.png'), optimize=True)
    for name in ['pilke-sovelluskuvake', 'pilke-sovelluskuvake-pyorea']:
        im = Image.open(os.path.join(OUT, 'Brändi', f'{name}.png')).resize((768, 768), Image.LANCZOS)
        quantized(im, 24).save(out('drive', 'Brändi', f'{name}-768.png'), optimize=True)
    copy('Brändi/paletti.txt', 'Brändi', 'paletti.txt')
    copy('Brändi/paletti.svg', 'Brändi', 'paletti.svg')
    for name, _ in SPARKLES:
        copy(f'Brändi/kipinat/kipina-{name}.svg', 'Brändi', 'Kipinät', f'kipina-{name}.svg')
        spark = Image.open(os.path.join(OUT, 'Brändi', 'kipinat', f'kipina-{name}.png')).resize((1000, 1000), Image.LANCZOS)
        quantized(spark, 16).save(out('drive', 'Brändi', 'Kipinät', f'kipina-{name}.png'), optimize=True)
    quantized(Image.open(os.path.join(OUT, 'Brändi', 'kipinat', 'kipinarivi.png')), 32).save(
        out('drive', 'Brändi', 'Kipinät', 'kipinarivi.png'), optimize=True)
    for f in sorted(os.listdir(os.path.join(OUT, 'QR'))):
        copy(f'QR/{f}', 'QR', f)


def skeletons():
    """The one-slide .pptx files each Slides file is first made from (skeleton.py)."""
    import skeleton
    for size, name in [('a4-landscape', 'elementit'), ('a4-portrait', 'poytakolmio'), ('a5-portrait', 'a5-flyer'),
                       ('a4-landscape', 'kuvat')]:
        skeleton.build(size, out('slides', f'{name}.pptx'))


# ───────────────────────────── main ─────────────────────────────

def manifest():
    entries = []
    for path in sorted(set(written)):
        data = open(path, 'rb').read()
        entries.append({'path': os.path.relpath(path, OUT), 'bytes': len(data),
                        'sha256': hashlib.sha256(data).hexdigest()})
    with open(os.path.join(OUT, 'manifest.json'), 'w') as f:
        json.dump(entries, f, indent=1, ensure_ascii=False)
        f.write('\n')
    return entries


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--clean', action='store_true', help='remove out/ first')
    args = ap.parse_args()
    for need in [BRAND, PHOTOS, SCREENS, FONTS, os.path.join(STORE, 'captures', 'iphone', 'fi')]:
        if not os.path.isdir(need):
            sys.exit(f'missing input {need}')
    if not os.path.isdir(os.path.join(STORE, 'out', 'fi', 'app-store', 'iphone-6.9')):
        sys.exit('missing the store images: run pilke-app/tools/store-assets/build.sh first')
    if args.clean and os.path.isdir(OUT):
        shutil.rmtree(OUT)
    read_sparkle()
    for step in [wordmarks, app_icon, sparkles, palette_sheet, qr_codes, photographs, screens, badges, drive_set, skeletons]:
        step()
        print(f'{step.__name__}: done')
    entries = manifest()
    total = sum(e['bytes'] for e in entries)
    print(f'{len(entries)} files, {total / 1e6:.1f} MB in {OUT}')


if __name__ == '__main__':
    main()
