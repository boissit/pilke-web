# The print kit

Everything the owner needs to make a flyer or a table tent in Google Slides lives in
one Drive folder, **Pilke – painotuotteet**, and every file in it is rebuilt from this
repository and `pilke-app` by `tools/print-kit/`. A picture or a line of copy on a
printed card is then as current as the site the day the kit was last refreshed.

## What is in Drive

| Drive | What it holds |
| --- | --- |
| `Brändi/` | The wordmark as SVG in ink, white and coral, and as 1000 px PNGs; the rounded app icon, 768 px; `paletti.svg` and `paletti.txt`, every colour with its hex and RGB; `Kipinät/`, the sparkle in seven colours as SVG and 1000 px PNG, and the counter's row; `Kauppamerkit/`, Apple's own Finnish App Store badge, black and white SVG |
| `QR/` | `https://pilke.app` and `https://pilke.app/#beta`, ink and white on transparency, PNG and SVG. The App Store and Google Play codes are there too, for after the release: both listings answer 404 today, and `osoitteet.txt` says so |
| `Kuvat/Pilke – kuvat` | A Slides file: every photograph, phone mockup, unframed screen and store image at full size, one group a page, the file name under each |
| `Pilke – elementit` | The element library, A4 landscape: wordmarks, the icon, sparkles, palette chips as shapes in the exact colours, the type styles, the struck-through steps, the coral disc, the pill buttons, cards and step numbers as native shapes, phones, photo crops and the QR codes. Copy and paste keeps size and colour |
| `Pilke – pöytäkolmio` | Three table-tent templates on A4 portrait, after a how-to page |
| `Pilke – A5-flyer` | Three two-sided flyer templates on A5, after a how-to page |

Slides gives a file one page size, so each format is its own file. Everything is the
owner's and private; nothing is shared.

### Why the big pictures are in a Slides file and not loose in the folder

The Google Drive connector Claude works through takes an upload's bytes typed into the
tool call as base64, and it can neither append to a file nor overwrite one. Past about
15 KB the typing stops coming out exact, which a PNG does not survive. So the folder
holds what fits: every SVG and text file, the QR codes, and palette PNGs of the
drawings at a size that fits. The square app icon, the full-size wordmark and palette
PNGs, the Google Play badge and the sparkle scatter did not survive the typing; they
are in the element library or in `out/`. The full-size PNGs and every photograph and screenshot
reach Slides another way: `createImage` fetches each from a URL, once, and Slides
keeps its own copy. Those URLs are a short-lived public branch of this repository
(below). Anything the folder lacks as a file is in `tools/print-kit/out/` after a
build, laid out with the folder's names, for dragging into Drive by hand.

## The table tent

A triangular prism standing on its end: three tall faces of 66 × 297 mm, each upright
when it stands.

```
 0   12           78           144          210 mm
 |liima| puoli 1   |  puoli 2   |  puoli 3   |
 | 12  |    66     |     66     |     66     |   297 mm tall
```

- **Print** one template page on A4, portrait, at 100 % (actual size), on 160–250 g/m²
  card if there is any.
- **Cut** nothing: the sheet is already the size. Each face is a rounded card 3 mm
  inside its folds and 8 mm inside the top and foot, so a printer's 3–5 mm blank edge
  falls on the white ground round it; text, phones and codes keep 8 mm from the folds
  and 15 mm from the top and foot.
- **Fold** along the three dashed lines, at 12, 78 and 144 mm from the left edge, each
  one backwards, print outwards.
- **Glue** the 12 mm flap ("liimaa tähän") and press the right edge of face 3 onto it
  from inside. The faces run 1, 2, 3 round the triangle.
- The fold lines, the flap's tint and its label are one group, **Ohjeviivat**, the
  topmost thing on each page: one click and Delete removes them all.

The A5 flyer keeps its content 6 mm or more from every edge. The how-to page of each
file says how to print it, on A5 or two to an A4 sheet.

## Rebuild the files

    tools/print-kit/build.sh

The first run makes `tools/print-kit/.venv` from `requirements.txt` (Pillow, qrcode,
resvg-py for the SVGs, fontTools for the site's own woff2, PyYAML for the copy). It
reads:

- `src/assets/brand/`, `src/assets/photos/`, `src/assets/screens/`, `public/fonts/` and
  `src/components/sparkleArtwork.ts` here;
- `assets/brand/icon.svg`, `tools/store-assets/captures/iphone/fi/` and
  `tools/store-assets/out/fi/app-store/iphone-6.9/` in `../pilke-app` (`PILKE_APP`
  moves it). The store images are that tool's output, so run
  `pilke-app/tools/store-assets/build.sh` first when they are stale;
- the two stores' badge pages, once, into `tools/print-kit/.cache/badges/`.

It writes `tools/print-kit/out/` (gitignored), about 20 MB: `Brändi/`, `Kuvat/` and
`QR/` at full size, `drive/` (the copies that go into Drive as files), `slides/` (the
one-slide .pptx each Slides file starts from) and `manifest.json` with every file's
size and SHA-256. The same inputs give the same bytes, so comparing the manifest with
the previous one says exactly which files a refresh has to replace.

The phone mockups are the store images' white shell (`pilke-app/tools/store-assets/render/build.py`)
redrawn round each iPhone capture with its shadow, on transparency. Three screens the
store set lacks (the personality quiz, feedback, settings) are the site's Android
stills with the navigation bar cut off, as `Phone.astro` cuts it.

Every transparent PNG carries its edge colour under its transparent pixels
(`bleed()` in `build.py`). Google's PDF export, which is how a card gets printed,
re-encodes each picture as a JPEG plus a mask, and a JPEG smears the hidden colour into
the antialiased edge; left black, it draws a dark rim round every sparkle.

`slides.py` holds every page of the four Slides files, in millimetres, and compiles a
deck into Slides API requests. Its copy is the Finnish side of `src/content/copy/*.yaml`
with the `{{tokens}}` resolved, so a wording change on the site reaches the cards on
the next refresh. `preview.py <deck> <dir>` draws each page locally from the same
requests, close enough to iterate a layout without the API; `overview.py` makes the
contact sheet.

## Refresh Drive (what Claude does)

The folder's ids are at the end of this page.

1. **Build and diff.** Keep the old `out/manifest.json`, run `build.sh`, and list the
   paths whose hash changed.
2. **Publish the pictures for Slides.** Push `out/` without `drive/` and `slides/` as
   an orphan branch `print-kit-assets` of `boissit/pilke-web` from a scratch
   directory (never from the working tree), and note the commit:

       git init -b print-kit-assets && rsync -a --exclude drive --exclude slides tools/print-kit/out/ .
       git add -A && git commit -m "print-kit assets" && git push -f git@github.com:boissit/pilke-web.git print-kit-assets

   The repository is public, so these files are public while the branch exists. Only
   `main` deploys, so the branch builds nothing. Delete it when step 4 is checked:
   `git push origin --delete print-kit-assets`.
3. **Replace the Drive files.** The connector cannot overwrite a file's content, so
   "in place" means in the same folder under the same name: upload the new file from
   `out/drive/` with `create_file` (`disableConversionToGoogleType`, base64 for a PNG,
   `textContent` for an SVG or text), download it back and compare its bytes with the
   local file, then trash the old one. The folder links stay; a file's own link
   changes. One upload per call, under about 15 KB of PNG. What has worked: write the
   base64 out in parts of about 3000 characters, compare each part with the file by
   script before the upload, and check the download against the file afterwards.
   Long runs of a repeated pattern are where characters go missing.
4. **Update the Slides files in place.** Object ids are fixed by `slides.py`
   (`<deck>_s<NN>_<role><NN>`), so a changed picture is one `replaceImage` request on
   the same id with the new branch URL and `imageReplaceMethod: CENTER_INSIDE`, which
   keeps the frame; a changed line of copy is `deleteText` and `insertText` on its
   text box. When a page's layout changes, delete its slide and resend it:

       tools/print-kit/.venv/bin/python tools/print-kit/slides.py poytakolmio --assets <commit> --layout p3 --slide 3

   prints that page's batches (each about 9 KB of JSON, one `update_presentation`
   each); the new slide lands last, and `updateSlidesPosition` puts it back. A new
   page size needs a new file: upload `out/slides/<deck>.pptx` with `create_file`,
   converted, and send every page.
5. **Check.** A thumbnail of every changed page (`read_slide_page_thumbnail`, LARGE):
   Fredoka and Figtree, nothing past a card or the margins, the struck bars on their
   words, and the table tent's faces upright. `slides.py <deck> --texts` lists every
   text box's text, to compare with a masked read of the deck for typos. Then
   `overview.py` on the thumbnails.

## Ids

| | Drive id |
| --- | --- |
| Pilke – painotuotteet | `1y8XShY6AJZVnYh28FE0i-OT5ZSUDTKpO` |
| Brändi | `192JSihUyyqQYxLV-UnrOfAGBkLordnJ-` |
| Brändi/Kipinät | `1z9SU-S_xZSxmeJ8VUxja5O1ucXByANje` |
| Brändi/Kauppamerkit | `1zUUSW6fcyDKfBIs2xi90owkRfotg6NPW` |
| Kuvat | `1f3Lt-qv-oiCMhKtEYnPT-mQECDbsfoYt` |
| QR | `1Mf7N8l70puVgiP2-WbbSG805petOPGIA` |
| Pilke – elementit | `17M4W07GlKV2ZZfE-2s2MKT8Hf3poGka8d3MExMuSlps` |
| Pilke – pöytäkolmio | `1d65fdXh29GshJoMswYYdr1NlCoxt4jYlC8yAz6p0G58` |
| Pilke – A5-flyer | `1T0juNo9puhLvO5qpoKV61WKCyHi3QQ6mUVkXITnZmVg` |
| Kuvat/Pilke – kuvat | `18F9QtSrwB0JcBRA7QkQwJYDWpmsgbM7eN1bv9KKsdaY` |

Every Slides file uses the blank layout `p3` of its skeleton.
