import { getCollection, type CollectionEntry } from 'astro:content';

import { resolveTokens } from '../manual/constants';
import { defaultLang, languages, localePath, type Lang } from './ui';

/**
 * The manual's pages, read once and checked, for the index that lists them, the page
 * that renders one and the header that links the whole thing.
 *
 * Modelled on `legal.ts`, and for the same reason everything here throws: a page in one
 * language only, or whose two languages disagree about where it sits, is a defect that
 * nothing downstream would make look wrong.
 */

/**
 * The segment the manual lives under, per language: `/ohje/<slug>` and
 * `/en/guide/<slug>`.
 *
 * The one place the site translates a path. Every other route keeps its Finnish slug
 * under `/en`, so a language switch is the prefix and nothing else; the manual is linked
 * to from outside — from the app's help, from a support reply — and an English reader
 * sent to `/en/ohje` is sent to a word they cannot read. The page slugs under it stay
 * Finnish in both, as `legal` does, so the two languages of one page still share a name.
 */
export const manualSegment: Record<Lang, string> = { fi: 'ohje', en: 'guide' };

type ManualEntry = CollectionEntry<'manual'>;

export type ManualKind = ManualEntry['data']['kind'];

export interface ManualPage {
  slug: string;
  kind: ManualKind;
  order: number;

  /** Both languages, guaranteed present. `draft` is read from each: a translation can lag. */
  entries: Record<Lang, ManualEntry>;

  /** Title and lead per language, with their `{{tokens}}` already resolved. */
  text: Record<Lang, { title: string; lead: string }>;
}

/** The Markdown file an entry came from, for error messages that say what to open. */
export function manualFile(entry: ManualEntry): string {
  return entry.filePath ?? `src/content/manual/${entry.id}.md`;
}

/** The `<slug>.<lang>` an entry's id is, split at the last dot. */
function parseId(id: string): { slug: string; lang: string } {
  const cut = id.lastIndexOf('.');
  return { slug: id.slice(0, cut), lang: id.slice(cut + 1) };
}

const langs = Object.keys(languages) as Lang[];

let cache: ManualPage[] | undefined;

/** Every page, in index order: by `order`, then by slug so a tie is stable. */
export async function manualPages(): Promise<ManualPage[]> {
  if (cache) return cache;

  const bySlug = new Map<string, Map<string, ManualEntry>>();
  for (const entry of await getCollection('manual')) {
    const { slug, lang } = parseId(entry.id);
    if (!(langs as string[]).includes(lang)) {
      throw new Error(`${manualFile(entry)} is not named <slug>.<lang>.md with lang one of ${langs.join(', ')}.`);
    }
    if (!bySlug.has(slug)) bySlug.set(slug, new Map());
    bySlug.get(slug)!.set(lang, entry);
  }

  const pages = [...bySlug].map(([slug, found]) => {
    // The same drift `legal.ts` refuses, for the same reason: a page in Finnish and not
    // in English is a language switch into a 404, and the route is made from the content,
    // so nothing else would notice.
    for (const lang of langs) {
      if (!found.has(lang)) {
        throw new Error(`Manual page "${slug}" has no ${lang} text. Every page needs src/content/manual/${slug}.${lang}.md.`);
      }
    }

    const entries = Object.fromEntries(langs.map((lang) => [lang, found.get(lang)!])) as Record<Lang, ManualEntry>;

    // `kind` and `order` place the page on the index, and the index is the same list in
    // both languages. If they disagree, one file was edited and the other was not.
    const authoritative = entries[defaultLang].data;
    for (const lang of langs) {
      const data = entries[lang].data;
      if (data.kind !== authoritative.kind || data.order !== authoritative.order) {
        throw new Error(
          `Manual page "${slug}" is ${authoritative.kind} ${authoritative.order} in ${defaultLang} and ${data.kind} ${data.order} in ${lang}. One of the two has not been updated.`,
        );
      }
    }

    const text = Object.fromEntries(
      langs.map((lang) => {
        const where = manualFile(entries[lang]);
        const { title, lead } = entries[lang].data;
        return [lang, { title: resolveTokens(title, where), lead: resolveTokens(lead, where) }];
      }),
    ) as ManualPage['text'];

    return { slug, kind: authoritative.kind, order: authoritative.order, entries, text } satisfies ManualPage;
  });

  pages.sort((a, b) => a.order - b.order || a.slug.localeCompare(b.slug));

  cache = pages;
  return pages;
}

/** The index in `lang`, or one page of the manual when `slug` is given. */
export function manualHref(lang: Lang, slug?: string): string {
  return localePath(lang, slug ? `${manualSegment[lang]}/${slug}` : manualSegment[lang]);
}

/**
 * `route` — a path without its language prefix, as the header works it out — as it is
 * spelled in `to`. Only the manual's segment differs between the languages, so anything
 * else comes back as it was.
 */
export function manualRouteIn(route: string, from: Lang, to: Lang): string {
  const [first, ...rest] = route.split('/');
  return first === manualSegment[from] ? [manualSegment[to], ...rest].join('/') : route;
}
