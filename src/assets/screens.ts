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

export const shots = {
  treffit,
  story,
  platter,
  invitation,
  feedback,
  asetukset,
  date,
} as const;
