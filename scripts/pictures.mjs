/**
 * The inventory of which picture is drawn on which page, taken from the built site.
 *
 * `npm run pictures` rewrites the generated table in `docs/pictures.md`; `npm run
 * pictures -- --check` fails instead of writing, which is what to run before shipping.
 *
 * WARNING: **It reads `dist/`, not `src/`.** A picture reaches a page through an import,
 * a shots table and a component prop, and following that chain by hand is how a page gets
 * missed. What the build emitted is the only account of it that cannot be wrong.
 *
 * It answers two questions the tables in that document cannot answer on their own: is
 * every picture the build draws written down, and does every picture written down still
 * appear. Either one failing is a document that has drifted from the site.
 */
import { readFileSync, writeFileSync, readdirSync } from 'node:fs';
import { join, relative } from 'node:path';

const ROOT = new URL('..', import.meta.url).pathname;
const DIST = join(ROOT, 'dist');
const DOC = join(ROOT, 'docs/pictures.md');
const SCREENS = join(ROOT, 'src/assets/screens');
const START = '<!-- inventory:start -->';
const END = '<!-- inventory:end -->';

function walk(dir) {
  return readdirSync(dir, { withFileTypes: true }).flatMap((e) =>
    e.isDirectory() ? walk(join(dir, e.name)) : [join(dir, e.name)],
  );
}

/** `/_astro/treffit.BHfrQq4m_Z1fLjvO.webp` is `treffit`: Astro keeps the source stem. */
function stem(src) {
  return src.split('/').pop().split('.')[0];
}

function route(file) {
  const r = relative(DIST, file).replace(/index\.html$/, '');
  return '/' + r.replace(/\/$/, '') + (r === '' ? '' : '/');
}

const pages = walk(DIST)
  .filter((f) => f.endsWith('.html'))
  .sort()
  .map((f) => {
    const html = readFileSync(f, 'utf8');
    const pictures = [...html.matchAll(/<img[^>]*>/g)].map((m) => {
      const tag = m[0];
      const src = /src="([^"]+)"/.exec(tag);
      const width = /width="(\d+)"/.exec(tag);
      return { stem: stem(src[1]), width: width ? Number(width[1]) : null };
    });
    return { route: route(f), pictures };
  });

if (pages.length === 0) {
  console.error('No pages in dist/. Run `npm run build` first: this reads the build.');
  process.exit(1);
}

// Every screenshot the repository carries, so one drawn nowhere is visible rather than
// merely absent. A picture can only be missed if nothing ever lists it.
const carried = readdirSync(SCREENS)
  .filter((f) => /\.(png|webp|jpg)$/.test(f))
  .map((f) => f.replace(/\.\w+$/, ''))
  .sort();
const drawn = new Set(pages.flatMap((p) => p.pictures.map((i) => i.stem)));
const unused = carried.filter((c) => !drawn.has(c));

const rows = [];
rows.push('| Page | Pictures, in the order they appear |');
rows.push('| --- | --- |');
for (const p of pages) {
  const list = p.pictures.map((i) => `\`${i.stem}\` ${i.width}px`).join('<br>');
  rows.push(`| \`${p.route}\` | ${list || 'none'} |`);
}
rows.push('');
rows.push(
  unused.length
    ? `Carried but drawn on no page: ${unused.map((u) => `\`${u}\``).join(', ')}.`
    : 'Every screenshot in `src/assets/screens` is drawn on at least one page.',
);

const table = [START, '', ...rows, '', END].join('\n');
const doc = readFileSync(DOC, 'utf8');
const from = doc.indexOf(START);
const to = doc.indexOf(END);
if (from === -1 || to === -1) {
  console.error(`docs/pictures.md has no ${START} / ${END} markers to write between.`);
  process.exit(1);
}
const next = doc.slice(0, from) + table + doc.slice(to + END.length);

// Every picture the build draws needs a row in the hand-kept table, which is where what
// each one shows is recorded. A picture with no row is one nobody has said anything about.
const described = new Set(
  [...doc.matchAll(/^\| `([a-z0-9-]+)` \|/gm)].map((m) => m[1]),
);
const missing = [...drawn].filter((d) => !described.has(d)).sort();

const check = process.argv.includes('--check');
let bad = false;

if (missing.length) {
  console.error(
    `Not described in docs/pictures.md: ${missing.join(', ')}.\n` +
      'Add a row saying which app screen it is and what it shows that can go stale.',
  );
  bad = true;
}

if (check) {
  if (next !== doc) {
    console.error(
      'docs/pictures.md is out of date with the build. Run `npm run pictures` and commit it.',
    );
    bad = true;
  }
  if (!bad) console.log(`docs/pictures.md matches the build: ${pages.length} pages, ${drawn.size} pictures.`);
} else {
  writeFileSync(DOC, next);
  console.log(`docs/pictures.md written: ${pages.length} pages, ${drawn.size} pictures drawn.`);
  for (const p of pages) {
    console.log(`  ${p.route}`);
    for (const i of p.pictures) console.log(`     ${String(i.width).padStart(4)}px  ${i.stem}`);
  }
  if (unused.length) console.log(`  carried but drawn nowhere: ${unused.join(', ')}`);
}

process.exit(bad ? 1 : 0);
