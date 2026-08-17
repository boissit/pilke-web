// @ts-check
import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://pilke.app',

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
