/**
 * The manual's screenshots, looked up by the name the text gives them and checked
 * against their sidecars.
 *
 * `docs/manual-shots.md` is the contract: a still is `src/assets/manual/<lang>/<name>.png`
 * with a `<name>.json` beside it, taken by the capture pipeline in `pilke-app`, and the
 * sidecar records where each testID sits on it in the PNG's own pixels. The text names
 * the testIDs it wants numbered; this turns those into boxes the page can draw.
 *
 * Both are globbed rather than imported by name so that a still the capture has not
 * produced yet is a question this module answers — "draft, so draw a box" or "not a
 * draft, so stop" — rather than an unresolved import that takes the whole build down
 * with Vite's message instead of ours. The PNGs come back as `ImageMetadata`, so they
 * still go through Astro's image pipeline exactly as `src/assets/screens` do.
 *
 * WARNING: **Everything wrong here fails the build except one thing.** A missing PNG on
 * a page with `draft: true` is drawn as a visible "screenshot missing" box, because the
 * text is written while the stills are captured and a draft has to be readable before
 * both are done. A missing sidecar, a missing testID, or a missing PNG on a finished
 * page all stop the build: each is a picture that would be drawn wrong or not at all on
 * a page that says it is done.
 */
import { z } from 'astro/zod';

import type { Lang } from '../i18n/ui';

const DIR = 'src/assets/manual';

const pngs = import.meta.glob<ImageMetadata>('/src/assets/manual/*/*.png', { eager: true, import: 'default' });
const sidecars = import.meta.glob<unknown>('/src/assets/manual/*/*.json', { eager: true, import: 'default' });

const bounds = z.object({
  x: z.number(),
  y: z.number(),
  width: z.number().nonnegative(),
  height: z.number().nonnegative(),
});

/**
 * The sidecar, as `docs/manual-shots.md` defines it. `commit` and `takenAt` are not
 * used to draw anything; they are checked here because `npm run pictures` reads
 * `commit` to say which stills may be stale, and a sidecar without one would be
 * silently exempt.
 */
const sidecarSchema = z.object({
  name: z.string(),
  language: z.string(),
  commit: z.string().min(1),
  takenAt: z.string(),
  screen: z.object({ width: z.number(), height: z.number() }),
  elements: z.record(z.string(), bounds),
});

/** A numbered marker, placed in percentages of the still so it scales with it. */
export interface Marker {
  number: number;
  testID: string;
  left: number;
  top: number;
  width: number;
  height: number;

  /** Where the number goes: the centre of its badge, beside the element rather than on it. */
  badgeLeft: number;
  badgeTop: number;
}

export interface Still {
  name: string;
  lang: Lang;
  alt: string;

  /** Absent only on a draft whose still has not been captured yet. */
  image?: ImageMetadata;

  /** In the order the text listed them, numbered from 1. */
  markers: Marker[];
}

/** What a paragraph of the form `![alt](shot:name#id1,id2)` asked for. */
export interface ShotReference {
  alt: string;
  name: string;
  testIDs: string[];
}

/** Names are file names in two directories and URL-ish in the text, so they stay plain. */
const NAME = /^[a-z0-9]+(-[a-z0-9]+)*$/;

function percent(part: number, whole: number): number {
  return Math.round((part / whole) * 10000) / 100;
}

/**
 * The badge's diameter as a share of the still's width, which `ManualStep.astro` draws
 * it at. A share rather than pixels, so where it fits is decided once for every size
 * the phone is drawn at.
 */
export const BADGE_SHARE = 0.11;

interface Box {
  x: number;
  y: number;
  width: number;
  height: number;
}

function overlaps(a: Box, b: Box): boolean {
  return a.x < b.x + b.width && b.x < a.x + a.width && a.y < b.y + b.height && b.y < a.y + a.height;
}

/**
 * The centre of each badge, in the still's pixels.
 *
 * A badge on top of its element hides the very thing it points at — a text link is
 * mostly covered by one — so each goes beside its element: to the left, then the right,
 * above, below, in that order, taking the first spot that stays on the screen and clears
 * every marked element and every badge already placed. Two icons side by side in a
 * header are the common case that rules out left and right. Where nothing fits, the
 * badge sits on the element's top-left corner, which at least leaves most of it visible.
 */
function placeBadges(elements: Box[], image: { width: number; height: number }): { x: number; y: number }[] {
  const size = image.width * BADGE_SHARE;
  const r = size / 2;
  const gap = size * 0.15;
  const placed: Box[] = [];

  return elements.map((e) => {
    const cy = e.y + e.height / 2;
    const cx = e.x + e.width / 2;
    const candidates = [
      { x: e.x - gap - r, y: cy },
      { x: e.x + e.width + gap + r, y: cy },
      { x: Math.min(cx, e.x + r), y: e.y - gap - r },
      { x: Math.min(cx, e.x + r), y: e.y + e.height + gap + r },
    ];
    const clear = candidates.find(({ x, y }) => {
      const badge = { x: x - r, y: y - r, width: size, height: size };
      const onScreen = badge.x >= 0 && badge.y >= 0 && badge.x + size <= image.width && badge.y + size <= image.height;
      return onScreen && !elements.some((other) => overlaps(badge, other)) && !placed.some((other) => overlaps(badge, other));
    });
    const centre = clear ?? { x: e.x + r * 0.2, y: e.y + r * 0.2 };
    placed.push({ x: centre.x - r, y: centre.y - r, width: size, height: size });
    return centre;
  });
}

/**
 * The still `reference` names, in `lang`, with its markers placed. `where` names the
 * Markdown file in every error, and `draft` is that file's own flag.
 */
export function resolveStill(reference: ShotReference, lang: Lang, draft: boolean, where: string): Still {
  const { alt, name, testIDs } = reference;
  const png = `${DIR}/${lang}/${name}.png`;
  const json = `${DIR}/${lang}/${name}.json`;

  if (!NAME.test(name)) {
    throw new Error(`${where} refers to shot:${name}, which is not a still name. Names are lowercase words joined by hyphens, as in docs/manual-shots.md.`);
  }

  // The alt carries the picture for anybody not seeing it, and on a page explaining an
  // app the picture carries the explaining, so there is no decorative case to allow for.
  if (!alt.trim()) {
    throw new Error(`${where} shows shot:${name} with no alt text. Write what the screenshot shows, in the page's language.`);
  }

  const duplicate = testIDs.find((id, index) => testIDs.indexOf(id) !== index);
  if (duplicate) {
    throw new Error(`${where} numbers ${duplicate} twice on shot:${name}. Each testID gets one marker.`);
  }

  const image = pngs[`/${png}`];

  if (!image) {
    if (draft) return { name, lang, alt, markers: [] };
    throw new Error(
      `${where} shows shot:${name}, but ${png} does not exist. Capture it, or keep the page at draft: true until it is.`,
    );
  }

  const raw = sidecars[`/${json}`];
  if (raw === undefined) {
    throw new Error(`${where} shows shot:${name}, and ${png} exists, but its sidecar ${json} does not. Recapture the still: the two are written together.`);
  }

  const parsed = sidecarSchema.safeParse(raw);
  if (!parsed.success) {
    throw new Error(`${json} is not a sidecar docs/manual-shots.md describes: ${parsed.error.issues.map((i) => `${i.path.join('.') || '(root)'} ${i.message}`).join('; ')}.`);
  }
  const sidecar = parsed.data;

  // A still copied into the wrong directory is a Finnish screen on the English page, and
  // nothing about the picture itself would say so.
  if (sidecar.name !== name || sidecar.language !== lang) {
    throw new Error(`${json} says it is ${sidecar.name} in ${sidecar.language}. It is filed as ${name} in ${lang}.`);
  }

  const elements = testIDs.map((testID) => {
    const element = sidecar.elements[testID];
    if (!element) {
      throw new Error(
        `${where} numbers ${testID} on shot:${name}, but ${json} has no bounds for it. Add ${testID} to the still's callouts in docs/manual-shots.md so the next capture records it.`,
      );
    }
    return element;
  });
  const badges = placeBadges(elements, image);

  // The bounds are in the PNG's pixels, which is what the image metadata measures, so
  // the markers land on the same spot at whatever size the phone is drawn.
  const markers = elements.map((element, index) => ({
    number: index + 1,
    testID: testIDs[index],
    left: percent(element.x, image.width),
    top: percent(element.y, image.height),
    width: percent(element.width, image.width),
    height: percent(element.height, image.height),
    badgeLeft: percent(badges[index].x, image.width),
    badgeTop: percent(badges[index].y, image.height),
  }));

  return { name, lang, alt, image, markers };
}
