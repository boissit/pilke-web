"""Cut the site's pictures out of the composites, into src/assets/photos.

Run after hero.py, loop.py, ex2.py and beta.py, each for fi and for en,
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
    loop = Image.open(f'loop-{lang}-full.jpg')
    loop.resize((1800, round(loop.height * 1800 / loop.width)), Image.LANCZOS).save(
        os.path.join(WEB, f'loop-calendar-{lang}.jpg'), quality=88, subsampling=0, optimize=True, progressive=True)
    web(f'ex2-{lang}-full.jpg', (570, 0, 2490, 1600), 1400, f'start-story-wide-{lang}.jpg')
    web(f'ex2-{lang}-full.jpg', (880, 165, 2180, 1255), 900, f'start-story-narrow-{lang}.jpg')
    # The right fifth of the original is left out: a blurred cheek and sunglasses.
    web(f'beta-{lang}-full.jpg', (970, 1650, 3050, 4250), 1000, f'beta-invitation-{lang}.jpg')

# The phone's part of the cut-out, as a mask of the same size, for both languages.
phone = Image.open('cutout-phone-full.png')
phone.resize((1400, round(phone.height * 1400 / phone.width)), Image.LANCZOS).save(
    os.path.join(WEB, 'hero-cutout-phone.png'), optimize=True)
