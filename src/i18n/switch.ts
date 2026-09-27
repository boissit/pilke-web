/**
 * Where the language switch points: the page being read, in the other language.
 *
 * Both the header and the footer carry the switch, and they have to agree, so the
 * path is worked out here once. A reader halfway down the safety page who switches
 * to English should still be on the safety page, not on the front page.
 */
import { manualRouteIn } from './manual';
import { localePath, type Lang } from './ui';

export function otherLanguage(lang: Lang): Lang {
  return lang === 'fi' ? 'en' : 'fi';
}

/**
 * `pathname` in the other language.
 *
 * The build is `format: 'file'`, so while building the path is the file's —
 * `/en/turvallisuus.html`, `/index.html`, `/en.html` — and the extension and an
 * `index` are dropped before the language is, or the front page would link to
 * `/.html`.
 *
 * The manual is the one section whose path is spelled differently per language —
 * `/ohje` and `/en/guide` — so its segment is translated on the way across.
 */
export function otherLanguageHref(pathname: string, lang: Lang): string {
  const other = otherLanguage(lang);
  const path = pathname.replace(/\.html$/, '').replace(/(^|\/)index$/, '$1');
  const route = manualRouteIn(
    path.replace(/^\/en(\/|$)/, '/').replace(/^\/+/, '').replace(/\/$/, ''),
    lang,
    other,
  );
  return localePath(other, route);
}
