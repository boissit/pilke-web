"""The beta card in the footer: q_lCo82aXeo (iPhone with a Dynamic Island, camera
app open, held up against peach house fronts) with the invitation screen.

The thumb lies over the bottom of the screen and stays on top. The bottom edge
of the display is under it, so the bottom comes from the display's aspect off
the fitted top and sides, and is checked against the photo's home indicator."""
import sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from comp2 import *

P = 'full/q_lCo82aXeo.jpg'
photo = read(P)
shape = photo.shape[:2]
L = photo.mean(2)
Pl = lin(photo)
ASPECT = 2.168

rough = [(1583, 1983), (2433, 1983), (2417, 3825), (1600, 3825)]
region = cv2.dilate(c1.region_mask(rough, shape, (0, 0, 1, 1)).astype(np.uint8), np.ones((61, 61), np.uint8)).astype(np.float32)

skin = np.clip((photo[..., 0] - photo[..., 2] - 0.10) / 0.10, 0, 1) * np.clip((L - 0.30) / 0.10, 0, 1)
lit = ((L > 0.12) & (skin < 0.3)).astype(np.float32) * region
Ls = filled_blur(np.dstack([L] * 3), lit, sigmas=(10, 30, 100))[..., 0]
E = np.clip((L - 0.06) / np.maximum(Ls - 0.06, 0.05), 0, 1) * region * (1 - skin)

# The display's edges, measured on the unlit border between it and the frame:
# the darkest run of each profile across it, plus the half-width of the border.
# (The luminance fit is thrown by the dark tree at the top left and the thumb.)
def line(p, q):
    return np.float64(p), np.float64(q) - np.float64(p)


def meet(l1, l2):
    (p, r), (s_, w) = l1, l2
    t = np.linalg.solve(np.array([r, -w]).T, s_ - p)
    return p + t[0] * r


left = line((1585, 2150), (1585, 3300))
right = line((2433, 2150), (2405, 3550))
top = line((1760, 1992), (2330, 1982))
bottom = line((1900, 3809), (2250, 3803))
quad = [tuple(meet(left, top)), tuple(meet(top, right)), tuple(meet(right, bottom)), tuple(meet(bottom, left))]
print('quad', [tuple(round(float(v), 1) for v in p) for p in quad])
W, Hc = canon_size(quad, ASPECT)
_, alpha = c1.warp_screen(Image.new('RGB', (W, Hc)), quad, shape, 0.14)

# The island is the photo's own pixels, inside a pill measured on it: ends at
# x 1867 and 2153, top and bottom at y 2012 and 2081. The green camera-in-use
# dot inside it is painted out with the island's own black.
yy, xx = np.mgrid[0:shape[0], 0:shape[1]].astype(np.float32)
r_ = (2092 - 2020) / 2
yc = (2092 + 2020) / 2
x0_, x1_ = 1892 + r_, 2132 - r_
dx = np.clip(xx, x0_, x1_) - xx
dist = np.sqrt(dx ** 2 + (yy - yc) ** 2)
island_soft = np.clip(r_ - dist + 0.5, 0, 1)
island = island_soft > 0.5
isl_col = np.median(photo[island & (L < 0.12)], 0)
green = island & (photo[..., 1] - photo[..., 0] > 0.08)
green = cv2.dilate(green.astype(np.uint8), np.ones((7, 7), np.uint8)).astype(bool) & island
print('island px', int(island.sum()), 'green px', int(green.sum()))

# The thumb: the one large bright blob over the lower part of the screen, where
# the old screen was the camera's dark controls. The opening drops the thin
# white labels and the home indicator; the contour is smoothed; across a narrow
# band either side of it the edge is the luminance ramp from screen to skin.
low = c1.region_mask(quad, shape, (0.0, 0.6, 1.0, 1.0)) > 0.5
ell = lambda k: cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k))
brightm = ((L > 0.33) & low).astype(np.uint8)
brightm = cv2.morphologyEx(brightm, cv2.MORPH_OPEN, ell(17))
n, lab, st, _ = cv2.connectedComponentsWithStats(brightm)
blob = fill_holes((lab == 1 + np.argmax(st[1:, 4])).astype(np.uint8))
blob = cv2.morphologyEx(blob, cv2.MORPH_CLOSE, ell(41))
# The camera's white labels touch the thumb in places; inpaint them out of the
# photo first, so the edge ramp sees the dark screen they stood on, not them.
labels = ((L > 0.36) & low & (cv2.dilate(blob, ell(5)) == 0)).astype(np.uint8)
labels = cv2.dilate(labels, ell(5))
photo_ip = cv2.inpaint((photo * 255).astype(np.uint8), labels, 5, cv2.INPAINT_TELEA).astype(np.float32) / 255
L_ip = photo_ip.mean(2)
core = cv2.erode(blob, ell(13)).astype(np.float32)
bandm = (cv2.dilate(blob, ell(13)) - cv2.erode(blob, ell(13))).astype(np.float32)
ramp = np.clip((cv2.GaussianBlur(L_ip, (0, 0), 0.8) - 0.15) / 0.17, 0, 1)
thumb = np.clip(core + bandm * ramp, 0, 1)
# Its shadowed underside is as dark as the cobbles but reddish, where they are
# neutral: a chroma key, kept only where it joins the thumb.
rb = cv2.GaussianBlur(photo_ip[..., 0] - photo_ip[..., 2], (0, 0), 1.0)
ck = np.clip((rb - 0.035) / 0.05, 0, 1) * low
ckb = (ck > 0.5).astype(np.uint8)
n, lab, st, _ = cv2.connectedComponentsWithStats(ckb)
touch = np.unique(lab[(cv2.dilate(blob, ell(9)) > 0) & (ckb > 0)])
joined = np.isin(lab, touch[touch > 0])
joined = cv2.morphologyEx(joined.astype(np.uint8), cv2.MORPH_CLOSE, ell(15))
thumb = np.maximum(thumb, ck * cv2.dilate(joined, ell(5)))
thumb = cv2.GaussianBlur(thumb, (0, 0), 0.6)
blob = np.maximum(blob, joined)
blob = cv2.dilate(blob, ell(13))
m = (alpha > 0.5).astype(np.uint8)
band = (cv2.dilate(m, np.ones((13, 13), np.uint8)) - cv2.dilate(m, np.ones((5, 5), np.uint8))).astype(bool)
band &= (L < 0.2) & (skin < 0.1)
B = np.median(Pl[band], 0)
inside = cv2.erode(m, np.ones((15, 15), np.uint8)).astype(bool) & (blob == 0)
Wc = np.percentile(Pl[inside], 99.8, axis=0)
Wc = np.full(3, Wc.mean()) * 0.5 + Wc * 0.5          # the camera UI's white text, not the tinted view
print('white (sRGB)', srgb(Wc).round(3), 'black (sRGB)', srgb(B).round(3))

still = c1.ios_screen(c1.load_still('screens/invitation.png'), ASPECT, notch_frac=0.32)
content = np.asarray(still.resize((W, Hc), Image.LANCZOS)).astype(np.float32) / 255
Cl = to_photo(lin(content), quad, W, Hc, shape)
room = cv2.GaussianBlur(cv2.resize(cv2.flip(Pl, 1), (shape[1], shape[0])), (0, 0), 40)
out_l = B + (Wc * 0.95 - B) * Cl + room * 0.015
out = srgb(out_l)
out = cv2.GaussianBlur(out, (0, 0), 1.0)
flat = inside & (cv2.Laplacian(L, cv2.CV_32F, ksize=3) ** 2 < 1e-4)
g = grain_sigma(L, flat)
out = np.clip(out + grain_field(shape, g, 51)[..., None], 0, 1)
print('grain', round(g, 4))

# Unmix at the thumb's edge against the old screen under it.
old = filled_blur(photo, ((alpha > 0.5) & (blob == 0)).astype(np.float32), sigmas=(6, 20, 60))
a = alpha * (1 - island_soft)
t = thumb
res = photo * (1 - a[..., None]) + a[..., None] * (out * (1 - t[..., None]) + (photo + (1 - t[..., None]) * 0) * t[..., None])
# Where the thumb is partial, the photo's pixel still holds some old screen:
# swap that part for the new.
edge = (t > 0.02) & (t < 0.98) & (a > 0.5)
res[edge] = (photo_ip + (1 - t[..., None]) * (out - old))[edge]
# The camera-in-use dot goes: the island is plain black.
res[green] = isl_col
save(res, 'beta-full.jpg', 95)

