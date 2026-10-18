"""What every picture made from an app still assumes about it, checked before use.

A still is cropped and composited by fixed pixel rows: `Phone.astro` cuts the
navigation bar (the bottom 136 rows) off every marketing shot and keeps the status
bar (the top 96), and `comp.py` keeps or replaces the same two bars when it puts a
still into a photograph. Those rows are right only for the capture profile, a
Pixel 4 at 1080 x 2280 with three-button navigation. A still from another profile,
or one where the app has started drawing into a bar, would still composite -- into a
picture with half a clock or a sliver of the Android back button in it -- so each
assumption is checked here and a still that breaks one stops the build, naming the
still and the assumption.

    python stills.py             # every still the site and the photographs use

`comp.load_still` runs `check` on every still a composite reads.
"""
import os
import re
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.normpath(os.path.join(HERE, '../..'))

WIDTH, HEIGHT = 1080, 2280
STATUS = 96              # rows of status bar at the top
NAV = 2144               # first row of the navigation bar
# The three-button bar's glyphs, measured on the capture profile: back, home,
# recents, each inside its window, vertically centred on this row.
NAV_GLYPHS = ((220, 300), (500, 580), (780, 860))
NAV_CENTRE = 2214
# The clock's text in the status bar, vertically centred on this row, and its height.
CLOCK_CENTRE = 42
CLOCK_ROWS = 30


class StillError(Exception):
    pass


def _ink(band, ref):
    """Pixels that differ clearly from the band's own background colour."""
    return np.abs(band - ref).sum(2) > 120


def check(img, name, grounds=False):
    """Raises StillError unless `img` has the capture profile's size and bars.
    `grounds` also checks the row `comp.ios_screen` samples for the colour of the
    home indicator's band: it must be the app's plain ground, not a card or photo."""
    if img.size != (WIDTH, HEIGHT):
        raise StillError(f'{name} is {img.size[0]} x {img.size[1]}, not the capture profile\'s '
                         f'{WIDTH} x {HEIGHT}: the bar crops ({STATUS} and {HEIGHT - NAV} px) are '
                         'measured on a Pixel 4 and would cut into the app')
    a = np.asarray(img.convert('RGB')).astype(int)

    nav = a[NAV:]
    ref = np.median(nav[:, :40].reshape(-1, 3), 0)
    ink = _ink(nav, ref)
    for x0, x1 in NAV_GLYPHS:
        ys, _ = np.nonzero(ink[:, x0:x1])
        if len(ys) < 200 or abs(ys.mean() + NAV - NAV_CENTRE) > 8:
            raise StillError(f'{name}: no navigation-bar glyph centred at y {NAV_CENTRE} between x {x0} '
                             f'and {x1}. The bar is not where the crop at row {NAV} expects it, so the '
                             'still is from another device profile, gesture navigation, or the app '
                             'draws over the bar')
    # Nothing but the glyphs in the bar: ink beside them is the app reaching into it.
    stray = ink.copy()
    for x0, x1 in NAV_GLYPHS:
        stray[:, x0:x1] = False
    stray[:, :12] = stray[:, -12:] = False    # a card's border running off the screen's edge
    if stray.sum() > 400:
        raise StillError(f'{name}: {int(stray.sum())} px of something other than the three buttons in '
                         f'the navigation bar (rows {NAV}-{HEIGHT}), which the crop would cut through')

    # The clock is the densest band of ink on the left of the bar, a line of text 30
    # rows tall. Judged by that band rather than by the mean of every inked row, because
    # a map drawn under the bar (the date screens) streaks it with streets and labels
    # that pulled the mean off the clock; app content in the bar's last rows -- a card
    # the crop would cut -- is denser than the clock and still fails.
    status = a[:STATUS]
    sref = np.median(status[:, 400:680].reshape(-1, 3), 0)
    rows = _ink(status[:, 40:300], sref).sum(1)
    band = np.convolve(rows, np.ones(CLOCK_ROWS, int), 'valid')
    centre = int(band.argmax()) + (CLOCK_ROWS - 1) / 2
    if band.max() < 100 or abs(centre - CLOCK_CENTRE) > 10:
        raise StillError(f'{name}: no clock centred at y {CLOCK_CENTRE} in the status bar (rows 0-{STATUS}); '
                         'the bar is not the height the crop assumes, or the app draws into its last rows')

    # The foot only: a screen drawn edge to edge under the status bar has no ground at
    # its top, and `comp.ios_screen` draws the bar over its picture instead.
    if grounds and not plain_row(a[NAV - 2]):
        raise StillError(f'{name}: row {NAV - 2} is not one colour. comp.ios_screen takes the colour '
                         'of the home indicator\'s band from the middle of this row, so the app has to '
                         'stand on its plain ground there')


def plain_row(row):
    """Whether a row of pixels is the app's plain ground: 85% of it one colour."""
    return (np.abs(row - row[WIDTH // 2]).max(1) <= 12).mean() >= 0.85


def check_phone_astro():
    """`Phone.astro` crops the same rows in CSS, and draws its camera in the middle
    of the status bar it keeps; the two have to agree."""
    css = open(os.path.join(WEB, 'src/components/Phone.astro')).read()
    want = [f'aspect-ratio: {WIDTH} / {NAV}', f'top: {STATUS / 2 / NAV * 100:.2f}%',
            f'top: {STATUS / 2 / HEIGHT * 100:.1f}%']
    missing = [w for w in want if w not in css]
    if missing:
        raise StillError('src/components/Phone.astro does not crop the rows this checks: '
                         f'wants {", ".join(missing)}. Change both together')


# Every still a picture on the site is made from, and whether it goes through
# `ios_screen`. The manual's stills are drawn whole, bars and all, and no picture
# made here reads one.
def stills():
    screens = os.path.join(WEB, 'src/assets/screens')
    out = [(os.path.join(screens, f), False) for f in sorted(os.listdir(screens)) if f.endswith('.png')]
    out += [(os.path.join(HERE, 'stills', f), False) for f in sorted(os.listdir(os.path.join(HERE, 'stills')))
            if f.endswith('.png')]
    ios = {'invitation.png', 'invitation-en.png', 'kalenteri-fi.png', 'kalenteri-en.png'}
    return [(p, os.path.basename(p) in ios) for p, _ in out]


if __name__ == '__main__':
    bad = 0
    try:
        check_phone_astro()
    except StillError as e:
        print(e, file=sys.stderr)
        bad += 1
    for path, grounds in stills():
        try:
            check(Image.open(path), os.path.relpath(path, WEB), grounds)
        except StillError as e:
            print(e, file=sys.stderr)
            bad += 1
    if bad:
        sys.exit(f'{bad} still(s) break what the crops and composites assume; see above')
    print(f'stills: {len(stills())} checked against the {WIDTH} x {HEIGHT} capture profile')
