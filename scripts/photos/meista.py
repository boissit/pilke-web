"""The owner's pictures for the timeline on /meista, from meista/ into src/assets/meista.

Run from this directory, by build.sh or on its own once a new file is in meista/.

The originals are the owner's files as they were sent, under the owner's own names,
which are also the names the page's slots look for. Each is made into its picture
by its kind:

  * A photograph is copied as it is. Astro resizes it for the page.
  * A phone shot comes as a device frame drawn on black, and black round a phone
    is a dark slab on the page's peach. The black is masked off: every near-black
    region touching the image's edge is background, and what is left is the
    device, cut out to its own outline on transparent and written as PNG.
  * A tile is artwork on a rounded tile, drawn on white: the white is masked off
    the same way, and the tile stands on the page by its own outline.
  * A screenshot of a browser keeps only the page it shows: the box below cuts the
    browser's toolbar, its address and profile picture, off the top, and the
    window's edge and scrollbar off the sides.
  * A screen is a design-tool frame on its grey canvas, with the frame's name
    above it. It is cut to the frame and set into the phone of another phone
    shot, so it stands beside that one as the same device: the screen is fitted
    whole to the phone's screen, inside the notch and the rounded corners, and
    the room its proportions leave above and below is its own top and bottom
    rows carried on. It runs the screen's full width: only its background meets
    the corners, and its content keeps the design's own margins inside them.

The same inputs give the same bytes out, every run.
"""
import os
import shutil

import cv2
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'meista')
WEB = os.path.join(HERE, '../../src/assets/meista')

# Below this in every channel a pixel is the black ground. The JPEGs' ground is
# noise round zero, and the darkest part of a device's own edge is well above it.
BLACK = 28

PHOTOS = ['boissit.jpg', 'designsprint.jpg', 'designsprint2.jpg']
DEVICES = ['visu2.jpg', 'mockup1.png', 'mockup2.png', 'mockup3.png', 'latevisu1.jpg', 'latevisu2.jpg']
TILES = ['logo.jpg']
# A browser screenshot, and the box of it that is the page: measured on the file.
BROWSER = {'map.jpg': (8, 26, 1263, 678)}
# Above this in every channel a pixel is a tile's white ground.
WHITE = 236
# A screen, and the device whose phone it is set into.
SCREENS = {'visu1.jpg': 'visu2.jpg'}

# Between the screen's content and the phone's notch, in the phone's pixels.
SCREEN_MARGIN = 12
# The design tool's anti-aliased edge round a frame, trimmed so it is not carried on.
FRAME_EDGE = 3


def stem(name):
    return os.path.splitext(name)[0]


def cut_out(rgb, ground=None):
    """The alpha of what stands on a plain ground: everything but the ground's
    regions touching the image's edge. The ground is near-black unless given."""
    dark = ((rgb.max(axis=2) < BLACK) if ground is None else ground).astype(np.uint8)
    count, labels = cv2.connectedComponents(dark, connectivity=4)
    edge = np.unique(np.concatenate([labels[0], labels[-1], labels[:, 0], labels[:, -1]]))
    ground = np.isin(labels, edge[edge != 0]) if count > 1 else np.zeros_like(dark, bool)
    # One pixel in from the cut, and softened over a pixel, so the outline keeps no
    # dark fringe of the ground it was cut from and no stair-steps.
    keep = cv2.erode((~ground).astype(np.uint8) * 255, np.ones((3, 3), np.uint8))
    return cv2.GaussianBlur(keep, (3, 3), 0.8)


def save_device(rgb, alpha, name):
    ys, xs = np.nonzero(alpha)
    box = (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)
    Image.fromarray(np.dstack([rgb, alpha])).crop(box).save(os.path.join(WEB, stem(name) + '.png'), optimize=True)


def device(name):
    rgb = np.array(Image.open(os.path.join(SRC, name)).convert('RGB'))
    save_device(rgb, cut_out(rgb), name)


def tile(name):
    rgb = np.array(Image.open(os.path.join(SRC, name)).convert('RGB'))
    save_device(rgb, cut_out(rgb, rgb.min(axis=2) > WHITE), name)


def browser(name, box):
    Image.open(os.path.join(SRC, name)).convert('RGB').crop(box).save(
        os.path.join(WEB, name), quality=90, subsampling=0, optimize=True)


def frame_of(rgb):
    """The phone's screen in a device shot: the lit region round the image's centre,
    with whatever is drawn on it filled in, and the notch and corners left out."""
    lit = (rgb.max(axis=2) >= BLACK).astype(np.uint8)
    _, labels = cv2.connectedComponents(lit, connectivity=4)
    h, w = lit.shape
    region = (labels == labels[h // 2, w // 2]).astype(np.uint8)
    contours, _ = cv2.findContours(region, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    screen = np.zeros_like(region)
    cv2.drawContours(screen, [max(contours, key=cv2.contourArea)], -1, 1, thickness=cv2.FILLED)
    return screen


def screen(name, into):
    im = Image.open(os.path.join(SRC, name)).convert('RGB')
    rgb = np.array(im).astype(int)
    canvas = rgb[2, 2]
    differs = np.abs(rgb - canvas).max(axis=2) > 6
    # The frame is the run of rows and columns that are mostly not canvas; the
    # frame's name above it is a few words, never most of a row.
    rows = np.nonzero(differs.mean(axis=1) > 0.5)[0]
    cols = np.nonzero(differs.mean(axis=0) > 0.5)[0]
    e = FRAME_EDGE
    design = np.array(im.crop((cols.min() + e, rows.min() + e, cols.max() + 1 - e, rows.max() + 1 - e)))

    phone = np.array(Image.open(os.path.join(SRC, into)).convert('RGB'))
    area = frame_of(phone)
    ys, xs = np.nonzero(area)
    top, bottom, left, right = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    # The notch's depth: how far down the screen's middle column starts below its top.
    notch = np.nonzero(area[:, (left + right) // 2])[0].min() - top

    # Whole, as wide as the screen, and below the notch.
    width = right - left
    height = round(design.shape[0] * width / design.shape[1])
    room = bottom - top - height
    above = max(room // 2, notch + SCREEN_MARGIN)
    if room - above < SCREEN_MARGIN:
        raise SystemExit(f'{name} does not fit inside the screen of {into} below its notch.')
    design = cv2.resize(design, (width, height), interpolation=cv2.INTER_AREA)
    # The design's own edges carried on round it, so the room left is its background.
    filled = cv2.copyMakeBorder(design, above, bottom - top - height - above, 0, 0, cv2.BORDER_REPLICATE)

    out = phone.copy()
    soft = cv2.GaussianBlur(area.astype(np.float32), (3, 3), 0.8)[top:bottom, left:right, None]
    out[top:bottom, left:right] = (filled * soft + phone[top:bottom, left:right] * (1 - soft)).round().astype(np.uint8)
    save_device(out, cut_out(phone), name)


os.makedirs(WEB, exist_ok=True)
for name in PHOTOS:
    shutil.copyfile(os.path.join(SRC, name), os.path.join(WEB, name))
for name in DEVICES:
    device(name)
for name in TILES:
    tile(name)
for name, box in BROWSER.items():
    browser(name, box)
for name, into in SCREENS.items():
    screen(name, into)

known = set(PHOTOS + DEVICES + TILES) | set(BROWSER) | set(SCREENS)
unknown = sorted(n for n in os.listdir(SRC) if not n.startswith('.') and n not in known)
if unknown:
    raise SystemExit(f"meista/ has {', '.join(unknown)}, which meista.py does not know: add each to its kind above.")
print(f'meista.py: {len(known)} pictures into src/assets/meista')
