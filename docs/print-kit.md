# The print kit

Everything the owner needs to make a flyer or a table tent in Google Slides lives in
one Drive folder (id `1jOGlLP45pesKXiPyRwUE9YvZOAOFzgap`, moved there by the owner on
2026-10-26), and every file in it is rebuilt from this
repository and `pilke-app` by `tools/print-kit/`. A picture or a line of copy on a
printed card is then as current as the site the day the kit was last refreshed.

## What is in Drive

| Drive | What it holds |
| --- | --- |
| `Brändi/` | The wordmark as SVG in ink, white and coral, and as 1000 px PNGs; the rounded app icon, 768 px; `paletti.svg` and `paletti.txt`, every colour with its hex and RGB; `Kipinät/`, the sparkle in seven colours as SVG and 1000 px PNG, and the counter's row; `Kauppamerkit/`, Apple's own Finnish App Store badge, black and white SVG |
| `QR/` | `https://pilke.app`, `https://pilke.app/#beta` and the beta's sign-up form (`qr-beta-lomake-*`, `https://forms.gle/LNjDw77d5giuxFWeA`), ink and white on transparency, PNG and SVG. The App Store and Google Play codes are there too, for after the release: both listings answer 404 today, and `osoitteet.txt` says so |
| `Kuvat/Pilke – kuvat` | A Slides file: every photograph, phone mockup, unframed screen and store image at full size, one group a page, the file name under each |
| `Pilke – elementit` | The element library, A4 landscape: wordmarks, the icon, sparkles, palette chips as shapes in the exact colours, the type styles, the struck-through steps, the coral disc, the pill buttons, cards and step numbers as native shapes, phones, photo crops and the QR codes. Copy and paste keeps size and colour |
| `Pilke – pöytäkolmio` | One table-tent template on A4 landscape, for the public release, after a how-to page |
| `Pilke – A5-flyer` | One two-sided A5 flyer for beta testers: exactly two pages, front and back; how to print it is in the front page's speaker notes |

Slides gives a file one page size, so each format is its own file. Everything is the
owner's and private; nothing is shared.

**What the connector can reach there.** The Drive connector Claude works through sees
only files it created or was handed by id. The owner's folder itself answers "not
found", so Claude cannot list it or add files to it. The decks are edited in place by
their ids (below), which puts the changes wherever the owner keeps them; a new loose
file (a PNG, a badge) stays in `tools/print-kit/out/` for the owner to drag in.

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

A triangular prism standing on its end: three faces of 99 × 210 mm side by side on A4
landscape, each upright when it stands. There is no glue flap: the sheet's left and
right edges meet at the third edge of the prism and are taped inside, so a printer's
blank margin falls where the faces meet.

```
 0              99             198            297 mm
 |   puoli 1    |    puoli 2    |    puoli 3    |
 |     99       |      99       |      99       |   210 mm tall
```

- **Print** one template page on A4, landscape, at 100 % (actual size), on 160–250 g/m²
  card if there is any.
- **Cut** nothing: the sheet is already the size. Each face is a rounded card 5 mm
  inside its folds or the sheet's edge and 6 mm inside the top and foot, so a printer's
  3–5 mm blank edge falls on the white ground round it; the content keeps 4 mm inside
  the card, 9 mm from a fold and 10 mm from the top and foot.
- **Fold** along the two dashed lines, at 99 and 198 mm from the left edge, each one
  backwards, print outwards.
- **Tape** the left and right edges together from inside. The faces run 1, 2, 3 round
  the triangle.
- The two fold lines are one group, **Ohjeviivat**, the topmost thing on each page: one
  click and Delete removes them.

The template is for the public release, so it says nothing about a beta:

- **Face 1**, peach: the wordmark, the site's headline and lead, and the hand holding
  the phone on the coral disc.
- **Face 2**, white: the wordmark small, the other apps' routine struck through as on
  the front page, then "Pilkkeessä ei swaippailla eikä chättäillä." and the lead under it.
- **Face 3**, mint: the wordmark small with "Näin se menee käytännössä" beside it on
  two lines, right-aligned on the face's edge and sized so its ink, the first line's
  capitals to the second line's baseline, is exactly as tall as the wordmark's (22.4 pt
  beside a 21 mm wordmark); the six numbered steps; then
  one footer row: the code to pilke.app with "pilke.app" centred under it on the left,
  the App Store and Google Play badges stacked on the right; "Pilke toimii toistaiseksi
  vain pääkaupunkiseudulla." under the row.

The wordmark sits in the same top-left corner of every face, 40 mm wide on face 1 and
21 mm on faces 2 and 3 (`SMALL_WM`), and faces 2 and 3 carry face 1's two top-right
sparkles (`corner_sparkles()`): on face 2 in face 1's place, on face 3 tucked under the
heading's right end, clear of it and of the first step. The steps are `flow()` in `slides.py`,
the same six on the tent and the flyer: Luo tili, Kutsu tai tule kutsutuksi, Aika ja
paikka valmiina, Käy treffeillä, Anna palautetta, Uudet treffit?. The first three bodies
are the site's own (`pitch.practice.one/two.body` cut to their first sentence,
`pitch.instead.ready.body` whole); the last three bodies and the sixth title are the
owner's, verbatim (`PRINT['flow.*']`). On face 3 they are set 10.5/8.5 pt (`TENT_STEP`)
and share out the height between the heading and the footer's clear space as equal
gaps (`steps_height()` measures them dry); `slides.py poytakolmio --summary` warns when
the gaps would fall under the least one.

The badges are the stores' own Finnish artwork, unaltered (`badges()` in `build.py`):
stacked and right-aligned on the content's edge, the same width (39.3 mm). The App Store
badge is 11 mm tall; the Google Play badge, less wide for its height, comes out 11.7 mm,
at least the size of the other store's as Google asks. They are a quarter of the
taller one's height apart, the clear space both stores ask for, and keep at least that
much from the steps and the link. The code and its link make a block as tall as the
stack: the code's plate starts level with the App Store badge's top, and the link's
baseline sits on the Google Play badge's foot. The Google Play PNG carries
transparent rows above and below the badge; `GOOGLE_ROWS` in `slides.py` is where the
drawn badge sits in it.

## The A5 flyer

Exactly two pages, front and back, so it prints double-sided. The front: the wordmark
on the left of the top row and the headline right-aligned on the same row, the lead
under them, then two columns. The page has two edges: the wordmark's ink edge on the
left, which the lead, the steps' heading and the step numbers share, and the headline's
ink edge on the right, which each struck line's bar and the line "Pilkkeessä ei
swaippailla eikä chättäillä." end on (the line is right-aligned too, ragged on the left
like the struck block above it). Then "Näin se menee käytännössä" in the same six steps as the
tent (`flow()`, set 11/8.5 pt in a 68 mm column, `FLYER_STEP`) on the left, and on the
right the other apps' routine struck through at 15 pt, "Pilkkeessä ei swaippailla eikä
chättäillä." and, at the foot, the hand holding the phone, as wide as the room right of
the steps' longest lines allows (57 mm). The
back is the owner's own text (`PRINT` in `slides.py`, verbatim): who is behind Pilke and
the ask for testers, in two paragraphs (`testers.body`, `testers.ask`), four things to
know about the beta, and the beta form's footer. The list's sparkle markers start on the
paragraphs' ink edge, their titles and bodies after them. Light peach sparkles sit top
right, beside "Hyvä tietää" at the right edge and above the wordmark at the foot. How to print it is in the front page's
speaker notes, which do not print: `slides.py a5-flyer --notes` prints them, and they go
into the notes shape (`read_slide_page`, `notesPage.notesProperties.speakerNotesObjectId`)
once the slide exists. Content keeps 6 mm or more from every edge.

The back's footer (`flyer_footer()`) stands on the content's foot: the wordmark on the
left, the beta form's code on the right with its plate on the content's edge, the
wordmark exactly as tall as the code's modules and level with them (`FLYER_CODE`, 19 mm),
and between them "Skannaa ja liity betaan" with the form's address,
`https://forms.gle/LNjDw77d5giuxFWeA`, printed as the code reads, right under it: the
address's baseline on the modules' foot, the line's descenders 1 mm above its capitals,
and the address sized so it is as wide as the line. The three are spaced evenly, 6.1 mm
of ink to ink. `qr_inset()` reads where the modules start in the code's PNG.

**Markers.** A sparkle or a step number beside a line is centred on that line's
capitals: `first_line_mid()` puts the first baseline of a Slides text box 2.39 mm plus
0.957 of the type size below its top, measured on the decks' own PDF export, and a
capital is 0.70 of the size in both faces. Check it on a fresh export when the faces
or the line spacing change.

**Ink edges.** A text box's first glyph does not start at its edge: `ink_in()` adds the
box's 2.54 mm inset and the first letter's side bearing as Slides sets it
(`INK_LSB_EM`, measured on the export), so a box can be placed by where its ink starts.
Fredoka's line advance at 100 % is `FREDOKA_ADVANCE`, also measured. Re-measure both when
a face or a size changes much.

**Step numbers.** `disc_number()` draws the disc and a separate text box holding only
the digit, grouped, and places the box so the digit's ink (Fredoka's own outline, via
PIL) sits on the disc's centre. A digit typed into the disc shape itself lands wherever
Slides' insets put it, low and to one side. Slides sets a lone digit 0.16 mm left of
PIL's ink box, so the box carries that correction; on the October 2026 export every
number sits within 0.05 mm of its disc's centre, and every disc within 0.07 mm of its
title's capitals, measured on the rendered ink of the first capital.

## Rebuild the files

    tools/print-kit/build.sh

The first run makes `tools/print-kit/.venv` from `requirements.txt` (Pillow, qrcode,
resvg-py for the SVGs, fontTools for the site's own woff2, PyYAML for the copy). It
reads:

- `src/assets/brand/`, `src/assets/photos/`, `src/assets/screens/`, `src/assets/manual/fi/`,
  `public/fonts/` and `src/components/sparkleArtwork.ts` here;
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

The phone mockups are `Phone.astro`'s marketing frame drawn as a PNG, with a shadow, on
transparency: a white shell, the screen edge to edge in an opening whose corners are 8 %
of the phone's width, and a punch-hole camera in the status bar. The navigation bar is
cut and the status bar kept, since the bar is what holds the top of a screen off the
top corners. Every phone is a still pilke.app already shows (`PHONE_SHOTS` in
`build.py`): the marketing stills of `src/assets/screens`, and for the home screen,
the calendar and the sparks, which the site shows only in the guide, the guide's
stills in `src/assets/manual/fi`. A guide still's status bar is swapped for the
marketing stills' demo-mode bar, so every phone says 9:41; the build stops if either
bar has anything but the clock and the icons on its plain ground. Look at the corners
of every phone at full size after a rebuild: a screen whose controls moved nearer a
corner shows there first.

The one phone with no still on pilke.app, `puhelin-treffikutsu-valittu.png` (the
invitation with a time and a place chosen), is framed from pilke-app's iPhone capture,
and its sheet's frame runs along the screen's edges, so the rounded opening cuts its
corners. It stays out of the public branch with the other private pictures below, and
goes into a deck by hand, if at all.

**What may be published.** Everything made from pilke-app's own captures and store
images, which are not public, is listed in `out/private.txt`: the store images, the
unframed iPhone screens and the private phone. Those never go on the assets branch.
Before adding a new picture to the kit, check that it is made only from what
pilke.app already serves; if it is not, give it `public=False` in `build.py`.

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
2. **Publish the pictures for Slides.** Push `out/` without `drive/`, `slides/` and
   every file `out/private.txt` lists, as an orphan branch `print-kit-assets` of
   `boissit/pilke-web` from a scratch directory (never from the working tree), and
   note the commit:

       git init -b print-kit-assets && rsync -a --exclude drive --exclude slides \
         --exclude-from tools/print-kit/out/private.txt tools/print-kit/out/ .
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
| The kit's folder (the owner's; the connector cannot list it) | `1jOGlLP45pesKXiPyRwUE9YvZOAOFzgap` |
| Brändi | `192JSihUyyqQYxLV-UnrOfAGBkLordnJ-` |
| Brändi/Kipinät | `1z9SU-S_xZSxmeJ8VUxja5O1ucXByANje` |
| Brändi/Kauppamerkit | `1zUUSW6fcyDKfBIs2xi90owkRfotg6NPW` |
| Kuvat | `1f3Lt-qv-oiCMhKtEYnPT-mQECDbsfoYt` |
| QR | `1Mf7N8l70puVgiP2-WbbSG805petOPGIA` |
| Pilke – elementit | `17M4W07GlKV2ZZfE-2s2MKT8Hf3poGka8d3MExMuSlps` |
| Pilke – pöytäkolmio | `12wuzVPzNYIIuJEo2YmZ62Ij9U3gFKqmA1VUCARX1hWw` |
| Pilke – A5-flyer | `1T0juNo9puhLvO5qpoKV61WKCyHi3QQ6mUVkXITnZmVg` |
| Kuvat/Pilke – kuvat | `18F9QtSrwB0JcBRA7QkQwJYDWpmsgbM7eN1bv9KKsdaY` |

Every Slides file uses the blank layout `p3` of its skeleton.
