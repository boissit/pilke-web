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
import kalenteri from '../../assets/screens/kalenteri.png';
import feedback from '../../assets/screens/feedback.png';
import platter from '../../assets/screens/platter.png';
import story from '../../assets/screens/story.png';
import treffit from '../../assets/screens/treffit.png';
import { useTranslations, type Lang } from '../../i18n/ui';

/**
 * The screens worth showing.
 *
 * Imported rather than referenced from `public/`, so Astro resizes them and
 * serves a modern format. Straight off the device they are 1080 wide and 1.4 MB
 * for the five, which is more than the rest of the page put together.
 *
 * All five are real screenshots of a real build, taken by
 * `pilke-app/.maestro/demo/screenshots.yaml` and `screenshotDate.yaml`.
 */
export const shots = {
  treffit,
  kalenteri,
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
    promises: [
      { title: t('promise.one.title'), body: t('promise.one.body'), tint: 'var(--card-received)' },
      { title: t('promise.two.title'), body: t('promise.two.body'), tint: 'var(--card-sent)' },
      { title: t('promise.three.title'), body: t('promise.three.body'), tint: 'var(--card-feedback)' },
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
    tips: [t('tips.one'), t('tips.two'), t('tips.three'), t('tips.four'), t('tips.five'), t('tips.six')],
    faq: [
      { q: t('faq.chat.q'), a: t('faq.chat.a') },
      { q: t('faq.who.q'), a: t('faq.who.a') },
      { q: t('faq.cost.q'), a: t('faq.cost.a') },
      { q: t('faq.cancel.q'), a: t('faq.cancel.a') },
      { q: t('faq.delete.q'), a: t('faq.delete.a') },
    ],
  };
}
