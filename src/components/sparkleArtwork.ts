/**
 * The sparkle: the four-pointed star in the wordmark, and the one shape
 * the site draws its sparks with.
 *
 * The path is the wordmark's own, as `pilke-app/src/components/svgs/Sparkle.tsx` carries
 * it, in the logo's coordinates. Everything that draws a spark draws this path: the
 * counter on the front page, the price on `nain-se-toimii`, the scatter behind a card
 * and the fact card's icon. A second drawing of the star anywhere would be a second
 * brand mark to keep in step.
 */

export const SPARKLE_PATH =
  'M101.92 49.83C101.64 50.93 100.11 50.92 99.84 49.83C98.57 44.7 95.95 42.19 90.78 40.97C89.7 40.72 89.7 39.17 90.78 38.91C95.91 37.68 98.43 35.13 99.71 29.85C99.98 28.73 101.54 28.73 101.81 29.85C103.08 35.1 105.54 37.63 110.67 38.87C111.76 39.13 111.76 40.69 110.67 40.96C105.65 42.19 103.21 44.73 101.91 49.83Z';

/** The box the path is drawn tight to, in the logo's coordinates. Near square. */
export const SPARKLE_BOX = { x: 89.97, y: 29.01, width: 21.52, height: 21.64 } as const;

export const SPARKLE_VIEWBOX = `${SPARKLE_BOX.x} ${SPARKLE_BOX.y} ${SPARKLE_BOX.width} ${SPARKLE_BOX.height}`;

/** Where the sparkle turns and where a core grows from. */
export const SPARKLE_CENTRE = {
  x: SPARKLE_BOX.x + SPARKLE_BOX.width / 2,
  y: SPARKLE_BOX.y + SPARKLE_BOX.height / 2,
} as const;

/**
 * The counter's colours, the app's `colors.spark`: a lit spark is the brand's rose,
 * and a spark on its way is a pale grey sparkle with a rose core that grows with it.
 */
export const SPARK_COLORS = {
  lit: '#F4504F',
  unlit: '#D9D2D4',
} as const;

/**
 * The growing sparkle's rose core, as a fraction of its size, for each count short of
 * a lit one: the app's `CORE_STEPS`, so two sparks here is the drawing the app shows
 * for two.
 */
export const CORE_STEPS = [0.17, 0.3, 0.44, 0.58, 0.72] as const;

/** How many sparks light one sparkle: one invitation's worth. */
export const SPARKS_PER_GLYPH = 5;
