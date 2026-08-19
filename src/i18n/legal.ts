import { getCollection, type CollectionEntry } from 'astro:content';

import { defaultLang, languages, localePath, type Lang } from './ui';

/**
 * The legal documents, read once and checked, for the page that renders them, the
 * footer that links them and the manifest that publishes their versions.
 *
 * Everything here is a build-time check that throws. A legal document that is
 * missing a language, or whose two languages disagree about which version they
 * are, is a defect that must not reach a reader — and the build is the last place
 * it can be caught, because nothing downstream would look wrong.
 */

/**
 * Every legal document, in the order they are offered to a reader: what is done
 * with their data first, then the terms they agreed to.
 *
 * The slug is Finnish and English keeps it under `/en`, as every other route on
 * the site does, so a language switch is the prefix and nothing else.
 */
export const legalSlugs = ['tietosuoja', 'kayttoehdot'] as const;

export type LegalSlug = (typeof legalSlugs)[number];

type LegalEntry = CollectionEntry<'legal'>;

export interface LegalDocument {
  slug: LegalSlug;

  /** Taken from the Finnish entry, which is the document Pilke writes. */
  version: string;
  effective: Date;
  draft: boolean;

  /** Both languages, guaranteed present. */
  entries: Record<Lang, LegalEntry>;
}

/** The `<slug>.<lang>` an entry's id is, split at the last dot. */
function parseId(id: string): { slug: string; lang: string } {
  const cut = id.lastIndexOf('.');
  return { slug: id.slice(0, cut), lang: id.slice(cut + 1) };
}

let cache: LegalDocument[] | undefined;

export async function legalDocuments(): Promise<LegalDocument[]> {
  if (cache) return cache;

  const entries = await getCollection('legal');

  const documents = legalSlugs.map((slug) => {
    const found = new Map<string, LegalEntry>();

    for (const entry of entries) {
      const parsed = parseId(entry.id);
      if (parsed.slug === slug) found.set(parsed.lang, entry);
    }

    // A document in Finnish and not in English is the usual way a bilingual site
    // drifts, and on a legal page it means a reader is handed the wrong language
    // of a binding text or a 404. The site's own routing cannot catch it here the
    // way `localeRoutes()` does for a page, because the content is the route.
    for (const lang of Object.keys(languages) as Lang[]) {
      if (!found.has(lang)) {
        throw new Error(
          `Legal document "${slug}" has no ${lang} text. Every document needs src/content/legal/${slug}.${lang}.md.`,
        );
      }
    }

    const entriesByLang = Object.fromEntries(
      (Object.keys(languages) as Lang[]).map((lang) => [lang, found.get(lang)!]),
    ) as Record<Lang, LegalEntry>;

    // The two languages are one document, so they are one version. If they
    // disagree, one of them has been edited and the other has not, and the
    // manifest would publish a version half the readers are not being shown.
    const authoritative = entriesByLang[defaultLang].data;

    for (const [lang, entry] of Object.entries(entriesByLang) as [Lang, LegalEntry][]) {
      if (entry.data.version !== authoritative.version) {
        throw new Error(
          `Legal document "${slug}" is version ${authoritative.version} in ${defaultLang} and ${entry.data.version} in ${lang}. One of the two has not been updated.`,
        );
      }
    }

    return {
      slug,
      version: authoritative.version,
      effective: authoritative.effective,
      draft: authoritative.draft,
      entries: entriesByLang,
    } satisfies LegalDocument;
  });

  cache = documents;
  return documents;
}

/** The route a document is served at, in one language. */
export function legalHref(slug: LegalSlug, lang: Lang): string {
  return localePath(lang, slug);
}

/**
 * The effective date, spelled for the reader: `1.9.2026` in Finnish and
 * `1 September 2026` in English.
 */
export function formatEffective(date: Date, lang: Lang): string {
  return date.toLocaleDateString(lang === 'fi' ? 'fi-FI' : 'en-GB', {
    day: 'numeric',
    month: lang === 'fi' ? 'numeric' : 'long',
    year: 'numeric',
  });
}
