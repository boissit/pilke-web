/**
 * The screens worth showing.
 *
 * Imported rather than referenced from `public/`, so Astro resizes them and serves a
 * modern format. Straight off the device each is 1080 wide, and the seven together
 * outweigh the rest of the page.
 *
 * Every one is a still of a real build, taken by the flows in
 * `pilke-app/.maestro/demo/`. Which page draws which, and what each one shows that can
 * go stale when the app changes, is `docs/pictures.md` — a screenshot only reaches a
 * page through this table and a component prop, so that document is the account of it.
 *
 * A screen with no entry here is not shown anywhere: `screenshots.yaml` also takes the
 * calendar and the question sets, and neither has a place on the site.
 */
import asetukset from './screens/asetukset.png';
import date from './screens/date.png';
import invitation from './screens/invitation.png';
import feedback from './screens/feedback.png';
import platter from './screens/platter.png';
import story from './screens/story.png';
import treffit from './screens/treffit.png';
import asetuksetEn from './screens/asetukset-en.png';
import dateEn from './screens/date-en.png';
import feedbackEn from './screens/feedback-en.png';
import invitationEn from './screens/invitation-en.png';
import platterEn from './screens/platter-en.png';
import storyEn from './screens/story-en.png';

export const shots = {
  treffit,
  story,
  platter,
  invitation,
  feedback,
  asetukset,
  date,
} as const;

/**
 * The English app, for `/en`. A screen missing here falls back to the Finnish one:
 * `treffit` has none, because no page draws it in a phone frame -- the English home is
 * in the hero's photograph.
 */
const shotsEn: Partial<Record<keyof typeof shots, ImageMetadata>> = {
  asetukset: asetuksetEn,
  story: storyEn,
  platter: platterEn,
  invitation: invitationEn,
  feedback: feedbackEn,
  date: dateEn,
};

/** The screens in a page's language, Finnish where English has none. */
export function shotsFor(lang: string): Record<keyof typeof shots, ImageMetadata> {
  return lang === 'en' ? { ...shots, ...shotsEn } : shots;
}
