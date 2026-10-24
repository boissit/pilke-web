/**
 * The site's copy as the copy desk sees it: every text, where in which file it is
 * written, its stable key and its hash. `export.mjs` reads it to make the snapshot and
 * `apply.mjs` to find what a rewrite replaces, so the two can never disagree about
 * what a key points at. `docs/copy-desk.md` is the account of both.
 *
 * Two kinds of source, and nothing else holds a string a reader sees:
 *
 * - `src/content/copy/*.yaml`, keyed. A key is the dotted name a page asks for,
 *   `hero.title`, and is the same in both languages.
 * - The guide and the legal documents, Markdown, one file per language. A key is the
 *   file, the nearest heading's anchor and the block's place under that heading:
 *   `manual/kipinat.fi#yläraja.p2` is the second paragraph under *Yläraja*. An edit in
 *   another section leaves it alone, and a renamed heading renames what is under it,
 *   which `apply` then reports as stale rather than writing to the wrong paragraph.
 *
 * The hash is of the text as the source holds it, `{{tokens}}` and inline Markdown
 * included, with a Markdown block's line breaks read as the spaces they render as.
 */
import { createHash } from 'node:crypto';
import { readdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

import GithubSlugger from 'github-slugger';
import { isMap, isScalar, parseDocument } from 'yaml';

export const ROOT = new URL('../..', import.meta.url).pathname.replace(/\/$/, '');
export const SITE = 'https://pilke.app';
export const LANGS = ['fi', 'en'];

const COPY_DIR = 'src/content/copy';
const MARKDOWN = { manual: 'src/content/manual', legal: 'src/content/legal' };

export const SHY = '\u00ad';

export function hashText(text) {
  return createHash('sha256').update(text.normalize('NFC')).digest('hex').slice(0, 12);
}

// ─── Tokens ─────────────────────────────────────────────────────────────────

let constants;

/** `src/data/app-constants.json`, flattened to `{ 'petals.set_cost': '5', … }`. */
export function appConstants() {
  if (constants) return constants;
  const tree = JSON.parse(readFileSync(join(ROOT, 'src/data/app-constants.json'), 'utf8'));
  constants = {};
  const walk = (value, path) => {
    if (value !== null && typeof value === 'object') {
      for (const [key, inner] of Object.entries(value)) walk(inner, path ? `${path}.${key}` : key);
    } else {
      constants[path] = String(value);
    }
  };
  walk(tree, '');
  return constants;
}

export const TOKEN = /\{\{\s*([^{}]*?)\s*\}\}/g;

export function resolveTokens(text) {
  const values = appConstants();
  return text.replace(TOKEN, (whole, path) => values[path] ?? whole);
}

/** Inline Markdown as the plain words a reader sees, for anchors and text fragments. */
export function plainText(markdown) {
  return resolveTokens(markdown)
    .replace(/!\[([^\]]*)\]\([^)]*\)/g, '$1')
    .replace(/\[([^\]]*)\]\([^)]*\)/g, '$1')
    .replace(/(\*\*|__)(.+?)\1/g, '$2')
    .replace(/(\*|_)(.+?)\1/g, '$2')
    .replace(/`([^`]*)`/g, '$1')
    .replace(/&shy;/g, SHY)
    .replace(/\\([\\`*_{}[\]()#+\-.!|])/g, '$1')
    .trim();
}

// ─── YAML ───────────────────────────────────────────────────────────────────

const RULE = /^#\s*─{6,}/;

/**
 * Every entry of every copy file: its two scalars with their place in the file, the
 * banner it sits under and the comment written above it.
 */
export function readYamlCopy() {
  const entries = new Map();

  for (const name of readdirSync(join(ROOT, COPY_DIR)).filter((f) => f.endsWith('.yaml')).sort()) {
    const file = `${COPY_DIR}/${name}`;
    const raw = readFileSync(join(ROOT, file), 'utf8');
    const document = parseDocument(raw);
    if (document.errors.length) throw new Error(`${file}: ${document.errors[0].message}`);

    // The banners and the comments are read off the lines, since they are the file's
    // layout rather than its data: a banner is the title line after a rule of `─`.
    const sections = new Map();
    const notes = new Map();
    const lines = raw.split('\n');
    let section = '';
    for (let i = 0; i < lines.length; i++) {
      if (RULE.test(lines[i]) && i + 1 < lines.length && !RULE.test(lines[i + 1])) {
        const title = lines[i + 1].replace(/^#\s?/, '').trim();
        if (title) section = title;
        while (i + 1 < lines.length && !RULE.test(lines[i + 1])) i++;
        i++;
        continue;
      }
      const key = /^'([^']+)':\s*$/.exec(lines[i])?.[1];
      if (!key) continue;
      sections.set(key, section);
      const above = [];
      for (let j = i - 1; j >= 0 && lines[j].startsWith('#') && !RULE.test(lines[j]); j--) {
        above.unshift(lines[j].replace(/^#\s?/, ''));
      }
      if (above.length) notes.set(key, above.join('\n').trim());
    }

    if (!isMap(document.contents)) continue;
    document.contents.items.forEach((pair, order) => {
      const key = String(pair.key.value);
      const value = {};
      for (const lang of LANGS) {
        const node = pair.value?.get?.(lang, true);
        if (!isScalar(node) || typeof node.value !== 'string') {
          throw new Error(`${file} (${key}) has no ${lang} string.`);
        }
        value[lang] = { text: node.value, start: node.range[0], end: node.range[1], style: node.type };
      }
      entries.set(key, {
        key,
        file,
        order,
        section: sections.get(key) ?? '',
        note: notes.get(key) ?? '',
        ...value,
      });
    });
  }

  return entries;
}

// ─── Markdown ───────────────────────────────────────────────────────────────

const HEADING = /^(#{1,6})[ \t]+(.*?)[ \t#]*$/;
const ITEM = /^([-*+]|\d{1,9}[.)])([ \t]+)(.*)$/;
const SHOT = /^!\[([^\]]*)\]\((shot:[^)]*)\)\s*$/;
const TABLE = /^\s*\|/;
const DIVIDER = /^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?\s*$/;
const BREAK = /^ {0,3}([-*_])( *\1){2,} *$/;

/**
 * One Markdown file as the blocks a reader sees, each with the key `apply` finds it by
 * and the span of the file its text occupies.
 *
 * Paragraphs, headings, list items, table cells, a screenshot's alt text and the
 * frontmatter's title and lead. A block's `spans` are the pieces of the file its text
 * is written in, one per source line, so a hard-wrapped paragraph can be rewritten in
 * place and wrapped to the file's own width again.
 */
export function readMarkdown(collection, slug, lang) {
  const file = `${MARKDOWN[collection]}/${slug}.${lang}.md`;
  const raw = readFileSync(join(ROOT, file), 'utf8');
  const base = `${collection}/${slug}.${lang}`;
  const blocks = [];

  const lineStarts = [0];
  for (let i = 0; i < raw.length; i++) if (raw[i] === '\n') lineStarts.push(i + 1);
  const lines = raw.split('\n');

  // Frontmatter: the title and lead are copy, the rest is data.
  let first = 0;
  if (lines[0] === '---') {
    const close = lines.indexOf('---', 1);
    const fmStart = lineStarts[1];
    const fmText = lines.slice(1, close).join('\n');
    const document = parseDocument(fmText);
    for (const field of ['title', 'lead']) {
      const node = document.contents?.get?.(field, true);
      if (!isScalar(node)) continue;
      blocks.push({
        key: `${base}#${field}`,
        kind: field,
        section: 0,
        local: field,
        text: String(node.value),
        frontmatter: { start: fmStart + node.range[0], end: fmStart + node.range[1], style: node.type },
      });
    }
    first = close + 1;
  }

  const slugger = new GithubSlugger();
  let anchor = 'top';
  let section = 0;
  let counts = {};
  const next = (kind) => (counts[kind] = (counts[kind] ?? 0) + 1);
  const span = (line, from = 0, to = lines[line].length) => ({
    start: lineStarts[line] + from,
    end: lineStarts[line] + to,
    line,
  });
  const trimmed = (line, from) => {
    const text = lines[line];
    let a = from;
    let b = text.length;
    while (a < b && /\s/.test(text[a])) a++;
    while (b > a && /\s/.test(text[b - 1])) b--;
    return span(line, a, b);
  };
  const textOf = (spans) => spans.map((s) => raw.slice(s.start, s.end)).join(' ');
  const isBlank = (line) => lines[line].trim() === '';
  const startsBlock = (line) => {
    const text = lines[line];
    return HEADING.test(text) || ITEM.test(text) || TABLE.test(text) || SHOT.test(text) || BREAK.test(text);
  };
  // What may cut a paragraph short. CommonMark lets an ordered list do it only when it
  // starts at 1, so a wrapped line that happens to begin `18. ` stays in its paragraph.
  const interrupts = (line) => {
    const text = lines[line];
    return HEADING.test(text) || /^[-*+][ \t]+\S/.test(text) || /^1[.)][ \t]+\S/.test(text) || TABLE.test(text) || SHOT.test(text) || BREAK.test(text);
  };

  let i = first;
  let tables = 0;
  while (i < lines.length) {
    const text = lines[i];
    if (isBlank(i) || BREAK.test(text) || text.startsWith('<!--')) {
      i++;
      continue;
    }

    const heading = HEADING.exec(text);
    if (heading) {
      const from = heading[1].length + text.slice(heading[1].length).search(/\S/);
      const spans = [trimmed(i, from)];
      const words = textOf(spans);
      anchor = slugger.slug(plainText(words).replace(new RegExp(SHY, 'g'), ''));
      section++;
      counts = {};
      tables = 0;
      blocks.push({ key: `${base}#${anchor}`, kind: 'heading', level: heading[1].length, section, local: 'h', anchor, spans, text: words });
      i++;
      continue;
    }

    const shot = SHOT.exec(text);
    if (shot) {
      const spans = [span(i, 2, 2 + shot[1].length)];
      const local = `img${next('img')}`;
      blocks.push({ key: `${base}#${anchor}.${local}`, kind: 'alt text', section, local, anchor, spans, text: shot[1], shot: shot[2] });
      i++;
      continue;
    }

    if (TABLE.test(text)) {
      tables++;
      let row = 0;
      while (i < lines.length && TABLE.test(lines[i])) {
        if (!DIVIDER.test(lines[i])) {
          const line = lines[i];
          // Cells between unescaped pipes, the outer two optional.
          const cuts = [];
          for (let c = 0; c < line.length; c++) if (line[c] === '|' && line[c - 1] !== '\\') cuts.push(c);
          const bounds = [];
          let from = line.trimStart().startsWith('|') ? cuts.shift() + 1 : 0;
          for (const cut of cuts) {
            bounds.push([from, cut]);
            from = cut + 1;
          }
          if (line.slice(from).trim()) bounds.push([from, line.length]);
          bounds.forEach(([a, b], column) => {
            while (a < b && /\s/.test(line[a])) a++;
            while (b > a && /\s/.test(line[b - 1])) b--;
            if (a === b) return;
            const cell = span(i, a, b);
            const local = `t${tables}.r${row}.c${column + 1}`;
            blocks.push({
              key: `${base}#${anchor}.${local}`,
              kind: row === 0 ? 'table header' : 'table cell',
              section,
              local,
              anchor,
              spans: [cell],
              text: raw.slice(cell.start, cell.end),
              table: { index: tables, row, column: column + 1 },
            });
          });
          row++;
        }
        i++;
      }
      continue;
    }

    const item = ITEM.exec(text);
    if (item) {
      const markerWidth = item[1].length + item[2].length;
      const spans = [trimmed(i, markerWidth)];
      i++;
      while (i < lines.length && !isBlank(i) && !startsBlock(i)) {
        spans.push(trimmed(i, 0));
        i++;
      }
      const local = `li${next('li')}`;
      blocks.push({ key: `${base}#${anchor}.${local}`, kind: 'list item', section, local, anchor, spans, text: textOf(spans), marker: item[1], indent: markerWidth });
      continue;
    }

    const spans = [trimmed(i, 0)];
    i++;
    while (i < lines.length && !isBlank(i) && !interrupts(i)) {
      spans.push(trimmed(i, 0));
      i++;
    }
    const local = `p${next('p')}`;
    blocks.push({ key: `${base}#${anchor}.${local}`, kind: 'paragraph', section, local, anchor, spans, text: textOf(spans) });
  }

  // The width a hard-wrapped file is wrapped to, for writing a paragraph back into it:
  // where its lines break, read off every line that is not a block's last. The files
  // are wrapped by hand, so it is the 90th percentile rather than the longest.
  const breaks = blocks
    .filter((b) => b.spans?.length > 1)
    .flatMap((b) => b.spans.slice(0, -1).map((s) => lines[s.line].length))
    .sort((a, b) => a - b);
  const width = breaks.length ? breaks[Math.floor(breaks.length * 0.9)] : 0;

  for (const block of blocks) block.hash = hashText(block.text);
  return { collection, slug, lang, file, raw, blocks, width };
}

/** Every Markdown document, as `{ collection, slug }`, from the files on disk. */
export function markdownDocuments() {
  const found = [];
  for (const [collection, dir] of Object.entries(MARKDOWN)) {
    const slugs = new Set(
      readdirSync(join(ROOT, dir))
        .filter((f) => f.endsWith('.md'))
        .map((f) => f.replace(/\.(fi|en)\.md$/, '')),
    );
    for (const slug of [...slugs].sort()) found.push({ collection, slug });
  }
  return found;
}

/**
 * The two languages of one document, block by block: the nth heading with the nth
 * heading, and under it the nth paragraph with the nth paragraph, the nth list item
 * with the nth, each table cell with the cell in the same place. A block with no twin
 * stands alone, in its own language.
 */
export function pairDocument(collection, slug) {
  const docs = Object.fromEntries(LANGS.map((lang) => [lang, readMarkdown(collection, slug, lang)]));
  const place = (b) => `${b.section}|${b.local}`;
  const byPlace = Object.fromEntries(LANGS.map((lang) => [lang, new Map(docs[lang].blocks.map((b) => [place(b), b]))]));
  const pairs = [];
  const seen = new Set();
  for (const lang of LANGS) {
    for (const block of docs[lang].blocks) {
      const at = place(block);
      if (seen.has(at)) continue;
      seen.add(at);
      const pair = Object.fromEntries(LANGS.map((l) => [l, byPlace[l].get(at)]));
      pairs.push({ id: (pair.fi ?? pair.en).key, ...pair, kind: block.kind });
    }
  }
  return { docs, pairs };
}

/** Where a key lives: a YAML entry's file, or a Markdown document and its language. */
export function parseKey(key) {
  const md = /^(manual|legal)\/(.+)\.(fi|en)#(.+)$/.exec(key);
  if (md) return { source: 'markdown', collection: md[1], slug: md[2], lang: md[3], local: md[4] };
  return { source: 'yaml', key };
}

// ─── Live URLs ──────────────────────────────────────────────────────────────

/** A text fragment, `#:~:text=…`, for the first words of `text`, or `''` if none fit. */
export function textFragment(text, words = 6) {
  const out = [];
  for (const word of plainText(text).split(/\s+/)) {
    // Anything the page renders differently from the source stops the fragment there:
    // a soft hyphen, typographer's quotes and dashes, a placeholder cut out of the text.
    if (!word || /[\u00ad"'`{}<>]|--|\.\.\./.test(word)) break;
    out.push(word);
    if (out.length === words) break;
  }
  if (!out.length) return '';
  const encode = (s) => encodeURIComponent(s).replace(/-/g, '%2D');
  return `:~:text=${encode(out.join(' '))}`;
}
