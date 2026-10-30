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
  * A tile is artwork on a rounded tile, drawn on white: the white is masked off
    the same way, and the tile stands on the page by its own outline.
  * A screenshot of a browser keeps only the page it shows: the box below cuts the
    browser's toolbar, its address and profile picture, off the top, and the
    window's edge and scrollbar off the sides.
  * A board is a design-tool page holding several screens: each is cut out by its
    box, its own frame label and the page's title left behind, and set into a
    phone as a screen is, below. These are cut off at the board's foot, so they
    stand on the phone's foot as if they ran on under it, and their own flat
    background is carried on above them.
  * A rounded tile is a square picture on no tile of its own, given the logo's
    rounded corners.
  * A screen is a design-tool frame on its grey canvas, with the frame's name
    above it. It is cut to the frame and set into the phone of another phone
    shot, so it stands beside that one as the same device: the screen is fitted
    whole to the phone's screen, inside the notch and the rounded corners, and
    the room its proportions leave above and below is its own top and bottom
    rows carried on. It runs the screen's full width: only its background meets
    the corners, and its content keeps the design's own margins inside them.

Before any of that, the prototype's screenshots lose a real person. Their sample
profile, "Esa, 26", wears the photograph of somebody who never agreed to be on a
dating site, so every place it is drawn is painted over with one face from the
backend's mock cast (`cast/`, Unsplash stock, credited in docs/pictures.md). The
same face in every screenshot, so the prototype still reads as one profile. Each
place is a box measured on the original, inside the slot's border, with the
slot's corner radius; the face is cropped to the box's proportions round its
centre and pasted under the slot's own border, and the one slot that prints the
name over the photo gets its darkening and its white letters back on top.

The same inputs give the same bytes out, every run.
"""
import os
import shutil

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'meista')
WEB = os.path.join(HERE, '../../src/assets/meista')

# Below this in every channel a pixel is the black ground. The JPEGs' ground is
# noise round zero, and the darkest part of a device's own edge is well above it.
BLACK = 28

PHOTOS = ['boissit.jpg', 'designsprint.jpg', 'designsprint2.jpg']
DEVICES = ['visu2.jpg', 'mockup1.png', 'mockup2.png', 'mockup3.png', 'latevisu1.jpg', 'latevisu2.jpg']
TILES = ['logo.jpg']
# A square picture, the box of it that is the square, and the corner radius as a
# share of its side, the logo tile's.
ROUNDED_TILES = {'maskotti.png': ((0, 0, 286, 285), 0.175)}
# A board, and each screen on it: the picture it becomes, its box on the board,
# and the device whose phone it is set into.
BOARDS = {
    'esimerkkiruudut.png': {
        'onboard.png': ((103, 89, 474, 898), 'visu2.jpg'),
        'overview.png': ((518, 89, 889, 898), 'visu2.jpg'),
    },
}
# A browser screenshot, and the box of it that is the page: measured on the file.
BROWSER = {'map.jpg': (8, 26, 1263, 678)}
# Above this in every channel a pixel is a tile's white ground.
WHITE = 236
# The stand-in for "Esa, 26": `spare-male-01.jpg` in treffit-backend's `test/`,
# the cast's Aleksi Rantala, 26, copied here under the cast's name so the credit
# in `treffit_backend/mocks/data.py` still finds it.
CAST = os.path.join(HERE, 'cast')
STAND_IN = 'spare-male-01.jpg'
# Where the stand-in's face is centred, in its 600 x 600 pixels.
STAND_IN_FACE = (300, 230)

# Every photo slot of Esa: the inside of its border as (left, top, right, bottom),
# measured on the original, and the border's inner corner radius. `square_bottom`
# for a photo whose foot is a straight cut onto the card, and `name_over` for the
# one that prints the name over the photo's foot, on a darkening.
PORTRAITS = {
    'mockup1.png': [{'box': (98, 325, 200, 426), 'radius': 15}],
    'mockup3.png': [{'box': (90, 302, 287, 498), 'radius': 20}],
    'latevisu1.jpg': [{'box': (71, 239, 336, 470), 'radius': 11, 'square_bottom': True, 'name_over': True}],
    'latevisu2.jpg': [{'box': (69, 245, 147, 323), 'radius': 8}],
}

# The darkening under the name on the Ehdokkaat card, read off the original's wall:
# none down to this share of the photo's height, then down to NAME_SHADE of the
# light at this share, and level to the foot.
NAME_SHADE_FROM, NAME_SHADE_TO, NAME_SHADE = 0.46, 0.87, 0.52
# Above this a pixel of the name's band is the white lettering (the darkened photo
# under it peaks near 110), and fully letter from NAME_FULL.
NAME_EDGE, NAME_FULL = 120, 235

# A screen, and the device whose phone it is set into.
SCREENS = {'visu1.jpg': 'visu2.jpg'}

# Between the screen's content and the phone's notch, in the phone's pixels.
SCREEN_MARGIN = 12
# The design tool's anti-aliased edge round a frame, trimmed so it is not carried on.
FRAME_EDGE = 3


def stem(name):
    return os.path.splitext(name)[0]


def cut_out(rgb, ground=None):
    """The alpha of what stands on a plain ground: everything but the ground's
    regions touching the image's edge. The ground is near-black unless given."""
    dark = ((rgb.max(axis=2) < BLACK) if ground is None else ground).astype(np.uint8)
    count, labels = cv2.connectedComponents(dark, connectivity=4)
    edge = np.unique(np.concatenate([labels[0], labels[-1], labels[:, 0], labels[:, -1]]))
    ground = np.isin(labels, edge[edge != 0]) if count > 1 else np.zeros_like(dark, bool)
    # One pixel in from the cut, and softened over a pixel, so the outline keeps no
    # dark fringe of the ground it was cut from and no stair-steps.
    keep = cv2.erode((~ground).astype(np.uint8) * 255, np.ones((3, 3), np.uint8))
    return cv2.GaussianBlur(keep, (3, 3), 0.8)


def save_device(rgb, alpha, name):
    ys, xs = np.nonzero(alpha)
    box = (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)
    Image.fromarray(np.dstack([rgb, alpha])).crop(box).save(os.path.join(WEB, stem(name) + '.png'), optimize=True)


def rounded(width, height, radius, square_bottom=False):
    """A rounded rectangle's coverage, 0 to 1, drawn at four times and averaged
    down, so its curve is anti-aliased as the screenshot's own border is."""
    k = 4
    mask = Image.new('L', (width * k, height * k), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, width * k - 1, height * k - 1), radius * k, fill=255,
                           corners=(True, True, not square_bottom, not square_bottom))
    return np.array(mask.resize((width, height), Image.LANCZOS)).astype(np.float32)[..., None] / 255


def stand_in(width, height):
    """The stand-in's face, cropped to `width` x `height` round its centre and as
    soft as the screenshot it goes into."""
    face = Image.open(os.path.join(CAST, STAND_IN)).convert('RGB')
    side = min(face.width, round(face.height * width / height))
    tall = round(side * height / width)
    fx, fy = STAND_IN_FACE
    left = min(max(fx - side // 2, 0), face.width - side)
    top = min(max(fy - round(tall * 0.45), 0), face.height - tall)
    crop = face.crop((left, top, left + side, top + tall)).resize((width, height), Image.LANCZOS)
    return np.array(crop.filter(ImageFilter.GaussianBlur(0.5))).astype(np.float32)


def paint_over_esa(rgb, name):
    out = rgb.astype(np.float32)
    for slot in PORTRAITS.get(name, []):
        x0, y0, x1, y1 = slot['box']
        w, h = x1 - x0, y1 - y0
        old = out[y0:y1, x0:x1].copy()
        face = stand_in(w, h)
        if slot.get('name_over'):
            t = (np.arange(h, dtype=np.float32) / (h - 1))[:, None, None]
            ramp = np.clip((t - NAME_SHADE_FROM) / (NAME_SHADE_TO - NAME_SHADE_FROM), 0, 1)
            ramp = ramp * ramp * (3 - 2 * ramp)
            face *= 1 - (1 - NAME_SHADE) * ramp
            # The white name, lifted off the original and laid back on.
            light = old.mean(axis=2, keepdims=True)
            letters = np.clip((light - NAME_EDGE) / (NAME_FULL - NAME_EDGE), 0, 1)
            letters[: round(h * NAME_SHADE_TO) - 40] = 0
            face = face * (1 - letters) + 255 * letters
        cover = rounded(w, h, slot['radius'], slot.get('square_bottom', False))
        out[y0:y1, x0:x1] = face * cover + old * (1 - cover)
    return out.round().clip(0, 255).astype(np.uint8)


def device(name):
    rgb = paint_over_esa(np.array(Image.open(os.path.join(SRC, name)).convert('RGB')), name)
    save_device(rgb, cut_out(rgb), name)


def tile(name):
    rgb = np.array(Image.open(os.path.join(SRC, name)).convert('RGB'))
    save_device(rgb, cut_out(rgb, rgb.min(axis=2) > WHITE), name)


def browser(name, box):
    Image.open(os.path.join(SRC, name)).convert('RGB').crop(box).save(
        os.path.join(WEB, name), quality=90, subsampling=0, optimize=True)


def frame_of(rgb):
    """The phone's screen in a device shot: the lit region round the image's centre,
    with whatever is drawn on it filled in, and the notch and corners left out."""
    lit = (rgb.max(axis=2) >= BLACK).astype(np.uint8)
    _, labels = cv2.connectedComponents(lit, connectivity=4)
    h, w = lit.shape
    region = (labels == labels[h // 2, w // 2]).astype(np.uint8)
    contours, _ = cv2.findContours(region, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    screen = np.zeros_like(region)
    cv2.drawContours(screen, [max(contours, key=cv2.contourArea)], -1, 1, thickness=cv2.FILLED)
    return screen


def design_frame(name):
    """A design-tool frame cut from its canvas, less the tool's anti-aliased edge."""
    im = Image.open(os.path.join(SRC, name)).convert('RGB')
    rgb = np.array(im).astype(int)
    canvas = rgb[2, 2]
    differs = np.abs(rgb - canvas).max(axis=2) > 6
    # The frame is the run of rows and columns that are mostly not canvas; the
    # frame's name above it is a few words, never most of a row.
    rows = np.nonzero(differs.mean(axis=1) > 0.5)[0]
    cols = np.nonzero(differs.mean(axis=0) > 0.5)[0]
    e = FRAME_EDGE
    return np.array(im.crop((cols.min() + e, rows.min() + e, cols.max() + 1 - e, rows.max() + 1 - e)))


def set_into_phone(design, into, out_name, align='centre'):
    """`design` whole on the screen of `into`'s phone, below its notch.

    Centred, it runs the screen's full width, and its top and bottom rows are
    carried on into the room left. On the foot, for a screen cut off at its foot,
    it stands on the screen's bottom edge and its top rows are carried on above;
    a design too tall for that is narrowed, and its side columns carried on.
    """
    phone = np.array(Image.open(os.path.join(SRC, into)).convert('RGB'))
    area = frame_of(phone)
    ys, xs = np.nonzero(area)
    top, bottom, left, right = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    # The notch's depth: how far down the screen's middle column starts below its top.
    notch = np.nonzero(area[:, (left + right) // 2])[0].min() - top
    screen_w, screen_h = right - left, bottom - top

    if align == 'centre':
        width = screen_w
        height = round(design.shape[0] * width / design.shape[1])
        room = screen_h - height
        above = max(room // 2, notch + SCREEN_MARGIN)
        if room - above < SCREEN_MARGIN:
            raise SystemExit(f'{out_name} does not fit inside the screen of {into} below its notch.')
        below = room - above
    else:
        scale = min(screen_w / design.shape[1], (screen_h - notch - SCREEN_MARGIN) / design.shape[0])
        width, height = round(design.shape[1] * scale), round(design.shape[0] * scale)
        above, below = screen_h - height, 0
    design = cv2.resize(design, (width, height), interpolation=cv2.INTER_AREA)
    side = screen_w - width
    # The design's own edges carried on round it, so the room left is its background.
    filled = cv2.copyMakeBorder(design, above, below, side // 2, side - side // 2, cv2.BORDER_REPLICATE)

    out = phone.copy()
    soft = cv2.GaussianBlur(area.astype(np.float32), (3, 3), 0.8)[top:bottom, left:right, None]
    out[top:bottom, left:right] = (filled * soft + phone[top:bottom, left:right] * (1 - soft)).round().astype(np.uint8)
    save_device(out, cut_out(phone), out_name)


def screen(name, into):
    set_into_phone(design_frame(name), into, name)


def board(name, screens):
    sheet = np.array(Image.open(os.path.join(SRC, name)).convert('RGB'))
    for out_name, (box, into) in screens.items():
        x0, y0, x1, y1 = box
        set_into_phone(np.ascontiguousarray(sheet[y0:y1, x0:x1]), into, out_name, align='foot')


def rounded_tile(name, box, radius):
    square = Image.open(os.path.join(SRC, name)).convert('RGB').crop(box)
    cover = (rounded(square.width, square.height, round(min(square.size) * radius))[..., 0] * 255).round().astype(np.uint8)
    Image.fromarray(np.dstack([np.array(square), cover])).save(os.path.join(WEB, stem(name) + '.png'), optimize=True)


os.makedirs(WEB, exist_ok=True)
for name in PHOTOS:
    shutil.copyfile(os.path.join(SRC, name), os.path.join(WEB, name))
for name in DEVICES:
    device(name)
for name in TILES:
    tile(name)
for name, box in BROWSER.items():
    browser(name, box)
for name, into in SCREENS.items():
    screen(name, into)
for name, screens in BOARDS.items():
    board(name, screens)
for name, (box, radius) in ROUNDED_TILES.items():
    rounded_tile(name, box, radius)

known = set(PHOTOS + DEVICES + TILES) | set(BROWSER) | set(SCREENS) | set(BOARDS) | set(ROUNDED_TILES)
unknown = sorted(n for n in os.listdir(SRC) if not n.startswith('.') and n not in known)
if unknown:
    raise SystemExit(f"meista/ has {', '.join(unknown)}, which meista.py does not know: add each to its kind above.")
print(f'meista.py: {len(known)} pictures into src/assets/meista')
