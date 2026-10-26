"""The Slides files of the print kit, as Google Slides API request batches.

    .venv/bin/python slides.py --assets <sha> --layout <id> elementit  > batches.json
    .venv/bin/python slides.py --list

Every shape, text box and image on the four Slides files is defined here in
millimetres, and this script compiles a deck into `presentations.batchUpdate`
requests: one batch per slide, written as a JSON list of lists, which Claude sends
through the Google Slides connector one batch at a time (docs/print-kit.md).

Images are placed by URL. Google fetches each one once, at insertion, from
`raw.githubusercontent.com/boissit/pilke-web/<sha>/…`, the commit `--assets` names on
the short-lived `print-kit-assets` branch that holds `out/`. Slides keeps its own
copy, so the branch can go once a deck is built.

Copy is read from `src/content/copy/*.yaml`, the Finnish side, with its `{{tokens}}`
resolved from `src/data/app-constants.json`, so a change of wording on the site is
a rebuild away. A few lines that only print needs are written here and marked.
"""
import argparse
import json
import math
import os
import re
import sys
import urllib.parse

from PIL import Image, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(HERE, 'out')
EMU = 36000  # per mm
PT_MM = 25.4 / 72

C = {
    'ground': '#FFF8F4', 'peach': '#FFE3DA', 'coral': '#FFA98C', 'rose': '#F4504F',
    'text': '#3A2E2B', 'soft': '#6E5F5A', 'ink': '#3C3C3C', 'white': '#FFFFFF',
    'spark_peach': '#FCD1C3', 'spark_coral': '#FFBDA6', 'mint': '#A8DACB', 'mint_ground': '#E4F3EE',
    'card_sent': '#DCFBFF', 'card_received': '#FFEAFC', 'card_feedback': '#FFF8C2', 'rule': '#F0DDD5',
    'guide': '#B9AEB1',
}


# ───────────────────────────── copy ─────────────────────────────

def site_copy():
    """Every Finnish string of the site, by key: `src/content/copy/*.yaml`, the files
    every page draws from, with `{{tokens}}` resolved as `src/manual/constants.ts` does."""
    import glob
    import yaml
    consts = json.load(open(os.path.join(WEB, 'src', 'data', 'app-constants.json')))

    def token(t):
        v = consts
        for k in t.group(1).strip().split('.'):
            v = v[k]
        return str(v)

    out = {}
    for path in sorted(glob.glob(os.path.join(WEB, 'src', 'content', 'copy', '*.yaml'))):
        for key, value in (yaml.safe_load(open(path, encoding='utf-8')) or {}).items():
            if isinstance(value, dict) and isinstance(value.get('fi'), str):
                out[key] = re.sub(r'\{\{([^}]+)\}\}', token, value['fi'].replace('\u00ad', ''))
    return out


T = site_copy()


def first_sentence(s):
    """A body's first sentence, for a box with room for one."""
    head = s.split('. ')[0]
    return head if head.endswith(('.', '!', '?')) else head + '.'


# ───────────────────────────── text metrics ─────────────────────────────

FONT_FILES = {'Fredoka': os.path.join(HERE, '.cache', 'Fredoka-latin.ttf'),
              'Figtree': os.path.join(HERE, '.cache', 'Figtree-latin.ttf')}
# Slides' single line, in em: the faces' ascent + descent (hhea), measured off the TTFs.
LINE_EM = {'Fredoka': 1.21, 'Figtree': 1.20}
INSET_X, INSET_Y = 2.54, 1.27  # a Slides text box's own padding, mm
_fonts = {}


def pil_font(face, weight):
    key = (face, weight)
    if key not in _fonts:
        f = ImageFont.truetype(FONT_FILES[face], 200)
        try:
            f.set_variation_by_axes([weight])
        except OSError:
            pass
        _fonts[key] = f
    return _fonts[key]


def text_width_mm(s, face, weight, size_pt):
    return pil_font(face, weight).getlength(s) / 200 * size_pt * PT_MM


def wrap(text, face, weight, size_pt, width_mm):
    lines = []
    for para in text.split('\n'):
        cur = ''
        for word in para.split(' '):
            trial = (cur + ' ' + word).strip()
            if cur and text_width_mm(trial, face, weight, size_pt) > width_mm:
                lines.append(cur)
                cur = word
            else:
                cur = trial
        lines.append(cur)
    return lines


# ───────────────────────────── assets ─────────────────────────────

ASSET_SHA = None


def url(path):
    return f'https://raw.githubusercontent.com/boissit/pilke-web/{ASSET_SHA}/' + urllib.parse.quote(path)


def size_of(path):
    return Image.open(os.path.join(OUT, path)).size


WORDMARK = {'muste': 'Brändi/pilke-wordmark-muste.png', 'valkoinen': 'Brändi/pilke-wordmark-valkoinen.png',
            'koralli': 'Brändi/pilke-wordmark-koralli.png'}
SPARK = {k: f'Brändi/kipinat/kipina-{k}.png' for k in
         ['ruusu', 'koralli', 'persikka', 'vaalea-koralli', 'harmaa', 'teksti', 'valkoinen']}
PHONE = {k: f'Kuvat/puhelimet/puhelin-{k}.png' for k in
         ['treffit', 'treffikutsu', 'treffikutsu-valittu', 'sovitut-treffit', 'kalenteri', 'kipinat', 'ehdokkaat',
          'persoonallisuuskysely', 'palaute', 'asetukset-turvallisuus']}
PHONE_MARGIN = 0.16   # build.py's phone_frame(): the shadow's room either side, in phone widths
QR_INK = 'QR/qr-pilke-app-muste.png'
QR_CODES = {'site': (QR_INK, 'https://pilke.app'),
            'beta': ('QR/qr-pilke-app-beta-muste.png', 'https://pilke.app/#beta'),
            'form': ('QR/qr-beta-lomake-muste.png', 'https://forms.gle/LNjDw77d5giuxFWeA')}
# The stores' own Finnish badges, as build.py fetches them. The Google Play PNG carries
# transparent rows above and below the badge: its drawn badge is rows 29-221 of 250.
BADGE_APPLE = 'Brändi/kauppamerkit/app-store-musta.png'
BADGE_GOOGLE = 'Brändi/kauppamerkit/google-play.png'
GOOGLE_ROWS = (29, 221, 250)
BETA_ROUNDED = 'Kuvat/valokuvat/rajaus-pyorea-talon-edessa.png'
HERO_DISC = 'Kuvat/valokuvat/kasi-ja-puhelin-korallilevylla.png'


# ───────────────────────────── the compiler ─────────────────────────────

def rgb(hx):
    hx = hx.lstrip('#')
    return {'red': round(int(hx[0:2], 16) / 255, 3), 'green': round(int(hx[2:4], 16) / 255, 3),
            'blue': round(int(hx[4:6], 16) / 255, 3)}


class Deck:
    def __init__(self, key, page_w, page_h, layout):
        self.key, self.W, self.H, self.layout = key, page_w, page_h, layout
        self.batches = []
        self.slide_no = 0
        self.warnings = []
        self.notes = {}  # slide id -> speaker notes, inserted after the slide exists

    # A slide is one batch, so a failure names the slide it belongs to.
    def slide(self, name, bg=C['white']):
        self.slide_no += 1
        self.sid = f'{self.key}_s{self.slide_no:02d}'
        self.n = 0
        self.reqs = [{'createSlide': {'objectId': self.sid, 'slideLayoutReference': {'layoutId': self.layout}}},
                     {'updatePageProperties': {'objectId': self.sid, 'pageProperties': {
                         'pageBackgroundFill': {'solidFill': {'color': {'rgbColor': rgb(bg)}}}},
                         'fields': 'pageBackgroundFill.solidFill.color'}}]
        self.batches.append({'slide': self.sid, 'name': name, 'requests': self.reqs})
        return self.sid

    def oid(self, role):
        self.n += 1
        return f'{self.sid}_{role}{self.n:02d}'

    def props(self, x, y, w, h, rot=0):
        if rot:
            a = math.radians(rot)
            cos, sin = math.cos(a), math.sin(a)
            cx, cy = (x + w / 2) * EMU, (y + h / 2) * EMU
            tx = cx - (cos * w * EMU / 2 - sin * h * EMU / 2)
            ty = cy - (sin * w * EMU / 2 + cos * h * EMU / 2)
            tr = {'scaleX': round(cos, 5), 'scaleY': round(cos, 5), 'shearX': round(-sin, 5),
                  'shearY': round(sin, 5), 'translateX': round(tx), 'translateY': round(ty), 'unit': 'EMU'}
        else:
            tr = {'scaleX': 1, 'scaleY': 1, 'translateX': round(x * EMU), 'translateY': round(y * EMU), 'unit': 'EMU'}
        return {'pageObjectId': self.sid,
                'size': {'width': {'magnitude': round(w * EMU), 'unit': 'EMU'},
                         'height': {'magnitude': round(h * EMU), 'unit': 'EMU'}},
                'transform': tr}

    def check_page(self, x, y, w, h, what, margin=0):
        if x < margin - 0.01 or y < margin - 0.01 or x + w > self.W - margin + 0.01 or y + h > self.H - margin + 0.01:
            self.warnings.append(f'{self.sid} {what}: outside the page margin ({x:.1f},{y:.1f},{w:.1f},{h:.1f})')

    def shape(self, kind, x, y, w, h, fill=None, outline=None, outline_pt=0.75, rot=0, role='sh', dash=None):
        oid = self.oid(role)
        self.reqs.append({'createShape': {'objectId': oid, 'shapeType': kind,
                                          'elementProperties': self.props(x, y, w, h, rot)}})
        sp, fields = {}, []
        if fill:
            sp['shapeBackgroundFill'] = {'solidFill': {'color': {'rgbColor': rgb(fill)}}}
            fields.append('shapeBackgroundFill.solidFill.color')
        else:
            sp['shapeBackgroundFill'] = {'propertyState': 'NOT_RENDERED'}
            fields.append('shapeBackgroundFill.propertyState')
        if outline:
            sp['outline'] = {'outlineFill': {'solidFill': {'color': {'rgbColor': rgb(outline)}}},
                             'weight': {'magnitude': outline_pt, 'unit': 'PT'}}
            fields += ['outline.outlineFill.solidFill.color', 'outline.weight']
            if dash:
                sp['outline']['dashStyle'] = dash
                fields.append('outline.dashStyle')
        else:
            sp['outline'] = {'propertyState': 'NOT_RENDERED'}
            fields.append('outline.propertyState')
        self.reqs.append({'updateShapeProperties': {'objectId': oid, 'shapeProperties': sp, 'fields': ','.join(fields)}})
        return oid

    def rect(self, *a, **k):
        return self.shape('RECTANGLE', *a, **k)

    def card(self, *a, **k):
        return self.shape('ROUND_RECTANGLE', *a, role='card', **k)

    def disc(self, x, y, d, fill=C['coral'], **k):
        return self.shape('ELLIPSE', x, y, d, d, fill=fill, role='disc', **k)

    def text(self, x, y, w, text, size, face='Figtree', weight=400, color=C['text'], align='START', spacing=None,
             h=None, valign='TOP', after=0, role='tx', rot=0, fill=None, check=True):
        spacing = spacing or (100 if face == 'Fredoka' else 125)
        lines = wrap(text, face, weight, size, w - 2 * INSET_X)
        line_mm = size * PT_MM * LINE_EM[face] * spacing / 100
        need = len(lines) * line_mm + text.count('\n') * after * PT_MM + 2 * INSET_Y + 0.6
        if h is None:
            h = need
        elif need > h + 0.2:
            self.warnings.append(f'{self.sid} text {text[:30]!r}: needs {need:.1f} mm, box is {h:.1f}')
        for line in lines:
            if text_width_mm(line, face, weight, size) > w - 2 * INSET_X + 0.1:
                self.warnings.append(f'{self.sid} text {line!r}: one word wider than its box')
        if check and not rot:
            self.check_page(x, y, w, h, f'text {text[:24]!r}')
        oid = self.oid(role)
        self.reqs.append({'createShape': {'objectId': oid, 'shapeType': 'TEXT_BOX',
                                          'elementProperties': self.props(x, y, w, h, rot)}})
        self.reqs.append({'insertText': {'objectId': oid, 'text': text}})
        self.reqs.append({'updateTextStyle': {'objectId': oid, 'textRange': {'type': 'ALL'}, 'style': {
            'weightedFontFamily': {'fontFamily': face, 'weight': weight},
            'fontSize': {'magnitude': size, 'unit': 'PT'},
            'foregroundColor': {'opaqueColor': {'rgbColor': rgb(color)}}},
            'fields': 'weightedFontFamily,fontSize,foregroundColor'}})
        ps, pf = {'lineSpacing': spacing}, ['lineSpacing']
        if align != 'START':
            ps['alignment'] = align
            pf.append('alignment')
        if after:
            ps['spaceBelow'] = {'magnitude': after, 'unit': 'PT'}
            pf.append('spaceBelow')
        self.reqs.append({'updateParagraphStyle': {'objectId': oid, 'textRange': {'type': 'ALL'}, 'style': ps,
                                                   'fields': ','.join(pf)}})
        if valign != 'TOP' or fill:
            sp, fields = {}, []
            if valign != 'TOP':
                sp['contentAlignment'] = valign
                fields.append('contentAlignment')
            if fill:
                sp['shapeBackgroundFill'] = {'solidFill': {'color': {'rgbColor': rgb(fill)}}}
                fields.append('shapeBackgroundFill.solidFill.color')
            self.reqs.append({'updateShapeProperties': {'objectId': oid, 'shapeProperties': sp, 'fields': ','.join(fields)}})
        return oid, h

    def style_range(self, oid, start, end, **style):
        st, fields = {}, []
        if 'weight' in style:
            st['weightedFontFamily'] = {'fontFamily': style['face'], 'weight': style['weight']}
            fields.append('weightedFontFamily')
        if 'color' in style:
            st['foregroundColor'] = {'opaqueColor': {'rgbColor': rgb(style['color'])}}
            fields.append('foregroundColor')
        if 'size' in style:
            st['fontSize'] = {'magnitude': style['size'], 'unit': 'PT'}
            fields.append('fontSize')
        self.reqs.append({'updateTextStyle': {'objectId': oid, 'textRange': {
            'type': 'FIXED_RANGE', 'startIndex': start, 'endIndex': end}, 'style': st, 'fields': ','.join(fields)}})

    def image(self, path, x, y, w=None, h=None, rot=0, role='im', check=True):
        iw, ih = size_of(path)
        if w is None:
            w = h * iw / ih
        if h is None:
            h = w * ih / iw
        oid = self.oid(role)
        self.reqs.append({'createImage': {'objectId': oid, 'url': url(path),
                                          'elementProperties': self.props(x, y, w, h, rot)}})
        return oid, w, h

    def phone(self, name, x, y, w):
        """A framed phone whose *visible* shell is w wide at (x, y); the PNG's shadow room
        hangs outside that box, transparent."""
        path = PHONE[name]
        iw, ih = size_of(path)
        k = 1 + 2 * PHONE_MARGIN
        img_w = w * k
        img_h = img_w * ih / iw
        m = w * PHONE_MARGIN
        oid, _, _ = self.image(path, x - m, y - m, img_w, img_h)
        return oid, img_h - 2 * m

    def sparkle(self, colour, cx, cy, d, rot=0):
        return self.image(SPARK[colour], cx - d / 2, cy - d / 2, d, d, rot=rot, role='sp')[0]

    def wordmark(self, tone, x, y, w=None, h=None):
        return self.image(WORDMARK[tone], x, y, w, h, role='wm')

    def line(self, x1, y1, x2, y2, colour, pt=0.75, dash=None, role='ln'):
        oid = self.oid(role)
        self.reqs.append({'createLine': {'objectId': oid, 'lineCategory': 'STRAIGHT', 'elementProperties':
                                         self.props(x1, y1, max(x2 - x1, 0.001), max(y2 - y1, 0.001))}})
        lp = {'lineFill': {'solidFill': {'color': {'rgbColor': rgb(colour)}}}, 'weight': {'magnitude': pt, 'unit': 'PT'}}
        fields = 'lineFill.solidFill.color,weight'
        if dash:
            lp['dashStyle'] = dash
            fields += ',dashStyle'
        self.reqs.append({'updateLineProperties': {'objectId': oid, 'lineProperties': lp, 'fields': fields}})
        return oid

    def group(self, ids, title=None, description=None):
        """Slides refuses alt text on a group, so the name goes on its first child,
        where the editor's alt-text box shows it when the group is opened."""
        gid = self.oid('grp')
        if title or description:
            self.alt(ids[0], title, description)
        self.reqs.append({'groupObjects': {'groupObjectId': gid, 'childrenObjectIds': ids}})
        return gid

    def alt(self, oid, title=None, description=None):
        r = {'objectId': oid}
        if title:
            r['title'] = title
        if description:
            r['description'] = description
        self.reqs.append({'updatePageElementAltText': r})

    # ── the site's pieces ──

    def pill(self, x, y, w, h, label, style='ink', size=None):
        fill, colour, outline, weight = {
            'ink': (C['text'], C['ground'], None, 700),
            'coral': (C['coral'], C['text'], None, 700),
            'ghost': (C['white'], C['text'], C['rule'], 600),
        }[style]
        size = size or round(h / PT_MM * 0.36)
        oid = self.shape('FLOW_CHART_TERMINATOR', x, y, w, h, fill=fill, outline=outline, role='pill')
        self.reqs.append({'insertText': {'objectId': oid, 'text': label}})
        self.reqs.append({'updateTextStyle': {'objectId': oid, 'textRange': {'type': 'ALL'}, 'style': {
            'weightedFontFamily': {'fontFamily': 'Figtree', 'weight': weight},
            'fontSize': {'magnitude': size, 'unit': 'PT'},
            'foregroundColor': {'opaqueColor': {'rgbColor': rgb(colour)}}},
            'fields': 'weightedFontFamily,fontSize,foregroundColor'}})
        self.reqs.append({'updateParagraphStyle': {'objectId': oid, 'textRange': {'type': 'ALL'},
                                                   'style': {'alignment': 'CENTER'}, 'fields': 'alignment'}})
        self.reqs.append({'updateShapeProperties': {'objectId': oid, 'shapeProperties': {'contentAlignment': 'MIDDLE'},
                                                    'fields': 'contentAlignment'}})
        if text_width_mm(label, 'Figtree', weight, size) > w - 8:
            self.warnings.append(f'{self.sid} pill {label!r}: too narrow')
        return oid

    def struck(self, x, y, w, steps, size, gap=0.35, colour=C['soft']):
        """The front page's struck-through steps: one line of Fredoka per step and a coral
        bar over it, a little below the middle of the lowercase (index.astro, `.elsewhere`).
        Each step is its text box and its bar, grouped, so it moves as one."""
        line_h = size * PT_MM * LINE_EM['Fredoka'] + 2 * INSET_Y + 0.6
        groups = []
        for step in steps:
            tid, _ = self.text(x, y, w, step, size, face='Fredoka', weight=600, color=colour, h=line_h,
                               valign='MIDDLE', spacing=100, role='st')
            tw = text_width_mm(step, 'Fredoka', 600, size)
            em = size * PT_MM
            bar_h = 0.09 * em * 1.15
            bar = self.shape('FLOW_CHART_TERMINATOR', x + INSET_X - 0.04 * em, y + line_h / 2 + 0.03 * em - bar_h / 2,
                             tw + 0.08 * em, bar_h, fill=C['coral'], role='bar')
            groups.append(self.group([tid, bar]))
            y += line_h - 2 * INSET_Y + gap * em
        return groups, y

    def numeral(self, x, y, d, n, fill=C['white']):
        oid = self.shape('ELLIPSE', x, y, d, d, fill=fill, role='num')
        self.reqs.append({'insertText': {'objectId': oid, 'text': str(n)}})
        self.reqs.append({'updateTextStyle': {'objectId': oid, 'textRange': {'type': 'ALL'}, 'style': {
            'weightedFontFamily': {'fontFamily': 'Fredoka', 'weight': 600},
            'fontSize': {'magnitude': round(d / PT_MM * 0.45), 'unit': 'PT'},
            'foregroundColor': {'opaqueColor': {'rgbColor': rgb(C['text'])}}},
            'fields': 'weightedFontFamily,fontSize,foregroundColor'}})
        self.reqs.append({'updateParagraphStyle': {'objectId': oid, 'textRange': {'type': 'ALL'},
                                                   'style': {'alignment': 'CENTER'}, 'fields': 'alignment'}})
        self.reqs.append({'updateShapeProperties': {'objectId': oid, 'shapeProperties': {'contentAlignment': 'MIDDLE'},
                                                    'fields': 'contentAlignment'}})
        return oid

    def qr(self, x, y, d, code='site', plate=True):
        """A code in ink on a white plate, since a code needs a light ground to scan:
        `site` is pilke.app, `beta` pilke.app/#beta."""
        path, target = QR_CODES[code]
        ids = []
        if plate:
            ids.append(self.card(x, y, d, d, fill=C['white']))
            pad = d * 0.06
            ids.append(self.image(path, x + pad, y + pad, d - 2 * pad, d - 2 * pad, role='qr')[0])
        else:
            ids.append(self.image(path, x, y, d, d, role='qr')[0])
        gid = self.group(ids, title=f'QR: {target}')
        return gid


# ───────────────────────────── shared copy for print ─────────────────────────────

# Lines written for print, not on the site, in the owner's register. Everything here
# is the kit's own copy, for the owner to review; the rest is the site's.
PRINT = {
    'url': 'pilke.app',
    'scan': 'Skannaa ja liity betaan',
    'area': 'Pilke toimii toistaiseksi vain pääkaupunkiseudulla.',
    # The flyer's back, the owner's own words (2026-10-26), kept verbatim.
    'testers.title': 'Etsimme testaajia',
    'testers.body': 'Pilke on uudenlainen treffisovellus, jonka ainoa tarkoitus on viedä sinut treffeille. '
                    'Pilkettä kehitetään kaveriporukan voimin ilman kaupallisia intressejä, joten toivomme '
                    'aidosti luovamme sovelluksen, joka auttaa löytämään parhaat mahdolliset treffikumppanit. '
                    'Etsimme ihmisiä, jotka ovat kiinnostuneita testaamaan sovelluskonseptia, varmentamaan idean '
                    'toimivuutta ja mielellään antamaan palautetta kokonaisuudesta.',
    'expect.title': 'Hyvä tietää',
    'expect.beta.title': 'Varhainen beta',
    'expect.beta.body': 'Olette sovelluksen ensimmäisiä testaajia ja käyttäjiä, joten bugeja todennäköisesti ilmenee.',
    'expect.few.title': 'Rajattu käyttäjäkunta',
    'expect.few.body': 'Sovellus on suljetussa testauksessa, joten käyttäjiä on vähän ja treffiparien muodostus on '
                       'haastavaa. Käykää treffeillä avoimin mielin!',
    'expect.area.title': 'Vain pääkaupunkiseudulla',
    'expect.area.body': 'Yksinkertaisuuden vuoksi sovellus toimii aluksi vain Helsinki-Espoo -akselilla, ja aluetta '
                        'laajennetaan myöhemmin.',
    'expect.feedback.title': 'Palaute on kultaa',
    'expect.feedback.body': 'Kerro meille mikä toimii ja mikä takkuaa, arvostamme kaikkea palautetta. Voit antaa '
                            'palautetta sovelluksen kautta tai suoraan meille.',
}


def how_to(d, title, steps, note=None, w=None):
    """The first slide of a template file: how to print it. `w` narrows the steps to
    leave room beside them."""
    d.slide('Näin tulostat', bg=C['ground'])
    m = 14 if d.W < 200 else 18
    w = w or d.W - 2 * m
    _, th = d.text(m, m, d.W - 2 * m, title, 26 if d.W < 200 else 30, face='Fredoka', weight=600)
    y = m + th + 6
    for i, (head, body) in enumerate(steps, 1):
        d.numeral(m, y, 9, i)
        tid, h1 = d.text(m + 12, y - 0.5, w - 12, head, 12, weight=700)
        _, h2 = d.text(m + 12, y + h1 - 1.5, w - 12, body, 10.5, color=C['soft'])
        y += max(h1 + h2, 10) + 3
    if note:
        d.text(m, y + 2, d.W - 2 * m, note, 9.5, color=C['soft'])
    return y


def first_line_mid(y, size_pt):
    """The middle of the capitals on the first line of a text box whose top is y: the
    first baseline of a Slides text box in Fredoka or Figtree sits 2.39 mm plus 0.957
    of the type size below its top (measured on the decks' own PDF export, at both
    faces' line spacings), and a capital is 0.70 of the size tall in both faces."""
    em = size_pt * PT_MM
    return y + 2.39 + (0.957 - 0.35) * em


def marker(d, x, y, size_pt, spark):
    """A rose sparkle beside a line of text whose box top is y, centred on its capitals."""
    d.sparkle('ruusu', x + spark / 2, first_line_mid(y, size_pt), spark)


def bullets(d, x, y, w, items, title_pt, body_pt=None, title_face='Fredoka', gap=4, spark=5):
    """Rows of a rose sparkle and a title, with a body under it when there is one: each
    sparkle sits on its title's first line, centred on the capitals, and the text starts
    the same distance from it on every row. Returns the y under the last row."""
    tx = x + spark + 0.8 - INSET_X + 2.5   # the glyphs start 2.5 mm right of the sparkle
    for title, body in items:
        marker(d, x, y, title_pt, spark)
        weight = 600 if title_face == 'Fredoka' else 700
        _, th = d.text(tx, y, x + w - tx, title, title_pt, face=title_face, weight=weight)
        y += th
        if body:
            _, bh = d.text(tx, y - 2, x + w - tx, body, body_pt)
            y += bh - 2
        y += gap
    return y


def steps(d, x, y, w, items, title_pt, body_pt, gap=3, d_num=7):
    """Numbered steps: a white disc with the number, centred on the title's capitals."""
    tx = x + d_num + 2.5 - INSET_X
    for n, (title, body) in enumerate(items, 1):
        cy = first_line_mid(y, title_pt)
        d.numeral(x, cy - d_num / 2, d_num, n)
        _, th = d.text(tx, y, x + w - tx, title, title_pt, face='Fredoka', weight=600)
        y += th
        if body:
            _, bh = d.text(tx, y - 2, x + w - tx, body, body_pt)
            y += bh - 2
        y += gap
    return y


# ───────────────────────────── Pöytäkolmio ─────────────────────────────

# A4 landscape, three upright faces side by side: folds at 99 and 198 mm, and the
# sheet's two short edges meet at the third edge of the prism, taped inside. Each face
# is a card 5 mm inside its folds or the sheet's edge (where a printer's blank margin
# falls on the white ground) and 6 mm inside the top and foot, and the content keeps
# 4 mm inside the card: 9 mm from a fold, 10 mm from the top and foot.
TT_W, TT_H = 297, 210
PANEL = 99
FOLDS = [PANEL, 2 * PANEL]
CARD_X, CARD_Y = 5, 6
PAD = 4


def face_box(i):
    """Face i (0, 1, 2): its left edge, its card and its content box, mm."""
    px = i * PANEL
    card = (px + CARD_X, CARD_Y, PANEL - 2 * CARD_X, TT_H - 2 * CARD_Y)
    content = (card[0] + PAD, card[1] + PAD, card[2] - 2 * PAD, card[3] - 2 * PAD)
    return px, card, content


def triangle_guides(d):
    """The two folds, a pale dashed line each: one group on top of the page, named so
    it is easy to find and delete."""
    ids = [d.line(x, 0, x, TT_H, C['guide'], pt=0.5, dash='DASH') for x in FOLDS]
    return d.group(ids, title='Ohjeviivat',
                   description='Taitteet. Poista koko ryhmä, jos et halua niitä tulosteeseen.')


def build_triangle(layout):
    d = Deck('pk', TT_W, TT_H, layout)
    how_to(d, 'Pöytäkolmio – näin tulostat ja taitat', w=162, steps=[
        ('Tulosta A4:lle vaakasuuntaan todellisessa koossa',
         'Tulosta sivu 2. Tiedosto › Lataa › PDF ja tulosta PDF: paperi A4, vaakasuunta, '
         'skaalaus 100 % eli todellinen koko. Paksu paperi (160–250 g/m²) seisoo parhaiten.'),
        ('Arkki on valmiiksi oikean kokoinen',
         'Kolme 99 mm leveää puolta täyttävät A4:n leveyden. Tulostimen 3–5 mm tyhjät reunat osuvat '
         'valkoiseen pohjaan korttien ympärillä, joten mitään ei tarvitse leikata.'),
        ('Taita kahdesta katkoviivasta',
         'Taitteet ovat 99 ja 198 mm:n kohdalla vasemmasta reunasta. Taita kumpikin taaksepäin, kuva ulospäin. '
         'Viivain ja tylppä veitsi tekevät taitteesta suoran.'),
        ('Teippaa viimeinen reuna sisäpuolelta',
         'Kierrä arkki kolmioksi niin, että sen vasen ja oikea reuna kohtaavat, ja teippaa sauma sisäpuolelta. '
         'Kolmio seisoo pystyssä, ja kaikki kolme puolta ovat oikein päin.'),
        ('Ohjeviivat ovat yksi ryhmä',
         'Taitteet ovat ryhmässä "Ohjeviivat". Klikkaa kumpaa tahansa katkoviivaa ja paina Delete, '
         'jos haluat tulosteen ilman niitä.'),
    ])
    # The sheet, drawn small beside the steps: three faces side by side.
    k = 0.32
    sx, sy = TT_W - 18 - TT_W * k, 52
    for i in range(3):
        x = sx + i * PANEL * k
        d.rect(x, sy, PANEL * k, TT_H * k, fill=C['white'], outline=C['guide'], outline_pt=0.5,
               dash=None if i == 0 else 'DASH')
        d.text(x, sy + TT_H * k / 2 - 4, PANEL * k, f'puoli {i + 1}', 9, weight=600, color=C['soft'], align='CENTER')
        d.text(x - 4, sy + TT_H * k + 1, PANEL * k + 8, '99 mm', 7, color=C['soft'], align='CENTER', check=False)
    d.text(sx, sy + TT_H * k + 7, TT_W * k,
           'Arkki edestä: kolme puolta vierekkäin. Taitettuna ne kiertävät kolmion ympäri, ja arkin vasen ja '
           'oikea reuna teipataan yhteen kolmion sisäpuolelta.', 10, color=C['soft'])

    d.slide(triangle_faces.__doc__.strip().split('\n')[0], bg=C['white'])
    triangle_faces(d)
    triangle_guides(d)
    return d


def tri_card(d, i, fill, outline=None):
    px, card, content = face_box(i)
    d.card(*card, fill=fill, outline=outline)
    return content


def scatter(d, colour, spots):
    for cx, cy, s, r in spots:
        d.sparkle(colour, cx, cy, s, r)


def headline(d, x, y, w, size):
    """The site's headline, broken where the site breaks it on a narrow screen."""
    return d.text(x, y, w, T['hero.title'].replace(', ', ',\n'), size, face='Fredoka', weight=600)


def tri_struck(d, i, fill, outline=None):
    """The other apps' routine, struck through as on the front page, and the line under it."""
    x, y, w, h = tri_card(d, i, fill, outline=outline)
    steps = [T['pitch.elsewhere.swipe'], T['pitch.elsewhere.chat'], T['pitch.elsewhere.ghost'],
             T['pitch.elsewhere.swipe'], T['pitch.elsewhere.more'], T['pitch.elsewhere.maybe']]
    _, yy = d.struck(x - 1, y + 10, w + 2, steps, 21, gap=0.3)
    _, th = d.text(x, yy + 10, w, T['pitch.instead.title'], 24, face='Fredoka', weight=600)
    return x, y, w, h, yy + 10 + th


def store_badges(d, cx, y, h):
    """The App Store and Google Play badges side by side, centred on cx, both drawn
    badges h tall (Google asks for its badge to be at least the size of the others), a
    quarter of their height apart and clear of everything round them. Returns the y
    under them."""
    iw, ih = size_of(BADGE_APPLE)
    aw = h * iw / ih
    top, bottom, full = GOOGLE_ROWS
    gw_px, _ = size_of(BADGE_GOOGLE)
    gh = h * full / (bottom - top)
    gw = h * gw_px / (bottom - top)
    gap = h / 4
    x = cx - (aw + gap + gw) / 2
    d.image(BADGE_APPLE, x, y, aw, h, role='bdg')
    d.image(BADGE_GOOGLE, x + aw + gap, y - h * top / (bottom - top), gw, gh, role='bdg')
    return y + h


def triangle_faces(d):
    """Pöytäkolmio · Vihdoin, treffisovellus"""
    # Face 1: the wordmark and the headline on peach, the hand and phone on the coral disc.
    x, y, w, h = tri_card(d, 0, C['peach'])
    scatter(d, 'persikka', [(x + w - 6, y + 4, 18, 14), (x + w - 14, y + 30, 8, -26), (x + 4, y + 104, 10, 30)])
    d.wordmark('muste', x + 1, y + 4, w=40)
    _, hh = headline(d, x, y + 38, w, 30)
    d.text(x, y + 38 + hh + 2, w - 4, T['pitch.hero.lead'], 12.5, weight=500)
    d.image(HERO_DISC, x + 6, y + h - 78 * 33525 / 29575, w=78)
    # Face 2: the other apps' routine, struck through, and what Pilke does with it.
    x, y, w, h, yy = tri_struck(d, 1, C['white'], outline=C['rule'])
    d.text(x, yy + 4, w - 4, T['pitch.instead.lead'], 13, weight=500)
    d.sparkle('vaalea-koralli', x + w - 10, y + h - 12, 16, 14)
    d.sparkle('vaalea-koralli', x + w - 26, y + h - 4, 7, -24)
    d.sparkle('persikka', x + 8, y + h - 14, 12, 30)
    # Face 3: how it goes, in the site's words, then the code to pilke.app and the stores.
    x, y, w, h = tri_card(d, 2, C['mint_ground'])
    bottom = y + h
    _, th = d.text(x, y + 2, w, T['pitch.practice.title'], 17, face='Fredoka', weight=600)
    flow = [
        (T['pitch.practice.one.title'], first_sentence(T['pitch.practice.one.body'])),
        (T['pitch.instead.ready.title'], first_sentence(T['detail.draw.body'])),
        (T['pitch.practice.two.title'], T['pitch.instead.invite.body']),
        (T['pitch.practice.three.title'], first_sentence(T['pitch.practice.three.body'])),
        (T['pitch.practice.four.title'], first_sentence(T['pitch.practice.four.body'])),
    ]
    yy = steps(d, x, y + 2 + th + 2, w, flow, 12, 9, gap=2.2)
    _, nh = d.text(x, bottom - 9, w, PRINT['area'], 8.5, color=C['soft'], align='CENTER')
    by = store_badges(d, x + w / 2, bottom - 9 - 3 - 10, 10)
    q = 30
    qy = by - 10 - 4 - 7 - q
    if qy < yy + 2:
        d.warnings.append(f'{d.sid} face 3: the steps run into the code ({yy:.1f} > {qy:.1f})')
    d.qr(x + (w - q) / 2, qy, q, code='site')
    d.text(x, qy + q + 0.5, w, PRINT['url'], 13, face='Fredoka', weight=600, align='CENTER')


# ───────────────────────────── A5 flyer ─────────────────────────────

A5_CARD = (6, 6, 136, 198)
A5_C = (14, 14, 120, 182)  # content box: 8 mm inside the card, 14 mm from the sheet's edge


def flyer_footer(d, y, tone='ink'):
    """The beta form's code, the line and the button, along the foot of a page."""
    x, _, w, _ = A5_C
    q = 28
    d.qr(x, y, q, code='form')
    _, th = d.text(x + q + 6, y + 3, w - q - 6, PRINT['scan'], 15, face='Fredoka', weight=600)
    d.pill(x + q + 8, y + q - 12, 46, 12, T['cta.button'], style=tone, size=12)


FLYER_HOW_TO = (
    'A5-flyer – näin tulostat. Flyer on kaksi sivua: etupuoli (sivu 1) ja takapuoli (sivu 2). '
    'Tiedosto › Lataa › PDF ja tulosta PDF skaalauksella 100 % (todellinen koko). '
    'A5-paperille: valitse kaksipuolinen tulostus, kääntö pitkän reunan mukaan. '
    'A4-paperille: valitse "2 sivua arkille" ja vaakasuunta, niin etu- ja takapuoli tulevat vierekkäin; '
    'leikkaa arkki keskeltä. Kaksipuoliseen flyeriin tulosta etupuolet ja takapuolet eri kierroksilla. '
    'Kaikki sisältö on vähintään 6 mm:n päässä reunasta.')


def build_flyer(layout):
    """Two pages, front and back, so it prints double-sided; how to print it is in the
    front page's speaker notes, which do not print."""
    d = Deck('fl', 148, 210, layout)
    for page in (flyer_front, flyer_back):
        d.slide(page.__doc__.strip(), bg=C['ground'])
        page(d)
    d.notes[d.batches[0]['slide']] = FLYER_HOW_TO
    return d


def flyer_front(d):
    """Etupuoli · Vihdoin, treffisovellus"""
    d.card(*A5_CARD, fill=C['peach'])
    scatter(d, 'persikka', [(128, 20, 20, 14), (112, 38, 8, -26), (24, 196, 10, -18)])
    x, y, w, h = A5_C
    d.wordmark('muste', x, y, w=28)
    _, th = headline(d, x, y + 25, w, 32)
    _, lh = d.text(x, y + 25 + th + 1, w - 10, T['pitch.hero.lead'], 12.5, weight=500)
    top = y + 25 + th + lh + 6
    # Left: the other apps' routine, struck through, and the line under it.
    steps_ = [T['pitch.elsewhere.swipe'], T['pitch.elsewhere.chat'], T['pitch.elsewhere.ghost'],
              T['pitch.elsewhere.swipe'], T['pitch.elsewhere.more'], T['pitch.elsewhere.maybe']]
    _, sy = d.struck(x - 1, top, 66, steps_, 15, gap=0.2)
    d.text(x, sy + 3, 62, T['pitch.instead.title'], 15, face='Fredoka', weight=600)
    # Right: what Pilke does instead, and the hand holding the phone.
    bullets(d, 82, top + 1, 54, [(T[f'pitch.instead.{k}.title'], None) for k in ['match', 'invite', 'ready']],
            11, title_face='Figtree', gap=2, spark=4.5)
    iw = 54
    d.image(HERO_DISC, 142 - 4 - iw, 204 - 4 - iw * 33525 / 29575, w=iw)


def flyer_back(d):
    """Takapuoli · Etsimme testaajia"""
    d.card(*A5_CARD, fill=C['white'], outline=C['rule'])
    d.sparkle('ruusu', 129, 18, 12, 14)
    x, y, w, h = A5_C
    _, th = d.text(x, y - 2, w - 22, PRINT['testers.title'], 21, face='Fredoka', weight=600)
    _, bh = d.text(x, y - 2 + th, w, PRINT['testers.body'], 10, weight=500)
    yy = y - 2 + th + bh + 3
    _, eh = d.text(x, yy, w, PRINT['expect.title'], 13, face='Fredoka', weight=600)
    end = bullets(d, x, yy + eh, w,
                  [(PRINT[f'expect.{k}.title'], PRINT[f'expect.{k}.body']) for k in ['beta', 'few', 'area', 'feedback']],
                  10.5, 9.5, title_face='Figtree', gap=2, spark=4.5)
    foot = 204 - 8 - 28
    if end > foot - 3:
        d.warnings.append(f'{d.sid} back: the list runs into the footer ({end:.1f} > {foot - 3:.1f})')
    flyer_footer(d, foot)


# ───────────────────────────── Elementit ─────────────────────────────

def label(d, x, y, w, s):
    return d.text(x, y, w, s, 8, color=C['soft'], check=False)


def build_elements(layout):
    d = Deck('el', 297, 210, layout)
    M = 14

    d.slide('Ohje', bg=C['ground'])
    d.wordmark('muste', M, M, w=44)
    d.text(M + 52, M + 2, 200, 'Pilke – elementit', 32, face='Fredoka', weight=600)
    d.text(M + 52, M + 18, 200,
           'Kopioi elementti omaan pohjaasi: valitse se, Ctrl+C (Macilla Cmd+C), siirry pohjaan ja Ctrl+V. '
           'Koko, värit ja fontit säilyvät. Kuvat ovat täysikokoisia, joten niitä voi suurentaa.', 12, weight=500)
    index = ['2  Wordmark ja sovelluskuvake', '3  Kipinät', '4  Värit', '5  Tekstityylit',
             '6  Yliviivaus, kiekko, painikkeet ja kortit', '7–8  Puhelimet', '9  Valokuvat ja rajaukset', '10  QR-koodit']
    d.text(M + 52, M + 44, 120, '\n'.join(index), 12, after=4)
    d.text(M + 52, M + 112, 200,
           'Fontit: Fredoka 600 otsikoissa, Figtree leipätekstissä. Molemmat löytyvät Slidesin fonttivalikosta. '
           'Värit ovat myös tämän tiedoston teemavärejä.', 10.5, color=C['soft'])

    # 2 wordmarks
    d.slide('Wordmark', bg=C['white'])
    d.text(M, M - 4, 200, 'Wordmark ja sovelluskuvake', 20, face='Fredoka', weight=600)
    d.wordmark('muste', M, 34, w=80)
    label(d, M, 34 + 58, 80, 'pilke-wordmark-muste · vaalealle pohjalle')
    d.wordmark('koralli', M + 92, 34, w=80)
    label(d, M + 92, 34 + 58, 80, 'pilke-wordmark-koralli · valkoiselle pohjalle')
    d.card(M + 184, 30, 86, 66, fill=C['text'])
    d.wordmark('valkoinen', M + 187, 34, w=80)
    label(d, M + 184, 30 + 68, 86, 'pilke-wordmark-valkoinen · tummalle pohjalle (kortti on erillinen muoto)')
    for i, wd in enumerate([40, 25, 15]):
        d.wordmark('muste', M + [0, 48, 80][i], 120, w=wd)
    label(d, M, 152, 100, 'Pienet koot: 40, 25 ja 15 mm')
    d.image('Brändi/pilke-sovelluskuvake-pyorea.png', M + 130, 118, w=34)
    label(d, M + 130, 154, 40, 'Sovelluskuvake, pyöristetty')
    d.image('Brändi/pilke-sovelluskuvake.png', M + 176, 118, w=34)
    label(d, M + 176, 154, 40, 'Sovelluskuvake, neliö')
    d.card(M + 222, 116, 46, 40, fill=C['coral'])
    d.wordmark('muste', M + 226, 120, w=38)
    label(d, M + 222, 158, 50, 'Musta wordmark korallilla')

    # 3 sparkles
    d.slide('Kipinät', bg=C['white'])
    d.text(M, M - 4, 200, 'Kipinät', 20, face='Fredoka', weight=600)
    names = [('ruusu', '#F4504F'), ('koralli', '#FFA98C'), ('persikka', '#FCD1C3'), ('vaalea-koralli', '#FFBDA6'),
             ('harmaa', '#D9D2D4'), ('teksti', '#3A2E2B'), ('valkoinen', '#FFFFFF')]
    for i, (n, hx) in enumerate(names):
        cx = M + 18 + i * 38
        if n == 'valkoinen':
            d.card(cx - 17, 30, 34, 34, fill=C['coral'])
        d.sparkle(n, cx, 47, 30)
        label(d, cx - 18, 66, 36, f'{n}\n{hx}')
    for i, s in enumerate([40, 20, 10, 5]):
        d.sparkle('ruusu', M + 22 + [0, 46, 74, 92][i], 110, s)
    label(d, M, 132, 120, 'Koot 40, 20, 10 ja 5 mm. Käännä vapaasti.')
    d.image('Brändi/kipinat/kipinarivi.png', M + 120, 96, h=24)
    label(d, M + 120, 122, 80, 'Kipinärivi, kuten sovelluksen laskuri')
    d.card(M, 142, 120, 52, fill=C['peach'])
    d.image('Brändi/kipinat/kipinaparvi-persikka.png', M, 142, w=83.2)
    label(d, M + 86, 170, 34, 'Kipinäparvi persikalla')
    d.card(M + 130, 142, 120, 52, fill=C['coral'])
    d.image('Brändi/kipinat/kipinaparvi-vaalea-koralli.png', M + 130, 142, w=83.2)
    label(d, M + 216, 170, 34, 'Kipinäparvi korallilla')

    # 4 palette
    d.slide('Värit', bg=C['white'])
    d.text(M, M - 4, 200, 'Värit', 20, face='Fredoka', weight=600)
    palette = [('Pohja', 'ground'), ('Persikka', 'peach'), ('Koralli', 'coral'), ('Ruusu', 'rose'),
               ('Teksti', 'text'), ('Pehmeä teksti', 'soft'), ('Muste', 'ink'), ('Valkoinen', 'white'),
               ('Kipinä persikalla', 'spark_peach'), ('Kipinä korallilla', 'spark_coral'), ('Minttu', 'mint'),
               ('Minttupohja', 'mint_ground'), ('Kortti sininen', 'card_sent'), ('Kortti pinkki', 'card_received'),
               ('Kortti keltainen', 'card_feedback'), ('Viiva', 'rule')]
    for i, (name, key) in enumerate(palette):
        r, c = divmod(i, 8)
        x, y = M + c * 34, 32 + r * 80
        d.card(x, y, 30, 40, fill=C[key], outline=C['rule'])
        d.text(x - 1, y + 42, 33, f'{name}\n{C[key]}', 8.5, weight=600, check=False)
    d.text(M, 194, 260, 'Muodot ovat tarkoissa väreissä: kopioi muoto tai käytä hex-koodia. Tekstin väri on #3A2E2B, '
           'ja korallilla teksti on aina tätä väriä.', 9, color=C['soft'])

    # 5 type
    d.slide('Tekstityylit', bg=C['white'])
    d.text(M, M - 4, 200, 'Tekstityylit', 20, face='Fredoka', weight=600)
    rows = [
        ('Otsikko · Fredoka 600 · 48 pt', T['hero.title'], 'Fredoka', 600, 48, C['text']),
        ('Väliotsikko · Fredoka 600 · 30 pt', 'Pilke pyörii kipinöillä', 'Fredoka', 600, 30, C['text']),
        ('Kortin otsikko · Figtree 700 · 14 pt', T['pitch.instead.ready.title'], 'Figtree', 700, 14, C['text']),
        ('Ingressi · Figtree 500 · 13 pt · #6E5F5A', T['pitch.hero.lead'], 'Figtree', 500, 13, C['soft']),
        ('Leipäteksti · Figtree 400 · 10 pt', T['pitch.instead.ready.body'], 'Figtree', 400, 10, C['text']),
        ('Pieni · Figtree 600 · 8 pt', PRINT['url'], 'Figtree', 600, 8, C['soft']),
    ]
    y = 30
    for lab, s, face, wt, size, col in rows:
        label(d, M, y + 1, 62, lab)
        _, hh = d.text(M + 66, y, 200, s, size, face=face, weight=wt, color=col)
        y += max(hh, 8) + 5

    # 6 motifs
    d.slide('Muodot', bg=C['ground'])
    d.text(M, M - 4, 200, 'Yliviivaus, kiekko, painikkeet ja kortit', 20, face='Fredoka', weight=600)
    steps = [T['pitch.elsewhere.swipe'], T['pitch.elsewhere.chat'], T['pitch.elsewhere.ghost'],
             T['pitch.elsewhere.swipe'], T['pitch.elsewhere.more'], T['pitch.elsewhere.maybe']]
    _, yy = d.struck(M - 2, 30, 90, steps, 18, gap=0.2)
    label(d, M, yy + 1, 90, 'Jokainen rivi on teksti ja korallinen viiva ryhmänä: muokkaa tekstiä, ja säädä viivan pituus.')
    d.disc(M + 98, 30, 56)
    d.disc(M + 158, 30, 28)
    d.disc(M + 158, 62, 14)
    label(d, M + 98, 88, 90, 'Korallikiekko #FFA98C')
    d.pill(M + 98, 104, 48, 13, T['cta.button'], style='ink', size=13)
    d.pill(M + 150, 104, 48, 13, T['cta.button'], style='coral', size=13)
    d.pill(M + 98, 122, 70, 13, T['pitch.instead.more'], style='ghost', size=13)
    label(d, M + 98, 137, 100, 'Painikkeet: muste, koralli ja valkoinen')
    d.card(M + 206, 116, 62, 22, fill=C['peach'])
    for i, n in enumerate(range(1, 5)):
        d.numeral(M + 211 + i * 14, 121.5, 11, n)
    for i, (fill, outline, title) in enumerate([(C['white'], C['rule'], 'Valkoinen kortti'),
                                               (C['peach'], None, 'Persikka'), (C['coral'], None, 'Koralli'),
                                               (C['mint_ground'], None, 'Minttu')]):
        x = M + 98 + i * 44
        d.card(x, 148, 40, 46, fill=fill, outline=outline)
        d.text(x + 3, 151, 34, title, 11, weight=700)
    d.card(M + 214, 30, 54, 70, fill=C['white'], outline=C['rule'])
    d.text(M + 218, 34, 46, T['pitch.instead.ready.title'], 12, weight=700)
    d.text(M + 218, 46, 46, first_sentence(T['pitch.instead.ready.body']), 9)

    # 7–8 phones
    for page, names in [(7, ['treffit', 'treffikutsu', 'treffikutsu-valittu', 'sovitut-treffit', 'ehdokkaat']),
                        (8, ['kipinat', 'kalenteri', 'persoonallisuuskysely', 'palaute', 'asetukset-turvallisuus'])]:
        d.slide(f'Puhelimet {page - 6}', bg=C['peach'])
        d.text(M, M - 4, 200, 'Puhelimet', 20, face='Fredoka', weight=600)
        for i, n in enumerate(names):
            x = M + 3 + i * 54
            _, ph = d.phone(n, x, 30, 46)
            label(d, x - 2, 30 + ph + 3, 50, n)

    # 9 photos
    d.slide('Valokuvat', bg=C['white'])
    d.text(M, M - 4, 200, 'Valokuvat ja rajaukset', 20, face='Fredoka', weight=600)
    _, w1, h1 = d.image(HERO_DISC, M, 30, h=110)
    label(d, M, 142, w1, 'Käsi ja puhelin korallikiekolla')
    _, w2, h2 = d.image('Kuvat/valokuvat/kasi-ja-puhelin-irrotettu.png', M + w1 + 6, 30, h=74)
    label(d, M + w1 + 6, 106, w2, 'Irrotettu, läpinäkyvä tausta')
    _, w3, _ = d.image('Kuvat/valokuvat/rajaus-pyorea-talon-edessa.png', M + w1 + w2 + 12, 30, h=74)
    label(d, M + w1 + w2 + 12, 106, w3, 'Pyöreäkulmainen rajaus')
    x2 = M + w1 + 6
    d.image('Kuvat/valokuvat/rajaus-ympyra-talon-edessa.png', x2, 122, h=50)
    label(d, x2, 174, 50, 'Ympyrä')
    d.image('Kuvat/valokuvat/rajaus-nelio-talon-edessa.jpg', x2 + 56, 122, h=50)
    label(d, x2 + 56, 174, 50, 'Neliö')
    d.image('Kuvat/valokuvat/kasi-ja-puhelin-talon-edessa.jpg', x2 + 112, 122, h=50)
    label(d, x2 + 112, 174, 40, 'Koko kuva')

    # 10 QR
    d.slide('QR-koodit', bg=C['white'])
    d.text(M, M - 4, 200, 'QR-koodit', 20, face='Fredoka', weight=600)
    d.image(QR_INK, M, 32, w=50)
    label(d, M, 84, 50, 'pilke.app · muste')
    d.card(M + 58, 30, 54, 54, fill=C['coral'])
    d.image('QR/qr-pilke-app-valkoinen.png', M + 60, 32, w=50)
    label(d, M + 58, 86, 54, 'pilke.app · valkoinen, vain tummalle tai värikkäälle pohjalle')
    d.qr(M + 120, 30, 54)
    label(d, M + 120, 86, 54, 'pilke.app · valkoisella levyllä (ryhmä)')
    d.image('QR/qr-pilke-app-beta-muste.png', M + 182, 32, w=50)
    label(d, M + 182, 84, 54, 'pilke.app/#beta · muste')
    d.image('QR/qr-app-store-muste.png', M, 108, w=40)
    label(d, M, 150, 44, 'App Store · muste')
    d.image('QR/qr-google-play-muste.png', M + 50, 108, w=40)
    label(d, M + 50, 150, 44, 'Google Play · muste')
    d.text(M + 100, 112, 150, 'App Storen ja Google Playn sivut avautuvat sovelluksen julkaisun myötä, ja siihen asti '
           'koodit vievät tyhjälle sivulle. Käytä niitä, kun sovellus on kaupoissa.', 11, weight=500, color=C['soft'])
    d.text(M + 100, 140, 150, 'Painettuna QR-koodi toimii parhaiten vähintään 20 mm leveänä ja tummana vaalealla pohjalla.',
           11, weight=500, color=C['soft'])
    return d


# ───────────────────────────── Kuvat ─────────────────────────────

def build_pictures(layout):
    d = Deck('ku', 297, 210, layout)
    M = 14
    d.slide('Ohje', bg=C['ground'])
    d.text(M, M, 260, 'Pilke – kuvat', 32, face='Fredoka', weight=600)
    d.text(M, M + 18, 260, 'Jokainen kuva täysikokoisena. Kopioi kuva (Ctrl+C) ja liitä omaan pohjaasi (Ctrl+V). '
           'Tiedostonimet ovat kuvien alla.', 12, weight=500)
    groups = [
        ('Valokuvat', 'valokuvat'), ('Puhelimet', 'puhelimet'), ('Näyttökuvat', 'nayttokuvat'), ('Kauppakuvat', 'kauppakuvat')]
    for title, folder in groups:
        files = sorted(f for f in os.listdir(os.path.join(OUT, 'Kuvat', folder)) if not f.startswith('.'))
        per = 6 if folder != 'valokuvat' else 6
        for start in range(0, len(files), per):
            chunk = files[start:start + per]
            d.slide(title, bg=C['white'] if folder != 'puhelimet' else C['peach'])
            d.text(M, M - 4, 200, title, 20, face='Fredoka', weight=600)
            cw = (297 - 2 * M) / len(chunk) if folder != 'valokuvat' else (297 - 2 * M) / 3
            for i, f in enumerate(chunk):
                path = f'Kuvat/{folder}/{f}'
                iw, ih = size_of(path)
                if folder == 'valokuvat':
                    r, c = divmod(i, 3)
                    bx, by, bw, bh = M + c * cw, 28 + r * 88, cw - 6, 74
                else:
                    bx, by, bw, bh = M + i * cw, 28, cw - 6, 160
                w = min(bw, bh * iw / ih)
                h = w * ih / iw
                d.image(path, bx, by, w, h)
                d.text(bx - 3, by + h + 1, bw + 6, f, 6.5, color=C['soft'], check=False)
    return d


BUILDERS = {'elementit': build_elements, 'poytakolmio': build_triangle, 'a5-flyer': build_flyer,
            'kuvat': build_pictures}


def main():
    global ASSET_SHA
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('deck', nargs='?', choices=list(BUILDERS))
    ap.add_argument('--assets', default='SHA', help='commit on print-kit-assets that holds out/')
    ap.add_argument('--layout', default='p3', help="the deck's blank layout id, from read_presentation")
    ap.add_argument('--slide', type=int, help='print only this slide number (1-based)')
    ap.add_argument('--summary', action='store_true', help='print slide names and request counts only')
    ap.add_argument('--max-chars', type=int, default=9000, help='split a slide into batches of about this much JSON')
    ap.add_argument('--part', type=int, help='print only this batch (0-based) of the selected slide(s)')
    ap.add_argument('--texts', action='store_true', help='print every text box id and its text, for checking a built deck')
    ap.add_argument('--notes', action='store_true',
                    help="print each slide's speaker notes as JSON: insert them into the slide's notes shape "
                         '(read_slide_page: notesPage.notesProperties.speakerNotesObjectId) once the slide exists')
    ap.add_argument('--replace-images', metavar='PATTERN',
                    help='print replaceImage requests for every image whose out/ path contains PATTERN, '
                         'pointing at --assets: how a refreshed picture reaches a built deck in place')
    args = ap.parse_args()
    if not args.deck:
        sys.exit('name a deck: ' + ', '.join(BUILDERS))
    ASSET_SHA = args.assets
    d = BUILDERS[args.deck](args.layout)
    for w in d.warnings:
        print('warning:', w, file=sys.stderr)
    if args.replace_images:
        reqs = []
        for bt in d.batches:
            for r in bt['requests']:
                if 'createImage' in r and args.replace_images in urllib.parse.unquote(r['createImage']['url']):
                    reqs.append({'replaceImage': {'imageObjectId': r['createImage']['objectId'],
                                                  'url': r['createImage']['url'], 'imageReplaceMethod': 'CENTER_INSIDE'}})
        json.dump(reqs, sys.stdout, ensure_ascii=False, separators=(',', ':'))
        print()
        return
    if args.notes:
        json.dump(d.notes, sys.stdout, ensure_ascii=False)
        print()
        return
    if args.texts:
        for b in d.batches:
            for r in b['requests']:
                if 'insertText' in r:
                    print(json.dumps([r['insertText']['objectId'], r['insertText']['text']], ensure_ascii=False))
        return
    if args.summary:
        for i, b in enumerate(d.batches, 1):
            print(i, b['slide'], b['name'], len(b['requests']), len(json.dumps(b['requests'], ensure_ascii=False)))
        return
    batches = d.batches if not args.slide else [d.batches[args.slide - 1]]
    out = []
    for b in batches:
        out += chunks(b['requests'], args.max_chars)
    if args.part is not None:
        out = [out[args.part]]
    json.dump(out, sys.stdout, ensure_ascii=False, separators=(',', ':'))
    print()


def chunks(reqs, limit):
    """A slide's requests in pieces of at most `limit` characters of JSON, in order, never
    splitting an element's own requests from its creation (a group comes after its
    children, which are earlier in the same order)."""
    out, cur, size = [], [], 0
    for r in reqs:
        n = len(json.dumps(r, ensure_ascii=False, separators=(',', ':')))
        starts = any(k in r for k in ('createShape', 'createImage', 'createLine', 'groupObjects'))
        if cur and starts and size + n > limit:
            out.append(cur)
            cur, size = [], 0
        cur.append(r)
        size += n
    if cur:
        out.append(cur)
    return out


if __name__ == '__main__':
    main()
