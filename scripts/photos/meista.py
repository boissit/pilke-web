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
  * A screen is a design-tool frame on its grey canvas, with the frame's name
    above it. It is cut to the frame.

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
SCREENS = ['visu1.jpg']


def stem(name):
    return os.path.splitext(name)[0]


def device(name):
    rgb = np.array(Image.open(os.path.join(SRC, name)).convert('RGB'))
    dark = (rgb.max(axis=2) < BLACK).astype(np.uint8)
    count, labels = cv2.connectedComponents(dark, connectivity=4)
    edge = np.unique(np.concatenate([labels[0], labels[-1], labels[:, 0], labels[:, -1]]))
    ground = np.isin(labels, edge[edge != 0]) if count > 1 else np.zeros_like(dark, bool)
    # One pixel in from the cut, and softened over a pixel, so the outline keeps no
    # dark fringe of the ground it was cut from and no stair-steps.
    keep = cv2.erode((~ground).astype(np.uint8) * 255, np.ones((3, 3), np.uint8))
    alpha = cv2.GaussianBlur(keep, (3, 3), 0.8)
    ys, xs = np.nonzero(alpha)
    box = (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)
    out = Image.fromarray(np.dstack([rgb, alpha])).crop(box)
    out.save(os.path.join(WEB, stem(name) + '.png'), optimize=True)


def screen(name):
    im = Image.open(os.path.join(SRC, name)).convert('RGB')
    rgb = np.array(im).astype(int)
    canvas = rgb[2, 2]
    differs = np.abs(rgb - canvas).max(axis=2) > 6
    # The frame is the run of rows and columns that are mostly not canvas; the
    # frame's name above it is a few words, never most of a row.
    rows = np.nonzero(differs.mean(axis=1) > 0.5)[0]
    cols = np.nonzero(differs.mean(axis=0) > 0.5)[0]
    im.crop((cols.min(), rows.min(), cols.max() + 1, rows.max() + 1)).save(
        os.path.join(WEB, stem(name) + '.jpg'), quality=92, subsampling=0, optimize=True)


os.makedirs(WEB, exist_ok=True)
for name in PHOTOS:
    shutil.copyfile(os.path.join(SRC, name), os.path.join(WEB, name))
for name in DEVICES:
    device(name)
for name in SCREENS:
    screen(name)

known = set(PHOTOS + DEVICES + SCREENS)
unknown = sorted(n for n in os.listdir(SRC) if not n.startswith('.') and n not in known)
if unknown:
    raise SystemExit(f"meista/ has {', '.join(unknown)}, which meista.py does not know: add each to its kind above.")
print(f'meista.py: {len(known)} pictures into src/assets/meista')
