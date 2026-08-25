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

**Everything legal lives in this repository, and nowhere else.** The published
documents are `src/content/legal/`; the audit they are written from —
`privacy-policy.md`, `terms.md` and the Play Data safety worksheet — is
`docs/legal/`. The app holds no copy of any of it: it opens these URLs and records
which version it showed. That is the point of the arrangement, so **do not add a
second copy of a legal text to `pilke-app` or `treffit-backend`**, not even as a
convenience.

The documents are the one exception to *every string lives in `ui.ts`*.
`src/content/legal/` holds them as Markdown, one file per document per language,
named `<slug>.<lang>.md`; `src/content.config.ts` declares the schema and
`src/pages/[...lang]/[doc].astro` renders every one of them. They are prose a
lawyer edits, and a lawyer does not edit a TypeScript object literal. Their titles
and ledes come from their own frontmatter, so the footer names a document from the
same place the page does.

`src/i18n/legal.ts` is the only reader of that collection, and it throws at build
time on the two failures nothing downstream would reveal: a document missing a
language, and two languages of one document claiming different versions.
`/legal.json` is generated from the same frontmatter and is what lets the app and
the backend agree with the site about which version is live — the app pins one in
`pilke-app/src/constants/legal.ts` and the backend stores what each user accepted.

**Where the documents' shape comes from.** The section order and the Finnish
register follow Wolt Oy's own `tietosuojaseloste` and `käyttöehdot` — a Finnish
company writing Finnish first, rather than a US service translated. Headings are
questions a reader would ask, in finite verbs rather than `-minen` nominalisations,
as the rest of the Finnish copy is. **The content is written from Pilke's own
source**, by way of `docs/legal/`, and is copied from nobody: their prose describes
their products and is theirs.

The text is complete prose and carries no notes to the drafter: everything a
reviewer needs that is not part of the text is in
`docs/legal/review-notes.md` — the five fields to fill in, the legal
positions taken, and the code changes each document now presumes. **Read that
before editing either document.** An engineering caveat belongs there or in the
audit, never in a text a user reads.

`/tietojen-poisto` is a hand-written page rather than a collection entry: it is
instructions, not a binding text, and it exists because Google Play requires a URL
where somebody can find out how to delete their data **without installing the
app**. Every claim on it is checked against `core/deletion.py` by way of
`docs/legal/privacy-policy.md` §11. Deletion is a tombstone rather than a
row delete, so the *what stays* list is the load-bearing half of that page.

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
2. **The legal documents are written and not reviewed.** `/tietosuoja` and
   `/kayttoehdot` exist in both languages, the footer links them, and the app opens
   these same URLs. Both carry `draft: true`, which renders a notice saying the text
   binds nobody, and **nothing may clear that flag until a lawyer has read the
   result.** Three things gate publication, all of them in
   `docs/legal/review-notes.md`: five fields nobody can read from the code — the
   company's name, business ID, address, a contact address and the host — the legal
   positions the text takes, and six places where the code has to change because the
   text now states something as a fact. Without a contact address a GDPR Art. 13
   notice cannot be published at all. The app's etiquette screen is placeholder text
   too, and is not one of these documents — house rules are app copy, and folding
   them into the terms would make a courtesy enforceable.
3. **Answering question sets does not affect matching yet.** The site says so
   plainly rather than implying otherwise. If that changes, the story test
   section changes with it.
4. **The waitlist form posts to PostStack, and opens itself when the privacy
   statement is finished.** It is the footer, in `SiteFooter.astro`, so that a
   reader who came to `turvallisuus` can join from where they are and the front
   page's hero button is an anchor down to it. It is the only thing on the site
   that asks the reader for anything.

   The address goes to a hosted signup form — a public, unauthenticated endpoint —
   so there is no server here and no key in the page. One form per language, each
   bound to its own subscription topic, because their endpoint keeps the address
   and drops everything else: the *list* is what carries the language. The submit
   handler is inline and first-party, so *no analytics, no cookies, no
   third-party script* above still holds.

   **Point 2 gates this in code rather than in a note.** While `tietosuoja`
   carries `draft: true` the field and the button are disabled and the note reads
   `cta.closed`; clearing that flag is the whole of what opens the form. The copy
   promises the address is used for the beta invitation and nothing else — so
   nothing else is sent to it, and there is deliberately no welcome mail.
   `pilke-app/docs/plans/email.md` argues the arrangement.
