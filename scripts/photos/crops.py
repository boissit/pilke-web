"""Cut the site's pictures out of the composites and the originals, into src/assets/photos.

Run after hero.py and beta.py, each for fi and for en,
and cutout.py, from this directory."""
import os
from PIL import Image

from comp import LANGS

WEB = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../src/assets/photos')


def web(src, box, width, name):
    c = Image.open(src).crop(box)
    c = c.resize((width, round(c.height * width / c.width)), Image.LANCZOS)
    c.save(os.path.join(WEB, name), quality=88, subsampling=0, optimize=True, progressive=True)


for lang in LANGS:
    # The hero's cut-out, transparent, at 1400 wide: the widest the page asks for.
    cut = Image.open(f'cutout-{lang}-full.png')
    cut.resize((1400, round(cut.height * 1400 / cut.width)), Image.LANCZOS).save(
        os.path.join(WEB, f'hero-cutout-{lang}.png'), optimize=True)
    # The right fifth of the original is left out: a blurred cheek and sunglasses.
    web(f'beta-{lang}-full.jpg', (970, 1650, 3050, 4250), 1000, f'beta-invitation-{lang}.jpg')

# The two on a garden bench under *Nauttikaa treffeistä!* on nain-se-toimii, one
# picture for both languages, cut twice because the card is 16:9 beside the copy and
# 4:5 on a phone, and the couple is small in the original: nearly the whole width at
# 16:9, wide enough for the path and the bush round them, and at 4:5 close enough
# that they fill most of it. 2240 and 1080 wide, the card's widest at 2x and a
# phone's at about 3x.
web('full/30696772.jpg', (0, 1200, 4100, 3506), 2240, 'date-bench-wide.jpg')
web('full/30696772.jpg', (880, 620, 3230, 3558), 1080, 'date-bench-tall.jpg')

# The phone's part of the cut-out, as a mask of the same size, for both languages.
phone = Image.open('cutout-phone-full.png')
phone.resize((1400, round(phone.height * 1400 / phone.width)), Image.LANCZOS).save(
    os.path.join(WEB, 'hero-cutout-phone.png'), optimize=True)
