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

    def struck(self, x, y, w, steps, size, gap=0.35, colour=C['soft'], right=None):
        """The front page's struck-through steps: one line of Fredoka per step and a coral
        bar over it, a little below the middle of the lowercase (index.astro, `.elsewhere`).
        Each step is its text box and its bar, grouped, so it moves as one. With `right`,
        each line is set so its bar, the line's rightmost ink, ends there."""
        groups = []
        for step in steps:
            if right is not None:
                tw = text_width_mm(step, 'Fredoka', 600, size)
                x = right - INSET_X - tw - 0.04 * size * PT_MM
                w = tw + 2 * INSET_X + 1
            g, line_h = self.struck_one(x, y, w, step, size, colour)
            groups.append(g)
            y += line_h - 2 * INSET_Y + gap * size * PT_MM
        return groups, y

    def struck_one(self, x, y, w, step, size, colour=C['soft']):
        line_h = size * PT_MM * LINE_EM['Fredoka'] + 2 * INSET_Y + 0.6
        tid, _ = self.text(x, y, w, step, size, face='Fredoka', weight=600, color=colour, h=line_h,
                           valign='MIDDLE', spacing=100, role='st')
        tw = text_width_mm(step, 'Fredoka', 600, size)
        em = size * PT_MM
        bar_h = 0.09 * em * 1.15
        bar = self.shape('FLOW_CHART_TERMINATOR', x + INSET_X - 0.04 * em, y + line_h / 2 + 0.03 * em - bar_h / 2,
                         tw + 0.08 * em, bar_h, fill=C['coral'], role='bar')
        return self.group([tid, bar]), line_h

    def disc_number(self, cx, cy, d, n, fill=C['white'], size=None):
        """A number centred in a disc, by its ink: the disc and a text box holding only
        the digits, placed so the digits' drawn middle sits on the disc's centre, and
        grouped. A number typed into the disc itself sits wherever Slides' own insets and
        the font's line box put it, which is a little low and off to one side."""
        size = size or round(d / PT_MM * 0.5, 1)
        disc = self.shape('ELLIPSE', cx - d / 2, cy - d / 2, d, d, fill=fill, role='num')
        label = str(n)
        f = pil_font('Fredoka', 600)
        x0, y0, x1, y1 = f.getbbox(label, anchor='ls')     # px at 200, y up is negative
        k = size * PT_MM / 200
        ink_cx, ink_cy = (x0 + x1) / 2 * k, (y0 + y1) / 2 * k
        baseline = cy - ink_cy
        top = baseline - first_line_mid(0, size) - 0.35 * size * PT_MM
        bw = (x1 - x0) * k + 2 * INSET_X + 2
        left = cx - ink_cx - INSET_X + 0.16   # Slides draws a lone digit 0.16 mm left of PIL's ink (PDF, 300 dpi)
        tid, _ = self.text(left, top, bw, label, size, face='Fredoka', weight=600, role='nt', check=False)
        return self.group([disc, tid])

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
    'form': 'forms.gle/LNjDw77d5giuxFWeA',   # printed; the code reads https://forms.gle/LNjDw77d5giuxFWeA
    'area': 'Pilke toimii toistaiseksi vain pääkaupunkiseudulla.',
    # The flyer's back, the owner's own words (2026-10-26), kept verbatim.
    'testers.title': 'Etsimme testaajia',
    'testers.body': 'Pilke on uudenlainen treffisovellus, jonka ainoa tarkoitus on viedä sinut treffeille. '
                    'Pilkettä kehitetään kaveriporukan voimin ilman kaupallisia intressejä, joten toivomme '
                    'aidosti luovamme sovelluksen, joka auttaa löytämään parhaat mahdolliset treffikumppanit.',
    'testers.ask': 'Etsimme ihmisiä, jotka ovat kiinnostuneita testaamaan sovelluskonseptia, varmentamaan idean '
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
    # The flow's last three bodies and its sixth step, the owner's own words (2026-10-26),
    # kept verbatim, capitals and all.
    'flow.date.body': 'Pitäkää hauskaa ja tutustukaa toisiinne!',
    'flow.feedback.body': 'Vastaa treffien jälkeen lyhyeen kyselyyn, jotta voimme löytää seuraaville treffeille '
                          'vielä parempia ehdokkaita.',
    'flow.again.title': 'Uudet treffit?',
    'flow.again.body': 'Jatka treffeillä käymistä kunnes löydät itsellesi Sen Oikean.',
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
        d.disc_number(m + 4.5, first_line_mid(y - 0.5, 12), 9, i)
        tid, h1 = d.text(m + 12, y - 0.5, w - 12, head, 12, weight=700)
        _, h2 = d.text(m + 12, y + h1 - 1.5, w - 12, body, 10.5, color=C['soft'])
        y += max(h1 + h2, 10) + 3
    if note:
        d.text(m, y + 2, d.W - 2 * m, note, 9.5, color=C['soft'])
    return y


# How far inside a left-aligned box the first glyph's ink starts, by its first letter,
# measured on the decks' PDF export: the box's own inset and the letter's side bearing as
# Slides sets it, in ems. A letter not listed takes 0.03 em.
INK_LSB_EM = {('Figtree', 500, 'P'): 0.045, ('Figtree', 500, 'E'): 0.045, ('Fredoka', 600, 'N'): 0.012,
              ('Fredoka', 600, 'H'): 0.013}
FREDOKA_ADVANCE = 1.216   # Slides' line advance for Fredoka at 100 % spacing and 22 pt, in ems (PDF export)


def ink_in(text, size_pt, face='Figtree', weight=400):
    """How far right of a left-aligned box's edge its first glyph's ink starts, mm."""
    return INSET_X + INK_LSB_EM.get((face, weight, text[0]), 0.03) * size_pt * PT_MM


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


def text_height(text, w, size, face='Figtree', weight=400, spacing=None, after=0):
    """The height Deck.text gives a box of this text and width, mm."""
    spacing = spacing or (100 if face == 'Fredoka' else 125)
    lines = wrap(text, face, weight, size, w - 2 * INSET_X)
    line_mm = size * PT_MM * LINE_EM[face] * spacing / 100
    return len(lines) * line_mm + text.count('\n') * after * PT_MM + 2 * INSET_Y + 0.6


def steps_height(x, w, items, title_pt, body_pt, d_num=7, tuck=2):
    """What steps() takes with no gaps, mm."""
    tx = x + d_num + 2.5 - INSET_X
    tw = x + w - tx
    return sum(text_height(t, tw, title_pt, face='Fredoka', weight=600)
               + (text_height(b, tw, body_pt) - tuck if b else 0) for t, b in items)


DESCENDS = set('gjpqy,;')
DESC_EM = {'Figtree': 0.21, 'Fredoka': 0.225}   # how far a descender reaches below the baseline (PDF export)


def ink_below(text, w, size, face='Figtree', weight=400):
    """From the ink's foot on a text box's last line down to the box's foot, mm: a line
    with no descender ends its ink on the baseline."""
    em = size * PT_MM
    lines = wrap(text, face, weight, size, w - 2 * INSET_X)
    line_mm = em * LINE_EM[face] * (100 if face == 'Fredoka' else 125) / 100
    foot = 2.39 + 0.957 * em + (len(lines) - 1) * line_mm
    if DESCENDS & set(lines[-1]):
        foot += DESC_EM[face] * em
    return text_height(text, w, size, face, weight) - foot


def steps_ink(x, w, items, title_pt, body_pt, d_num=7, tuck=2):
    """The steps' ink with no gaps between them, from the first disc's top to the last
    line's ink foot, and what each gap must be to leave a given space ink to ink: the
    space less the ink-free strip below each body and above the next disc."""
    tx = x + d_num + 2.5 - INSET_X
    ink_top = first_line_mid(0, title_pt) - d_num / 2
    below = [ink_below(b, x + w - tx, body_pt) for _, b in items]
    ink = steps_height(x, w, items, title_pt, body_pt, d_num, tuck) - ink_top - below[-1]
    ink -= sum(b + ink_top for b in below[:-1])
    return ink_top, ink, [b + ink_top for b in below[:-1]]


def steps(d, x, y, w, items, title_pt, body_pt, gap=3, d_num=7, tuck=2):
    """Numbered steps: a white disc with its number centred in it by the ink, the disc
    centred on the title's capitals, the title the same distance from it on every row.
    Each body's box starts `tuck` mm up inside its title's, which sets the space between
    the two. A list of gaps sets each one in turn."""
    tx = x + d_num + 2.5 - INSET_X
    gaps = gap if isinstance(gap, list) else [gap] * len(items)
    for n, (title, body) in enumerate(items, 1):
        cy = first_line_mid(y, title_pt)
        d.disc_number(x + d_num / 2, cy, d_num, n)
        _, th = d.text(tx, y, x + w - tx, title, title_pt, face='Fredoka', weight=600)
        y += th
        if body:
            _, bh = d.text(tx, y - tuck, x + w - tx, body, body_pt)
            y += bh - tuck
        y += gaps[n - 1] if n <= len(gaps) else 0
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


def store_badges(d, right, y, apple_h):
    """The App Store badge over the Google Play badge, right-aligned on `right` and the
    same width, so the Google Play badge, whose drawn shape is less wide for its height,
    comes out a little taller: at least the size of the other store's badge, as Google
    asks. They are a quarter of the taller one's height apart, the clear space both
    stores ask for round a badge. Returns (width, the y under them, that clear space)."""
    iw, ih = size_of(BADGE_APPLE)
    bw = apple_h * iw / ih
    top, bottom, full = GOOGLE_ROWS
    gw_px, _ = size_of(BADGE_GOOGLE)
    gh_drawn = bw * (bottom - top) / gw_px
    clear = max(apple_h, gh_drawn) / 4
    d.image(BADGE_APPLE, right - bw, y, bw, apple_h, role='bdg')
    gy = y + apple_h + clear
    d.image(BADGE_GOOGLE, right - bw, gy - gh_drawn * top / (bottom - top), bw, gh_drawn * full / (bottom - top),
            role='bdg')
    return bw, gy + gh_drawn, clear


# "Näin se menee käytännössä" in six steps, the same on the tent and the flyer: the
# front page's step cards with the pitch's "Aika ja paikka valmiina" third. The first
# three bodies are the site's own, the first two cut to their first sentence to fit the
# tent's face; the last three are the owner's (PRINT).
def flow():
    return [
        (T['pitch.practice.one.title'], first_sentence(T['pitch.practice.one.body'])),
        (T['pitch.practice.two.title'], first_sentence(T['pitch.practice.two.body'])),
        (T['pitch.instead.ready.title'], T['pitch.instead.ready.body']),
        (T['pitch.practice.three.title'], PRINT['flow.date.body']),
        (T['pitch.practice.four.title'], PRINT['flow.feedback.body']),
        (PRINT['flow.again.title'], PRINT['flow.again.body']),
    ]


def corner_sparkles(d, x, y, w, big=(-6, 4, 18), small=(-21, 13)):
    """Face 1's two top-right sparkles, kept above the face's first line and clear of the
    small wordmark at the left; `big` and `small` place them from the top-right corner."""
    scatter(d, 'persikka', [(x + w + big[0], y + big[1], big[2], 14), (x + w + small[0], y + small[1], 7, -26)])


SMALL_WM = 21   # the wordmark on faces 2 and 3, mm wide


def small_wordmark(d, x, y):
    """The wordmark in the face's top-left corner, small, the same place on faces 2 and 3."""
    d.wordmark('muste', x + 1, y + 3, w=SMALL_WM)
    return SMALL_WM * 0.72 + 4


def triangle_faces(d):
    """Pöytäkolmio · Vihdoin, treffisovellus"""
    # Face 1: the wordmark and the headline on peach, the hand and phone on the coral disc.
    x, y, w, h = tri_card(d, 0, C['peach'])
    scatter(d, 'persikka', [(x + w - 6, y + 4, 18, 14), (x + w - 14, y + 30, 8, -26), (x + 4, y + 104, 10, 30)])
    d.wordmark('muste', x + 1, y + 3, w=40)
    _, hh = headline(d, x, y + 38, w, 30)
    d.text(x, y + 38 + hh + 2, w - 4, T['pitch.hero.lead'], 12.5, weight=500)
    d.image(HERO_DISC, x + 6, y + h - 78 * 33525 / 29575, w=78)
    # Face 2: the wordmark small, the other apps' routine struck through, and what Pilke does.
    x, y, w, h = tri_card(d, 1, C['white'], outline=C['rule'])
    top = y + small_wordmark(d, x, y)
    corner_sparkles(d, x, y, w)
    steps_ = [T['pitch.elsewhere.swipe'], T['pitch.elsewhere.chat'], T['pitch.elsewhere.ghost'],
              T['pitch.elsewhere.swipe'], T['pitch.elsewhere.more'], T['pitch.elsewhere.maybe']]
    _, yy = d.struck(x - 1, top + 4, w + 2, steps_, 21, gap=0.3)
    _, th = d.text(x, yy + 8, w, T['pitch.instead.title'], 24, face='Fredoka', weight=600)
    d.text(x, yy + 8 + th + 4, w - 4, T['pitch.instead.lead'], 13, weight=500)
    d.sparkle('vaalea-koralli', x + w - 10, y + h - 12, 16, 14)
    d.sparkle('vaalea-koralli', x + w - 26, y + h - 4, 7, -24)
    d.sparkle('persikka', x + 8, y + h - 14, 12, 30)
    # Face 3: the small wordmark with the heading beside it, the six steps, then one row:
    # the code with the link under it on the left, the store badges stacked on the right.
    x, y, w, h = tri_card(d, 2, C['mint_ground'])
    bottom = y + h
    # The heading, right-aligned on the face's edge: its first line's capitals start at
    # the top of the wordmark's letters (below the sparkle that sits on the P) and its
    # second line's baseline stands on the letters' foot.
    wm = SMALL_WM
    wh = wm * 0.72
    d.wordmark('muste', x + 1, y + 3, w=wm)
    head = T['pitch.practice.title']
    head = '\n'.join(head.rsplit(' ', 1))
    lead = HEAD_LEADING
    cap_top = y + 3 + WM_LETTER_TOP * wh
    base2 = y + 3 + wh - HEAD_FOOT
    hpt = round((base2 - cap_top) / ((0.70 + FREDOKA_ADVANCE * lead / 100) * PT_MM), 2)
    em = hpt * PT_MM
    lines = head.split('\n')
    widest = max(text_width_mm(t, 'Fredoka', 600, hpt) for t in lines)
    if x + 1 + wm + 3 > x + w - widest:
        d.warnings.append(f'{d.sid} face 3: the heading does not fit beside the wordmark')
    hh = 2 * INSET_Y + 0.6 + len(lines) * em * LINE_EM['Fredoka'] * lead / 100
    base1 = base2 - FREDOKA_ADVANCE * em * lead / 100
    d.text(x + w - widest - 4, baseline_box(base1, hpt) + HEAD_FIRST_BASE * em, widest + 4 + INSET_X, head,
           hpt, face='Fredoka', weight=600, align='END', spacing=lead, h=hh)
    corner_sparkles(d, x, y, w, big=(-5, 23.5, 8), small=(-15, 22.5))
    # One rhythm down the face: the header row, the steps, the code-and-badges row and the
    # note, measured ink to ink, with equal gaps between them; the gaps between the steps,
    # ink to ink as well, are a share of those. The note stands on the content's foot.
    tpt, bpt, gmin = TENT_STEP[:3]
    d_num, tuck = 6.5, 2.5
    note_pt = 8
    note_base = bottom - DESC_EM['Figtree'] * note_pt * PT_MM - 0.2
    note_top = note_base - 0.70 * note_pt * PT_MM
    head_bottom = base2 + DESC_EM['Fredoka'] * em   # the heading's descender, below the wordmark's foot
    apple_h = 11
    iw, ih = size_of(BADGE_APPLE)
    top_r, bottom_r, _ = GOOGLE_ROWS
    gw_px, _ = size_of(BADGE_GOOGLE)
    bw = apple_h * iw / ih
    stack = apple_h + bw * (bottom_r - top_r) / gw_px
    clear = max(apple_h, stack - apple_h) / 4
    stack += clear
    url_pt = 11
    uem = url_pt * PT_MM
    foot_h = stack + DESC_EM['Fredoka'] * uem    # down to pilke.app's descender
    ink_top, need, strips = steps_ink(x, w, flow(), tpt, bpt, d_num=d_num, tuck=tuck)
    n_gaps = len(strips)
    G = (note_top - head_bottom - foot_h - need) / (3 + n_gaps * STEP_SHARE)
    gaps = [G * STEP_SHARE - strip for strip in strips]
    gap = min(gaps)
    if gap < gmin:
        d.warnings.append(f'{d.sid} face 3: the gap between two steps would be {gap:.1f} mm')
    top = head_bottom + G - ink_top
    ry = head_bottom + G + need + n_gaps * G * STEP_SHARE + G
    d.text(x, baseline_box(note_base, note_pt), w, PRINT['area'], note_pt, color=C['soft'], align='CENTER')
    store_badges(d, x + w, ry, apple_h)
    # The code and pilke.app under it make a block as tall as the badges: the plate's top
    # level with the App Store badge's, the link's baseline on the Google Play badge's foot.
    q = stack - 1.5 - 0.70 * uem
    d.qr(x, ry, q, code='site')
    d.text(x - INSET_X, baseline_box(ry + stack, url_pt), q + 2 * INSET_X, PRINT['url'], url_pt, face='Fredoka',
           weight=600, align='CENTER')
    steps(d, x, top, w, flow(), tpt, bpt, gap=gaps, d_num=d_num, tuck=tuck)


TENT_STEP = (10.5, 8.5, 1.0)   # face 3: step title pt, body pt, least gap mm
STEP_SHARE = 1.0    # face 3: the gap between two steps, ink to ink, as a share of the gap between two groups
WM_LETTER_TOP = 0.134   # the wordmark's letters start this far down its height; the sparkle is above
HEAD_FOOT = 0.10        # the heading's second baseline stands this far above the wordmark's foot, mm
HEAD_LEADING = 90       # the heading's line spacing, %
HEAD_FIRST_BASE = 0.097   # at that spacing Slides sets the first baseline this many ems higher (PDF export)


# ───────────────────────────── A5 flyer ─────────────────────────────

A5_CARD = (6, 6, 136, 198)
A5_C = (14, 14, 120, 182)  # content box: 8 mm inside the card, 14 mm from the sheet's edge


def qr_inset(code, d):
    """How far inside a code's plate of side d its modules start, mm: the plate's own
    padding and the quiet zone the PNG carries."""
    path, _ = QR_CODES[code]
    im = Image.open(os.path.join(OUT, path)).convert('RGBA').getchannel('A')
    quiet = im.point(lambda v: 255 if v > 128 else 0).getbbox()[1] / im.size[1]
    pad = d * 0.06
    return pad + (d - 2 * pad) * quiet


def cap_top_box(cap_top, size_pt):
    """The top of a text box whose first line's capitals start at cap_top."""
    return cap_top - 2.39 - (0.957 - 0.70) * size_pt * PT_MM


def baseline_box(baseline, size_pt):
    """The top of a text box whose first baseline is at `baseline`."""
    return baseline - 2.39 - 0.957 * size_pt * PT_MM


def flyer_footer(d, bottom, left):
    """Along the foot of the back, standing on `bottom`: the wordmark on the left, its ink
    starting on the page's shared left edge `left`, the beta form's code on the right,
    the wordmark as tall as the code's modules and level with them, and between them the
    line, the form's address and pilke.app, the address's ink as wide as the line's, the
    three lines' ink starting on one edge and pilke.app's baseline on the modules' foot.
    The block's gaps to the wordmark and the code are equal, as are the lines'."""
    x, _, w, _ = A5_C
    mods = FLYER_CODE
    frac = qr_inset('form', 100) / 100
    q = mods / (1 - 2 * frac)
    inset = q * frac
    title_pt = 16
    t_em = title_pt * PT_MM
    tw = text_width_mm(PRINT['scan'], 'Fredoka', 600, title_pt)
    ink_w = tw - sum(FOOTER_INK['scan'][:2]) * t_em
    per_pt = text_width_mm(PRINT['form'], 'Figtree', 500, 1) - sum(FOOTER_INK['form'][:2]) * PT_MM
    url_pt = round(ink_w / per_pt, 2)
    url_em = url_pt * PT_MM
    iw, ih = size_of(WORDMARK['muste'])   # the PNG is the wordmark's ink box, sparkle tip to the e's foot
    wm_w = mods * iw / ih
    gap = (x + w - inset - left - wm_w - ink_w - mods) / 2
    mod_bottom = bottom - inset
    mod_top = mod_bottom - mods
    d.wordmark('muste', left, mod_top, w=wm_w)
    col = left + wm_w + gap
    # The block runs from the line's ink on the modules' top to pilke.app's baseline on
    # their foot, with equal gaps between the three lines' ink.
    site_base = mod_bottom
    ink = (sum(FOOTER_INK['scan'][2:]) * t_em + sum(FOOTER_INK['form'][2:]) * url_em
           + FOOTER_INK['url'][2] * url_em)
    g = (mods - ink) / 2
    form_base = site_base - FOOTER_INK['url'][2] * url_em - g - FOOTER_INK['form'][3] * url_em
    title_base = mod_top + FOOTER_INK['scan'][2] * t_em
    for key, base, size, face, weight in (('scan', title_base, title_pt, 'Fredoka', 600),
                                          ('form', form_base, url_pt, 'Figtree', 500),
                                          ('url', site_base, url_pt, 'Figtree', 500)):
        bx = col - FOOTER_INK[key][0] * size * PT_MM - INSET_X
        d.text(bx, baseline_box(base, size), tw + 2 * INSET_X + 1, PRINT[key], size, face=face, weight=weight)
    d.qr(x + w - q, bottom - q, q, code='form')
    return mod_top


FLYER_CODE = 18   # the back's code: its modules' side, mm; the wordmark is as tall
# The back's footer lines' ink as Slides sets it, in ems (PDF export): from the box's
# inset edge to the first glyph's ink, from the last glyph's ink back to where PIL ends
# the line, and above and below the baseline.
FOOTER_INK = {'scan': (0.0, 0.120, 0.714, 0.225), 'form': (0.0, 0.102, 0.731, 0.226),
              'url': (0.040, 0.0, 0.718, 0.0)}


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


ELSEWHERE = ['pitch.elsewhere.swipe', 'pitch.elsewhere.chat', 'pitch.elsewhere.ghost',
             'pitch.elsewhere.swipe', 'pitch.elsewhere.more', 'pitch.elsewhere.maybe']


def flyer_front(d):
    """Etupuoli · Vihdoin, treffisovellus"""
    d.card(*A5_CARD, fill=C['peach'])
    x, y, w, h = A5_C
    # The wordmark on the left and the headline on the right of one row.
    wm = 28
    d.wordmark('muste', x, y, w=wm)
    hl = T['hero.title'].replace(', ', ',\n')
    hl_pt = 26
    hl_h = 2 * hl_pt * PT_MM * LINE_EM['Fredoka'] + 2 * INSET_Y + 0.6
    d.text(x + wm + 4, y + wm * 0.72 / 2 - hl_h / 2 + 1, w - wm - 4 + INSET_X, hl, hl_pt, face='Fredoka',
           weight=600, align='END', h=hl_h)
    # Two axes: the wordmark's ink edge on the left, which the lead, the heading and the
    # step numbers share, and the headline's ink edge on the right, which the routine and
    # its line share. The headline's ink ends on the content edge (PDF export).
    right = x + w
    yy = y + wm * 0.72 + 3
    lead = T['pitch.hero.lead']
    lx = x - ink_in(lead, 11.5, weight=500)
    _, lh = d.text(lx, yy, w + x - lx, lead, 11.5, weight=500)
    yy += lh + 2
    # Left: how it goes, the six steps. Right: the other apps' routine struck through and
    # the line under it, and the hand at the foot.
    lw = FLYER_STEP[3]
    head = T['pitch.practice.title']
    hx = x - ink_in(head, 14, face='Fredoka', weight=600)
    _, th = d.text(hx, yy, lw + x - hx, head, 14, face='Fredoka', weight=600)
    end = steps(d, x, yy + th, lw, flow(), FLYER_STEP[0], FLYER_STEP[1], gap=FLYER_STEP[2], d_num=6.5,
                tuck=2.5)
    if end - FLYER_STEP[2] > y + h + 0.2:
        d.warnings.append(f'{d.sid} front: the steps run past the content box ({end - FLYER_STEP[2]:.1f} > {y + h:.1f})')
    rx = x + lw + 4
    rw = x + w - rx
    spt = FLYER_STEP[4]
    _, sy = d.struck(rx - 1, yy, rw + 2, [T[k] for k in ELSEWHERE], spt, gap=0.12, right=right)
    # The line under them follows them to the right edge, its lines ragged on the left as
    # theirs are.
    _, ph = d.text(rx, sy + 1.5, right - rx + INSET_X, T['pitch.instead.title'], spt, face='Fredoka',
                   weight=600, align='END')
    # The hand as wide as the room right of the steps' longest lines, to the card's edge.
    left = x + lw - INSET_X + 1.5
    iw = A5_CARD[0] + A5_CARD[2] - 4 - left
    ih = iw * 1341 / 1183
    iy = A5_CARD[1] + A5_CARD[3] - 4 - ih
    if iy < sy + 1.5 + ph + 2:
        d.warnings.append(f'{d.sid} front: the hand runs into the struck lines ({iy:.1f})')
    d.image(HERO_DISC, left, iy, w=iw)


FLYER_STEP = (11, 8.5, 1.0, 68, 15)   # the front's flow: title pt, body pt, gap mm, column mm, routine pt


def flyer_back(d):
    """Takapuoli · Etsimme testaajia"""
    d.card(*A5_CARD, fill=C['white'], outline=C['rule'])
    scatter(d, 'persikka', [(128, 14, 13, 14), (113, 11, 6, -26), (126, 71, 10, 18)])
    x, y, w, h = A5_C
    _, th = d.text(x, y - 2, w - 22, PRINT['testers.title'], 21, face='Fredoka', weight=600)
    _, bh = d.text(x, y - 2 + th, w, PRINT['testers.body'] + '\n' + PRINT['testers.ask'], 10, weight=500, after=5)
    yy = y - 2 + th + bh + 2
    _, eh = d.text(x, yy, w, PRINT['expect.title'], 13, face='Fredoka', weight=600)
    # The markers' ink starts where the paragraphs' does; the sparkle's ink fills its box.
    mx = x + ink_in(PRINT['testers.body'], 10, weight=500)
    end = bullets(d, mx, yy + eh, x + w - mx,
                  [(PRINT[f'expect.{k}.title'], PRINT[f'expect.{k}.body']) for k in ['beta', 'few', 'area', 'feedback']],
                  10.5, 9.5, title_face='Figtree', gap=2, spark=4.5)
    foot = flyer_footer(d, A5_C[1] + A5_C[3], mx)
    if end > foot - 3:
        d.warnings.append(f'{d.sid} back: the list runs into the footer ({end:.1f} > {foot - 3:.1f})')


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
