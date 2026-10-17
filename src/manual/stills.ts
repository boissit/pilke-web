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
import { inkColumns, inkIn, readPixels, type Pixels } from './pixels';

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

/**
 * How far the ring stands off its element, as a share of the still's width.
 *
 * A testID's bounds are the element's own edge, so a ring drawn on them sits on the
 * element's border and hides it, and the dashes cut across the first letters of a
 * link. The padding is applied before the badges are placed, so a badge clears the
 * ring and not merely the element inside it.
 */
const RING_PADDING_SHARE = 0.018;

/**
 * The corner `Phone.astro` cuts the manual's still to, as a share of its width, a
 * little over: the screen's 12.7 of the 95.2 the picture is wide is 0.133.
 */
const CORNER_SHARE = 0.14;

/**
 * The Android status bar and navigation bar, in rows of the Pixel 4 profile every
 * still is captured on: the same 96 and 136 `Phone.astro` crops off a marketing
 * screen and `scripts/photos/stills.py` checks. Rings and badges stay between them:
 * the camera is drawn over the middle of the status bar, and the bars are not the app.
 */
const STATUS_BAR = 96;
const NAVIGATION_BAR = 136;

/**
 * The tallest element, as a share of the still's width, that is trimmed to its ink:
 * one line of text, a little over the 52 pixels a line of body copy is.
 *
 * A `Text` stretches to its row, so its testID's bounds run on past the last word to
 * the edge of the card, and a ring drawn on them marks the empty half of the row too.
 * Such a line is ringed from its first drawn column to its last. Anything taller is a
 * control, a card or an area, whose bounds are its edge, and is ringed as it stands.
 */
const LINE_SHARE = 0.065;

/**
 * The most of a badge's disc that may be drawn on for it to count as clear: a thin
 * rule, a map's street name glancing its edge. A word under it is several times this.
 */
const CLEAR_INK = 0.006;

interface Box {
  x: number;
  y: number;
  width: number;
  height: number;
}

function overlaps(a: Box, b: Box): boolean {
  return a.x < b.x + b.width && b.x < a.x + a.width && a.y < b.y + b.height && b.y < a.y + a.height;
}

function contains(outer: Box, inner: Box): boolean {
  return (
    outer.x <= inner.x &&
    outer.y <= inner.y &&
    outer.x + outer.width >= inner.x + inner.width &&
    outer.y + outer.height >= inner.y + inner.height
  );
}

/** One line of text trimmed to what is drawn in it; anything else as it is. */
function trimmed(element: Box, pixels: Pixels): Box {
  if (element.height > pixels.width * LINE_SHARE) return element;
  const columns = inkColumns(pixels, element);
  if (!columns) return element;
  return { x: columns[0], y: element.y, width: columns[1] + 1 - columns[0], height: element.height };
}

/**
 * The ring round an element: its bounds and `RING_PADDING_SHARE` on every side, kept
 * between the status bar and the navigation bar and on the screen.
 *
 * An element that reaches a screen edge or runs under a bar, a map drawn edge to edge,
 * is ringed that padding inside the edge instead, so the whole ring shows: one on the
 * edge itself would be drawn half under the bezel and lose its corners to its curve.
 */
function ring(element: Box, image: { width: number; height: number }): Box {
  const pad = image.width * RING_PADDING_SHARE;
  const top = STATUS_BAR;
  const bottom = image.height - NAVIGATION_BAR;
  const right = element.x + element.width;
  const foot = element.y + element.height;

  const x1 = element.x <= 0 ? pad : Math.max(0, element.x - pad);
  const x2 = right >= image.width ? image.width - pad : Math.min(image.width, right + pad);
  const y1 = element.y <= top ? top + pad : Math.max(top, element.y - pad);
  const y2 = foot >= bottom ? bottom - pad : Math.min(bottom, foot + pad);
  return { x: x1, y: y1, width: x2 - x1, height: y2 - y1 };
}

/** Points from `from` to `to`, `step` apart and centred on the span; its middle if it is shorter than a step. */
function spread(from: number, to: number, step: number): number[] {
  if (to <= from) return [(from + to) / 2];
  const count = Math.floor((to - from) / step) + 1;
  const start = from + (to - from - (count - 1) * step) / 2;
  return Array.from({ length: count }, (_, index) => start + index * step);
}

function distance(x: number, y: number, box: Box): number {
  const dx = Math.max(box.x - x, 0, x - (box.x + box.width));
  const dy = Math.max(box.y - y, 0, y - (box.y + box.height));
  return Math.hypot(dx, dy);
}

/**
 * The centre of each badge, in the still's pixels.
 *
 * A badge on top of its element hides the very thing it points at, and one beside it
 * may hide the heading, the name or the label next to it, which no testID marks. So
 * the spots round each ring are looked at in the picture, and a badge goes on the
 * nearest one whose disc is clear (`CLEAR_INK`): a margin, an empty stretch of card,
 * streets on a map.
 *
 * The spots are the ring's outline pushed out by a badge's radius and a gap, every
 * half radius along it, and a badge's width or so past its ends above and below, so a
 * badge may stand over the empty end of a row when the row's own stretch is all words.
 * Between spots equally near, the order is: level with the middle, left and then
 * right; above and then below, from the left. A ring as big as a map also has spots
 * inside it, tried after every spot round it: a clear patch of map is as good as a
 * margin when there is no margin. A spot first has to be clear by a gap all round the
 * badge; on a crowded screen, clear under the badge alone, closer in. Where nothing is
 * clear, the least drawn-on spot is taken.
 *
 * Every spot must also stay on the screen between the bars, clear of the picture's
 * rounded corners (the manual's phone clips anything past them), clear of the badges
 * already placed and clear of every other ring, unless that ring holds this one: the
 * badge of a button in a marked bar may sit in the bar.
 */
function placeBadges(
  rings: Box[],
  elements: Box[],
  others: Box[],
  image: { width: number; height: number },
  pixels: Pixels,
): { x: number; y: number }[] {
  const size = image.width * BADGE_SHARE;
  const r = size / 2;
  const gap = size * 0.15;
  const step = r / 2;
  const placed: Box[] = [];
  const corner = image.width * CORNER_SHARE;

  // Inside the picture's rounded rectangle: within the edges by the badge's radius, and
  // within the corner's curve by the same where it is near one; and between the bars.
  const onScreen = (x: number, y: number) => {
    const inEdges = x >= r && y >= STATUS_BAR + r && x <= image.width - r && y <= image.height - NAVIGATION_BAR - r;
    const nearestX = Math.min(Math.max(x, corner), image.width - corner);
    const nearestY = Math.min(Math.max(y, corner), image.height - corner);
    return inEdges && Math.hypot(x - nearestX, y - nearestY) <= corner - r;
  };

  return rings.map((e, index) => {
    const cy = e.y + e.height / 2;

    // The spots round the ring with their centres `offset` out from it.
    const around = (offset: number) => {
      const left = e.x - offset;
      const right = e.x + e.width + offset;
      const top = e.y - offset;
      const bottom = e.y + e.height + offset;
      const lengthwise = spread(e.x + r, e.x + e.width - r, step);
      const beyond = spread(left - size, right + size, step).filter((x) => x < e.x || x > e.x + e.width);
      return [
        { x: left, y: cy },
        { x: right, y: cy },
        ...lengthwise.map((x) => ({ x, y: top })),
        ...lengthwise.map((x) => ({ x, y: bottom })),
        ...spread(e.y, e.y + e.height, step).flatMap((y) => [
          { x: left, y },
          { x: right, y },
        ]),
        ...beyond.flatMap((x) => [
          { x, y: top },
          { x, y: bottom },
        ]),
      ].map((spot) => ({ ...spot, near: Math.round(distance(spot.x, spot.y, e) / step) }));
    };
    const off = gap + r;
    const inside =
      e.width >= size * 3 && e.height >= size * 2
        ? spread(e.y + off, e.y + e.height - off, step).flatMap((y) =>
            spread(e.x + off, e.x + e.width - off, step).map((x) => ({ x, y, near: Infinity })),
          )
        : [];

    // Every other ring and every other element the sidecar has, except the ones this
    // element stands in: the sheet it is on, the map under everything.
    const element = elements[index];
    const obstacles = [
      ...rings.filter((other, at) => at !== index && !contains(other, e)),
      ...others.filter((other) => !contains(other, element)),
    ];
    const allowed = (spots: { x: number; y: number; near: number }[]) =>
      spots.filter(({ x, y }) => {
        const badge = { x: x - r, y: y - r, width: size, height: size };
        const spaced = { x: badge.x - gap, y: badge.y - gap, width: size + 2 * gap, height: size + 2 * gap };
        return onScreen(x, y) && !obstacles.some((other) => overlaps(badge, other)) && !placed.some((other) => overlaps(spaced, other));
      });

    // First a spot with a gap's margin of clear ground round the badge, a gap off the
    // ring. Then, on a crowded screen, one that is clear only under the badge itself,
    // which may also stand closer, touching the ring or over its dashed edge.
    const tiers = [
      { spots: allowed([...around(off), ...inside]), margin: gap },
      { spots: allowed([...around(off), ...around(r), ...around(r * 0.75), ...inside]), margin: 0 },
    ];
    let centre: { x: number; y: number } | undefined;
    let least: { x: number; y: number; ink: number } | undefined;
    for (const { spots, margin } of tiers) {
      const scored = spots.map((spot, order) => ({ ...spot, order, ink: inkIn(pixels, spot.x, spot.y, r + margin) }));
      centre = scored.filter(({ ink }) => ink <= CLEAR_INK).sort((a, b) => a.near - b.near || a.order - b.order)[0];
      if (centre) break;
      least = [...scored].sort((a, b) => a.ink - b.ink || a.order - b.order)[0] ?? least;
    }
    centre ??= least ?? {
      x: Math.min(Math.max(e.x + r * 0.2, r), image.width - r),
      y: Math.min(Math.max(e.y + r * 0.2, STATUS_BAR + r), image.height - NAVIGATION_BAR - r),
    };
    placed.push({ x: centre.x - r, y: centre.y - r, width: size, height: size });
    return { x: centre.x, y: centre.y };
  });
}

/**
 * What one callout in the text names, one ring for each:
 *
 * - a testID, `agreed-time`;
 * - a testID ending in `*`, every element whose testID starts with what comes before
 *   it, ringed as one: `timeslot-*` is the whole row of times, however many the
 *   capture's fixture offered that day;
 * - `from..to`, either of those at each end: the box that runs from the top left of
 *   `from` to the bottom right of `to`. The match screens draw their map under the
 *   whole screen and lay the sheet over its lower half, so `live-map` has the screen's
 *   bounds; `live-map..date-map-directions` is the map down to its Reitti button,
 *   which stands on the sheet's edge, and so the map a reader sees.
 */
export const SPAN = '..';
const GROUP = '*';

function partBox(part: string, elements: Record<string, Box>): Box | undefined {
  if (!part.endsWith(GROUP)) return elements[part];
  const prefix = part.slice(0, -GROUP.length);
  const matches = Object.entries(elements)
    .filter(([id]) => id.startsWith(prefix))
    .map(([, box]) => box);
  if (matches.length === 0) return undefined;
  const x = Math.min(...matches.map((box) => box.x));
  const y = Math.min(...matches.map((box) => box.y));
  return {
    x,
    y,
    width: Math.max(...matches.map((box) => box.x + box.width)) - x,
    height: Math.max(...matches.map((box) => box.y + box.height)) - y,
  };
}

function calloutBox(callout: string, elements: Record<string, Box>, where: string, json: string, name: string): Box {
  const parts = callout.split(SPAN);
  if (parts.length > 2 || parts.some((id) => id === '' || id === GROUP || id.slice(0, -1).includes(GROUP))) {
    throw new Error(
      `${where} numbers ${callout} on shot:${name}. A callout is a testID, a testID prefix ending in ${GROUP}, or two of those joined by ${SPAN} (from${SPAN}to).`,
    );
  }
  const boxes = parts.map((part) => partBox(part, elements));
  const missing = parts.find((_, index) => !boxes[index]);
  if (missing) {
    throw new Error(
      `${where} numbers ${callout} on shot:${name}, but ${json} has no bounds for ${missing}. Add it to the still's callouts in docs/manual-shots.md so the next capture records it.`,
    );
  }
  const [from, to] = boxes as Box[];
  if (!to) return from;
  const width = to.x + to.width - from.x;
  const height = to.y + to.height - from.y;
  if (width <= 0 || height <= 0) {
    throw new Error(`${where} numbers ${callout} on shot:${name}, but in ${json} ${parts[1]} does not end below and right of where ${parts[0]} starts.`);
  }
  return { x: from.x, y: from.y, width, height };
}

/** Whether a callout is one testID as it stands, the only kind trimmed to its ink. */
function single(callout: string): boolean {
  return !callout.includes(SPAN) && !callout.endsWith(GROUP);
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

  const pixels = readPixels(png);
  if (pixels.width !== image.width || pixels.height !== image.height) {
    throw new Error(`${png} decodes as ${pixels.width} x ${pixels.height}, and Astro reads it as ${image.width} x ${image.height}.`);
  }
  const boxes = testIDs.map((callout) => calloutBox(callout, sidecar.elements, where, json, name));
  const elements = boxes.map((box, index) => ring(single(testIDs[index]) ? trimmed(box, pixels) : box, image));
  const parts = testIDs.flatMap((callout) => callout.split(SPAN));
  const isMarked = (id: string) => parts.some((part) => (part.endsWith(GROUP) ? id.startsWith(part.slice(0, -GROUP.length)) : id === part));
  const others = Object.entries(sidecar.elements)
    .filter(([id]) => !isMarked(id))
    .map(([, box]) => trimmed(box, pixels));
  const badges = placeBadges(elements, boxes, others, image, pixels);

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
