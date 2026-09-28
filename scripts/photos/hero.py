"""The hero: uD5SvzjOsgY (iPhone X-style, blank white screen, warm wood) with
the treffit home screen, iOS bars drawn."""
import sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from comp2 import *

P = 'full/uD5SvzjOsgY.jpg'
photo = read(P)
shape = photo.shape[:2]
L = photo.mean(2)
Pl = lin(photo)

rough = [(2461.3, 555.6), (3842.7, 557.3), (3817.0, 3459.0), (2502.8, 3471.1)]
region = cv2.dilate(c1.region_mask(rough, shape, (0, 0, 1, 1)).astype(np.uint8), np.ones((61, 61), np.uint8)).astype(np.float32)

# Screen-ness: bright and the screen's own cool white; skin is warm.
skin = np.clip((photo[..., 0] - photo[..., 2] - 0.04) / 0.12, 0, 1)
white = ((L > 0.7) & (skin < 0.05)).astype(np.float32) * region
Sl = filled_blur(Pl, white, sigmas=(12, 40, 150))          # the white screen, linear
Slum = Sl.mean(2)
A = np.clip(Pl.mean(2) / np.maximum(Slum, 1e-3), 0, 1) * (1 - skin) * region
E = A.copy()

quad, spread = subpixel_quad(E, rough, t_ranges=[[(0.09, 0.19), (0.81, 0.91)], (0.06, 0.28), (0.25, 0.75), (0.15, 0.85)], reach=40)
print('quad', [tuple(round(v, 2) for v in p) for p in quad], 'spread px', [round(s, 2) for s in spread])
A = A * quad_mask(quad, shape, 3.0)

W, Hc = canon_size(quad, 2.165)
still = c1.ios_screen(c1.load_still('screens/treffit.png'), 2.165, notch_frac=0.557)
content = np.asarray(still.resize((W, Hc), Image.LANCZOS)).astype(np.float32) / 255
Cl = to_photo(lin(content), quad, W, Hc, shape)

# The glass's black: the display's inactive border just outside the lit area,
# which is the same glass over an unlit panel.
ring = (cv2.dilate((A > 0.5).astype(np.uint8), np.ones((15, 15), np.uint8)) - cv2.dilate((A > 0.5).astype(np.uint8), np.ones((5, 5), np.uint8))).astype(bool)
ring &= (L < 0.2) & (skin < 0.05)
B = np.median(Pl[ring], 0)
print('white (sRGB)', srgb(np.median(Sl[white > 0.5], 0)).round(3), 'black (sRGB)', srgb(B).round(3))

# A faint reflection of the room: warm wood and the window, mirrored and blurred.
room = cv2.GaussianBlur(cv2.resize(cv2.flip(Pl[:, :2400], 1), (shape[1], shape[0])), (0, 0), 45)
lit = B + (Sl - B) * Cl + room * 0.012

# Sharpness and grain, measured on the blank screen.
lit = srgb(lit)
lit = cv2.GaussianBlur(lit, (0, 0), 1.2)
flat = cv2.erode((A > 0.99).astype(np.uint8), np.ones((25, 25), np.uint8)) > 0
g = grain_sigma(L, flat)
lit = lin(np.clip(lit + grain_field(shape, g, 21)[..., None], 0, 1))
print('grain', round(g, 4))

# Exact unmix in linear light: where the photo was part screen white, swap
# that part for the app and keep the rest (bezel, fringe, finger) as it was.
out_l = Pl + A[..., None] * (lit - Sl)
save(srgb(out_l), "hero-full.jpg", 95)

