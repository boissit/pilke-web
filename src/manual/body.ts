/**
 * A manual page's Markdown, turned into the runs of prose and the steps the page draws.
 *
 * Two things in the text are not Markdown. `{{area.name}}` is a figure from the app's
 * constants, and a paragraph that is nothing but `![alt](shot:name#id1,id2)` is a step:
 * a screenshot in a phone with numbered markers, and the text that follows it set
 * beside it.
 *
 * WARNING: **This runs when the page is built, not when the collection is loaded, and
 * that is the reason it is not a Markdown plugin.** The content layer renders an entry
 * once and caches the HTML against a digest of the file's own text, so a still captured
 * or a constant changed after the page was written would never reach it until somebody
 * edited the Markdown. And it logs a plugin that throws rather than failing the build,
 * which would turn every check in `stills.ts` into a line in a log. Here the stills and
 * the constants are read on every build, and an error is the build's error.
 *
 * The Markdown itself goes through the same Sätteri processor Astro renders `legal`
 * with, so smart quotes, dashes and heading ids come out the same on both.
 */
import { createSatteriMarkdownProcessor } from '@astrojs/markdown-satteri';

import type { Lang } from '../i18n/ui';
import { resolveTokens } from './constants';
import { resolveStill, type Still } from './stills';

export type ManualBlock = { kind: 'prose'; html: string } | { kind: 'step'; still: Still; html: string };

/**
 * A shot on a line of its own. It has to start the line: indented, it would belong to a
 * list item or a quote, and a phone drawn inside a bullet is not a layout this has.
 */
const SHOT_LINE = /^!\[([^\]]*)\]\(shot:([^)#\s]*)(?:#([^)\s]*))?\)\s*$/;

/** Any `shot:` image at all, to catch one that is not on a paragraph of its own. */
const SHOT_ANYWHERE = /!\[[^\]]*\]\(shot:/;

const FENCE = /^ {0,3}(`{3,}|~{3,})/;
const HEADING = /^ {0,3}#{1,6}(\s|$)/;
const BREAK = /^ {0,3}([-*_])( *\1){2,} *$/;

/** Stand-ins the text is cut at once it is HTML. Comments, so they survive the render. */
const stepStart = (index: number) => `<!--manual-step:${index}-->`;
const STEP_END = '<!--manual-step-end-->';
const SENTINEL = /<!--manual-step:(\d+)-->|<!--manual-step-end-->/;

let renderer: Awaited<ReturnType<typeof createSatteriMarkdownProcessor>> | undefined;

/**
 * Highlighting off: a manual has no code in it, and loading Shiki for every page to
 * colour none is the one difference from the site's configured processor.
 */
async function markdown() {
  renderer ??= await createSatteriMarkdownProcessor({ syntaxHighlight: false });
  return renderer;
}

/**
 * Mark where each step starts and ends, and pull out what each shot asked for.
 *
 * A step is the shot and every block after it up to the next shot, the next heading or
 * a thematic break. Text before a page's first shot, and text after a heading until the
 * next shot, stays a run of full-width prose — an introduction to a section is not a
 * caption for its first picture.
 */
function markSteps(body: string, where: string) {
  const lines = body.split('\n');
  const out: string[] = [];
  const shots: { alt: string; name: string; testIDs: string[] }[] = [];

  let fence: string | undefined;
  let open = false;

  const close = () => {
    if (open) out.push('', STEP_END, '');
    open = false;
  };

  lines.forEach((line, index) => {
    const opener = FENCE.exec(line)?.[1];
    if (fence) {
      if (opener && opener[0] === fence[0] && opener.length >= fence.length) fence = undefined;
      out.push(line);
      return;
    }
    if (opener) {
      fence = opener;
      out.push(line);
      return;
    }

    const shot = SHOT_LINE.exec(line);
    const alone = (lines[index - 1] ?? '').trim() === '' && (lines[index + 1] ?? '').trim() === '';

    if (shot && alone) {
      close();
      const [, alt, name, ids] = shot;
      const testIDs = ids === undefined ? [] : ids.split(',').map((id) => id.trim());
      if (testIDs.some((id) => id === '')) {
        throw new Error(`${where} has an empty testID in ${line.trim()}. List them as shot:${name}#first,second.`);
      }
      out.push(stepStart(shots.length));
      shots.push({ alt, name, testIDs });
      open = true;
      return;
    }

    if (SHOT_ANYWHERE.test(line)) {
      throw new Error(
        `${where} has a shot: image that is not a paragraph of its own: "${line.trim()}". Put it on its own line, at the start, with a blank line above and below.`,
      );
    }

    if (HEADING.test(line) || (BREAK.test(line) && (lines[index - 1] ?? '').trim() === '')) close();
    out.push(line);
  });

  close();
  return { marked: out.join('\n'), shots };
}

/**
 * `(1)`, `(2)` in a step's text, drawn as the same badge the marker on the phone is, so
 * the two read as one reference. Only numbers the step has a marker for: a `(3)` on a
 * step with two markers is left as the text it is. Tags are skipped, and so is anything
 * inside `<code>`.
 */
function badgeReferences(html: string, count: number): string {
  if (count === 0) return html;
  let inCode = 0;
  return html
    .split(/(<[^>]+>)/)
    .map((part) => {
      if (part.startsWith('<')) {
        if (/^<code[\s>]/.test(part)) inCode++;
        if (part === '</code>') inCode = Math.max(0, inCode - 1);
        return part;
      }
      if (inCode) return part;
      return part.replace(/\((\d+)\)/g, (whole, n: string) =>
        Number(n) >= 1 && Number(n) <= count ? `<span class="callout-ref">${n}</span>` : whole,
      );
    })
    .join('');
}

/**
 * The page as blocks, in order. `where` is the Markdown file, for errors; `draft` is its
 * own flag, which is what lets a still be missing.
 */
export async function renderManualBody(body: string, lang: Lang, draft: boolean, where: string): Promise<ManualBlock[]> {
  const { marked, shots } = markSteps(resolveTokens(body, where), where);
  const stills = shots.map((shot) => resolveStill(shot, lang, draft, where));

  const rendered = await (await markdown()).render(marked, {});

  // An ordinary relative image would be collected for Astro's pipeline and then never
  // replaced, because nothing here runs the step that replaces it: it would ship as an
  // `<img>` with no `src`. Screenshots are `shot:` and nothing else is a picture here.
  if (rendered.metadata.localImagePaths.length) {
    throw new Error(
      `${where} has an image that is not a shot: ${rendered.metadata.localImagePaths.join(', ')}. The manual draws screenshots only, as ![alt](shot:name).`,
    );
  }

  const blocks: ManualBlock[] = [];
  const parts = rendered.code.split(SENTINEL);

  // `split` with a capturing group interleaves text and captures: text, index-or-undefined,
  // text, … An index opens a step; `undefined` is the end marker, which closes one.
  let step: Still | undefined;
  for (let i = 0; i < parts.length; i += 2) {
    const html = parts[i].trim();
    if (step) {
      blocks.push({ kind: 'step', still: step, html: badgeReferences(html, step.markers.length) });
    } else if (html) {
      blocks.push({ kind: 'prose', html });
    }

    if (i + 1 < parts.length) {
      const captured = parts[i + 1];
      step = captured === undefined ? undefined : stills[Number(captured)];
    }
  }

  return blocks;
}
