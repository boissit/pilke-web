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

  /**
   * The same markers in percentages of the picture with its bars cut, for a phone
   * drawn with `bars="crop"`. An element that lies wholly in a bar has no marker
   * here, and the others keep the number they have in `markers`, which is the one
   * the text refers to.
   */
  cropped: Marker[];

  /** The colour behind the app on this still, for a frame that insets it. */
  ground: string;
}

/**
 * The device's status bar and navigation bar, in the stills' pixels. Every still is
 * captured on the same emulator profile, so this is the same on all of them, and it is
 * the crop `Phone.astro` makes with `bars="crop"`.
 */
export const BARS = { top: 96, bottom: 136 } as const;

/**
 * The colour the app paints behind a still, for a frame that sets the picture in a
 * margin, as `grounds` in `src/assets/screens.ts` is for the marketing shots. Sampled
 * from the stills: the app's `white` unless named here. A modal's scrim is the
 * dimmed white it is drawn over, so the margin is dimmed with the screen. A map runs
 * to the screen's edges, so its margin is the map's grey down to where the map ends:
 * 1160 of the still on `date-map`, which is 51.8% of the inset screen once the bars
 * are cut, and 1213 on `date-map-sharing`, 54.1%.
 *
 * WARNING: **A reshoot that changes a screen's background has to change it here**, or
 * the frame draws a band of the old colour round the new picture.
 */
const stillGrounds: Record<string, string> = {
  platter: 'var(--brand-background)',
  'kalenteri-valikko': '#979394',
  'date-location-consent': 'linear-gradient(#8c8c8c 51.8%, #979394 51.8%)',
  'date-map': 'linear-gradient(#ebebeb 51.8%, var(--white) 51.8%)',
  'date-map-sharing': 'linear-gradient(#ebebeb 54.1%, var(--white) 54.1%)',
};

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

/**
 * How far the ring stands off its element, as a share of the still's width.
 *
 * A testID's bounds are the element's own edge, so a ring drawn on them sits on the
 * element's border and hides it, and the dashes cut across the first letters of a
 * link. The padding is applied before the badges are placed, so a badge clears the
 * ring and not merely the element inside it. It is clamped to the screen, which is
 * where an edge-to-edge element such as a map already ends.
 */
const RING_PADDING_SHARE = 0.018;

/**
 * The roundest corner any frame in `Phone.astro` cuts the picture to, as a share of its
 * width: a `rounded` screen's 12.7 of the 93.4 the picture is wide is 0.136.
 */
const CORNER_SHARE = 0.14;

function padded(element: Box, image: { width: number; height: number }): Box {
  const pad = image.width * RING_PADDING_SHARE;
  const x = Math.max(0, element.x - pad);
  const y = Math.max(0, element.y - pad);
  return {
    x,
    y,
    width: Math.min(image.width, element.x + element.width + pad) - x,
    height: Math.min(image.height, element.y + element.height + pad) - y,
  };
}

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
 *
 * Every badge is inside the picture and clear of its rounded corners, whatever the
 * frame: a phone whose screen is cut to the shell's corner, or a card, clips anything
 * past the picture's edge, and half a numeral is no numeral.
 */
function placeBadges(elements: Box[], image: { width: number; height: number }): { x: number; y: number }[] {
  const size = image.width * BADGE_SHARE;
  const r = size / 2;
  const gap = size * 0.15;
  const placed: Box[] = [];
  const corner = image.width * CORNER_SHARE;

  // Inside the picture's rounded rectangle: within the edges by the badge's radius, and
  // within the corner's curve by the same where it is near one.
  const onScreen = (x: number, y: number) => {
    const inEdges = x >= r && y >= r && x <= image.width - r && y <= image.height - r;
    const nearestX = Math.min(Math.max(x, corner), image.width - corner);
    const nearestY = Math.min(Math.max(y, corner), image.height - corner);
    return inEdges && Math.hypot(x - nearestX, y - nearestY) <= corner - r;
  };

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
      return onScreen(x, y) && !elements.some((other) => overlaps(badge, other)) && !placed.some((other) => overlaps(badge, other));
    });
    const centre = clear ?? {
      x: Math.min(Math.max(e.x + r * 0.2, r), image.width - r),
      y: Math.min(Math.max(e.y + r * 0.2, r), image.height - r),
    };
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
    if (draft) return { name, lang, alt, markers: [], cropped: [], ground: 'var(--white)' };
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
    return padded(element, image);
  });
  const numbered = elements.map((box, index) => ({ box, number: index + 1, testID: testIDs[index] }));

  // The band between the bars, with every box moved up by the status bar and cut to
  // the band. One that has nothing left is in a bar, out of the picture, and goes.
  const band = { width: image.width, height: image.height - BARS.top - BARS.bottom };
  const inBand = numbered.flatMap((marker) => {
    const top = Math.max(marker.box.y - BARS.top, 0);
    const bottom = Math.min(marker.box.y + marker.box.height - BARS.top, band.height);
    return bottom > top ? [{ ...marker, box: { ...marker.box, y: top, height: bottom - top } }] : [];
  });

  const ground = stillGrounds[name] ?? 'var(--white)';
  return { name, lang, alt, image, markers: markersOn(numbered, image), cropped: markersOn(inBand, band), ground };
}

/**
 * Badges placed for these boxes on a picture of this size, and the lot in its
 * percentages. The bounds are in the PNG's pixels, which is what the image metadata
 * measures, so the markers land on the same spot at whatever size the phone is drawn.
 */
function markersOn(
  numbered: { box: Box; number: number; testID: string }[],
  picture: { width: number; height: number },
): Marker[] {
  const badges = placeBadges(
    numbered.map(({ box }) => box),
    picture,
  );
  return numbered.map(({ box, number, testID }, index) => ({
    number,
    testID,
    left: percent(box.x, picture.width),
    top: percent(box.y, picture.height),
    width: percent(box.width, picture.width),
    height: percent(box.height, picture.height),
    badgeLeft: percent(badges[index].x, picture.width),
    badgeTop: percent(badges[index].y, picture.height),
  }));
}
