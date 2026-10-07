/**
 * `{{area.name}}` in manual text: a number the app actually uses, spelled out on the
 * page from the same source the app reads it from.
 *
 * A manual is full of figures — how many sparks an invitation takes, how long a cooldown lasts,
 * how far ahead the calendar goes — and every one written by hand is one the backend
 * can change without the page noticing. `src/data/app-constants.json` is generated from
 * the backend's own values, so a token here is a figure that moves when they do.
 *
 * WARNING: **An unknown token fails the build, drafts included.** A draft may be missing
 * a picture, because a missing picture is drawn as a box that says so; a missing figure
 * would be drawn as nothing at all, or as the literal braces, and read as a sentence
 * with a hole in it. There is no placeholder for a number that is honest.
 *
 * The file is looked up by glob rather than imported, so its absence is this module's
 * error message rather than Vite's: the site builds without it until a page asks for a
 * value, and the page that asks is named.
 */

const CONSTANTS_PATH = 'src/data/app-constants.json';

const found = import.meta.glob<unknown>('/src/data/app-constants.json', { eager: true, import: 'default' });

const constants = Object.values(found)[0];

/** `{{ … }}`, spaces allowed inside the braces. What is inside is checked, not assumed. */
const TOKEN = /\{\{([^{}]*)\}\}/g;

/** A dotted path of plain keys: `area.name`, `cooldown.hidden-days`, `limits.0`. */
const PATH = /^[A-Za-z0-9_-]+(\.[A-Za-z0-9_-]+)*$/;

function lookup(path: string, where: string): string {
  if (constants === undefined) {
    throw new Error(`${where} uses {{${path}}}, but ${CONSTANTS_PATH} does not exist.`);
  }

  let value: unknown = constants;
  for (const key of path.split('.')) {
    if (value === null || typeof value !== 'object' || !(key in value)) {
      throw new Error(`${where} uses {{${path}}}, which is not in ${CONSTANTS_PATH}.`);
    }
    value = (value as Record<string, unknown>)[key];
  }

  // A token stands for a figure or a word in a sentence. An object here is a path that
  // stopped one key short, and printing it would put `[object Object]` on the page.
  if (typeof value !== 'string' && typeof value !== 'number' && typeof value !== 'boolean') {
    const shape = value === null ? 'null' : Array.isArray(value) ? 'a list' : 'an object';
    throw new Error(
      `${where} uses {{${path}}}, which is ${shape} in ${CONSTANTS_PATH} rather than a value. Name a key inside it.`,
    );
  }

  return String(value);
}

/**
 * `text` with every token replaced by its value. `where` names the file in the error, so
 * the message says which page to fix rather than only which token.
 */
export function resolveTokens(text: string, where: string): string {
  return text.replace(TOKEN, (_, inner: string) => {
    const path = inner.trim();
    if (!PATH.test(path)) {
      throw new Error(`${where} has {{${inner}}}, which is not a token. A token is a dotted path: {{area.name}}.`);
    }
    return lookup(path, where);
  });
}
