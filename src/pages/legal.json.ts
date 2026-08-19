import type { APIContext } from 'astro';

import { legalDocuments } from '../i18n/legal';
import { languages, localePath, type Lang } from '../i18n/ui';

/**
 * `https://pilke.app/legal.json` — which version of each legal document is live,
 * and where each language of it is served.
 *
 * The app pins the version it was built against in `src/constants/legal.ts` and the
 * backend stores what a user accepted, so three places hold the same date. This
 * endpoint is generated from the documents' own frontmatter and is what lets them
 * agree without anybody retyping it: a build that publishes a new version publishes
 * the fact that it did.
 *
 * `draft` is here on purpose. A reader is told by the notice on the page; anything
 * reading this file is told by the field.
 */
export const GET = async ({ site }: APIContext) => {
  const documents = await legalDocuments();

  const body = Object.fromEntries(
    documents.map((legal) => [
      legal.slug,
      {
        version: legal.version,
        effective: legal.effective.toISOString().slice(0, 10),
        draft: legal.draft,
        ...Object.fromEntries(
          (Object.keys(languages) as Lang[]).map((lang) => [
            lang,
            new URL(localePath(lang, legal.slug), site).href,
          ]),
        ),
      },
    ]),
  );

  return new Response(JSON.stringify(body, null, 2), {
    headers: { 'content-type': 'application/json; charset=utf-8' },
  });
};
