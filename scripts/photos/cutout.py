"""The hero: the hand and the phone cut out of the take-1 composite, for the
coral disc.

GrabCut, seeded with the phone as certain and a hand drawn round the rest, gives
a trimap: certain hand, certain room, and a band between. In the band the alpha
is solved from the colours either side, the hand's and the room's, each spread
in from the certain pixels nearest; the room behind is out of focus, so its
colour under the edge is well estimated. The phone's rim is dark and the room
round it light, so dark pixels by the phone stay. The colours in the band are
the hand's own, spread in from inside, so no fringe of the room shows on the
coral. The arm fades
out towards the left, where the photograph cuts it.

The cut is made once, on the Finnish composite, and the same alpha is laid on
each language's: the phone is opaque, so what its screen shows cannot move the
edge. Reads hero-<lang>-full.jpg (hero.py fi, hero.py en), writes
cutout-<lang>-full.png."""
import sys

import cv2
import numpy as np
from PIL import Image

sys.path.insert(0, __file__.rsplit('/', 1)[0])
from comp import LANGS
from comp2 import filled_blur

im = cv2.imread('hero-fi-full.jpg')
H, W = im.shape[:2]
I = cv2.cvtColor(im, cv2.COLOR_BGR2RGB).astype(np.float32) / 255
L = I.mean(2)

# The screen as fitted by hero.py, and the phone's body round it.
screen = np.float32([(1352.36, 1421.98), (2256.93, 1500.17), (2036.83, 3363.11), (1157.08, 3253.44)])
phone = np.float32([(1320, 1360), (2290, 1440), (2080, 3430), (1175, 3310)])
hand = np.float32([(0, 2860), (600, 2480), (950, 1930), (1150, 1360), (1210, 1285), (1270, 1265), (1320, 1290),
                   (1330, 1340), (2290, 1420), (2400, 1850), (2410, 2760), (2250, 2800), (2100, 3450), (1150, 3310),
                   (1170, 3100), (1000, 3205), (850, 3275), (700, 3335), (0, 3570)])
wedge = np.float32([(1148, 3120), (1150, 3292), (700, 3345), (1000, 3212)])          # table under the palm
nail = np.float32([(1246, 1341), (1261, 1328), (1279, 1327), (1289, 1337), (1300, 1420), (1244, 1440)])  # thumbnail, certain


def poly(pts, scale=1.0, shape=(H, W)):
    m = np.zeros((round(shape[0]), round(shape[1])), np.uint8)
    cv2.fillPoly(m, [np.int32(np.round(pts * scale))], 1)
    return m


# 1. GrabCut at half size.
s = 0.5
sm = cv2.resize(im, None, fx=s, fy=s, interpolation=cv2.INTER_AREA)
shp = sm.shape[:2]
mask = np.full(shp, cv2.GC_BGD, np.uint8)
pf = poly(hand, s, shp)
mask[cv2.dilate(pf, np.ones((61, 61), np.uint8)) > 0] = cv2.GC_PR_BGD
mask[pf > 0] = cv2.GC_PR_FGD
mask[poly(phone, s, shp) > 0] = cv2.GC_FGD
mask[poly(nail, s, shp) > 0] = cv2.GC_FGD
mask[poly(wedge, s, shp) > 0] = cv2.GC_BGD
cv2.setRNGSeed(7)
bgd = np.zeros((1, 65), np.float64)
fgd = np.zeros((1, 65), np.float64)
cv2.grabCut(sm, mask, None, bgd, fgd, 8, cv2.GC_INIT_WITH_MASK)
m = np.where((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD), 1, 0).astype(np.uint8)
n, lab, st, _ = cv2.connectedComponentsWithStats(m)
m = (lab == 1 + np.argmax(st[1:, 4])).astype(np.uint8)
m = cv2.resize(m, (W, H), interpolation=cv2.INTER_NEAREST)
m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15)))

# 2. The trimap.
ell = lambda k: cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k))
screen_in = cv2.dilate(poly(screen), ell(21))
fg_sure = np.maximum(np.maximum(cv2.erode(m, ell(19)), screen_in), poly(nail))
bg_sure = cv2.erode(1 - m, ell(19))
bg_sure[poly(wedge) > 0] = 1
bg_sure[fg_sure > 0] = 0
band = (1 - fg_sure) * (1 - bg_sure)

# 3. The colours either side, spread in from the certain pixels nearest.
F = filled_blur(I, fg_sure.astype(np.float32), sigmas=(3, 8, 24, 80))
B = filled_blur(I, bg_sure.astype(np.float32), sigmas=(3, 8, 24, 80))
d = F - B
den = (d * d).sum(2)
a_band = np.clip(((I - B) * d).sum(2) / np.maximum(den, 1e-4), 0, 1)
# Where the two are too alike to tell apart, the cut decides, softened.
soft_m = cv2.GaussianBlur(m.astype(np.float32), (0, 0), 1.5)
w = np.clip((np.sqrt(den) - 0.05) / 0.08, 0, 1)
a_band = a_band * w + soft_m * (1 - w)
a = np.where(fg_sure > 0, 1.0, np.where(bg_sure > 0, 0.0, a_band)).astype(np.float32)

# 4. The rim: dark pixels by the phone are the phone. It is a neutral dark,
# where the plant seen past its top corner is a dark green.
near = cv2.dilate(poly(phone), ell(61)).astype(np.float32)
Ib = cv2.GaussianBlur(I, (0, 0), 0.8)
neutral = np.clip((Ib[..., 0] - Ib[..., 1] + 0.02) / 0.03, 0, 1)
rim = np.clip((0.36 - Ib.mean(2)) / 0.1, 0, 1) * neutral * near
a = np.maximum(a, rim)
# Below the fingers, past the phone's glass edge (25px out from the fitted
# screen, measured), there is only the room.
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
edge = screen[1][0] + (yy - screen[1][1]) * (screen[2][0] - screen[1][0]) / (screen[2][1] - screen[1][1]) + 27
past = np.clip((xx - edge) / 2.0, 0, 1) * (yy > 2760)
a = a * (1 - past)
# Past the phone's foot (its bottom bezel, 75px below the fitted screen) there is
# only its rim: the room there is light, the rim dark.
foot = screen[3][1] + (xx - screen[3][0]) * (screen[2][1] - screen[3][1]) / (screen[2][0] - screen[3][0]) + 75
below = np.clip((yy - foot) / 2.0, 0, 1) * (xx > 1150)
a = a * (1 - below) + np.minimum(a, rim) * below
# Round the phone's bottom-right corner the same way: off the screen, only rim.
corner = ((xx > 1980) & (yy > 3330) & (poly(screen) == 0)).astype(np.float32)
a = a * (1 - corner) + np.minimum(a, rim) * corner

# Round the thumb, where the plant behind is green, nothing green is hand
# (skin's r - g is at least 0.03 on this hand, the plant's at most 0.012); the
# thumb's edge is short and smooth, so the test cannot roughen it much.
notgreen = np.clip((Ib[..., 0] - Ib[..., 1] - 0.012) / 0.02, 0, 1)
thumb = np.zeros((H, W), np.float32)
thumb[1260:1480, 1140:1400] = 1
thumb = cv2.GaussianBlur(thumb, (0, 0), 8)
a = np.where(band > 0, a * (1 - thumb + thumb * np.maximum(notgreen, rim)), a)

# 5. Feather: a smooth, slightly soft edge, then the arm's fade.
a = cv2.GaussianBlur(a, (0, 0), 0.8)
x = np.arange(W, dtype=np.float32)
a *= np.clip((x - 350) / 650, 0, 1)[None, :] ** 1.5

# 6. The band takes the hand's own colour, spread in from inside, fading to the
# photo's where the alpha is nearly whole: none of the room's colour is left at
# the edge to show against the coral. The same for each language's composite.
t = np.clip((a - 0.7) / 0.3, 0, 1)[..., None]
alpha8 = (np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8)
ys, xs = np.nonzero(alpha8 > 2)
box = (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)
print('bbox', box)
for lang in LANGS:
    Il = cv2.cvtColor(cv2.imread(f'hero-{lang}-full.jpg'), cv2.COLOR_BGR2RGB).astype(np.float32) / 255
    Fl = F if lang == 'fi' else filled_blur(Il, fg_sure.astype(np.float32), sigmas=(3, 8, 24, 80))
    col = np.clip(np.where((band > 0)[..., None], Il * t + Fl * (1 - t), Il), 0, 1)
    rgba = np.dstack([(col * 255 + 0.5).astype(np.uint8), alpha8])
    Image.fromarray(rgba).crop(box).save(f'cutout-{lang}-full.png', optimize=True)
open('cutout-box.txt', 'w').write(' '.join(map(str, box)))
