"""One contact sheet of every page of the print kit's Slides files.

    .venv/bin/python overview.py THUMBS_DIR overview.jpg

THUMBS_DIR holds the Slides thumbnails (or preview.py's drawings) named
`<deck>-<slide>.png`. The sheet has one row per deck, in the order below, each page
scaled to the same height and labelled, and is at most 3600 px on its long side.
"""
import glob
import os
import sys

from PIL import Image, ImageDraw

import slides

DECKS = [('poytakolmio', 'Pilke – pöytäkolmio (A4 vaaka)'), ('a5-flyer', 'Pilke – A5-flyer'),
         ('elementit', 'Pilke – elementit (A4 vaaka)'), ('kuvat', 'Pilke – kuvat (A4 vaaka)')]
ROW_H, GAP, HEAD, MAX = 560, 24, 70, 3600


def main(src, dst):
    rows = []
    for key, title in DECKS:
        files = sorted(glob.glob(os.path.join(src, f'{key}-*.png')))
        if files:
            ims = [Image.open(f).convert('RGB') for f in files]
            ims = [im.resize((round(im.width * ROW_H / im.height), ROW_H), Image.LANCZOS) for im in ims]
            rows.append((title, ims))
    width = max(sum(im.width for im in ims) + GAP * (len(ims) + 1) for _, ims in rows)
    height = sum(HEAD + ROW_H + GAP for _ in rows) + GAP
    sheet = Image.new('RGB', (width, height), (240, 221, 213))
    d = ImageDraw.Draw(sheet)
    title_font = slides.pil_font('Fredoka', 600).font_variant(size=44)
    title_font.set_variation_by_axes([600])
    y = GAP
    for title, ims in rows:
        d.text((GAP, y + 10), title, font=title_font, fill=(58, 46, 43))
        x = GAP
        for im in ims:
            sheet.paste(im, (x, y + HEAD))
            x += im.width + GAP
        y += HEAD + ROW_H + GAP
    sheet.thumbnail((MAX, MAX), Image.LANCZOS)
    sheet.save(dst, quality=88, optimize=True)
    print(dst, sheet.size)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
