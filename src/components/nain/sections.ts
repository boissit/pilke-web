/**
 * `nain-se-toimii`'s sections, in the order the page draws them: the copy and the
 * screen of each, kept apart from `GridLayout`, which only decides how wide each
 * card stands. Kipinät, the date's photograph and the plans that change are drawn
 * by their own components, `Economy`, `DateSection` and `Changes`; the rest are a
 * title, one or two paragraphs and a screen.
 */
import { shotsFor } from '../../assets/screens';
import type { Lang } from '../../i18n/ui';
import { useTranslations } from '../../i18n/ui';

type Section =
  | { kind: 'text'; id: string; title: string; body: string[]; shot: ImageMetadata; alt: string }
  | { kind: 'economy'; id: string; title: string }
  | { kind: 'date'; id: string; title: string }
  | { kind: 'changes'; id: string; title: string; shot: ImageMetadata; alt: string }
  | { kind: 'chat'; id: string; title: string; body: string[]; shot: ImageMetadata; alt: string };

export function nainSections(lang: Lang): Section[] {
  const t = useTranslations(lang);
  const shots = shotsFor(lang);

  return [
    { kind: 'text', id: 'start', title: t('detail.start.title'), body: [t('detail.start.body')], shot: shots.preferences, alt: t('shot.preferences') },
    { kind: 'text', id: 'prefs', title: t('detail.prefs.title'), body: [t('detail.prefs.body')], shot: shots.kalenteri, alt: t('shot.kalenteri') },
    { kind: 'text', id: 'draw', title: t('detail.draw.title'), body: [t('detail.draw.body'), t('detail.draw.feedback')], shot: shots.platter, alt: t('shot.platter') },
    { kind: 'text', id: 'invite', title: t('detail.invite.title'), body: [t('detail.invite.body')], shot: shots.invitation, alt: t('shot.invitation') },
    { kind: 'economy', id: 'economy', title: t('detail.economy.title') },
    { kind: 'date', id: 'date', title: t('detail.enjoy.title') },
    { kind: 'text', id: 'after', title: t('detail.after.title'), body: [t('detail.after.body')], shot: shots.feedback, alt: t('shot.feedback') },
    { kind: 'changes', id: 'changes', title: t('detail.changes.title'), shot: shots.dateCancel, alt: t('shot.date-cancel') },
    { kind: 'chat', id: 'chat', title: t('detail.chat.title'), body: [t('detail.chat.body'), t('detail.chat.wishes')], shot: shots.date, alt: t('shot.date') },
  ];
}
