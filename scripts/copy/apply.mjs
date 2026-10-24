/**
 * `npm run copy:apply -- <file.json> [--dry-run] [--report <out.json>]`: write the
 * owner's rewrites into the files they came from. `docs/copy-desk.md` is the runbook.
 *
 * The file is a list of `{ key, lang, base_hash, new_text }`, or `{ items: [...] }`;
 * anything else on an item, such as the desk's own `id`, is carried through to the
 * report untouched. `base_hash` is the hash the snapshot gave the text the rewrite was
 * written against.
 *
 * WARNING: **A rewrite of a text that has changed since is refused, never merged.** If
 * the source no longer hashes to `base_hash`, or the key no longer exists because the
 * heading above it was renamed, the item is reported `stale` with what the text is
 * now, and the file is left alone. The owner rewrote a sentence; writing it over a
 * different sentence is how a correction somebody else made gets lost.
 *
 * Only the text itself is replaced: a YAML scalar between its quotes, a Markdown
 * block's words. Comments, the other language, key order and every other byte stay as
 * they are, and a hard-wrapped paragraph is wrapped again to its file's width. Each
 * file is read back after it is written, and put back as it was if the text did not
 * come out as asked.
 *
 * Exit status 0 when every item was applied or already said that, 2 when any was
 * stale or refused, 1 when the input could not be read.
 */
import { readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

import { appConstants, hashText, LANGS, parseKey, readMarkdown, readYamlCopy, ROOT, SHY, TOKEN } from './sources.mjs';

const args = process.argv.slice(2);
const flag = (name) => args.includes(name);
const option = (name) => (args.includes(name) ? args[args.indexOf(name) + 1] : undefined);
const input = args.find((a, i) => !a.startsWith('--') && args[i - 1] !== '--report');
const dryRun = flag('--dry-run');
const reportPath = option('--report');

if (!input) {
  console.error('Usage: npm run copy:apply -- <file.json> [--dry-run] [--report <out.json>]');
  process.exit(1);
}

let items;
try {
  const parsed = JSON.parse(readFileSync(input, 'utf8'));
  items = Array.isArray(parsed) ? parsed : parsed.items;
  if (!Array.isArray(items)) throw new Error('expected a list, or { items: [...] }');
} catch (error) {
  console.error(`${input}: ${error.message}`);
  process.exit(1);
}

const yaml = readYamlCopy();
const markdown = new Map();
const docFor = (collection, slug, lang) => {
  const id = `${collection}/${slug}.${lang}`;
  if (!markdown.has(id)) markdown.set(id, readMarkdown(collection, slug, lang));
  return markdown.get(id);
};

const report = { applied: [], unchanged: [], stale: [], refused: [] };
const edits = new Map();

// ─── Writing a text back ────────────────────────────────────────────────────

/** A YAML scalar for `text`, in the quoting the old one had where it can keep it. */
function yamlScalar(text, style, old) {
  const invisible = /[\u0000-\u001f\u007f-\u009f\u00ad\u200b-\u200f\u2028\u2029\ufeff]/;
  if (style === 'QUOTE_DOUBLE' || invisible.test(text)) {
    const upper = /\\u00AD/.test(old);
    const escaped = [...text]
      .map((c) => {
        if (c === '\\') return '\\\\';
        if (c === '"') return '\\"';
        if (invisible.test(c)) {
          const hex = c.codePointAt(0).toString(16).padStart(4, '0');
          return `\\u${upper ? hex.toUpperCase() : hex}`;
        }
        return c;
      })
      .join('');
    return `"${escaped}"`;
  }
  const plainSafe =
    style === 'PLAIN' &&
    /^[^\s\-?:,[\]{}#&*!|>'"%@`]/.test(text) &&
    !/: | #|:$|\s$/.test(text) &&
    !/^(true|false|null|yes|no|on|off|~|[-+]?(\d[\d_]*)?\.?\d+([eE][-+]?\d+)?|\d{4}-\d\d-\d\d.*)$/i.test(text);
  return plainSafe ? text : `'${text.replace(/'/g, "''")}'`;
}

/** A line that would start a different block if a wrap put this word first on it. */
const LEADS_BLOCK = /^([-*+>|]|#{1,6}$|\d{1,9}[.)]$)/;

/** `text` as lines no wider than `width`, the first after `first` columns and the rest indented. */
function wrap(text, width, first, indent) {
  const words = text.split(' ');
  const lines = [];
  let line = '';
  let room = width - first;
  for (const word of words) {
    if (line && line.length + 1 + word.length > room && !LEADS_BLOCK.test(word)) {
      lines.push(line);
      line = word;
      room = width - indent;
    } else {
      line = line ? `${line} ${word}` : word;
    }
  }
  if (line) lines.push(line);
  return lines.join(`\n${' '.repeat(indent)}`);
}

function refuse(item, reason, detail) {
  report.refused.push({ ...item, reason, detail });
}

function edit(file, start, end, replacement, item, after) {
  if (!edits.has(file)) edits.set(file, []);
  edits.get(file).push({ start, end, replacement, item, after });
}

const placeholders = (text) => [...new Set(text.match(/\{(?!\{)[a-z]+\}(?!\})/g) ?? [])].sort().join(' ');

/** What is wrong with a rewrite whatever its source: an unknown figure, or nothing at all. */
function commonProblem(text) {
  if (!text.trim()) return ['empty', 'The new text is empty.'];
  const values = appConstants();
  for (const [, path] of text.matchAll(TOKEN)) {
    if (!(path in values)) return ['unknown_token', `{{${path}}} is not in src/data/app-constants.json.`];
  }
  return undefined;
}

// ─── Each item ──────────────────────────────────────────────────────────────

for (const item of items) {
  const { key, lang, base_hash: baseHash } = item;
  if (typeof key !== 'string' || !LANGS.includes(lang) || typeof baseHash !== 'string' || typeof item.new_text !== 'string') {
    refuse(item, 'malformed', 'An item needs key, lang (fi or en), base_hash and new_text.');
    continue;
  }
  const where = parseKey(key);
  let text = item.new_text.replace(/\r\n?/g, '\n').normalize('NFC').trim();

  if (where.source === 'yaml') {
    const entry = yaml.get(key);
    if (!entry) {
      report.stale.push({ ...item, reason: 'unknown_key', detail: `No file in src/content/copy/ holds "${key}" now.` });
      continue;
    }
    const current = entry[lang];
    text = text.replace(/&shy;/g, SHY).replace(/\s*\n\s*/g, ' ');
    if (hashText(current.text) !== baseHash) {
      report.stale.push({ ...item, reason: 'changed', current_text: current.text, current_hash: hashText(current.text), file: entry.file });
      continue;
    }
    if (text === current.text) {
      report.unchanged.push({ ...item, file: entry.file });
      continue;
    }
    const problem = commonProblem(text);
    if (problem) {
      refuse(item, ...problem);
      continue;
    }
    if (placeholders(text) !== placeholders(current.text)) {
      refuse(item, 'placeholder', `The text must keep ${placeholders(current.text) || 'no placeholder'} exactly: the page cuts it there. It has ${placeholders(text) || 'none'}.`);
      continue;
    }
    if (/\*\*|__|\]\(|`/.test(text)) {
      refuse(item, 'markdown_in_plain_text', 'This text is drawn as it is written, so bold and links would show as asterisks and brackets.');
      continue;
    }
    const raw = readFileSync(join(ROOT, entry.file), 'utf8');
    edit(entry.file, current.start, current.end, yamlScalar(text, current.style, raw.slice(current.start, current.end)), item, () =>
      readYamlCopy().get(key)?.[lang].text === text,
    );
    continue;
  }

  if (where.lang !== lang) {
    refuse(item, 'malformed', `${key} is the ${where.lang} text, and the item says ${lang}.`);
    continue;
  }
  let doc;
  try {
    doc = docFor(where.collection, where.slug, lang);
  } catch {
    report.stale.push({ ...item, reason: 'unknown_key', detail: `There is no ${where.collection}/${where.slug}.${lang}.md now.` });
    continue;
  }
  const block = doc.blocks.find((b) => b.key === key);
  if (!block) {
    report.stale.push({ ...item, reason: 'unknown_key', detail: `${doc.file} has no ${key} now: the heading above it may have been renamed.` });
    continue;
  }
  if (block.hash !== baseHash) {
    report.stale.push({ ...item, reason: 'changed', current_text: block.text, current_hash: block.hash, file: doc.file });
    continue;
  }

  if (block.frontmatter) {
    text = text.replace(/&shy;/g, SHY).replace(/\s*\n\s*/g, ' ');
  } else {
    text = text.replace(new RegExp(SHY, 'g'), '&shy;');
  }
  const paragraphs = block.kind === 'paragraph' ? text.split(/\n\s*\n/).map((p) => p.replace(/\s*\n\s*/g, ' ').trim()).filter(Boolean) : [text.replace(/\s*\n\s*/g, ' ')];
  text = paragraphs.join('\n\n');

  if (text === block.text) {
    report.unchanged.push({ ...item, file: doc.file });
    continue;
  }
  const problem = commonProblem(text);
  if (problem) {
    refuse(item, ...problem);
    continue;
  }
  if (/\]\(shot:/.test(text)) {
    refuse(item, 'shot', 'A screenshot is placed by the guide’s own syntax and cannot be added from the desk.');
    continue;
  }
  if (block.kind === 'alt text' && /[[\]]/.test(text)) {
    refuse(item, 'alt_brackets', 'Alt text cannot hold [ or ].');
    continue;
  }
  if (block.kind !== 'heading' && /^(#{1,6}\s|[-*+]\s|\d{1,9}[.)]\s|>|\|)/m.test(paragraphs.join('\n'))) {
    refuse(item, 'block_syntax', 'The text starts like a heading, a list or a table, which would change what kind of block it is.');
    continue;
  }

  if (block.frontmatter) {
    const { start, end, style } = block.frontmatter;
    const raw = readFileSync(join(ROOT, doc.file), 'utf8');
    edit(doc.file, start, end, yamlScalar(text, style, raw.slice(start, end)), item, () =>
      readMarkdown(where.collection, where.slug, lang).blocks.find((b) => b.key === key)?.text === text,
    );
    continue;
  }

  const first = block.spans[0];
  const last = block.spans[block.spans.length - 1];
  const lineStart = doc.raw.lastIndexOf('\n', first.start - 1) + 1;
  const firstColumn = first.start - lineStart;
  let replacement;
  if (block.kind === 'table header' || block.kind === 'table cell') {
    replacement = text.replace(/(?<!\\)\|/g, '\\|');
  } else if (doc.width && block.kind !== 'heading' && block.kind !== 'alt text') {
    const second = block.spans[1];
    const indent = second ? second.start - (doc.raw.lastIndexOf('\n', second.start - 1) + 1) : block.kind === 'list item' ? firstColumn : 0;
    replacement = paragraphs.map((p, n) => wrap(p, doc.width, n === 0 ? firstColumn : indent, indent)).join(`\n\n${' '.repeat(indent)}`);
  } else {
    replacement = text;
  }
  const expected = block.kind === 'table header' || block.kind === 'table cell' ? replacement : text;
  edit(doc.file, first.start, last.end, replacement, item, () => {
    const fresh = readMarkdown(where.collection, where.slug, lang).blocks;
    return fresh.some((b) => b.kind === block.kind && b.text === expected) || paragraphs.length > 1;
  });
}

// ─── Writing the files ──────────────────────────────────────────────────────

for (const [file, list] of edits) {
  list.sort((a, b) => b.start - a.start);
  for (let i = 1; i < list.length; i++) {
    if (list[i].end > list[i - 1].start) {
      for (const e of list) refuse(e.item, 'overlap', `Two rewrites in ${file} cover the same text.`);
      edits.delete(file);
      break;
    }
  }
}

for (const [file, list] of edits) {
  const path = join(ROOT, file);
  const original = readFileSync(path, 'utf8');
  let next = original;
  for (const e of list) next = next.slice(0, e.start) + e.replacement + next.slice(e.end);

  if (dryRun) {
    for (const e of list) report.applied.push({ ...e.item, file, dry_run: true, written: e.replacement });
    continue;
  }

  writeFileSync(path, next);
  // Read back through the same parser the site uses for the file: if any text did not
  // come out as asked, nothing in this file is kept.
  let failed;
  try {
    failed = list.find((e) => !e.after());
  } catch (error) {
    failed = { item: list[0].item, error };
  }
  if (failed) {
    writeFileSync(path, original);
    for (const e of list) refuse(e.item, 'write_failed', `${file} did not read back as written${failed.error ? `: ${failed.error.message}` : ''}, so it was left as it was.`);
    continue;
  }
  for (const e of list) report.applied.push({ ...e.item, file });
}

// ─── The report ─────────────────────────────────────────────────────────────

const line = (i) => `  ${i.key} (${i.lang})${i.file ? ` in ${i.file}` : ''}`;
if (report.applied.length) console.log(`${dryRun ? 'Would apply' : 'Applied'} ${report.applied.length}:\n${report.applied.map(line).join('\n')}`);
if (report.unchanged.length) console.log(`Already the text asked for, ${report.unchanged.length}:\n${report.unchanged.map(line).join('\n')}`);
if (report.stale.length) {
  console.log(`Stale, left alone, ${report.stale.length}:`);
  for (const i of report.stale) console.log(`${line(i)}: ${i.detail ?? `the text is now "${i.current_text}"`}`);
}
if (report.refused.length) {
  console.log(`Refused, ${report.refused.length}:`);
  for (const i of report.refused) console.log(`${line(i)}: ${i.reason}. ${i.detail}`);
}
if (reportPath) writeFileSync(reportPath, `${JSON.stringify(report, null, 2)}\n`);

process.exit(report.stale.length || report.refused.length ? 2 : 0);
