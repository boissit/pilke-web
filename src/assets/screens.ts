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

/**
 * The colour the app paints behind each screen, for the phone frame to inset it on.
 *
 * `Phone.astro` crops a marketing shot's status bar and navigation bar and sets what
 * is left inside a margin of this colour, so the frame's rounded corner falls on the
 * app's own background and never on a photo or a button. Sampled from the stills:
 * most screens stand on the app's `white`, the two onboarding-coloured ones on
 * `brandBackground`. The questionnaire's card runs off the bottom of its screen, so its
 * margin is peach down the sides and white along the bottom, where the card is cut.
 *
 * WARNING: **A reshoot that changes a screen's background has to change it here**, or
 * the frame draws a band of the old colour round the new picture.
 */
export const grounds: Record<keyof typeof shots, string> = {
  treffit: 'var(--white)',
  story: 'linear-gradient(var(--brand-background) 95.5%, var(--white) 95.5%)',
  platter: 'var(--brand-background)',
  invitation: 'var(--white)',
  feedback: 'var(--white)',
  asetukset: 'var(--white)',
  date: 'var(--white)',
};
