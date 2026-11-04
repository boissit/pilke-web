/**
 * `npm run copy:export [-- --out <file>]`: every text on the site as one JSON
 * snapshot, for the copy desk. `docs/copy-desk.md` describes the file and the desk.
 *
 * WARNING: **What is drawn where is read off a build, not off the templates.** The
 * export builds the site once more into a scratch folder with `COPY_TRACE=1`, which
 * makes `traced()` in `src/i18n/ui.ts` wrap every string with its key, and then walks
 * the pages: which keys each draws, in what order, in which element and under which
 * heading. A text no build draws — the waitlist's closed note while the form is open —
 * is still exported, on the page its YAML file is for, marked `conditional`. The
 * Markdown bodies are not traced; they are read from their files block by block and
 * set where the page draws its `.manual` or `.legal` body.
 *
 * The snapshot is written to `.copy-desk/snapshot.json` unless `--out` says otherwise,
 * and is not committed: it is a picture of one commit, and the desk carries its own.
 */
import { execFileSync } from 'node:child_process';
import { mkdirSync, mkdtempSync, readdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join, relative, resolve } from 'node:path';

import {
  appConstants,
  hashText,
  LANGS,
  markdownDocuments,
  pairDocument,
  plainText,
  readYamlCopy,
  resolveTokens,
  ROOT,
  SITE,
  textFragment,
  TOKEN,
} from './sources.mjs';

const args = process.argv.slice(2);
const out = resolve(ROOT, args.includes('--out') ? args[args.indexOf('--out') + 1] : '.copy-desk/snapshot.json');

// ─── Reading the pages ──────────────────────────────────────────────────────

const OPEN = '\uE000';
const MID = '\uE001';
const CLOSE = '\uE002';
const VOID = new Set(['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr']);
const ATTRS = ['alt', 'aria-label', 'placeholder', 'title', 'content', 'value'];

function decode(text) {
  return text
    .replace(/&#x([0-9a-f]+);/gi, (_, h) => String.fromCodePoint(parseInt(h, 16)))
    .replace(/&#(\d+);/g, (_, d) => String.fromCodePoint(Number(d)))
    .replace(/&quot;/g, '"')
    .replace(/&#39;|&apos;/g, "'")
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&nbsp;/g, '\u00a0')
    .replace(/&shy;/g, '\u00ad')
    .replace(/&amp;/g, '&');
}

/** `/ohje/kipinat` for `ohje/kipinat.html`, `/` for `index.html`, `/en` for `en.html`. */
function routeOf(file) {
  const path = file.replace(/\.html$/, '').replace(/(^|\/)index$/, '');
  return `/${path}`;
}

/**
 * Every traced string on every page, in document order, with what it is drawn in.
 *
 * Astro's output is regular enough for a tag-and-text scanner: the elements are
 * balanced, `<script>` and `<style>` are read as raw text, and the markers are
 * private-use characters no page writes for itself.
 */
function walkBuild(dir) {
  const files = [];
  const walk = (d) => {
    for (const e of readdirSync(d, { withFileTypes: true })) {
      if (e.isDirectory()) walk(join(d, e.name));
      else if (e.name.endsWith('.html')) files.push(join(d, e.name));
    }
  };
  walk(dir);

  const pages = new Map();
  for (const path of files.sort()) {
    const html = readFileSync(path, 'utf8');
    // The old manual address is a redirect page, and draws nothing of its own.
    if (/<meta http-equiv="refresh"/i.test(html)) continue;
    pages.set(routeOf(relative(dir, path)), scan(html));
  }
  return pages;
}

function scan(html) {
  const found = [];
  const stack = [];
  const open = [];
  let lastId = '';
  let heading = '';
  let headingBuffer = null;
  let headingDepth = 0;

  const context = () => {
    const tags = stack.map((e) => e.tag);
    const region = stack.some((e) => e.tag === 'head')
      ? 'meta'
      : stack.some((e) => e.tag === 'header' || (e.tag === 'a' && e.classes.includes('skip')))
        ? 'header'
        : stack.some((e) => e.tag === 'footer')
          ? 'footer'
          : stack.some((e) => e.id === 'beta')
            ? 'beta'
            : 'main';
    const ancestorId = [...stack].reverse().find((e) => e.id && e.id !== 'main')?.id ?? '';
    return { stack: stack.map((e) => ({ tag: e.tag, classes: e.classes, id: e.id, attrs: e.attrs })), tags, region, anchor: ancestorId || lastId, section: heading };
  };

  const text = (chunk, attr) => {
    for (let i = 0; i < chunk.length; i++) {
      const c = chunk[i];
      if (c === OPEN) {
        const mid = chunk.indexOf(MID, i);
        const [lang, key] = chunk.slice(i + 1, mid).split(/:(.*)/s);
        // Listed where it opens, so a link inside a sentence comes after the sentence.
        const occurrence = { lang, key, attr, ctx: context(), text: '' };
        found.push(occurrence);
        open.push(occurrence);
        i = mid;
      } else if (c === CLOSE) {
        open.pop();
      } else {
        for (const o of open) o.text += c;
        if (headingBuffer !== null && !attr) headingBuffer += c;
      }
    }
  };

  const TAG = /<!--[\s\S]*?-->|<(\/?)([a-zA-Z][\w-]*)((?:\s+[^\s=>/]+(?:\s*=\s*(?:"[^"]*"|'[^']*'|[^\s>]+))?)*)\s*(\/?)>/g;
  let at = 0;
  let match;
  while ((match = TAG.exec(html))) {
    if (match.index > at) text(decode(html.slice(at, match.index)));
    at = TAG.lastIndex;
    if (match[0].startsWith('<!--')) continue;
    const [, closing, rawTag, rawAttrs, selfClosing] = match;
    const tag = rawTag.toLowerCase();

    if (closing) {
      const index = stack.map((e) => e.tag).lastIndexOf(tag);
      if (index >= 0) stack.length = index;
      if (/^h[1-3]$/.test(tag) && headingBuffer !== null && stack.length < headingDepth) {
        heading = headingBuffer.replace(/\s+/g, ' ').trim();
        headingBuffer = null;
      }
      continue;
    }

    const attrs = {};
    for (const a of rawAttrs.matchAll(/([^\s=>/]+)(?:\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+)))?/g)) {
      attrs[a[1].toLowerCase()] = decode(a[2] ?? a[3] ?? a[4] ?? '');
    }
    const element = { tag, id: attrs.id ?? '', classes: (attrs.class ?? '').split(/\s+/).filter(Boolean), attrs };

    if (['section', 'header', 'footer', 'main', 'head'].includes(tag)) lastId = '';
    if (element.id && element.id !== 'main') lastId = element.id;

    stack.push(element);
    if (/^h[1-3]$/.test(tag) && !stack.some((e) => e.tag === 'head')) {
      headingBuffer = '';
      headingDepth = stack.length;
    }
    for (const name of ATTRS) {
      if (attrs[name]?.includes(OPEN)) text(attrs[name], name);
    }
    // The Markdown body of a guide or legal page: its blocks go here, read from the file.
    if (tag === 'div' && (element.classes.includes('manual') || element.classes.includes('legal'))) {
      found.push({ body: true, ctx: context() });
    }

    if (tag === 'script' || tag === 'style') {
      const end = html.indexOf(`</${tag}`, at);
      if (tag === 'script') text(html.slice(at, end));
      at = end;
      continue;
    }
    if (VOID.has(tag) || selfClosing) stack.pop();
  }
  return found;
}

// ─── What each text is ──────────────────────────────────────────────────────

/** The kind of text an occurrence is, from the element it is drawn in. */
function kindOf(o) {
  const { stack } = o.ctx;
  const top = stack[stack.length - 1] ?? { tag: '' };
  const meta = top.tag === 'meta' ? top.attrs?.name ?? top.attrs?.property : '';
  if (o.attr === 'content') {
    return meta === 'description' ? 'meta description' : meta === 'og:title' ? 'social title' : meta === 'og:description' ? 'social description' : 'meta';
  }
  if (o.attr === 'alt') return 'alt text';
  if (o.attr === 'aria-label') return top.attrs?.role === 'img' ? 'alt text' : 'screen-reader label';
  if (o.attr === 'placeholder') return 'placeholder';
  if (o.attr) return o.attr;
  if (top.tag === 'title') return 'meta title';
  if (top.tag === 'script') return 'message';
  for (const e of [...stack].reverse()) {
    if (e.classes.includes('visually-hidden')) return 'screen-reader text';
    if (e.tag === 'del') return 'struck';
    if (/^h[1-6]$/.test(e.tag)) return 'heading';
    if (e.tag === 'button') return 'button';
    if (e.tag === 'a') return e.classes.includes('go') ? 'button' : 'link';
    if (e.tag === 'label') return 'label';
    if (e.tag === 'strong' || e.tag === 'b') return e.tag === 'b' ? 'amount' : 'subheading';
    if (e.classes.includes('tag')) return 'tag';
    if (e.tag === 'dt') return 'question';
    if (e.tag === 'dd') return 'answer';
    if (e.tag === 'li') return 'list item';
    if (e.tag === 'p' || e.tag === 'figure') return 'paragraph';
  }
  return 'text';
}

function levelOf(o) {
  const h = [...o.ctx.stack].reverse().find((e) => /^h[1-6]$/.test(e.tag));
  return h ? Number(h.tag[1]) : undefined;
}

// ─── The traced build ───────────────────────────────────────────────────────

const traceDir = mkdtempSync(join(tmpdir(), 'pilke-copy-trace-'));
let occurrences;
try {
  execFileSync(join(ROOT, 'node_modules/.bin/astro'), ['build', '--outDir', traceDir], {
    cwd: ROOT,
    env: { ...process.env, COPY_TRACE: '1' },
    stdio: ['ignore', 'ignore', 'inherit'],
  });
  occurrences = walkBuild(traceDir);
} finally {
  rmSync(traceDir, { recursive: true, force: true });
}

// ─── The pages the desk lists ───────────────────────────────────────────────

const yaml = readYamlCopy();
const markdown = markdownDocuments().map(({ collection, slug }) => ({ collection, slug, ...pairDocument(collection, slug) }));

/** A Markdown key in either language, to the id of the text it is one language of. */
const textIdOf = new Map();
for (const doc of markdown) for (const pair of doc.pairs) for (const lang of LANGS) if (pair[lang]) textIdOf.set(pair[lang].key, pair.id);

const idOf = (key) => textIdOf.get(key) ?? key;

/** The English route of a Finnish one: `/en` in front, and the guide's segment translated. */
function enRoute(fi) {
  if (fi === '/') return '/en';
  if (fi === '/404') return '/404';
  return `/en${fi.replace(/^\/ohje(?=\/|$)/, '/guide')}`;
}

const t = (key, lang) => resolveTokens(yaml.get(key)[lang].text);
const both = (key) => ({ fi: t(key, 'fi'), en: t(key, 'en') });

const guide = markdown.filter((d) => d.collection === 'manual');
const legalDocs = ['tietosuoja', 'kayttoehdot', 'lapsiturvallisuus'];
const order = (d) => Number(/^order:\s*(\d+)/m.exec(d.docs.fi.raw)?.[1] ?? 0);
guide.sort((a, b) => order(a) - order(b) || a.slug.localeCompare(b.slug));
const mdTitle = (collection, slug) => {
  const doc = markdown.find((d) => d.collection === collection && d.slug === slug);
  return Object.fromEntries(LANGS.map((lang) => [lang, plainText(doc.docs[lang].blocks.find((b) => b.kind === 'title').text)]));
};

/*
  The desk's list, in the site's own order: the pages the header carries, the guide
  page by page, the legal pages, and then contact, the waitlist, the header and
  footer, the meta texts and the 404. A page's label is the one the site's own
  navigation gives it.
*/
const PAGES = [
  { id: 'etusivu', group: 'pages', route: '/', label: { fi: 'Etusivu', en: 'Front page' } },
  { id: 'nain-se-toimii', group: 'pages', route: '/nain-se-toimii', label: both('nav.how') },
  { id: 'turvallisuus', group: 'pages', route: '/turvallisuus', label: both('nav.safety') },
  { id: 'kysyttya', group: 'pages', route: '/kysyttya', label: both('nav.questions') },
  // The one page with a title and description of its own, so its head is read too.
  { id: 'meista', group: 'pages', route: '/meista', region: ['main', 'meta'], label: both('nav.about') },
  { id: 'ohje', group: 'guide', route: '/ohje', label: both('manual.title') },
  ...guide.map((d) => ({ id: `ohje/${d.slug}`, group: 'guide', route: `/ohje/${d.slug}`, label: mdTitle('manual', d.slug), body: d })),
  ...legalDocs.map((slug) => ({
    id: slug,
    group: 'legal',
    route: `/${slug}`,
    label: mdTitle('legal', slug),
    body: markdown.find((d) => d.collection === 'legal' && d.slug === slug),
  })),
  { id: 'tietojen-poisto', group: 'legal', route: '/tietojen-poisto', label: both('legal.deletion.nav') },
  { id: 'yhteystiedot', group: 'more', route: '/yhteystiedot', label: both('contact.nav') },
  { id: 'betajono', group: 'more', route: '/', region: 'beta', label: { fi: 'Betajono', en: 'Waitlist' } },
  { id: 'sivusto', group: 'more', route: '/', region: ['header', 'footer'], label: { fi: 'Yläpalkki ja alatunniste', en: 'Header and footer' } },
  { id: 'meta', group: 'more', route: '/', region: 'meta', label: { fi: 'Metatekstit', en: 'Meta texts' } },
  { id: '404', group: 'more', route: '/404', label: { fi: 'Sivua ei löydy (404)', en: 'Page not found (404)' } },
];

/** The page a YAML file's texts belong to, for a text no build draws. */
const HOME = {
  'etusivu.yaml': 'etusivu',
  'nain-se-toimii.yaml': 'nain-se-toimii',
  'turvallisuus.yaml': 'turvallisuus',
  'kysyttya.yaml': 'kysyttya',
  'meista.yaml': 'meista',
  'ohje.yaml': 'ohje',
  'legal.yaml': 'tietosuoja',
  'tietojen-poisto.yaml': 'tietojen-poisto',
  'yhteystiedot.yaml': 'yhteystiedot',
  'waitlist.yaml': 'betajono',
  'site.yaml': 'sivusto',
  'screenshots.yaml': 'etusivu',
};

const texts = new Map();
const warnings = [];

function urlFor(route, lang, o, rendered, kind) {
  const path = lang === 'fi' ? route : enRoute(route);
  const base = `${SITE}${path === '/' ? '/' : path}`;
  const own = o?.ctx.stack[o.ctx.stack.length - 1]?.id;
  if (own) return `${base}#${own}`;
  const visible = !['alt text', 'meta title', 'meta description', 'social title', 'social description', 'screen-reader label', 'screen-reader text', 'placeholder', 'message'].includes(kind);
  const fragment = visible ? textFragment(rendered) : '';
  if (fragment) return `${base}#${fragment}`;
  return o?.ctx.anchor ? `${base}#${o.ctx.anchor}` : base;
}

function yamlText(key) {
  if (texts.has(key)) return texts.get(key);
  const entry = yaml.get(key);
  if (!entry) throw new Error(`The build draws "${key}", which no YAML file holds.`);
  const record = {
    id: key,
    source: 'yaml',
    file: entry.file,
    section: entry.section,
    note: entry.note,
    format: 'plain',
    placeholders: [...new Set(entry.fi.text.match(/\{(?!\{)[a-z]+\}(?!\})/g) ?? [])],
    kind: undefined,
    pages: [],
    drawn: 0,
  };
  for (const lang of LANGS) {
    const text = entry[lang].text;
    record[lang] = { key, text, rendered: resolveTokens(text), hash: hashText(text), url: '' };
  }
  texts.set(key, record);
  return record;
}

function markdownText(pair, doc) {
  if (texts.has(pair.id)) return texts.get(pair.id);
  const first = pair.fi ?? pair.en;
  const record = {
    id: pair.id,
    source: 'markdown',
    file: Object.fromEntries(LANGS.filter((l) => pair[l]).map((l) => [l, doc.docs[l].file])),
    section: '',
    note: '',
    format: first.kind === 'title' || first.kind === 'lead' ? 'plain' : 'markdown',
    placeholders: [],
    kind: first.kind,
    level: first.level,
    table: first.table,
    shot: first.shot,
    pages: [],
    drawn: 0,
  };
  for (const lang of LANGS) {
    const block = pair[lang];
    if (!block) continue;
    record[lang] = { key: block.key, text: block.text, rendered: plainText(block.text), hash: block.hash, url: '' };
  }
  texts.set(pair.id, record);
  return record;
}

function headingOf(doc, lang, section) {
  const h = doc.docs[lang].blocks.find((b) => b.kind === 'heading' && b.section === section);
  return h ? plainText(h.text) : '';
}

const pairById = new Map();
for (const doc of markdown) for (const pair of doc.pairs) pairById.set(pair.id, { pair, doc });

const pages = [];
for (const page of PAGES) {
  const traced = occurrences.get(page.route);
  if (!traced) throw new Error(`The build has no page at ${page.route}.`);
  const tracedEn = occurrences.get(enRoute(page.route)) ?? [];
  const regions = [page.region ?? 'main'].flat();
  const items = [];
  const seen = new Set();

  // A text is listed once per page, except a struck step, which the line repeats.
  const add = (id, kind, extra = {}) => {
    if (seen.has(id) && kind !== 'struck') return;
    seen.add(id);
    items.push({ id, kind, ...extra });
  };

  // Where the same text is drawn on the English page, for its English link.
  const enOccurrence = (id) => tracedEn.find((o) => !o.body && o.lang === 'en' && idOf(o.key) === id);

  for (const o of traced) {
    if (!regions.includes(o.ctx.region)) continue;

    if (o.body) {
      for (const pair of page.body.pairs) {
        if (pair.kind === 'title' || pair.kind === 'lead') continue;
        const record = markdownText(pair, page.body);
        if (!record.pages.includes(page.id)) record.pages.push(page.id);
        record.drawn++;
        record.section = headingOf(page.body, 'fi', (pair.fi ?? pair.en).section);
        for (const lang of LANGS) {
          const block = pair[lang];
          if (!block || record[lang].url) continue;
          const path = `${SITE}${lang === 'fi' ? page.route : enRoute(page.route)}`;
          const fragment = block.kind === 'alt text' ? '' : textFragment(block.text);
          record[lang].url =
            block.kind === 'heading'
              ? `${path}#${block.anchor}`
              : fragment
                ? `${path}#${fragment}`
                : block.anchor !== 'top'
                  ? `${path}#${block.anchor}`
                  : path;
        }
        const block = pair.fi ?? pair.en;
        const url = Object.fromEntries(LANGS.filter((l) => record[l]).map((l) => [l, record[l].url]));
        const shape = block.kind === 'heading' ? { level: block.level } : block.table ? { table: block.table } : block.marker ? { ordered: /\d/.test(block.marker) } : {};
        add(pair.id, pair.kind, { url, ...shape });
      }
      continue;
    }

    const id = idOf(o.key);
    const record = pairById.has(id) ? markdownText(pairById.get(id).pair, pairById.get(id).doc) : yamlText(o.key);
    const kind = kindOf(o);
    record.kind ??= kind;
    if (!record.pages.includes(page.id)) record.pages.push(page.id);
    record.drawn++;
    if (!record.section) record.section = o.ctx.section;

    // A page drawing something other than what the source says is a trace gone wrong.
    const drawn = o.text.replace(/\s+/g, ' ').trim();
    const expected = record[o.lang]?.rendered.replace(/\s+/g, ' ').trim().split('{')[0].trim() ?? '';
    if (o.ctx.region !== 'meta' && !o.ctx.tags.includes('script') && !drawn.startsWith(expected)) {
      warnings.push(`${page.route}: ${o.key} is drawn as "${drawn.slice(0, 60)}"`);
    }

    // Each item links to its own place on the page being read, and the text's own link
    // is the first page that draws it.
    const url = {};
    for (const lang of LANGS) {
      if (!record[lang]) continue;
      const at = lang === 'fi' ? (o.lang === 'fi' ? o : undefined) : enOccurrence(id);
      url[lang] = urlFor(page.route, lang, at, record[lang].rendered, kind);
      if (!record[lang].url) record[lang].url = url[lang];
    }
    add(id, kind, { url, ...(kind === 'heading' ? { level: levelOf(o) } : {}) });
  }

  pages.push({
    id: page.id,
    group: page.group,
    label: page.label,
    url: Object.fromEntries(LANGS.map((lang) => [lang, `${SITE}${lang === 'fi' ? page.route : enRoute(page.route)}`])),
    items,
  });
}

// Every YAML key no build draws, on the page its file is for.
for (const entry of yaml.values()) {
  if (texts.has(entry.key)) continue;
  const record = yamlText(entry.key);
  record.conditional = true;
  record.kind = 'text';
  const home = pages.find((p) => p.id === (HOME[entry.file.split('/').pop()] ?? 'sivusto'));
  record.pages.push(home.id);
  for (const lang of LANGS) record[lang].url = home.url[lang];
  home.items.push({ id: entry.key, kind: 'text', conditional: true, url: home.url });
}

for (const record of texts.values()) {
  for (const lang of LANGS) {
    for (const [, path] of (record[lang]?.text ?? '').matchAll(TOKEN)) {
      if (!(path in appConstants())) warnings.push(`${record[lang].key} uses {{${path}}}, which app-constants.json does not hold.`);
    }
  }
}

// ─── The snapshot ───────────────────────────────────────────────────────────

const git = (...a) => execFileSync('git', a, { cwd: ROOT, encoding: 'utf8' }).trim();
const dirty = git('status', '--porcelain', '--', 'src').length > 0;

const usedTokens = {};
for (const record of texts.values()) {
  for (const lang of LANGS) for (const [, path] of (record[lang]?.text ?? '').matchAll(TOKEN)) usedTokens[path] = appConstants()[path];
}

const snapshot = {
  version: 1,
  generated_at: new Date().toISOString(),
  commit: git('rev-parse', '--short=12', 'HEAD') + (dirty ? '-dirty' : ''),
  site: SITE,
  constants: Object.fromEntries(Object.entries(usedTokens).sort()),
  groups: [
    { id: 'pages', label: { fi: 'Sivut', en: 'Pages' } },
    { id: 'guide', label: { fi: 'Käyttöohje', en: 'Guide' } },
    { id: 'legal', label: { fi: 'Ehdot ja tietosuoja', en: 'Terms and privacy' } },
    { id: 'more', label: { fi: 'Muut', en: 'More' } },
  ],
  pages,
  texts: Object.fromEntries([...texts].map(([id, record]) => [id, Object.fromEntries(Object.entries(record).filter(([, v]) => v !== undefined))])),
};

mkdirSync(dirname(out), { recursive: true });
writeFileSync(out, `${JSON.stringify(snapshot, null, 1)}\n`);

const count = (p) => p.items.length;
console.log(`Wrote ${relative(process.cwd(), out)}: ${texts.size} texts on ${pages.length} pages (${pages.map((p) => `${p.id} ${count(p)}`).join(', ')}).`);
const conditional = [...texts.values()].filter((r) => r.conditional).map((r) => r.id);
if (conditional.length) console.log(`Drawn by no page in this build, so listed on their file's page: ${conditional.join(', ')}.`);
for (const w of warnings) console.warn(`warning: ${w}`);
