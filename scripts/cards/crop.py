"""Cut one card out of a simulator screenshot, to its outer ink rule, transparent outside.

    python crop.py <screenshot.png> <x0> <y0> <x1> <y1> <out.png>

The box is a rough one round the card; the card's own rule is found inside it: the
first and last rows and columns that are mostly ink. Outside the rounded corners the
sheet's ground is flood-filled from the four corners and made transparent, and the
pixels on the curve get an alpha from how far they are from that ground, so the edge
stays anti-aliased.
"""
import sys
from collections import deque

import numpy as np
from PIL import Image

src, x0, y0, x1, y1, out = sys.argv[1], *map(int, sys.argv[2:6]), sys.argv[6]
im = np.asarray(Image.open(src).convert('RGB')).astype(int)
box = im[y0:y1, x0:x1]
dark = box.sum(2) < 3 * 110

rows = np.nonzero(dark.mean(1) > 0.6)[0]
cols = np.nonzero(dark.mean(0) > 0.6)[0]
top, bottom = rows[0], rows[-1]
left, right = cols[0], cols[-1]
card = box[top:bottom + 1, left:right + 1]
h, w, _ = card.shape

ground = card[0, 0].copy()
ink = np.array([60, 60, 60])
dist = np.sqrt(((card - ground) ** 2).sum(2))
full = np.sqrt(((ink - ground) ** 2).sum())

outside = np.zeros((h, w), bool)
queue = deque([(0, 0), (0, w - 1), (h - 1, 0), (h - 1, w - 1)])
for y, x in queue:
    outside[y, x] = True
while queue:
    y, x = queue.popleft()
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        ny, nx = y + dy, x + dx
        if 0 <= ny < h and 0 <= nx < w and not outside[ny, nx] and dist[ny, nx] < 0.35 * full:
            outside[ny, nx] = True
            queue.append((ny, nx))

alpha = np.full((h, w), 255.0)
alpha[outside] = 0
# The curve: the first inside pixels next to the cut take their coverage from colour.
edge = ~outside & (np.roll(outside, 1, 0) | np.roll(outside, -1, 0) | np.roll(outside, 1, 1) | np.roll(outside, -1, 1))
alpha[edge] = np.clip(dist[edge] / full, 0, 1) * 255
rgb = card.copy()
rgb[edge] = ink

Image.fromarray(np.dstack([rgb, alpha]).astype(np.uint8), 'RGBA').save(out, optimize=True)
print(out, w, h, 'from', x0 + left, y0 + top)
