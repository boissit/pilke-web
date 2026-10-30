# pilke-web

The marketing site for Pilke, built with Astro. Two languages: Finnish at the
root, English under `/en`.

```
npm install
npm run dev      # http://localhost:4321
npm run build    # static output in dist/
npx astro check  # types and content collections
npm run copy:export  # every text on the site as one JSON snapshot, for the copy desk
```

## How it is put together

**Every string a reader meets has one source.** The pages' copy is
`src/content/copy/*.yaml`, one file per page with each key's `fi` and `en` side by
side and the house style in the header of `site.yaml`; the guide and the legal
documents are Markdown. `src/i18n/ui.ts` reads the YAML and is where a page's
`t('key')` comes from. It holds no string of its own, and it fails the build on a key
missing a language, an empty string, a key in two files or a page asking for a key
no file holds, which is the check a typed dictionary used to make.
`docs/copy-desk.md` is how the owner's rewrites reach these files.

One file is the whole of a page in both languages. They live under
`src/pages/[...lang]/`: `index.astro`, `nain-se-toimii.astro`,
`turvallisuus.astro`, `kysyttya.astro`, `meista.astro`. The `[...lang]` segment is a rest
parameter, and `localeRoutes()` in `src/i18n/ui.ts` builds each file twice — once
with no segment at all, which is Finnish at the root, and once as `en`. A section
therefore cannot exist in one language and not the other, which is the usual way a
bilingual site drifts, and the English routes keep the Finnish slug so a language
switch is the prefix and nothing else.

A page holds its own sections, its own lists and its own styles. `src/components/`
is what more than one page draws: `Phone`, `SparkleScatter`, `Sparkle`, `Logo`,
the `PageHead` card every subpage opens with, and the
`SiteHeader` and `SiteFooter` that `Base.astro` puts around every page.
`sparkleArtwork.ts` holds the sparkle those draw from, and `src/assets/brand/` the
owner's wordmark.
`src/assets/screens.ts` is the table of screenshots, and is the only thing the
pages share besides the copy.

**Everything legal lives in this repository, and nowhere else.** The published
documents are `src/content/legal/`; the audit they are written from —
`privacy-policy.md`, `terms.md` and the Play Data safety worksheet — is
`docs/legal/`. The app holds no copy of any of it: it opens these URLs and records
which version it showed. That is the point of the arrangement, so **do not add a
second copy of a legal text to `pilke-app` or `treffit-backend`**, not even as a
convenience.

The documents are Markdown rather than YAML. `src/content/legal/` holds them, one
file per document per language, named `<slug>.<lang>.md`; `src/content.config.ts` declares the schema and
`src/pages/[...lang]/[doc].astro` renders every one of them. They are prose a
lawyer edits, and a lawyer edits a document rather than a list of keys. Their titles
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
nothing else, and a slab is a rounded card in the page's gutter: `slab-white`,
`slab-pale` (peach), `slab-brand` (coral) or `slab-mint`. The button those
sections link out with is `.go` in `src/styles/soft.css` — one definition, an ink
pill, with `.ghost` for the white one and `.coral` for the header's.

`src/styles/global.css` carries the app's design tokens under the same names they
have in `pilke-app/src/constants/`, so a change on either side is traceable to
the other, and beside them the site's own: the blush ground, the warm ink, the
soft rules and shadows. The wordmark and the favicons are the owner's release
artwork, drawn as paths, and the sparkle is the wordmark's own. Fredoka, the
display face, and Figtree, the body, are Google Fonts' variable files,
self-hosted in `public/fonts` so no page asks a third party for anything.

**The look is the Pehmeä direction**: rounded cards with soft shadows on a blush
page, a floating pill for the header, the phone on a coral disc, and the app's own
card tints — blue for an invitation sent, pink for one received, peach for a
confirmed date, yellow for the feedback after it — carrying the four steps of the
loop. It is light only, as the site has always been. The front page is one
composition at every width: every measure is a straight line between the 390 and
the 1440 artboard, and the layout changes shape only at 40rem, 64rem, 69rem and
75rem.

`Phone.astro` never lets a rounded corner cut into a screenshot. The picture is
inset on the colour the app paints behind that screen (`grounds` in
`src/assets/screens.ts`), and the marketing shots have the device's status bar
and navigation bar cropped; the manual keeps them, because its markers are
positioned on the whole picture.

## What the front page argues

The order of the sections is the argument, and it is the owner's pitch: what the
other apps make you do, what Pilke does instead, how it goes in practice, and who
would be better off with another app. Each part says its point once and links on
to the page that says it in full.

- **The hero** is the owner's headline and a two-sentence lead beside the app's
  home screen on a coral disc, with two buttons: down to the waitlist, and down to
  the next part.
- **The other apps** are one line of steps on the page's own ground, no card,
  between the hero and the next card: *Swaippaa. Chättäile. Tule ghostatuksi.
  Swaippaa. Chättäile lisää. Ehkä treffit.*, each struck through in coral, drawn
  in as it scrolls into view unless the reader asks for less motion. Each step is
  a `<del>`, and a hidden lead-in tells a screen reader the steps are struck.
- **What Pilke does instead** opens with the owner's line *Pilkkeessä ei
  swaippailla eikä chättäillä*, the one sentence on the site allowed to open with
  a negation, and a lead whose *nämä* points back at the struck steps. Then the
  owner's four points beside the candidates screen: candidates by your wishes and
  ordered by the persoonallisuuskysely, an invitation received or sent to one of
  three, time and place already set, and what happens after the date. The
  ordering is claimed carefully — it gets better as there are more users — and
  the feedback claim rests on the privacy statement. It links to `nain-se-toimii`.
- **In practice** is the owner's four steps on the app's four card tints, each
  with its screen running off the bottom of the card: the persoonallisuuskysely,
  an invitation, the date and the feedback. It links to the manual.
- **Who it is not for** is the owner's four questions, set large, each answered
  under it with the app that does that one thing — Tinder, Bumble, OkCupid, Valo —
  as a friend's tip and never a dig. It links to `kysyttya` and `yhteystiedot`.

**Sparks and safety are not on the front page.** Sparks are how an invitation is
paid for, which matters once somebody is using the app, and `nain-se-toimii`
carries the whole of it; on a front page even one line of them reads as a game to
be played. Safety has its own page, `turvallisuus`, in the header.

**Never set body text beside a title.** A lede to the right of a heading reads as
a second column and the eye does not know which to follow first, so every section
head stacks: title, then lede under it.

Astro scopes every compound selector, so a rule like `.start > :not(.sparkles)`
carries more attribute selectors than a bare `.start-phone` and wins on
specificity; a later override of a child has to be written with the same parent
(`.start > .start-phone`) or it silently does nothing.

Two deliberate omissions:

- **The report and the meeting-safely advice are not on the front page.** Both
  are on `turvallisuus`, which the header links to.
- **The questions are their own page** at `kysyttya`, which the header points at.
  Somebody arriving with one question is a different visit from reading the front
  page top to bottom, and a stack of six answers has no business being the last
  thing a front-page reader meets before the waitlist. The four questions the front
  page does carry are part of the pitch — who Pilke is not for — and are answered
  in a line each.

## Where the claims come from

Every factual statement was taken from the code in `pilke-app` and
`treffit-backend` rather than from their documentation, because the docs in those
repositories have repeatedly been found stale.

That rule has been broken at least once and the result was a paragraph describing
a screen that does not exist. **If a claim here cannot be traced to a constant, a
model field or a string in the app's own dictionaries, it does not go on the
site** — and a plausible-sounding sentence about what an app "asks" is exactly the
shape the invented ones take.

**The manual in `src/content/manual/` states no number by hand.** Every figure in
it is a `{{area.name}}` token, and `src/data/app-constants.json` is what fills them
in. That file is generated, not edited: `make export-constants` in
`treffit-backend` (containers up) reads each value off the setting or constant the
backend enforces and writes it here. Rerun it whenever one of those rules changes
and commit the result; a token the file does not hold fails the build. The same
tokens work in `src/content/copy/`, whose strings `t()` in `src/i18n/ui.ts` fills
in, and in the legal
documents, which `renderLegalBody()` in `src/i18n/legal.ts` renders. Most of those
pages still carry their numbers as prose, so a change the export picks up has to be
checked against them by hand; the location-sharing window and the decline and
no-answer cooldowns are tokens everywhere they appear.

The load-bearing numbers:

- A set of three candidates takes five sparks, and nothing else spends them.
- The sparks are spent when the set is drawn, not when the invitation is sent.
- One spark per ten hours of availability kept marked for a week
  (`PETAL_HOUR_DAYS`, 70 hour-days), counting only the next 14 days
  (`CALENDAR_EARNING_HORIZON`) and at most 40 hours at once
  (`CALENDAR_PENDING_HOURS_CAP`), so at most four a week. Two for a date once
  feedback is given, and five for finishing registration.
- The five a set cost come back if the invitation is declined, lapses, or is
  accepted and then called off by the person invited.
- Earning stops at fifteen sparks, which is three invitations' worth. Refunds are
  uncapped, so a balance can legitimately pass it.
- **Pilke never asks where anybody lives.** There is no home address and no
  device-location read outside a date. The date area is a choice of the server's
  drawn segments (`date_areas`, `pilke-app#81`, treffit-backend#39), picked on a
  map in onboarding — *"Missä voisit käydä treffeillä?"*, *"Ehdotamme
  treffipaikkoja vain valituilta alueilta"*. It used to be a circle the user
  dragged; the server still fills the old point and radius in from the selection
  for older builds. `privacy.area` says what the screen says.
- Location sharing runs from twenty minutes before the agreed start to twenty
  after it (`POSITION_SHARING_LEAD` and `POSITION_SHARING_TRAIL`), only within
  300 m of the venue (`POSITION_PROXIMITY_RADIUS`), and only to the other party.
  The copy says *jakaa sijainti* and *share your location*, as the app does.
- **Do not write that Pilke cannot see a shared position.** It is a row in the
  database until `core.tasks.sweep_closed_positions` deletes it, so "ei meille" and
  "Pilke itself does not see it" were both overclaims and are gone. What is true
  and worth saying instead is that nothing reads it: no penalty, no report and no
  sparks depend on it, which is what `test_positions.TestLocationIsNeverEvidence`
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
- **Strong electronic identification does not exist in either repository**, and
  the site says nothing about it. If it ships, it belongs on `turvallisuus`.
- There is no way to buy a spark, no paid visibility, no boost and no ranking.
  `TokenGrantReason` in `users/models.py` declares nine reasons and not one of
  them is a purchase, and there is no billing, in-app-purchase, boost or ranking
  code in either repository. The front page's sparks, earned and never bought, and
  the *what does it cost* answer both rest on that. Ship any of those four and both
  have to change.

The backend calls the unit a **token** in code, and its exported constants keep
the old name, `{{petals.*}}`, except `{{sparks.per_date}}`; `kipinä` and `spark` are the words users read, and
they are never called a currency. `SparkleScatter.astro` is decoration behind a
card and stands for no amount; a `Sparkle` with a count is the app's counter,
lit at five.

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
