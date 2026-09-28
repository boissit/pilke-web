"""Composite a Pilke app still onto a photographed phone screen.

Run from this directory: hero.py, ex2.py, ex3.py and beta.py write the full-size
composites (hero.py and beta.py through comp2.py), and crops.py cuts the site's
pictures from them. The originals go in full/, fetched
from the Unsplash URLs in docs/pictures.md. Needs numpy, opencv-python-headless and
Pillow.

The screen is warped from a canonical upright rectangle onto the four fitted
screen corners with a homography. The rounded-corner mask goes through the
same warp, so the corners bend with the perspective. Where the photo's screen
was blank white, the original is multiplied in, which keeps its own falloff,
colour cast, and any shadow a thumb casts; where it showed another app, a
blur or a plane fitted to its background pixels carries the falloff instead.
"""
import os

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../src/assets') + '/'
SF = '/System/Library/Fonts/SFNS.ttf'


def load_still(name):
    return Image.open(ASSETS + name).convert('RGB')


# ── Building the screen at the device's own proportions ──────────────────────

def android_screen(still, aspect):
    """An Android still for an Android phone: keep both bars, and take the
    difference in aspect out of the empty margins of the navigation bar."""
    w, h = still.size
    target = round(w * aspect)
    cut = h - target
    if cut <= 0:
        return still
    top, nav = still.crop((0, 0, w, 2144)), still.crop((0, 2144, w, h))
    half = cut // 2
    nav = nav.crop((0, half, w, nav.height - (cut - half)))
    out = Image.new('RGB', (w, target))
    out.paste(top, (0, 0))
    out.paste(nav, (0, 2144))
    return out


def ios_screen(still, aspect, notch_frac=0.415, clock='9.41', ink=(28, 24, 24)):
    """An Android still for an iPhone: the Android status bar and navigation bar
    go, the app's own band 96..2144 stays untouched, and an iOS status bar and
    home indicator are drawn on the app's own ground colour above and below."""
    w = still.width
    H = round(w * aspect)
    status = round(w * 47 / 390)
    app = still.crop((0, 96, w, 2144))
    top_c = still.getpixel((w // 2, 97))
    bot_c = still.getpixel((w // 2, 2142))
    out = Image.new('RGB', (w, H), bot_c)
    ImageDraw.Draw(out).rectangle((0, 0, w, status), fill=top_c)
    out.paste(app, (0, status))
    d = ImageDraw.Draw(out)
    # Clock, centred in the left ear.
    f = ImageFont.truetype(SF, round(w * 17 / 390))
    try:
        f.set_variation_by_name('Semibold')
    except Exception:
        pass
    ear = (w - w * notch_frac) / 2
    cy = round(status * 0.56)
    d.text((ear / 2 + w * 0.02, cy), clock, font=f, fill=ink, anchor='mm')
    # Signal, wifi and battery, centred in the right ear.
    s = w / 390
    cx = w - ear / 2 - w * 0.01
    x = cx - 34 * s
    for i in range(4):
        bh = (4 + i * 2.2) * s
        d.rounded_rectangle((x + i * 4.6 * s, cy + 5.5 * s - bh, x + i * 4.6 * s + 3 * s, cy + 5.5 * s), radius=s, fill=ink)
    wx, wy = cx + 2 * s, cy + 5.5 * s
    for r, wdt in ((10.5, 2.2), (6.8, 2.2)):
        d.arc((wx - r * s, wy - r * s, wx + r * s, wy + r * s), 225, 315, fill=ink, width=round(wdt * s))
    d.pieslice((wx - 3 * s, wy - 3 * s, wx + 3 * s, wy + 3 * s), 225, 315, fill=ink)
    bx = cx + 14 * s
    d.rounded_rectangle((bx, cy - 6 * s, bx + 24 * s, cy + 6 * s), radius=3.5 * s, outline=ink, width=round(1.1 * s))
    d.rounded_rectangle((bx + 2 * s, cy - 4 * s, bx + 17 * s, cy + 4 * s), radius=1.8 * s, fill=ink)
    d.rounded_rectangle((bx + 25 * s, cy - 2.2 * s, bx + 26.6 * s, cy + 2.2 * s), radius=s, fill=ink)
    # Home indicator.
    hw, hh = 134 * s, 5 * s
    d.rounded_rectangle(((w - hw) / 2, H - 8 * s - hh, (w + hw) / 2, H - 8 * s), radius=hh / 2, fill=ink)
    return out


# ── Warping ─────────────────────────────────────────────────────────────────

def _homography(w, h, quad):
    src = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
    return cv2.getPerspectiveTransform(src, np.float32(quad))


def warp_screen(screen, quad, shape, radius_frac):
    """Warp `screen` onto `quad` in an image of `shape` (h, w). Returns the
    warped RGB as float 0..1 and its rounded-rectangle alpha."""
    qw = max(np.hypot(*(np.subtract(quad[1], quad[0]))), np.hypot(*(np.subtract(quad[2], quad[3]))))
    # Pre-shrink so the warp never minifies by more than ~1.4x: no aliasing.
    scale = min(1.0, qw * 1.4 / screen.width)
    sw, sh = round(screen.width * scale), round(screen.height * scale)
    small = np.asarray(screen.resize((sw, sh), Image.LANCZOS)).astype(np.float32) / 255
    Hm = _homography(sw, sh, quad)
    rgb = cv2.warpPerspective(small, Hm, (shape[1], shape[0]), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    # Mask drawn at 4x and warped: an antialiased corner at any angle.
    k = 4
    m = Image.new('L', (sw * k, sh * k), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, sw * k - 1, sh * k - 1), radius=radius_frac * sw * k, fill=255)
    m = np.asarray(m.resize((sw * 2, sh * 2), Image.LANCZOS)).astype(np.float32) / 255
    Hm2 = _homography(sw * 2, sh * 2, quad)
    a = cv2.warpPerspective(m, Hm2, (shape[1], shape[0]), flags=cv2.INTER_LINEAR)
    return np.clip(rgb, 0, 1), np.clip(a, 0, 1)


def region_mask(quad, shape, box):
    """A mask of the part of the screen given as fractions (x0, y0, x1, y1)
    of its canonical rectangle, warped into the photo."""
    W, H = 1000, 2000
    m = np.zeros((H, W), np.float32)
    x0, y0, x1, y1 = box
    m[int(y0 * H):int(y1 * H), int(x0 * W):int(x1 * W)] = 1
    return cv2.warpPerspective(m, _homography(W, H, quad), (shape[1], shape[0]), flags=cv2.INTER_LINEAR)


def masked_blur(img, mask, sigma):
    num = cv2.GaussianBlur(img * mask[..., None], (0, 0), sigma)
    den = cv2.GaussianBlur(mask, (0, 0), sigma)[..., None]
    return num / np.maximum(den, 1e-4)


def plane_fit(img, mask):
    """Per channel a + bx + cy fitted over the masked pixels."""
    ys, xs = np.nonzero(mask > 0.5)
    sel = np.random.default_rng(0).choice(len(xs), min(len(xs), 60000), replace=False)
    xs, ys = xs[sel], ys[sel]
    A = np.stack([np.ones_like(xs), xs, ys], 1).astype(np.float64)
    h, w = mask.shape
    gy, gx = np.mgrid[0:h, 0:w]
    out = np.zeros((h, w, 3), np.float32)
    for c in range(3):
        coef, *_ = np.linalg.lstsq(A, img[ys, xs, c].astype(np.float64), rcond=None)
        out[..., c] = coef[0] + coef[1] * gx + coef[2] * gy
    return out


def composite(photo_path, quad, screen, radius_frac, mode, occluder=None, keep_dark=None,
              bg_ref=None, dim=1.0, sheen=0.035, blur=0.6, grain=None, feather=0.6):
    """mode 'multiply': the photo's screen was blank white.
    mode 'replace': the photo's screen showed content; `bg_ref` is a mask of
    its background pixels, whose plane fit gives the white point and falloff.
    `occluder`: alpha 0..1 of things in front of the screen (a thumb), kept.
    `keep_dark`: fractional box of the screen whose dark pixels are kept (the
    notch), so the photo's own camera cutout stays."""
    photo = cv2.cvtColor(cv2.imread(photo_path), cv2.COLOR_BGR2RGB).astype(np.float32) / 255
    shape = photo.shape[:2]
    rgb, alpha = warp_screen(screen, quad, shape, radius_frac)
    if feather:
        alpha = cv2.GaussianBlur(alpha, (0, 0), feather)

    inside = (alpha > 0.5).astype(np.float32)
    if mode == 'multiply':
        key = inside if occluder is None else inside * (1 - occluder)
        shade = masked_blur(photo, key, 6)
        # Normalise so the brightest part of the blank screen is the device's
        # own white, and the rest falls off as the photo does.
        ref = np.percentile(shade[key > 0.5], 99.5, axis=0)
        shade = shade / ref * np.minimum(ref, 1.0) * dim
        lit = rgb * shade
    else:
        base = plane_fit(photo, bg_ref)
        lit = rgb * np.clip(base, 0, 1) * dim

    # A faint glass sheen, brightest at the top-left, as the room's light falls.
    if sheen:
        h, w = shape
        gy, gx = np.mgrid[0:h, 0:w].astype(np.float32)
        q = np.float32(quad)
        u = q[1] - q[0]; v = q[3] - q[0]
        t = ((gx - q[0][0]) * (u[0] + v[0]) + (gy - q[0][1]) * (u[1] + v[1])) / (np.dot(u + v, u + v))
        band = np.clip(1 - np.abs(t - 0.22) / 0.22, 0, 1) ** 2
        lit = 1 - (1 - lit) * (1 - sheen * band[..., None])

    if blur:
        lit = cv2.GaussianBlur(lit, (0, 0), blur)
    if grain:
        rng = np.random.default_rng(1)
        n = rng.normal(0, grain, shape).astype(np.float32)
        n = cv2.GaussianBlur(n, (0, 0), 0.7) * 1.6
        lit = lit + n[..., None]

    a = alpha.copy()
    if keep_dark is not None:
        region = region_mask(quad, shape, keep_dark)
        lum = photo.mean(2)
        dark = np.clip((0.33 - lum) / 0.13, 0, 1) * region
        dark = cv2.GaussianBlur(dark, (0, 0), 0.6)
        a = a * (1 - dark)
    if occluder is not None:
        a = a * (1 - occluder)
    out = photo * (1 - a[..., None]) + np.clip(lit, 0, 1) * a[..., None]
    return np.clip(out, 0, 1), alpha


def save(arr, path, quality=90):
    Image.fromarray((arr * 255 + 0.5).astype(np.uint8)).save(path, quality=quality, subsampling=0)


def estimate_grain(photo_path, box):
    im = cv2.imread(photo_path).astype(np.float32) / 255
    x0, y0, x1, y1 = box
    p = im[y0:y1, x0:x1].mean(2)
    return float((p - cv2.GaussianBlur(p, (0, 0), 3)).std())
