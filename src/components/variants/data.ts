/**
 * The content each variant renders, assembled once.
 *
 * The three layouts differ in arrangement, not in what they say, so they read
 * from one place. A variant that quietly said something different would make the
 * comparison useless.
 */
import asetukset from '../../assets/screens/asetukset.png';
import date from '../../assets/screens/date.png';
import invitation from '../../assets/screens/invitation.png';
import feedback from '../../assets/screens/feedback.png';
import platter from '../../assets/screens/platter.png';
import story from '../../assets/screens/story.png';
import treffit from '../../assets/screens/treffit.png';
import { useTranslations, type Lang } from '../../i18n/ui';

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
export const shots = {
  treffit,
  story,
  platter,
  invitation,
  feedback,
  asetukset,
  date,
} as const;

export function content(lang: Lang) {
  const t = useTranslations(lang);

  return {
    t,
    /*
      The three claims that sit in a bar under the headline. One line each and no
      card around them: as boxes they were three shadowed rectangles competing
      with the phone beside them, and none of the three needs a paragraph.
    */
    facts: [
      { title: t('fact.one.title'), body: t('fact.one.body') },
      { title: t('fact.two.title'), body: t('fact.two.body') },
      { title: t('fact.three.title'), body: t('fact.three.body') },
    ],
    /*
      The two ways to end up on a date, each as a chain of one-word steps. The
      argument is the length of the chain, so the steps are single words and the
      prose under them stays to two sentences.
    */
    routes: [
      {
        label: t('diff.old.label'),
        body: t('diff.old.body'),
        ours: false,
        steps: [t('diff.old.one'), t('diff.old.two'), t('diff.old.three'), t('diff.old.four')],
      },
      {
        label: t('diff.new.label'),
        body: t('diff.new.body'),
        ours: true,
        steps: [t('diff.new.one'), t('diff.new.two'), t('diff.new.three')],
      },
    ],
    steps: [
      { title: t('how.one.title'), body: t('how.one.body'), shot: shots.platter, alt: t('shot.platter') },
      { title: t('how.two.title'), body: t('how.two.body'), shot: shots.invitation, alt: t('shot.invitation') },
      { title: t('how.three.title'), body: t('how.three.body'), shot: shots.date, alt: t('shot.date') },
      { title: t('how.four.title'), body: t('how.four.body'), shot: shots.feedback, alt: t('shot.feedback') },
    ],
    safety: [
      { title: t('safety.contact.title'), body: t('safety.contact.body') },
      { title: t('safety.button.title'), body: t('safety.button.body') },
      { title: t('safety.report.title'), body: t('safety.report.body') },
    ],
    /*
      The front page's three safety cards. Shorter than the ones above and not
      the same three: the location window replaces the report, because a reader
      who has not yet used the app is served better by what the app will not do
      with their whereabouts than by how to complain afterwards. The full set,
      report included, is on `turvallisuus`.
    */
    safetyCards: [
      {
        title: t('safety.card.contact.title'),
        body: t('safety.card.contact.body'),
        tint: 'var(--card-received)',
      },
      {
        title: t('safety.card.button.title'),
        body: t('safety.card.button.body'),
        tint: 'var(--card-sent)',
      },
      {
        title: t('safety.card.places.title'),
        body: t('safety.card.places.body'),
        tint: 'var(--card-feedback)',
      },
    ],
    tips: [t('tips.one'), t('tips.two'), t('tips.three'), t('tips.four'), t('tips.five'), t('tips.six')],
    faq: [
      { q: t('faq.chat.q'), a: t('faq.chat.a') },
      { q: t('faq.who.q'), a: t('faq.who.a') },
      { q: t('faq.safety.q'), a: t('faq.safety.a') },
      { q: t('faq.cost.q'), a: t('faq.cost.a') },
      { q: t('faq.cancel.q'), a: t('faq.cancel.a') },
      { q: t('faq.delete.q'), a: t('faq.delete.a') },
    ],
  };
}
