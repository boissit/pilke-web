"""The hero: Ebb8fe-NZtM, a Galaxy S9 with curved edges, with the treffit home
screen and its own Android bars.

The outline is the photo's own lit screen, fitted sub-pixel and clipped to the
fitted quad so the rim's highlight stays the photo's; the app is bent round the
curved edges, and laid between the old screen's measured black and white in
linear light, with the glass's highlights kept in the curved bands."""
import sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from comp2 import *

P = 'full/Ebb8fe-NZtM.jpg'
photo = read(P)
shape = photo.shape[:2]
L = photo.mean(2)

rough = [(1351.51, 1428.89), (2266.16, 1442.33), (2044.57, 3364.03), (1156.96, 3253.59)]
region = cv2.dilate(c1.region_mask(rough, shape, (0, 0, 1, 1)).astype(np.uint8), np.ones((41, 41), np.uint8))

# Screen-ness, normalised to the local brightness of the lit screen, so the
# dimmer curved bands still read as screen and the bezel as not.
bright = ((L > 0.6) & ((photo.max(2) - photo.min(2)) < 0.12)).astype(np.float32) * region
Ls = masked_blur(L[..., None].repeat(3, 2), bright, 18)[..., 0]
Lb = 0.13
E = np.clip((L - Lb) / np.maximum(Ls - Lb, 0.05), 0, 1) * region

quad, spread = subpixel_quad(E, rough, t_ranges=[(0.3, 0.7), (0.2, 0.8), (0.3, 0.7), (0.2, 0.8)], reach=40)
print('quad', [tuple(round(v, 2) for v in p) for p in quad], 'spread px', [round(s, 2) for s in spread])

# Alpha: the photo's own outline. Inside the lit silhouette (text holes filled)
# it is 1; across the boundary it is the normalised luminance ramp.
core = fill_holes(((E > 0.5) * region).astype(np.uint8))
inner = cv2.erode(core, np.ones((7, 7), np.uint8)).astype(np.float32)
ring = cv2.dilate(core, np.ones((5, 5), np.uint8)).astype(np.float32) - inner
alpha = np.clip(inner + ring * E, 0, 1) * quad_mask(quad, shape, 2.0)

# Canonical space at the photo's own scale: the silhouette, bend included.
EDGE, THETA = 0.045, np.radians(62)
total = curved_total(EDGE, THETA)
W, _ = canon_size(quad, 1)
Hc = int(round(W / total * 2.056))
Pc = to_canon(photo, quad, W, Hc)
Ac = to_canon(alpha, quad, W, Hc)

# The light, measured on the old screen in linear light.
Pl = lin(Pc)
Lc = Pc.mean(2)
satc = Pc.max(2) - Pc.min(2)
bg = ((Lc > 0.62) & (satc < 0.12) & (Ac > 0.98)).astype(np.float32)
bg = cv2.erode(bg, np.ones((3, 3), np.uint8)).astype(np.float32)
S = filled_blur(Pl, bg)                                   # white, with falloff and cast
dark = (Lc < 0.35) & (satc < 0.12) & (Ac > 0.98)
B = np.percentile(Pl[dark], 8, axis=0)                     # the glass: black as photographed
print('white (sRGB) median', srgb(np.median(S[bg > 0.5], 0)).round(3), 'black (sRGB)', srgb(B).round(3))

# The app, bent round the edges.
LANG = c1.lang_arg()
STILL = {'fi': 'screens/treffit.png', 'en': 'stills/treffit-en.png'}[LANG]
still = c1.android_screen(c1.load_still(STILL), 2.056)
content = np.asarray(still.resize((int(round(W / total)), Hc), Image.LANCZOS)).astype(np.float32) / 255
content, cos = curved_remap(content, W, EDGE, THETA)
Cl = lin(content)

out_l = B + (S - B) * Cl

# A reflection of the room, faint, stronger where the glass bends away.
room = lin(photo[200:1400, 400:3000])
room = cv2.resize(cv2.flip(room, 0), (W, Hc), interpolation=cv2.INTER_AREA)
room = cv2.GaussianBlur(room, (0, 0), 30)
fres = 0.018 + 0.09 * (1 - cos)[None, :, None]
out_l = out_l + room * fres

# The glass's own highlights in the curved bands, where the old screen was plain
# white: whatever the photo shows above its white field there is the glass.
band = np.clip((0.985 - cos) / 0.1, 0, 1)[None, :, None]
out_l = out_l + np.clip(Pl - S, 0, None) * band * (Ac[..., None] > 0.5)

out_c = srgb(out_l)
comp_p = to_photo(out_c, quad, W, Hc, shape)

# Match the photo's sharpness and grain, measured on the old screen's flat white.
comp_p = cv2.GaussianBlur(comp_p, (0, 0), 0.75)
flat = (to_photo(bg, quad, W, Hc, shape, cv2.INTER_NEAREST) > 0.5)
flat = cv2.erode(flat.astype(np.uint8), np.ones((9, 9), np.uint8)) > 0
g = grain_sigma(L, flat)
n = grain_field(shape, g, 11)
comp_p = comp_p + n[..., None]
print('grain', round(g, 4))

a = cv2.GaussianBlur(alpha, (0, 0), 0.4)[..., None]
out = photo * (1 - a) + np.clip(comp_p, 0, 1) * a
save(out, f'hero-{LANG}-full.jpg', 95)

