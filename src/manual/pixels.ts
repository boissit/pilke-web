/**
 * A manual still's pixels, read when the page is built, so a marker can be placed by
 * what is drawn on the screen and not only by where its testIDs are.
 *
 * The sidecar's bounds say where each element with a testID sits, and nothing about
 * the text, photos and map labels that have none: a badge placed by bounds alone lands
 * on whatever is beside its element, which is often a heading or a name. So
 * `stills.ts` asks two things of the picture itself: how much of a disc is drawn on
 * (`inkIn`), and how far a line of text really runs inside the row its testID spans
 * (`inkColumns`).
 *
 * The stills are 8-bit RGB PNGs straight off the emulator's `screencap`, which is all
 * this decodes. Read with `node:zlib` rather than an image library, so the build has
 * no dependency for it, and synchronously, so the step that places the markers stays
 * the plain function it is. Anything else throws by name, because a still that cannot
 * be read here cannot have its markers placed.
 */
import { readFileSync } from 'node:fs';
import { inflateSync } from 'node:zlib';

export interface Pixels {
  width: number;
  height: number;
  /** RGB, row after row, three bytes a pixel. */
  data: Uint8Array;
}

/**
 * How far a channel may stray from the ground around it and still be ground.
 *
 * Measured on the stills: the stars printed on a Treffit card differ from its fill by
 * 13, a map's streets from its land by 26, text and icons by a hundred and more. So a
 * badge may cover a card's pattern or the streets of a map, and never a word.
 */
export const INK_TOLERANCE = 48;

const cache = new Map<string, Pixels>();

export function readPixels(path: string): Pixels {
  const known = cache.get(path);
  if (known) return known;

  const file = readFileSync(path);
  const signature = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
  if (!signature.every((byte, index) => file[index] === byte)) {
    throw new Error(`${path} is not a PNG.`);
  }

  let width = 0;
  let height = 0;
  const chunks: Buffer[] = [];
  for (let at = 8; at < file.length; ) {
    const length = file.readUInt32BE(at);
    const type = file.toString('latin1', at + 4, at + 8);
    const body = file.subarray(at + 8, at + 8 + length);
    if (type === 'IHDR') {
      width = body.readUInt32BE(0);
      height = body.readUInt32BE(4);
      const [depth, colour, , , interlace] = body.subarray(8, 13);
      if (depth !== 8 || colour !== 2 || interlace !== 0) {
        throw new Error(
          `${path} is a PNG of bit depth ${depth}, colour type ${colour}, interlace ${interlace}. The manual reads 8-bit RGB without interlace, which is what the capture writes.`,
        );
      }
    } else if (type === 'IDAT') {
      chunks.push(body);
    } else if (type === 'IEND') {
      break;
    }
    at += 12 + length;
  }

  const raw = inflateSync(Buffer.concat(chunks));
  const stride = width * 3;
  const data = new Uint8Array(stride * height);

  // The five PNG row filters, undone in place, each against the row above it.
  for (let row = 0; row < height; row++) {
    const filter = raw[row * (stride + 1)];
    const source = row * (stride + 1) + 1;
    const out = row * stride;
    for (let i = 0; i < stride; i++) {
      const value = raw[source + i];
      const left = i >= 3 ? data[out + i - 3] : 0;
      const up = row > 0 ? data[out - stride + i] : 0;
      const upLeft = row > 0 && i >= 3 ? data[out - stride + i - 3] : 0;
      let predicted = 0;
      if (filter === 1) predicted = left;
      else if (filter === 2) predicted = up;
      else if (filter === 3) predicted = (left + up) >> 1;
      else if (filter === 4) {
        const p = left + up - upLeft;
        const pa = Math.abs(p - left);
        const pb = Math.abs(p - up);
        const pc = Math.abs(p - upLeft);
        predicted = pa <= pb && pa <= pc ? left : pb <= pc ? up : upLeft;
      } else if (filter !== 0) {
        throw new Error(`${path} has a row with PNG filter ${filter}, which does not exist.`);
      }
      data[out + i] = (value + predicted) & 0xff;
    }
  }

  const pixels = { width, height, data };
  cache.set(path, pixels);
  return pixels;
}

function at(pixels: Pixels, x: number, y: number): [number, number, number] {
  const i = (Math.round(y) * pixels.width + Math.round(x)) * 3;
  return [pixels.data[i], pixels.data[i + 1], pixels.data[i + 2]];
}

function near(a: [number, number, number], b: [number, number, number]): boolean {
  return Math.abs(a[0] - b[0]) <= INK_TOLERANCE && Math.abs(a[1] - b[1]) <= INK_TOLERANCE && Math.abs(a[2] - b[2]) <= INK_TOLERANCE;
}

/** The commonest colour among `samples`, to a sixteenth of each channel. */
function ground(samples: [number, number, number][]): [number, number, number] {
  const counts = new Map<number, { n: number; colour: [number, number, number] }>();
  for (const colour of samples) {
    const key = ((colour[0] >> 4) << 8) | ((colour[1] >> 4) << 4) | (colour[2] >> 4);
    const entry = counts.get(key);
    if (entry) entry.n++;
    else counts.set(key, { n: 1, colour });
  }
  let best = { n: 0, colour: [0, 0, 0] as [number, number, number] };
  for (const entry of counts.values()) if (entry.n > best.n) best = entry;
  return best.colour;
}

/**
 * The share of a disc that is drawn on: pixels that differ from the disc's own
 * commonest colour by more than `INK_TOLERANCE`. 0 is a clear patch of card or map,
 * and a word anywhere under it shows as a few hundredths at least.
 */
export function inkIn(pixels: Pixels, cx: number, cy: number, radius: number): number {
  const samples: [number, number, number][] = [];
  const step = 2;
  for (let y = cy - radius; y <= cy + radius; y += step) {
    for (let x = cx - radius; x <= cx + radius; x += step) {
      if (x < 0 || y < 0 || x >= pixels.width || y >= pixels.height) continue;
      if ((x - cx) ** 2 + (y - cy) ** 2 > radius ** 2) continue;
      samples.push(at(pixels, x, y));
    }
  }
  if (samples.length === 0) return 1;
  const colour = ground(samples);
  return samples.filter((sample) => !near(sample, colour)).length / samples.length;
}

/**
 * The columns of a box that something is drawn in, against the ground just outside
 * it: `[first, last]` in the still's pixels, or `undefined` when the box holds nothing
 * but ground. What `stills.ts` trims a line of text to.
 */
export function inkColumns(pixels: Pixels, box: { x: number; y: number; width: number; height: number }): [number, number] | undefined {
  const x1 = Math.max(0, Math.round(box.x));
  const x2 = Math.min(pixels.width - 1, Math.round(box.x + box.width) - 1);
  const y1 = Math.max(0, Math.round(box.y));
  const y2 = Math.min(pixels.height - 1, Math.round(box.y + box.height) - 1);

  const outside: [number, number, number][] = [];
  for (let x = x1; x <= x2; x++) {
    if (y1 > 0) outside.push(at(pixels, x, y1 - 1));
    if (y2 < pixels.height - 1) outside.push(at(pixels, x, y2 + 1));
  }
  for (let y = y1; y <= y2; y++) {
    if (x1 > 0) outside.push(at(pixels, x1 - 1, y));
    if (x2 < pixels.width - 1) outside.push(at(pixels, x2 + 1, y));
  }
  if (outside.length === 0) return undefined;
  const colour = ground(outside);

  const drawn = (x: number) => {
    for (let y = y1; y <= y2; y++) if (!near(at(pixels, x, y), colour)) return true;
    return false;
  };
  let first = x1;
  while (first <= x2 && !drawn(first)) first++;
  if (first > x2) return undefined;
  let last = x2;
  while (last > first && !drawn(last)) last--;
  return [first, last];
}
