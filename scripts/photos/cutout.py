"""The hero: the hand and the phone cut out of the take-1 composite, for the
coral disc.

GrabCut, seeded with the phone as certain and a hand drawn round the rest, gives
a trimap: certain hand, certain room, and a band between. In the band the alpha
is solved from the colours either side, the hand's and the room's, each spread
in from the certain pixels nearest; the room behind is out of focus, so its
colour under the edge is well estimated. The phone's rim is dark and the room
round it light, so dark pixels by the phone stay. The colours in the band are
the hand's own, spread in from inside, so no fringe of the room shows on the
coral.

The page clips the hand and arm with the disc and lets the phone stand over the
disc's edge; the phone's part is a second file, a mask of the same size. Outside
the disc the mask is the phone's body and the fingers gripping it, their own
contour; see step 8.

The cut is made once, on the Finnish composite, and the same alpha is laid on
each language's: the phone is opaque, so what its screen shows cannot move the
edge. Reads hero-<lang>-full.jpg (hero.py fi, hero.py en), writes
cutout-<lang>-full.png."""
import json
import sys

import cv2
import numpy as np
from PIL import Image

sys.path.insert(0, __file__.rsplit('/', 1)[0])
from comp import LANGS
import comp as c1
from comp2 import filled_blur, subpixel_quad

im = cv2.imread('hero-fi-full.jpg')
H, W = im.shape[:2]
I = cv2.cvtColor(im, cv2.COLOR_BGR2RGB).astype(np.float32) / 255
L = I.mean(2)

# The screen as fitted by hero.py, and the phone's body round it.
screen = np.float32([(1352.36, 1421.98), (2256.93, 1500.17), (2036.83, 3363.11), (1157.08, 3253.44)])
# The fit is the photograph's, so it moves only if the original does; the check is
# for that day, when this cut would otherwise be laid a pixel or more off the phone.
fitted = np.float32(json.load(open('hero-quad.json')))
assert np.abs(fitted - screen).max() < 1.0, f'hero.py now fits the screen at {fitted.tolist()}; update `screen`'
phone = np.float32([(1320, 1360), (2290, 1440), (2080, 3430), (1175, 3310)])
hand = np.float32([(0, 2860), (600, 2480), (950, 1930), (1150, 1360), (1210, 1285), (1270, 1265), (1320, 1290),
                   (1330, 1340), (2290, 1420), (2400, 1850), (2410, 2760), (2250, 2800), (2100, 3450), (1150, 3310),
                   (1170, 3100), (1000, 3205), (850, 3275), (700, 3335), (0, 3570)])
wedge = np.float32([(1148, 3120), (1150, 3292), (700, 3345), (1000, 3212)])          # table under the palm
fgap = np.float32([(2167, 2505), (2262, 2505), (2262, 2562), (2200, 2563), (2182, 2568), (2168, 2583)])  # room between two fingertips
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
mask[poly(fgap, s, shp) > 0] = cv2.GC_BGD
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
bg_sure[poly(fgap) > 0] = 1
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

# The room seen between the fingers, right against the phone's glass edge, is
# light and cool, green or lavender, where the fingers are warm (skin's r - b is
# at least 0.08 on this hand): gone. The strip starts at the glass's edge, so
# the screen is never tested.
strip = (xx > edge - 24) & (xx < edge + 45) & (yy > 1850) & (yy < 2800)
room = np.clip((Ib.mean(2) - 0.45) / 0.1, 0, 1) * np.clip((0.06 - (Ib[..., 0] - Ib[..., 2])) / 0.03, 0, 1)
a = np.where(strip, a * (1 - room), a)
a = a * (1 - poly(fgap))

# The phone's body, and nothing beside it. The body's outer edges
# are fitted where its dark rim meets the lighter room or palm, clear of the
# thumb and fingers; its corners are rounded less than the phone's own, and it
# is grown by 10px past the rim's light outer edge, so the outline drawn outside
# the disc is the cut-out's own edge of the phone. Everything the growing takes
# in outside the disc is room the cut-out already left transparent.
TL, TR, BR, BL = [np.float64(p) for p in screen]
u = (TR - TL) / np.linalg.norm(TR - TL)
v = (BL - TL) / np.linalg.norm(BL - TL)
rough = [TL - u * 26 - v * 70, TR + u * 26 - v * 70, BR + u * 26 + v * 75, BL - u * 26 + v * 75]
dark = np.clip((0.42 - cv2.GaussianBlur(L, (0, 0), 1.0)) / 0.2, 0, 1).astype(np.float32)
body, spread = subpixel_quad(dark, rough, t_ranges=[(0.45, 0.85), (0.72, 0.9), (0.2, 0.8), (0.1, 0.25)], reach=30)
print('body', [tuple(round(x, 1) for x in p) for p in body], 'spread', [round(x, 2) for x in spread])
# The page's disc, in this image's pixels: the page draws x 380 to the right
# edge 100% of the art box wide (0.049702 of the box per pixel), x 380 4% left of
# the box, and the disc's centre 63.52% of the box below y 1323, its radius 50%:
# the disc 54% right of x 380.
#
# Outside the disc the page shows the phone and the fingers gripping it, over
# the pale card, so there the picture holds those and nothing else, each by its
# own edge in the photo. The phone is told from the room behind it by colour:
# its frame, rim and glass are neutral or lavender (g - b at most 0.01), the
# room green, olive or brown (g - b at least 0.03). So the phone is the region
# of those colours joined to its screen, and its edge is where that colour
# ends. The fingers are the pieces of the hand that touch it and are skin by
# their colour (r - g at least 0.04 on average), after the plant's green is
# taken out of them (skin's r - g is at least 0.03, the plant's at most 0.012).
# The cut is made 6px outside the circle, so that on the page the disc's own
# mask, not this, is the arc.
S = 0.049702
TOP = 1310       # the image's top: y 1323, the page's reference, less 13px of margin
cx, cy, r = 380 + 54 / S, 1323 + 63.52 / S, 50 / S
outside = np.hypot(xx - cx, yy - cy) > r + 6
bw = int(round(np.linalg.norm(np.float64(body[1]) - np.float64(body[0]))))
bh = int(round(np.linalg.norm(np.float64(body[3]) - np.float64(body[0]))))
_, body_a = c1.warp_screen(Image.new('RGB', (bw, bh)), body, (H, W), 0.10)
body_bin = (body_a > 0.5).astype(np.uint8)
grown = cv2.dilate(body_bin, ell(13))

Ic = cv2.GaussianBlur(I, (0, 0), 1.0)
phone_col = np.clip((0.03 - (Ic[..., 1] - Ic[..., 2])) / 0.02, 0, 1)
scr = poly(screen)
vicinity = cv2.dilate(scr, ell(161))
n, lab, st, _ = cv2.connectedComponentsWithStats(((phone_col > 0.5) & (vicinity > 0) | (scr > 0)).astype(np.uint8))
region = np.isin(lab, np.unique(lab[scr > 0]))
# Its outline smoothed, the photo's grain taken out of it, then anti-aliased.
region = cv2.morphologyEx(region.astype(np.uint8), cv2.MORPH_CLOSE, ell(9))
region = cv2.morphologyEx(region, cv2.MORPH_OPEN, ell(7))
soft = cv2.GaussianBlur(region.astype(np.float32), (0, 0), 2.0)
phone_a = np.maximum(scr.astype(np.float32), np.clip((soft - 0.5) * 2.5 + 0.5, 0, 1))

near_phone = cv2.dilate(region, ell(81)) > 0
notgreen2 = np.clip((Ib[..., 0] - Ib[..., 1] - 0.012) / 0.02, 0, 1)
a_hand = np.where(near_phone & (poly(nail) == 0), a * notgreen2, a)
hand_out = ((a_hand > 0.5) & outside & (region == 0)).astype(np.uint8)
n, lab, st, _ = cv2.connectedComponentsWithStats(hand_out)
keep = np.zeros((H, W), np.uint8)
rg = Ib[..., 0] - Ib[..., 1]
touch = cv2.dilate(region, ell(41)) > 0
for i in range(1, n):
    part = lab == i
    if st[i, 4] > 200 and (touch & part).any() and rg[part].mean() > 0.04:
        keep[part] = 1
print('fingers kept outside the disc:', int(keep.sum()), 'px')
fingers = a_hand * (cv2.dilate(keep, ell(5)) > 0)
a_out = np.maximum(phone_a, fingers)

# 5. A smooth edge, anti-aliased and no softer.
a = np.where(outside, a_out, cv2.GaussianBlur(a, (0, 0), 0.8))

# 6. The band takes the hand's own colour, spread in from inside, fading to the
# photo's where the alpha is nearly whole: none of the room's colour is left at
# the edge to show against the coral. The same for each language's composite.
t = np.clip((a - 0.7) / 0.3, 0, 1)
# The dark junction of rim and finger keeps its own colour, not the hand's.
t = np.maximum(t, np.clip((0.45 - Ib.mean(2)) / 0.1, 0, 1) * (cv2.dilate(grown, ell(41)) > 0))[..., None]
alpha8 = (np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8)
ys, xs = np.nonzero(alpha8 > 2)
# The arm runs out to the photograph's left edge, well past the disc, which
# clips it; the image keeps it so that the clip, not the crop, ends it.
box = (0, TOP, int(xs.max()) + 1, int(ys.max()) + 1)
assert ys.min() >= TOP, ys.min()
print('bbox', box)
for lang in LANGS:
    Il = cv2.cvtColor(cv2.imread(f'hero-{lang}-full.jpg'), cv2.COLOR_BGR2RGB).astype(np.float32) / 255
    Fl = F if lang == 'fi' else filled_blur(Il, fg_sure.astype(np.float32), sigmas=(3, 8, 24, 80))
    col = np.clip(np.where((band > 0)[..., None], Il * t + Fl * (1 - t), Il), 0, 1)
    rgba = np.dstack([(col * 255 + 0.5).astype(np.uint8), alpha8])
    Image.fromarray(rgba).crop(box).save(f'cutout-{lang}-full.png', optimize=True)
open('cutout-box.txt', 'w').write(' '.join(map(str, box)))

bw = int(round(np.linalg.norm(np.float64(body[1]) - np.float64(body[0]))))
bh = int(round(np.linalg.norm(np.float64(body[3]) - np.float64(body[0]))))
_, m = c1.warp_screen(Image.new('RGB', (bw, bh)), body, (H, W), 0.06)
body_m = cv2.dilate((m > 0.5).astype(np.uint8), ell(21))

# 8. The fingers holding it: the phone's part of the mask is what the picture
# holds outside the disc, grown a little so the picture's own edge shows.
m = np.maximum(body_m, cv2.dilate((a_out > 0.02).astype(np.uint8), ell(9))).astype(np.float32)
m = cv2.GaussianBlur(m, (0, 0), 0.7)
mask = np.dstack([np.full((H, W, 3), 255, np.uint8), (m * 255 + 0.5).astype(np.uint8)])
Image.fromarray(mask).crop(box).save('cutout-phone-full.png', optimize=True)
