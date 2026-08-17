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

`src/components/Page.astro` is the whole page, and both routes render it. A
section therefore cannot exist in one language and not the other, which is the
usual way a bilingual site drifts. `src/pages/index.astro` passes `lang="fi"`,
`src/pages/en/index.astro` passes `lang="en"`.

`src/styles/global.css` carries the app's design tokens under the same names they
have in `pilke-app/src/constants/`, so a change on either side is traceable to
the other. Fonts and the currency mark are copied from
`pilke-app/assets/`.

## Where the claims come from

Every factual statement was taken from the code in `pilke-app` and
`treffit-backend` rather than from their documentation, because the docs in those
repositories have repeatedly been found stale. The load-bearing numbers:

- A set of three candidates costs five glimmers, and there is no other price.
- The glimmers are spent when the set is drawn, not when the invitation is sent.
- One glimmer per three credited calendar spans, two for a date once feedback is
  given, five for finishing registration, five if somebody calls off a date on you.
- Earning stops at fifteen glimmers, which is three invitations' worth. Refunds are
  uncapped, so a balance can legitimately pass it.
- Position sharing runs about ten minutes either side of the agreed start, only
  within 300 m of the venue, and only to the other party.
- The safety button texts the trusted contact and nobody else. The message names no
  location, no venue and no partner.

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

Three more things to settle before launch:

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
