import { glob } from 'astro/loaders';
import { defineCollection } from 'astro:content';
// `astro/zod` rather than the `z` that `astro:content` re-exports, which is
// deprecated and slated for removal.
import { z } from 'astro/zod';

/**
 * The legal documents: the privacy statement and the terms.
 *
 * They live in this repository, and so does everything else legal: `docs/legal/`
 * holds the audit they are written from. The URL is the operative artefact — a
 * store listing links to one, a GDPR Art. 13 notice has to be readable by
 * somebody who has installed nothing, and the waitlist form may not take an
 * address until there is a policy to link it to. The app and the backend hold no
 * copy of any of it; the app opens these URLs and records which version it showed.
 * One copy of each document, so correcting one is a deploy of this site rather
 * than a store release.
 *
 * One file per document per language, named `<slug>.<lang>.md`, so the two
 * languages of a document sit next to each other and the file name is the route
 * it is served at. `legalDocuments()` in `src/i18n/legal.ts` is the only reader;
 * it refuses to build a document that exists in one language and not the other.
 */
const legal = defineCollection({
  // The id is the file name without its extension — `tietosuoja.fi` — rather than
  // the slug the default `generateId` would make of it, which drops the dot and
  // runs the two halves together.
  loader: glob({ pattern: '*.md', base: './src/content/legal', generateId: ({ entry }) => entry.replace(/\.md$/, '') }),

  schema: z.object({
    /** The heading, in the document's own language. */
    title: z.string(),

    /** One sentence under the heading, as every other page on the site opens. */
    lead: z.string(),

    /**
     * The identity of this text, and what the app records a user as having
     * accepted. A date because a legal document's identity is the day it took
     * effect, and because it sorts.
     *
     * It is carried as a string rather than a date: it is an identifier that has
     * to match `LEGAL_VERSION` in the app and a column in the database
     * character for character, and a `Date` would put a timezone between the
     * three of them. YAML hands us one anyway — an unquoted `2026-09-01` is a
     * date to a YAML parser — so it is narrowed back here rather than made the
     * author's problem to remember to quote.
     */
    version: z.preprocess(
      (value) => (value instanceof Date ? value.toISOString().slice(0, 10) : value),
      z.string().regex(/^\d{4}-\d{2}-\d{2}$/, 'version is the effective date, written YYYY-MM-DD'),
    ),

    /** The date the reader is shown. The same day as `version`, spelled for them. */
    effective: z.coerce.date(),

    /**
     * Whether this text has been through legal review.
     *
     * It defaults to `true` because that is the safe way round: a document is a
     * draft until somebody says otherwise, and a draft renders a notice saying so
     * at the top of the page. Clearing the flag is the same act as finishing the
     * text, so a page cannot quietly present placeholder terms as binding ones.
     */
    draft: z.boolean().default(true),
  }),
});

/**
 * The user manual: the rules of the app a user cannot see on its screens — why a
 * candidate appeared, where the petals went, why a report was refused — one system
 * to a page.
 *
 * Named and paired exactly as `legal` is — `<slug>.<lang>.md`, a Finnish slug in
 * both languages, both languages required — so a reader who switches language
 * lands on the same page, and a page cannot exist in Finnish and quietly 404 in
 * English. `manualPages()` in `src/i18n/manual.ts` is the only reader and is
 * where that is enforced.
 *
 * The body is ordinary Markdown with two additions, both resolved when the page
 * is built rather than here: `![alt](shot:<name>#testID,…)` on a paragraph of its
 * own is a screenshot from `src/assets/manual/<lang>/`, drawn in a phone with
 * numbered markers, and `{{area.name}}` is a value from
 * `src/data/app-constants.json`. `docs/manual-shots.md` is the contract for the
 * first. `src/manual/body.ts` explains why neither is a Markdown plugin.
 */
const manual = defineCollection({
  // The same id as `legal`, for the same reason: `kalenteri.fi`, not `kalenterifi`.
  loader: glob({ pattern: '*.md', base: './src/content/manual', generateId: ({ entry }) => entry.replace(/\.md$/, '') }),

  schema: z.object({
    /** The heading, in the page's own language. */
    title: z.string(),

    /** One sentence under the heading, and the line the index shows under the link. */
    lead: z.string(),

    /**
     * Where the page sits on the index, lowest first. The manual is one list, read
     * top to bottom as the order the app is learnt in, so this is the whole of its
     * structure. Only the order relative to the others matters, so leave gaps: `10`,
     * `20`, `30`.
     */
    order: z.number(),

    /**
     * Whether the text and its pictures are finished.
     *
     * It defaults to `true`, as `legal` does and for the same reason: a page is
     * unfinished until somebody says otherwise, and an unfinished one says so at
     * the top. It is also the one switch that lets a page be built before its
     * screenshots exist — a draft draws a "screenshot missing" box where a still
     * has not been captured yet, and a finished page refuses to build without it.
     */
    draft: z.boolean().default(true),
  }),
});

export const collections = { legal, manual };
