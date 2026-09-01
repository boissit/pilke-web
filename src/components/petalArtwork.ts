/**
 * The eight petals as pure geometry: one silhouette each, in the box they share.
 *
 * Ported from `pilke-app/assets/rose/petal-*.svg`, the same artwork the app draws a
 * grant with. The site draws them in one place only — the tiled texture behind its
 * slabs — and it draws them **flat**: the files' stroked interior creases and each
 * shape's own baked rotation are left in the app, because a mark at a tenth of a
 * 300px tile is thirty pixels across, where an outline over three creases reads as
 * grit rather than as a petal, and the tile's own angles are one of the things keeping
 * five marks off a grid.
 *
 * All eight are carried, not only the five the tile names. They are the artwork's set,
 * `PETAL_INK_RADIUS` is measured across all of them, and a placement can be re-pointed
 * at another shape without a trip back to the app.
 */

/**
 * The box every petal was drawn in, `240 × 240`. All eight share it, so they are the
 * same size beside each other with no per-shape fitting.
 */
export const PETAL_VIEWBOX = 240;

type PetalSilhouette = { name: string; d: string };

/**
 * The eight silhouettes, in the order the artwork files sit on disk, which is
 * alphabetical.
 */
export const petalSilhouettes: readonly PetalSilhouette[] = [
  { name: 'backroll', d: 'M96 190 C66 172 46 140 50 108 C54 74 86 50 122 52 C158 54 188 78 190 112 C192 144 170 176 140 192 C124 200 110 198 96 190 Z' },
  { name: 'comma', d: 'M78 200 C58 166 60 116 86 82 C108 54 146 40 174 52 C168 86 152 120 130 148 C114 170 98 190 78 200 Z' },
  { name: 'curl', d: 'M104 198 C70 180 42 146 44 110 C46 72 82 46 122 48 C164 50 196 80 198 118 C200 152 174 182 138 196 C126 200 114 202 104 198 Z' },
  { name: 'doodle', d: 'M76 186 C46 156 40 108 62 80 C86 50 130 44 156 62 C182 80 190 116 178 144 C166 170 138 186 106 190 C92 192 82 192 76 186 Z' },
  { name: 'fan', d: 'M118 196 C110 186 100 180 88 176 C60 168 34 152 30 130 C26 108 44 90 70 88 C96 86 148 86 174 90 C200 94 214 112 208 132 C202 152 172 168 146 176 C134 180 126 186 118 196 Z' },
  { name: 'ripple', d: 'M116 196 C108 186 98 180 88 176 C68 168 46 156 40 138 C34 122 36 110 44 100 C36 88 44 74 60 68 C76 62 86 68 92 76 C104 62 128 58 146 66 C164 60 182 70 188 86 C196 100 194 112 188 122 C194 134 188 150 172 160 C152 172 130 182 122 190 C120 193 118 194 116 196 Z' },
  { name: 'split', d: 'M116 196 C108 186 98 180 88 176 C62 166 36 146 36 116 C36 84 62 60 96 60 C110 60 118 68 122 80 C124 86 125 90 126 94 C128 88 130 80 134 72 C142 58 164 54 180 64 C200 76 204 112 188 138 C172 164 136 184 122 190 C120 193 118 194 116 196 Z' },
  { name: 'spoon', d: 'M114 208 C104 174 92 146 88 114 C83 74 98 40 120 34 C142 40 157 74 152 114 C148 146 136 174 126 208 C124 214 116 214 114 208 Z' },
];

/**
 * The radius the ink actually reaches, in the petals' own 240-unit box: **95 units from
 * the box's centre**, which is where a placement turns.
 *
 * ⚠️ **Not the box's half-diagonal, and substituting that is what breaks a placement.**
 * The box is not drawn tight to the artwork — it carries 25 to 50 units of dead margin
 * on every side — so its half-diagonal is 170 where the ink stops at 95. Read the box's
 * way, the largest mark in the tile fails clearance against an edge it is nowhere near.
 *
 * 95 is the farthest **control point** of any of the eight silhouettes from the box's
 * centre (`fan`'s, at 94.76), rounded up. Control points rather than sampled curves,
 * because a cubic lies inside the convex hull of its own control points, so a bound over
 * those bounds the drawn curve too. One figure for all eight rather than one each: the
 * shapes share a box precisely so they need no per-shape fitting.
 */
export const PETAL_INK_RADIUS = 95;

/** How much room a petal drawn at `size` needs each way, as a fraction of the tile. */
export function petalClearance(size: number): number {
  return (size * PETAL_INK_RADIUS) / PETAL_VIEWBOX;
}

/**
 * The silhouette a name asks for.
 *
 * ⚠️ **It throws rather than falling back on a shape that exists.** The two ways of
 * surviving a bad name are both worse than a failed build: drawing one shape five times
 * is the lattice the tile is arranged to avoid, and dropping the mark thins the texture
 * silently.
 */
export function petalSilhouette(name: string): string {
  const shape = petalSilhouettes.find((candidate) => candidate.name === name);

  if (!shape) {
    throw new Error(
      `petalSilhouette: no petal named "${name}", only ` +
        `${petalSilhouettes.map((candidate) => candidate.name).join(', ')}.`,
    );
  }

  return shape.d;
}
