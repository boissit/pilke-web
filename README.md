# pilke-web

The marketing site for Pilke, built with Astro. Two languages: Finnish at the
root, English under `/en`.

```
npm install
npm run dev      # http://localhost:4321
npm run build    # static output in dist/
npx astro check  # types, including a key missing from one language
```

## How it is put together

`src/i18n/ui.ts` holds every string in both languages. `en` is typed
`Record<keyof typeof fi, string>`, so a key present in Finnish and missing in
English is a type error rather than a blank on the page. This mirrors how the app
itself types its dictionaries.

One file is the whole of a page in both languages. They live under
`src/pages/[...lang]/`: `index.astro`, `nain-se-toimii.astro`,
`turvallisuus.astro`, `kysyttya.astro`. The `[...lang]` segment is a rest
parameter, and `localeRoutes()` in `src/i18n/ui.ts` builds each file twice — once
with no segment at all, which is Finnish at the root, and once as `en`. A section
therefore cannot exist in one language and not the other, which is the usual way a
bilingual site drifts, and the English routes keep the Finnish slug so a language
switch is the prefix and nothing else.

A page holds its own sections, its own lists and its own styles. `src/components/`
is what more than one page draws: `Phone`, `Glimmer`, `Sparkle`, `Logo`,
`GlimmerPile`, the `PageHead` slab the three subpages open with, and the
`SiteHeader` and `SiteFooter` that `Base.astro` puts around every page.
`src/assets/screens.ts` is the table of screenshots, and is the only thing the
pages share besides the dictionary.

`Base.astro` loads both stylesheets, so a page is a run of `.slab` sections and
nothing else. The button those sections link out with is `.go` in
`src/styles/bold.css` — one definition, `.ghost` for the white one that stands on
a yellow slab.

`src/styles/global.css` carries the app's design tokens under the same names they
have in `pilke-app/src/constants/`, so a change on either side is traceable to
the other. Fonts and the currency mark are copied from
`pilke-app/assets/`.

## What the front page argues

The order of the sections is the argument, and it runs: dates rather than
swiping, three claims to stand behind, why that is not the same product as the
others, the loop, both halves of it are somebody's decision, and it is safe to
do.

Two things carry that argument visually, and both replaced a grid of shadowed
boxes:

- **The fact bar under the headline.** Three claims on one rule — three
  candidates at a time, time and place already set, nothing to game — one line
  each. As cards they were three shadowed rectangles beside a phone that is
  already a rectangle, and none of the three has enough to say to fill one.
- **The two routes in *Miksi tämä on erilaista*.** Each way of ending up on a
  date is a chain of one-word chips: elsewhere it is profile → scrolling → chat →
  *maybe a date*, and here it is questions → calendar → a date. The argument is
  that one chain is long and the other is short, so the two are stacked rather
  than set side by side, where each would wrap onto three lines and destroy the
  comparison. The last chip of the long chain is drawn dashed and muted, because
  it is the step that may never arrive. Emphasis is carried by the chips, so
  neither row needs a box.

**Never set body text beside a title.** A lede to the right of a heading reads as
a second column and the eye does not know which to follow first, so every section
head stacks: title, then lede under it at a wider measure (46ch) so the block does
not read as a narrow column.

Two spacing rules earn their keep. Blocks inside a section are `--pad-large`
apart, and a lede keeps a tighter `--pad-normal` under its own title so it stays
attached to it. Where a block needs more than that — the fact bar under the
tilted phone, the note below the two routes — the selector has to be written
`.wrap > .thing`: Astro scopes every compound selector, so `.wrap > * + *`
carries three attribute selectors against a bare class's two and wins on
specificity otherwise. A bare `.learn { margin-top }` silently does nothing.

Three deliberate omissions:

- **The glimmer economy is not on the front page.** A price and an earning table
  read as a game to be played, which is the opposite of what this product is.
  `nain-se-toimii` carries all of it, and the front page's *Kutsu, ja vastaa
  kutsuihin* section links there. That section exists because an app where
  everybody waits to be asked has no dates in it, so inviting and answering are
  given equal weight and the front page says what each one costs in one line.
- **The report and the meeting-safely advice are not on the front page.** Its
  three safety cards are the trusted contact, the safety button and the curated
  venues. Venues are there rather than the report because a reader who has not
  used the app yet is better served by knowing where they will be sent than by
  knowing how to complain afterwards. The forward-looking note about *vahva
  tunnistautuminen* sits under the cards and is drawn dashed, not as a fourth
  card: beside two features that ship, a card reads as a third feature that
  ships.
- **The questions are their own page** at `kysyttya`, which the header points at.
  Somebody arriving with one question is a different visit from reading the front
  page top to bottom, and a stack of six answers was the last thing a front-page
  reader met before the waitlist.

## Where the claims come from

Every factual statement was taken from the code in `pilke-app` and
`treffit-backend` rather than from their documentation, because the docs in those
repositories have repeatedly been found stale.

That rule has been broken at least once and the result was a paragraph describing
a screen that does not exist. **If a claim here cannot be traced to a constant, a
model field or a string in the app's own dictionaries, it does not go on the
site** — and a plausible-sounding sentence about what an app "asks" is exactly the
shape the invented ones take. The load-bearing numbers:

- A set of three candidates costs five glimmers, and there is no other price.
- The glimmers are spent when the set is drawn, not when the invitation is sent.
- One glimmer per three credited calendar spans, two for a date once feedback is
  given, five for finishing registration, five if somebody calls off a date on you.
- Earning stops at fifteen glimmers, which is three invitations' worth. Refunds are
  uncapped, so a balance can legitimately pass it.
- **Pilke never asks where anybody lives.** There is no home address and no
  device-location read outside a date. `User.date_location_preference` is a point
  plus `date_location_preference_radius`, written from `MapInput` — a map the user
  pans, defaulting to Helsinki — and the app's own label for it is *"Kuinka kauas
  voisit lähteä treffeille?"* with the sublabel *"Ehdotamme treffipaikkoja ympyrän
  sisältä"*. The site said "Pilke kysyy suunnilleen missä asut" for a while and
  that was invented; `privacy.area` now says what the screen says.
- Position sharing runs ten minutes either side of the agreed start
  (`POSITION_SHARING_LEAD` and `POSITION_SHARING_TRAIL`, both 10 minutes), only
  within 300 m of the venue (`POSITION_PROXIMITY_RADIUS`), and only to the other
  party.
- **Do not write that Pilke cannot see a shared position.** It is a row in the
  database until `core.tasks.sweep_closed_positions` deletes it, so "ei meille" and
  "Pilke itself does not see it" were both overclaims and are gone. What is true
  and worth saying instead is that nothing reads it: no penalty, no report and no
  compensation depends on it, which is what `test_positions.TestLocationIsNeverEvidence`
  exists to keep true.
- The safety button texts the trusted contact and nobody else. The message names no
  location, no venue and no partner.
- Date venues are chosen by Pilke, not proposed by users. `core.models.Activity`
  is written through `ActivityAdmin` only; the API exposes `GET /activities` and
  no create, update or delete, and `core/seed.py` refuses to seed any because
  "seeding a set of them would put invented venues in front of users". **The
  curation is provable from the code; "a public place with other people around" is
  not.** No field records it, so that half of the *Paikat valitsemme itse* card is
  a promise about how the team fills the table, and it is the only claim on the
  site that rests on a practice rather than on a constant. Keep it true.
- **Strong electronic identification does not exist in either repository.** The
  safety section says so in the copy itself — not in use, no date promised — and
  it is the only forward-looking statement on the site. If it ships, that note
  becomes a card; if it is dropped, the note goes.
- There is no way to buy a glimmer, no paid visibility, no boost and no ranking.
  `TokenGrantReason` in `users/models.py` declares nine reasons and not one of
  them is a purchase, and there is no billing, in-app-purchase, boost or ranking
  code in either repository. The front page's *Ei mitään pelattavaa* claim and the
  *what does it cost* answer both rest on that. Ship any of those four and both
  have to change.

The backend calls the unit a **token** in code; `glimmer` and `kipinä` are the
words users read. `Glimmer.astro` is the sparkle texture and is unrelated to the
currency.

## Copy that needs a human before this goes public

**The safety guidance under "Meeting somebody safely" has not been reviewed.** It
was written for this site from what the app actually does, deliberately not
copied from `pilke-app/docs/copy-drafts.md`, whose safety tips are an unapproved
draft (pilke-app#30). It is ordinary meeting-safely advice and claims nothing
about what Pilke will do for the reader, but it is safety text on a dating site
and should be read by somebody qualified.

Four more things to settle before launch:

1. **The product has two names in the code.** Onboarding copy calls it
   *Treffit*; the safety SMS and the location notification call it *Pilke*. This
   site says Pilke throughout.
2. **There is no privacy policy, and the terms and etiquette screens in the app
   are placeholder text.** The site links to none of them, which is why it has no
   footer legal links. That has to change before a public launch, and this site
   is where those documents would be served from.
3. **Answering question sets does not affect matching yet.** The site says so
   plainly rather than implying otherwise. If that changes, the story test
   section changes with it.
4. **The waitlist form submits nowhere.** It is the footer, in
   `SiteFooter.astro`, so
   that a reader who came to `turvallisuus` can join from where they are and the
   front page's hero button is an anchor down to it. It has no `action` and no
   handler, and it is the only thing on the site that asks the reader for
   anything. Wire it up or take it out before the site is public.
   It needs somewhere to put the addresses, and it needs the privacy policy in
   point 2 to exist, because this form is the first thing here that collects a
   personal detail. The copy promises the address is used for the beta
   invitation and nothing else, and is not passed on; whatever it is wired to
   has to make that true.
