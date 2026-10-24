/**
 * The site's copy, read from `src/content/copy/*.yaml`, and the routes every page is
 * built at.
 *
 * Every string a page draws comes from those files, one page per file with the two
 * languages of a sentence side by side; the house style is the header of `site.yaml`.
 * The guide and the legal documents are Markdown and are read by `manual.ts` and
 * `legal.ts`. Nothing here holds a string of its own.
 *
 * WARNING: **The guarantees a typed dictionary gave are checked here instead.** YAML
 * cannot say that a key has both languages, so this module throws while the site is
 * built on an entry missing one, an empty string, a key in two files, and a page
 * asking for a key no file holds. A failed build names the file and the key.
 */
import { parse } from 'yaml';

import { resolveTokens } from '../manual/constants';

export const langs = ['fi', 'en'] as const;

export type Lang = (typeof langs)[number];

export const defaultLang: Lang = 'fi';

type Entry = Record<Lang, string> & { file: string };

const COPY_DIR = 'src/content/copy';

const sources = import.meta.glob<string>('/src/content/copy/*.yaml', { query: '?raw', import: 'default', eager: true });

function load(): Map<string, Entry> {
  const copy = new Map<string, Entry>();

  for (const [path, raw] of Object.entries(sources)) {
    const file = `${COPY_DIR}/${path.split('/').pop()}`;
    // `uniqueKeys` is the parser's default and is what refuses a key twice in one file.
    const document: unknown = parse(raw);
    if (document === null) continue;
    if (typeof document !== 'object' || Array.isArray(document)) {
      throw new Error(`${file} is not a map of keys to { fi, en }.`);
    }

    for (const [key, value] of Object.entries(document)) {
      const where = `${file} (${key})`;
      const earlier = copy.get(key);
      if (earlier) throw new Error(`${where} is also in ${earlier.file}. A key lives in one file.`);
      if (value === null || typeof value !== 'object' || Array.isArray(value)) {
        throw new Error(`${where} is not { fi, en }.`);
      }

      const extra = Object.keys(value).filter((lang) => !(langs as readonly string[]).includes(lang));
      if (extra.length) throw new Error(`${where} has ${extra.join(', ')}, which is not a language of the site.`);

      for (const lang of langs) {
        const text: unknown = (value as Record<string, unknown>)[lang];
        if (typeof text !== 'string' || text.trim() === '') {
          throw new Error(`${where} has no ${lang} text. Every key needs both ${langs.join(' and ')}.`);
        }
      }

      copy.set(key, { ...(value as Record<Lang, string>), file });
    }
  }

  return copy;
}

const copy = load();

/*
  `npm run copy:export` builds the site once with `COPY_TRACE=1`, and every string a
  page draws then carries its key between private-use characters, so the export can
  read off the built pages which text is drawn where, in what order and as what. They
  are never in a build that ships: without the variable this is the identity.
*/
const tracing = process.env.COPY_TRACE === '1';

/** `text` as the page draws it, wrapped with its key and language in a traced build. */
export function traced(lang: Lang, key: string, text: string): string {
  return tracing ? `\uE000${lang}:${key}\uE001${text}\uE002` : text;
}

/**
 * A lookup in `lang`, with every `{{area.name}}` token filled in from the app's
 * constants, as the manual's are (`src/manual/constants.ts`). A figure the backend
 * owns, like how long location sharing runs, is written as a token rather than as
 * prose, so it moves when the backend's value does.
 */
export function useTranslations(lang: Lang) {
  return function t(key: string): string {
    const entry = copy.get(key);
    if (!entry) throw new Error(`No file in ${COPY_DIR}/ holds the key "${key}".`);
    return traced(lang, key, resolveTokens(entry[lang], `${entry.file} (${lang}.${key})`));
  };
}

/** A language's own name for itself, `Suomi` or `English`, as the language switch reads. */
export function languageName(lang: Lang): string {
  return useTranslations(lang)('language.name');
}

/** The path to `route` in `lang`: Finnish at the root, English under /en. */
export function localePath(lang: Lang, route = ''): string {
  const clean = route.replace(/^\/+/, '');
  const prefix = lang === defaultLang ? '/' : `/${lang}/`;
  return `${prefix}${clean}`.replace(/\/+$/, '') || '/';
}

/**
 * The routes every page is built at: Finnish at the root, English under `/en`.
 *
 * A page file lives at `pages/[...lang]/<slug>.astro` and hands this to
 * `getStaticPaths`, so one file is both languages of one page and a section
 * cannot exist in Finnish and not in English. The Finnish entry has no segment
 * at all — a rest parameter matches zero of them — which is what puts Finnish at
 * the root without a redirect.
 */
export function localeRoutes() {
  return [{ params: { lang: undefined } }, { params: { lang: 'en' } }];
}

/** The language of the route being built, from the `[...lang]` segment. */
export function localeOf(params: { lang?: string | undefined }): Lang {
  return params.lang === 'en' ? 'en' : defaultLang;
}
