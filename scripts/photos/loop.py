"""The loop card in Näin se toimii: -piUPY2-44A, an iPhone with a Dynamic Island
held up against an orange wall, with the calendar (stills/kalenteri-<lang>.png)
and iOS bars drawn.

The screen's edges are fitted sub-pixel where the old screen was lit against
the unlit glass round it; the Dynamic Island stays the photo's own. The app's white is the old screen's brightest broad white, its
black the glass's border, both in linear light."""
import sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from comp2 import *

T = dict(
    photo='full/piUPY2-44A.jpg',
    rough=[(1402, 157), (2212, 165), (2205, 1852), (1410, 1852)],
    top=[(0.08, 0.3), (0.7, 0.92)], sides=(0.12, 0.6), bottom=(0.2, 0.8),
    cutout=(0.3, 0.0, 0.7, 0.07), aspect=2.168, island=0.32,
    blur=0.9, seed=31, radius=0.14, dim=0.92,
)
photo = read(T['photo'])
shape = photo.shape[:2]
L = photo.mean(2)
Pl = lin(photo)
rough = T['rough']
region = cv2.dilate(c1.region_mask(rough, shape, (0, 0, 1, 1)).astype(np.uint8), np.ones((61, 61), np.uint8)).astype(np.float32)
skin = np.clip((photo[..., 0] - photo[..., 2] - 0.06) / 0.14, 0, 1)

lit = ((L > 0.22) & (skin < 0.3)).astype(np.float32) * region
Ls = filled_blur(np.dstack([L] * 3), lit, sigmas=(10, 30, 100))[..., 0]
Lb = 0.08
E = np.clip((L - Lb) / np.maximum(Ls - Lb, 0.05), 0, 1) * region * (1 - skin)

quad, spread = subpixel_quad(E, rough, t_ranges=[T['top'], T['sides'], T['bottom'], T['sides']], reach=45)
print('quad', [tuple(round(v, 2) for v in p) for p in quad], 'spread px', [round(s, 2) for s in spread])

# The old screen was dark at the bottom, as dark as the glass round it, so its
# outline cannot be read there: the display's own rounded rectangle, through the
# edges fitted where the old screen was lit.
Wq, Hq = canon_size(quad, T['aspect'])
_, alpha = c1.warp_screen(Image.new('RGB', (Wq, Hq)), quad, shape, T['radius'])
# The camera cutout is the photo's own: its dark pixels at the top stay.
cut = c1.region_mask(quad, shape, T['cutout'])
dark = cv2.GaussianBlur(np.clip((0.2 - L) / 0.1, 0, 1) * cut, (0, 0), 0.5)
alpha = alpha * (1 - dark)

# The glass's black: the unlit border just outside the lit area.
m = (alpha > 0.5).astype(np.uint8)
band = (cv2.dilate(m, np.ones((13, 13), np.uint8)) - cv2.dilate(m, np.ones((5, 5), np.uint8))).astype(bool)
band &= (L < 0.2) & (skin < 0.1)
B = np.median(Pl[band], 0)

# The display's white, from the brightest broad area of the old screen. A
# median filter first, so small white text does not count, only a field of it.
inside = cv2.erode((alpha > 0.99).astype(np.uint8), np.ones((15, 15), np.uint8)) > 0
med = cv2.medianBlur((photo * 255).astype(np.uint8), 31).astype(np.float32) / 255
cand = inside & (med.mean(2) > np.percentile(med.mean(2)[inside], 99.5))
Wc = np.median(lin(med)[cand], 0)
Wf = np.broadcast_to(Wc, photo.shape).astype(np.float32)
print('white (sRGB)', srgb(np.median(Wf[inside], 0)).round(3), 'black (sRGB)', srgb(B).round(3))

W, Hc = canon_size(quad, T['aspect'])
LANG = c1.lang_arg()
still = c1.ios_screen(c1.load_still(f'stills/kalenteri-{LANG}.png'), T['aspect'], notch_frac=T['island'], clock=c1.CLOCK[LANG])
content = np.asarray(still.resize((W, Hc), Image.LANCZOS)).astype(np.float32) / 255
Cl = to_photo(lin(content), quad, W, Hc, shape)

room = cv2.GaussianBlur(cv2.resize(cv2.flip(Pl, 1), (shape[1], shape[0])), (0, 0), 40)
out_l = B + (Wf * T.get('dim', 1.0) - B) * Cl + room * 0.012

out = srgb(out_l)
out = cv2.GaussianBlur(out, (0, 0), T['blur'])
flat = inside & (cv2.Laplacian(L, cv2.CV_32F, ksize=3) ** 2 < 1e-4)
g = grain_sigma(L, flat)
out = out + grain_field(shape, g, T['seed'])[..., None]
print('grain', round(g, 4))

a = alpha[..., None]
res = photo * (1 - a) + np.clip(out, 0, 1) * a
save(res, f'loop-{LANG}-full.jpg', 95)
