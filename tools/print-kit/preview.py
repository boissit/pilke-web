"""A local, approximate drawing of what slides.py will put on a page.

    .venv/bin/python preview.py poytakolmio out/preview/      # one PNG per slide

It reads the same request batches `slides.py` compiles and draws them with Pillow:
shapes, lines, images from out/, and text wrapped with the site's own font files at
Slides' line heights. It is close to what Google draws, not identical, and it exists
so a layout can be iterated on without a round trip to the Slides API. The real check
is the Slides thumbnail of each page, after the deck is built.
"""
import math
import os
import sys
import urllib.parse

from PIL import Image, ImageDraw

import slides

PX = 6  # pixels per mm
EMU = slides.EMU


def hexrgb(c):
    return tuple(round(c.get(k, 0) * 255) for k in ('red', 'green', 'blue'))


def render(deck, outdir, prefix):
    os.makedirs(outdir, exist_ok=True)
    W, H = round(deck.W * PX), round(deck.H * PX)
    paths = []
    for b in deck.batches:
        els, order, bg = {}, [], (255, 255, 255)
        for r in b['requests']:
            (kind, body), = r.items()
            if kind == 'updatePageProperties':
                bg = hexrgb(body['pageProperties']['pageBackgroundFill']['solidFill']['color']['rgbColor'])
            elif kind in ('createShape', 'createImage', 'createLine'):
                e = {'kind': kind, 'type': body.get('shapeType') or body.get('lineCategory'), 'props': body['elementProperties'],
                     'url': body.get('url'), 'text': '', 'fill': None, 'outline': None}
                els[body['objectId']] = e
                order.append(body['objectId'])
            elif kind == 'updateShapeProperties':
                e, sp = els[body['objectId']], body['shapeProperties']
                f = sp.get('shapeBackgroundFill', {})
                if 'solidFill' in f:
                    e['fill'] = hexrgb(f['solidFill']['color']['rgbColor'])
                o = sp.get('outline', {})
                if 'outlineFill' in o:
                    e['outline'] = (hexrgb(o['outlineFill']['solidFill']['color']['rgbColor']), o['weight']['magnitude'])
                if 'contentAlignment' in sp:
                    e['valign'] = sp['contentAlignment']
            elif kind == 'updateLineProperties':
                lp = body['lineProperties']
                els[body['objectId']]['line'] = (hexrgb(lp['lineFill']['solidFill']['color']['rgbColor']),
                                                 lp['weight']['magnitude'], lp.get('dashStyle'))
            elif kind == 'insertText':
                els[body['objectId']]['text'] = body['text']
            elif kind == 'updateTextStyle' and body['textRange']['type'] == 'ALL':
                st = body['style']
                els[body['objectId']]['font'] = (st['weightedFontFamily']['fontFamily'], st['weightedFontFamily']['weight'],
                                                 st['fontSize']['magnitude'],
                                                 hexrgb(st['foregroundColor']['opaqueColor']['rgbColor']))
            elif kind == 'updateParagraphStyle':
                e = els[body['objectId']]
                e['align'] = body['style'].get('alignment', e.get('align', 'START'))
                e['spacing'] = body['style'].get('lineSpacing', e.get('spacing', 100))
                e['after'] = body['style'].get('spaceBelow', {}).get('magnitude', 0)
        page = Image.new('RGB', (W, H), bg)
        for oid in order:
            draw_element(page, els[oid])
        path = os.path.join(outdir, f'{prefix}-{b["slide"]}.png')
        page.save(path)
        paths.append(path)
    return paths


def geometry(props):
    w = props['size']['width']['magnitude'] / EMU
    h = props['size']['height']['magnitude'] / EMU
    t = props['transform']
    a, b = t.get('scaleX', 0), t.get('shearY', 0)
    rot = math.degrees(math.atan2(b, a))
    tx, ty = t['translateX'] / EMU, t['translateY'] / EMU
    c, d = t.get('shearX', 0), t.get('scaleY', 0)
    cx = tx + a * w / 2 + c * h / 2
    cy = ty + b * w / 2 + d * h / 2
    return w, h, rot, cx, cy


def draw_element(page, e):
    w, h, rot, cx, cy = geometry(e['props'])
    pw, ph = max(1, round(w * PX)), max(1, round(h * PX))
    layer = Image.new('RGBA', (pw, ph), (0, 0, 0, 0))
    dr = ImageDraw.Draw(layer)
    if e['kind'] == 'createImage':
        path = urllib.parse.unquote(e['url'].split('/', 6)[6])
        im = Image.open(os.path.join(slides.OUT, path)).convert('RGBA')
        im.thumbnail((pw, ph), Image.LANCZOS)
        layer.alpha_composite(im, ((pw - im.width) // 2, (ph - im.height) // 2))
    elif e['kind'] == 'createLine':
        col, wt, dash = e.get('line', ((0, 0, 0), 1, None))
        lw = max(1, round(wt * 25.4 / 72 * PX))
        if dash:
            seg, n = 3 * PX, 0
            length = max(pw, ph)
            while n < length:
                if pw >= ph:
                    dr.line([(n, 0), (min(n + seg, pw), 0)], fill=col, width=lw)
                else:
                    dr.line([(0, n), (0, min(n + seg, ph))], fill=col, width=lw)
                n += 2 * seg
        else:
            dr.line([(0, 0), (pw - 1, ph - 1)], fill=col, width=lw)
    else:
        box = (0, 0, pw - 1, ph - 1)
        ol = e['outline']
        olw = max(1, round(ol[1] * 25.4 / 72 * PX)) if ol else 0
        kw = dict(fill=e['fill'], outline=ol[0] if ol else None, width=olw)
        if e['type'] == 'ROUND_RECTANGLE':
            dr.rounded_rectangle(box, radius=min(pw, ph) / 6, **kw)
        elif e['type'] == 'FLOW_CHART_TERMINATOR':
            dr.rounded_rectangle(box, radius=min(pw, ph) / 2, **kw)
        elif e['type'] == 'ELLIPSE':
            dr.ellipse(box, **kw)
        elif e['type'] == 'RECTANGLE' or (e['type'] == 'TEXT_BOX' and e['fill']):
            dr.rectangle(box, **kw)
        if e['text'] and 'font' in e:
            draw_text(layer, e, w, h)
    if rot:
        layer = layer.rotate(-rot, expand=True, resample=Image.BICUBIC)
    page.paste(layer, (round(cx * PX - layer.width / 2), round(cy * PX - layer.height / 2)), layer)


def draw_text(layer, e, w, h):
    face, weight, size, col = e['font']
    spacing = e.get('spacing', 100)
    inset_x, inset_y = (slides.INSET_X, slides.INSET_Y) if e['type'] == 'TEXT_BOX' else (2.54, 1.27)
    lines = slides.wrap(e['text'], face, weight, size, w - 2 * inset_x)
    f = slides.pil_font(face, weight).font_variant(size=max(1, round(size * 25.4 / 72 * PX)))
    try:
        f.set_variation_by_axes([weight])
    except OSError:
        pass
    line = size * 25.4 / 72 * slides.LINE_EM[face] * spacing / 100
    total = len(lines) * line
    va = e.get('valign', 'TOP')
    y = inset_y if va == 'TOP' else (h - total) / 2 if va == 'MIDDLE' else h - inset_y - total
    dr = ImageDraw.Draw(layer)
    asc = 0.974 if face == 'Fredoka' else 0.95
    for s in lines:
        tw = slides.text_width_mm(s, face, weight, size)
        al = e.get('align', 'START')
        x = inset_x if al == 'START' else (w - tw) / 2 if al == 'CENTER' else w - inset_x - tw
        base = y + (line - size * 25.4 / 72 * slides.LINE_EM[face]) / 2 + size * 25.4 / 72 * asc
        dr.text((x * PX, base * PX), s, font=f, fill=col, anchor='ls')
        y += line


if __name__ == '__main__':
    deck, outdir = sys.argv[1], sys.argv[2]
    slides.ASSET_SHA = 'local'
    d = slides.BUILDERS[deck]('p3')
    for w in d.warnings:
        print('warning:', w)
    for p in render(d, outdir, deck):
        print(p)
