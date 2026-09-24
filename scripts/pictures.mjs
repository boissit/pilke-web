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
 *
 * The manual's stills are counted too, by the same reading of the build. They are told
 * apart from the marketing screenshots by the `data-still="fi/kalenteri"` that
 * `Phone.astro` puts on them — both sets have a `treffit`, and a file stem alone would
 * count one as the other — and a draft's missing still by the `data-still-missing` on
 * the box drawn in its place. What each still shows is described in
 * `docs/manual-shots.md`, not here, so that is the table a drawn still is checked
 * against.
 *
 * Then, as a warning and never a failure, it says which manual stills may be stale: any
 * whose sidecar's `commit` is older than a change under `pilke-app/src`. That is a
 * question about another repository on this machine, so it is best-effort — skipped
 * without a word when `../pilke-app` is not there — and kept out of `docs/pictures.md`,
 * where it would make `--check` answer differently on every machine.
 */
import { execFileSync } from 'node:child_process';
import { existsSync, readFileSync, writeFileSync, readdirSync } from 'node:fs';
import { join, relative } from 'node:path';

const ROOT = new URL('..', import.meta.url).pathname;
const DIST = join(ROOT, 'dist');
const DOC = join(ROOT, 'docs/pictures.md');
const SCREENS = join(ROOT, 'src/assets/screens');
const MANUAL = join(ROOT, 'src/assets/manual');
const MANUAL_DOC = join(ROOT, 'docs/manual-shots.md');
const APP = join(ROOT, '../pilke-app');
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
      const still = /data-still="([^"]+)"/.exec(tag);
      return {
        stem: still ? still[1] : stem(src[1]),
        still: Boolean(still),
        width: width ? Number(width[1]) : null,
      };
    });
    const missing = [...html.matchAll(/data-still-missing="([^"]+)"/g)].map((m) => m[1]);
    return { route: route(f), pictures, missing };
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
const drawn = new Set(pages.flatMap((p) => p.pictures.filter((i) => !i.still).map((i) => i.stem)));
const unused = carried.filter((c) => !drawn.has(c));

// The manual's stills, as `fi/kalenteri`. The directory does not exist until the first
// capture, and that is not an error.
const manualCarried = existsSync(MANUAL)
  ? readdirSync(MANUAL, { withFileTypes: true })
      .filter((e) => e.isDirectory())
      .flatMap((e) =>
        readdirSync(join(MANUAL, e.name))
          .filter((f) => f.endsWith('.png'))
          .map((f) => `${e.name}/${f.replace(/\.png$/, '')}`),
      )
      .sort()
  : [];
const stillsDrawn = new Set(pages.flatMap((p) => p.pictures.filter((i) => i.still).map((i) => i.stem)));
const stillsUnused = manualCarried.filter((c) => !stillsDrawn.has(c));
const stillsMissing = [...new Set(pages.flatMap((p) => p.missing))].sort();

const rows = [];
rows.push('| Page | Pictures, in the order they appear |');
rows.push('| --- | --- |');
for (const p of pages) {
  const list = [
    ...p.pictures.map((i) => `\`${i.stem}\` ${i.width}px`),
    ...p.missing.map((m) => `\`${m}\` missing`),
  ].join('<br>');
  rows.push(`| \`${p.route}\` | ${list || 'none'} |`);
}
rows.push('');
rows.push(
  unused.length
    ? `Carried but drawn on no page: ${unused.map((u) => `\`${u}\``).join(', ')}.`
    : 'Every screenshot in `src/assets/screens` is drawn on at least one page.',
);
if (manualCarried.length || stillsMissing.length) {
  rows.push('');
  rows.push(
    stillsUnused.length
      ? `Manual stills carried but drawn on no page: ${stillsUnused.map((u) => `\`${u}\``).join(', ')}.`
      : 'Every still in `src/assets/manual` is drawn on at least one page.',
  );
}
if (stillsMissing.length) {
  rows.push('');
  rows.push(
    `Drawn as "screenshot missing" on a draft, not captured yet: ${stillsMissing.map((m) => `\`${m}\``).join(', ')}.`,
  );
}

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

// A manual still is described in the contract's table instead, once for both languages.
const manualDoc = existsSync(MANUAL_DOC) ? readFileSync(MANUAL_DOC, 'utf8') : '';
const contracted = new Set([...manualDoc.matchAll(/^\| ([a-z0-9-]+) \|/gm)].map((m) => m[1]));
const uncontracted = [...stillsDrawn, ...stillsMissing]
  .filter((s) => !contracted.has(s.split('/').pop()))
  .sort();

const check = process.argv.includes('--check');
let bad = false;

if (missing.length) {
  console.error(
    `Not described in docs/pictures.md: ${missing.join(', ')}.\n` +
      'Add a row saying which app screen it is and what it shows that can go stale.',
  );
  bad = true;
}

if (uncontracted.length) {
  console.error(
    `Manual stills not in docs/manual-shots.md: ${uncontracted.join(', ')}.\n` +
      'Add a row naming the screen and its state, so the capture pipeline takes it.',
  );
  bad = true;
}

/**
 * Which stills may no longer match the app: for each sidecar, the files under
 * `pilke-app/src` that differ between the commit it was captured at and pilke-app's
 * HEAD. A `-dirty` commit is compared from its clean half, which may flag a still that
 * already shows the change; "possibly" is the honest word for what this knows.
 */
function staleness() {
  if (!manualCarried.length || !existsSync(join(APP, '.git'))) return;

  const git = (...args) => execFileSync('git', ['-C', APP, ...args], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] });
  const changedSince = new Map();
  const stale = [];

  for (const still of manualCarried) {
    let commit;
    try {
      commit = JSON.parse(readFileSync(join(MANUAL, `${still}.json`), 'utf8')).commit;
    } catch {
      continue; // No sidecar, or not one: the build is where that fails, loudly.
    }
    if (typeof commit !== 'string' || !commit) continue;
    const sha = commit.replace(/-dirty$/, '');

    if (!changedSince.has(sha)) {
      try {
        changedSince.set(sha, git('diff', '--name-only', sha, 'HEAD', '--', 'src').split('\n').filter(Boolean));
      } catch {
        changedSince.set(sha, null); // A commit pilke-app does not have: unknown, so said.
      }
    }
    const changed = changedSince.get(sha);
    if (changed === null) stale.push({ still, why: `captured at ${commit}, which pilke-app does not have` });
    else if (changed.length) stale.push({ still, why: `${changed.length} file(s) under src changed since ${commit.slice(0, 12)}` });
  }

  if (stale.length) {
    console.warn(`\nManual stills possibly stale against pilke-app (a warning, not a failure):`);
    for (const s of stale) console.warn(`  ${s.still.padEnd(36)} ${s.why}`);
  }
}

try {
  staleness();
} catch {
  // Best-effort by design: no git, an odd checkout, anything — the inventory stands.
}

if (check) {
  if (next !== doc) {
    console.error(
      'docs/pictures.md is out of date with the build. Run `npm run pictures` and commit it.',
    );
    bad = true;
  }
  if (!bad)
    console.log(
      `docs/pictures.md matches the build: ${pages.length} pages, ${drawn.size} pictures, ${stillsDrawn.size} manual stills.`,
    );
} else {
  writeFileSync(DOC, next);
  console.log(
    `docs/pictures.md written: ${pages.length} pages, ${drawn.size} pictures and ${stillsDrawn.size} manual stills drawn.`,
  );
  for (const p of pages) {
    console.log(`  ${p.route}`);
    for (const i of p.pictures) console.log(`     ${String(i.width).padStart(4)}px  ${i.stem}`);
    for (const m of p.missing) console.log(`  missing  ${m}`);
  }
  if (unused.length) console.log(`  carried but drawn nowhere: ${unused.join(', ')}`);
  if (stillsUnused.length) console.log(`  manual stills drawn nowhere: ${stillsUnused.join(', ')}`);
}

process.exit(bad ? 1 : 0);
