// @ts-check
import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://pilke.app',

  // `/tietosuoja`, not `/tietosuoja/`. The app links to the slashless form —
  // `legalUrl()` in pilke-app builds `${LEGAL_SITE}/${slug}` — and the default
  // `directory` format emits `tietosuoja/index.html`, which GitHub Pages answers
  // with a 301 to the trailing-slash URL. A browser follows it, so nothing was
  // broken; but the screen where somebody accepts the terms is a poor place to
  // spend a redirect, and anything fetching without following one would break.
  //
  // `format: 'file'` emits `tietosuoja.html` instead, which Pages serves at
  // `/tietosuoja` directly. `trailingSlash` is the setting people reach for and
  // is not this: it governs how routes are *matched*, not how files are named.
  trailingSlash: 'never',
  build: {
    format: 'file',
  },

  // Finnish is the product's language and sits at the root; English is the
  // secondary locale under /en. `prefixDefaultLocale: false` is what keeps
  // pilke.app/ Finnish rather than redirecting to pilke.app/fi/, so a shared
  // link is the language the person sharing it was reading.
  i18n: {
    defaultLocale: 'fi',
    locales: ['fi', 'en'],
    routing: {
      prefixDefaultLocale: false,
    },
  },
});
