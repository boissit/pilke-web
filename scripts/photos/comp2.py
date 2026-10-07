"""Second-generation compositing, for the hero and the beta card.

What changed from comp.py, after the owner's review of the first hero:

- The screen's corners come from sub-pixel edge fits: a profile across each
  edge, the crossing found by interpolation, and a robust line through the
  crossings. Where the photo's screen is lit, its outline (the rounded corners
  and a curved-edge display's bend) comes from the photo itself, not a drawn
  rectangle.
- The light is measured, in linear light, from the photo's own screen: what a
  black pixel looks like there (the glass: reflection and flare) and what a
  white one does (emission, falloff, white balance). The app is laid between the
  two, so its blacks are as lifted as the photo's; its white is the measured one
  lifted to a screen's own light, `screen_white`, keeping the falloff and some of
  the cast.
- A curved-edge display gets its content bent round the edge, compressed and
  shaded as the glass does it.
"""
import cv2
import numpy as np
from PIL import Image

import comp as c1


def lin(x):
    return np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4)


def srgb(x):
    x = np.clip(x, 0, 1)
    return np.where(x <= 0.0031308, x * 12.92, 1.055 * x ** (1 / 2.4) - 0.055)


def read(path):
    return cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB).astype(np.float32) / 255


# ── Sub-pixel edges ─────────────────────────────────────────────────────────

def subpixel_quad(E, quad, t_ranges=None, reach=14, n=160, level=0.5):
    """Refine `quad` (TL, TR, BR, BL) on the edge image E, which is ~1 inside
    the screen and ~0 outside. For each side, profiles along the inward normal
    find where E crosses `level`; a Huber line through them; the four lines
    intersected. `t_ranges` limits each side to (t0, t1) of its length, to keep
    clear of corners, a notch or a finger."""
    q = [np.float64(p) for p in quad]
    t_ranges = t_ranges or [(0.2, 0.8)] * 4
    cx, cy = np.mean(q, 0)
    lines, spreads = [], []
    for k in range(4):
        a, b = q[k], q[(k + 1) % 4]
        v = b - a
        L = np.hypot(*v)
        u = v / L
        nrm = np.array([-u[1], u[0]])
        if np.dot(np.array([cx, cy]) - (a + b) / 2, nrm) < 0:
            nrm = -nrm  # inward
        pts = []
        rng_k = t_ranges[k] if isinstance(t_ranges[k][0], (tuple, list)) else [t_ranges[k]]
        ts = np.concatenate([np.linspace(t0, t1, max(8, int(n * (t1 - t0) / 0.6))) for t0, t1 in rng_k])
        for t in ts:
            base = a + u * (t * L)
            s = np.linspace(-reach, reach, reach * 8 + 1)
            xs = base[0] + nrm[0] * s
            ys = base[1] + nrm[1] * s
            prof = cv2.remap(E, xs.astype(np.float32)[None, :], ys.astype(np.float32)[None, :], cv2.INTER_LINEAR)[0]
            prof = np.convolve(prof, np.ones(3) / 3, mode='same')
            # Walk out from the inside and take the first drop below `level`:
            # a rim highlight further out is not the screen's edge.
            idx = np.nonzero((prof[:-1] < level) & (prof[1:] >= level))[0]
            if len(idx) == 0:
                continue
            i = idx[-1]
            f = (level - prof[i]) / max(prof[i + 1] - prof[i], 1e-6)
            si = s[i] + f * (s[1] - s[0])
            pts.append(base + nrm * si)
        P = np.float32(pts)
        vx, vy, x0, y0 = cv2.fitLine(P, cv2.DIST_HUBER, 0, 0.01, 0.01).ravel()
        d = np.abs((P[:, 0] - x0) * vy - (P[:, 1] - y0) * vx)
        spreads.append(float(np.median(d)))
        lines.append((np.array([x0, y0], np.float64), np.array([vx, vy], np.float64)))

    def inter(l1, l2):
        p, r = l1
        s_, w = l2
        t = np.linalg.solve(np.array([r, -w]).T, s_ - p)
        return p + t[0] * r

    Q = [inter(lines[3], lines[0]), inter(lines[0], lines[1]), inter(lines[1], lines[2]), inter(lines[2], lines[3])]
    return [(float(p[0]), float(p[1])) for p in Q], spreads


# ── Canonical space: the screen upright, at the photo's own scale ───────────

def canon_size(quad, aspect):
    q = np.float64(quad)
    w = max(np.hypot(*(q[1] - q[0])), np.hypot(*(q[2] - q[3])))
    W = int(round(w))
    return W, int(round(W * aspect))


def H_of(W, H, quad):
    return cv2.getPerspectiveTransform(np.float32([[0, 0], [W, 0], [W, H], [0, H]]), np.float32(quad))


def to_canon(img, quad, W, H):
    Hm = H_of(W, H, quad)
    return cv2.warpPerspective(img, np.linalg.inv(Hm), (W, H), flags=cv2.INTER_LINEAR | cv2.WARP_FILL_OUTLIERS)


def to_photo(img, quad, W, H, shape, interp=cv2.INTER_CUBIC, pad=12):
    """Canonical to photo. The canonical image is padded by replicating its edge
    first, so the alpha's soft boundary never samples black from outside it."""
    p = cv2.copyMakeBorder(img, pad, pad, pad, pad, cv2.BORDER_REPLICATE)
    T = np.array([[1, 0, -pad], [0, 1, -pad], [0, 0, 1]], np.float64)
    return cv2.warpPerspective(p, H_of(W, H, quad) @ T, (shape[1], shape[0]), flags=interp, borderMode=cv2.BORDER_CONSTANT)


def quad_mask(quad, shape, grow=2.0):
    """The fitted quad as an antialiased mask, grown by `grow` pixels, so a
    matte taken from the photo cannot reach past the screen onto the rim."""
    q = np.float64(quad)
    c = q.mean(0)
    q = c + (q - c) * (1 + grow / np.linalg.norm(q - c, axis=1).mean())
    k = 4
    m = np.zeros((shape[0] * 1, shape[1] * 1), np.uint8)
    cv2.fillPoly(m, [np.int32(np.round(q * k))], 255, lineType=cv2.LINE_AA, shift=2)
    return cv2.GaussianBlur(m.astype(np.float32) / 255, (0, 0), 0.5)


def curved_total(edge=0.045, theta_max=np.radians(62)):
    """The visible width of a curved-edge display, in widths of its content."""
    r = edge / theta_max
    return 1 - 2 * edge + 2 * r * np.sin(theta_max)


def curved_remap(img, W, edge=0.045, theta_max=np.radians(62)):
    """Bend the content round a curved-edge display. `img` is the content at its
    own width; the result is `W` wide, the visible silhouette. `edge` is the arc
    length of each curved band as a fraction of the content's width. Returns the
    remapped image and the per-column cosine of the glass, for shading the bend."""
    H, Wc = img.shape[:2]
    r = edge / theta_max
    proj = r * np.sin(theta_max)            # visible width of one band
    total = 1 - 2 * edge + 2 * proj          # visible width, in content widths
    x = (np.arange(W) + 0.5) / W * total     # visible coordinate, content widths
    s = np.empty_like(x)
    cos = np.ones_like(x)
    left = x < proj
    right = x > total - proj
    mid = ~(left | right)
    s[mid] = x[mid] - proj + edge
    th = np.arcsin(np.clip((proj - x[left]) / r, -1, 1))
    s[left] = edge - th * r
    cos[left] = np.cos(th)
    th = np.arcsin(np.clip((x[right] - (total - proj)) / r, -1, 1))
    s[right] = 1 - edge + th * r
    cos[right] = np.cos(th)
    mapx = np.tile((s * Wc - 0.5).astype(np.float32), (H, 1))
    mapy = np.tile(np.arange(H, dtype=np.float32)[:, None], (1, W))
    return cv2.remap(img, mapx, mapy, cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE), cos


def masked_blur(img, mask, sigma):
    return c1.masked_blur(img, mask.astype(np.float32), sigma)


# ── The screen's white ──────────────────────────────────────────────────────
# What the old screen measured is the white of a phone photographed in a room,
# exposed for the room: 0.66 to 0.85 in sRGB, and laid under the app as it was,
# the owner found every screen dim. A phone screen lights itself and is normally
# the brightest thing in the shot, so the measured white is lifted towards a
# clean one: scaled in sRGB until its median reaches `SCREEN_WHITE`, by at most
# `SCREEN_GAIN`, and its colour cast kept at `SCREEN_CAST` of its strength, so
# the screen still sits in the scene's light without reading as a grey card.
# The falloff across the screen is kept, being a scale rather than a level.
SCREEN_WHITE = 0.955
SCREEN_GAIN = 1.4
SCREEN_CAST = 0.4


def screen_white_srgb(ws, ref):
    """The lifted white in sRGB. `ws` is the measured white in sRGB, one colour
    or a field of them; `ref` is its median colour, which sets the gain."""
    ws = np.asarray(ws, np.float32)
    level = float(np.mean(ref))
    gain = float(np.clip(SCREEN_WHITE / max(level, 1e-3), 1.0, SCREEN_GAIN))
    lifted = ws * gain
    grey = lifted.mean(-1, keepdims=True)
    return np.clip(grey + (lifted - grey) * SCREEN_CAST, 0, 1).astype(np.float32)


def screen_white(Wl, ref):
    """The same in linear light: `Wl` and `ref` are linear, and so is the result."""
    return lin(screen_white_srgb(srgb(Wl), srgb(np.asarray(ref, np.float32)))).astype(np.float32)


def grain_like(photo_path, box, shape, seed):
    g = c1.estimate_grain(photo_path, box)
    rng = np.random.default_rng(seed)
    n = cv2.GaussianBlur(rng.normal(0, g, shape).astype(np.float32), (0, 0), 0.6) * 1.5
    return n, g


def save(arr, path, q=93):
    Image.fromarray((np.clip(arr, 0, 1) * 255 + 0.5).astype(np.uint8)).save(path, quality=q, subsampling=0)


def fill_holes(mask):
    m = (mask > 0).astype(np.uint8)
    cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    out = np.zeros_like(m)
    if cs:
        cv2.drawContours(out, [max(cs, key=cv2.contourArea)], -1, 1, -1)
    return out


def filled_blur(img, mask, sigmas=(9, 30, 90, 300)):
    """A masked blur that never runs out of samples: from the coarsest scale in,
    each finer one takes over where it has enough of the mask under it, so a
    dense patch of UI inherits the light of the background around it."""
    mask = mask.astype(np.float32)
    out = None
    for sg in sorted(sigmas, reverse=True):
        num = cv2.GaussianBlur(img * mask[..., None], (0, 0), sg)
        den = cv2.GaussianBlur(mask, (0, 0), sg)[..., None]
        est = num / np.maximum(den, 1e-6)
        if out is None:
            out = est
        else:
            w = np.clip(den / 0.3, 0, 1)
            out = est * w + out * (1 - w)
    return out


def grain_sigma(L, flat):
    """The photo's noise on a flat area, robust to the odd edge: the median
    absolute deviation of what the finest blur takes away."""
    hp = (L - cv2.GaussianBlur(L, (0, 0), 1.0))[flat]
    return float(1.4826 * np.median(np.abs(hp - np.median(hp))))


def grain_field(shape, g, seed):
    """Noise with the photo's own fine grain: white noise blurred a little, then
    scaled so the same measurement on it gives `g`."""
    rng = np.random.default_rng(seed)
    n = cv2.GaussianBlur(rng.normal(0, 1, shape).astype(np.float32), (0, 0), 0.6)
    k = grain_sigma(n, np.ones(shape, bool))
    return n * (g / k)
