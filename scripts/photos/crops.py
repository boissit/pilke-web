"""Cut the site's pictures out of the composites, into src/assets/photos.

Run after hero.py, loop.py, ex2.py, ex3.py and beta.py, from this directory."""
import os
from PIL import Image

WEB = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../src/assets/photos')


def web(src, box, width, name):
    c = Image.open(src).crop(box)
    c = c.resize((width, round(c.height * width / c.width)), Image.LANCZOS)
    c.save(os.path.join(WEB, name), quality=88, subsampling=0, optimize=True, progressive=True)


# The pill's own proportion, placed so neither round end reaches the phone, the
# thumb or the fingertips (see the hero's comment in the front page).
web('hero-full.jpg', (990, 1059, 2440, 3653), 1200, 'hero-treffit.jpg')
loop = Image.open('loop-full.jpg')
loop.resize((1800, round(loop.height * 1800 / loop.width)), Image.LANCZOS).save(
    os.path.join(WEB, 'loop-calendar.jpg'), quality=88, subsampling=0, optimize=True, progressive=True)
web('ex2-full.jpg', (570, 0, 2490, 1600), 1400, 'start-story-wide.jpg')
web('ex2-full.jpg', (880, 165, 2180, 1255), 900, 'start-story-narrow.jpg')
web('ex3-full.jpg', (1150, 1500, 3445, 4560), 1100, 'safety-date.jpg')
# The right fifth of the original is left out: a blurred cheek and sunglasses.
web('beta-full.jpg', (970, 1650, 3050, 4250), 1000, 'beta-invitation.jpg')
