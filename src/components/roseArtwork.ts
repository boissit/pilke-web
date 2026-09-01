/**
 * The rose as pure geometry: the artwork's paths, the box they were drawn in, and the
 * colours they fill with.
 *
 * `pilke-app/assets/rose/rose.svg` is the artwork and the source of truth for every
 * path below; `pilke-app/src/components/svgs/RoseIcon.tsx` is the app's port of the
 * same file, and the two ports are kept in step by going back to the `.svg` rather
 * than to each other. This is geometry in a module of its own so that nothing on the
 * site draws a near copy of the mark: a hand-redrawn rose would be a second brand
 * mark, and there is only one.
 */

/**
 * **The plant's measured extent, not `rose.svg`'s own `0 0 736 736`.**
 *
 * The artwork does not fill its square canvas — there is dead margin on every side,
 * most of it below the stem — so drawing at the file's viewBox spends about a third of
 * the height on nothing and makes every size read visibly smaller than the number
 * asking for it. The measurements are tabulated in `pilke-app/assets/rose/README.md`.
 */
export const ROSE_VIEWBOX = '116 43 484 653';

/**
 * Width over height, `484 / 653` — about 0.741.
 *
 * The mark is asked for by height, so this is what a caller working from a width has
 * to divide by, and what turns a rose's height into the room it takes on a line.
 */
export const ROSE_ASPECT = 484 / 653;

/**
 * The five petal groups, **in the order they fill**, which is centre-outwards.
 *
 * Centre-out reads as a bud opening. The reverse reads as a rose being pulled apart,
 * which is the wrong story for a currency that is earned.
 *
 * `upperLeft` here and `petal-upper-left` in the artwork: both spellings are
 * load-bearing — the id is what a port has to match when it goes back to the `.svg`,
 * and the camelCase key is what callers use.
 */
export const petalFillOrder = ['inner', 'front', 'upperLeft', 'left', 'right'] as const;

export type PetalGroup = (typeof petalFillOrder)[number];

/**
 * How many petals one whole rose has, and so the most this mark can fill.
 *
 * It is also the price of one invitation — five petals make the rose that opens a set
 * — but that is the economy's number and this is the drawing's, and the site quotes the
 * price from `ui.ts` where the rest of the copy lives.
 */
export const PETALS_PER_ROSE = petalFillOrder.length;

/** How many of the five groups are filled. The mark draws nothing else. */
export type PetalCount = 0 | 1 | 2 | 3 | 4 | 5;

/**
 * The artwork's own three fills, and the ink it is outlined in.
 *
 * The three are the values `pilke-app/assets/rose/README.md` records for the drawing,
 * carried as literals rather than as tokens because they belong to the artwork and not
 * to the site's palette: nothing else on any page is this red, this green or this grey.
 *
 * The outline is the site's `--ink`, the same value every rule, border and chip edge on
 * the page draws with, so the mark is outlined in the weight of ink it sits among.
 *
 * ⚠️ **Only the petals grey.** The stem, the leaves and the outline are the same at
 * zero petals as at five. Greying the foliage too makes the drawing read as *disabled*,
 * which says the rose is unavailable rather than unearned — and the plant is not the
 * thing being paid for. The outline in particular is what keeps the mark legible at the
 * wordmark's size, where the fills are only a few pixels across.
 */
export const roseColors = {
  /** A petal that has been earned. */
  petal: '#F4504F',
  /** A petal that has not. */
  unfilledPetal: '#D9D2D4',
  /** Stem and both leaves. One value, because the artwork gives them one. */
  foliage: '#529A74',
  /** The outline, at every size and every count. */
  outline: 'var(--ink)',
} as const;

type PetalPath = { group: PetalGroup; d: string };

/**
 * Every petal path in the artwork, **in the artwork's own order, which is z-order**.
 *
 * ⚠️ **An ordered array carrying each path's group, not a map keyed by group.** The
 * petals overlap and `outlinePath` is a filled shape drawn last over all of them, so
 * document order is what makes the bloom read as a bloom: `front` is drawn both before
 * and after the three outer petals, which is how the near petal sits in front of them.
 * Collect these paths by group and the whorl comes apart.
 *
 * ⚠️ **`rose.svg` carries `petal-inner` on four paths and `petal-front` on two**, which
 * is invalid SVG and the reason nothing here selects by id: a `#petal-inner` lookup
 * reaches the first match and silently ignores the other three, lighting part of a
 * group and reading as a rendering fault. A group is a set of paths, and a fill applies
 * to all of them.
 */
export const petalPaths: readonly PetalPath[] = [
  { group: 'front', d: 'M398.2 60.2 C363.2 62.2 335.4 75.4 315.6 99.4 C307.3 109.3 311.8 116.9 323.8 113.2 C335.8 109.6 345.1 108.2 358.5 108.2 C375.5 108.2 386.7 111.2 399.2 119 C406 123.2 408.9 123.9 415.2 122.7 C446.7 117.1 467.5 147.5 453.2 178.2 C448.2 189 437.6 198.7 415.2 213 C394.8 226.2 375.5 236.5 339.8 253.6 C275.1 284.5 267.6 289.8 276.2 298.6 C284.7 307.2 348.7 291.8 397.6 269.2 C407.8 264.6 409.8 263.6 415.9 260.4 C472.8 230.7 495.7 205.9 502.2 167 C507.7 134.1 500.5 107.3 481.7 90.5 C458.6 69.9 427.1 58.5 398.2 60.2 Z' },
  { group: 'right', d: 'M522.5 150.6 C516.6 151.8 514.2 155.1 513.1 163.5 C511.1 179.1 505.8 196.1 499.4 207.1 C494.4 215.7 494 218.6 495.8 231 C502.1 273.3 495.1 315.5 476.9 345.1 C470.3 355.8 461.8 364.8 449.8 373.7 C441.3 379.9 439.8 384 444.4 388.3 C449.3 392.8 476 391.6 495.7 386 C539.1 373.5 564.6 345.5 569.6 304.8 C570.5 297.4 570.6 295.3 570.6 280.9 C570.7 259.5 571.1 255.9 575.8 239.4 C585.6 204.2 580.2 178.4 559.6 161.9 C549.5 153.8 532.6 148.6 522.5 150.6 Z' },
  { group: 'left', d: 'M184.8 240.7 C140.3 245.4 126.3 310.6 163.7 338.8 C168.7 342.6 172.8 344.3 185.4 347.9 C207.4 354.1 216.1 359.4 232.5 376.8 C242.9 387.7 246.1 390.8 251.1 394.7 C278.7 416.2 317.4 417.4 356.1 398.1 C362.4 394.9 364.2 392.9 364.2 389.2 C364.2 385.2 362.6 383.6 355.3 381 C320.4 368.2 295.4 350.5 275.9 324.6 C265.7 311.1 262.3 303.6 261.2 292.2 C260.5 284.5 257.7 281.1 249.3 277.9 C231.6 271.1 212.6 259.6 200.4 248.3 C195.4 243.8 194.2 242.8 192.4 242 C191.1 241.4 186.7 240.4 185.9 240.5 C185.8 240.5 185.2 240.6 184.8 240.7 Z' },
  { group: 'upperLeft', d: 'M266.8 83.8 C250.2 84.5 232 91.6 220 102 C177.7 138.5 170.1 200.9 203.7 235.6 C215.1 247.3 237.2 261.3 244.4 261.3 C251.1 261.3 252.6 257.5 250.2 245.9 C248.1 234.9 246.8 227.2 246.2 221.8 C246.1 220.3 245.8 217.5 245.6 215.6 C244.9 209.8 245 192.8 245.7 186.8 C249.1 159.7 256.8 143 269.7 134.4 C271.1 133.5 273.6 131.9 275.4 130.7 C286.7 123.3 292.7 116.3 298.4 103.8 C302.7 94.4 301 89.1 293.1 86.8 C287.8 85.2 274.1 83.2 271.2 83.5 C271 83.5 269 83.7 266.8 83.8 Z' },
  { group: 'front', d: 'M477.8 235.8 C475.8 236.2 474.2 237.1 470.4 240.1 C465 244.4 458.5 248.9 447.1 256.2 C444.6 257.8 433.2 264.5 429.2 266.8 C425.1 269.1 413.5 275 409.2 277 C406.5 278.3 402.8 280 400.8 281 C373.2 294 334 306.5 304.1 311.8 C293.4 313.6 292.1 314.2 290.5 317.8 C288.4 322.3 291.1 326.3 303.8 337.8 C324.1 356.2 357.2 371 389.4 376.2 C449.7 385.9 494.8 324.8 487 243.8 C486.5 238 482.7 234.8 477.8 235.8 Z' },
  { group: 'inner', d: 'M273.8 148.5 C260.9 151 252.7 185.2 256.5 220.9 C258.4 239.2 265.1 264.1 269.2 268.5 C273.2 272.9 276.3 272.3 291.1 264.6 C300.5 259.6 320.7 249.5 330.8 244.6 C356.5 232.1 356 232.5 356 227.5 C356 223.3 354 221.4 346.4 218.5 C301.5 201.3 284.9 185.6 282.7 158.6 C282 150.9 279.1 147.5 273.8 148.5 Z' },
  { group: 'inner', d: 'M351.2 120.4 C303.4 125.4 279.9 150.3 299.1 175.8 C311.5 192.2 325.2 193.9 326.3 179.1 C327.9 156 332.3 147.8 345.9 142.4 C363.6 135.4 383.3 140.1 394.7 154 C403.7 165.1 413.2 157.5 407.2 144.1 C400.5 129.1 374.4 118 351.2 120.4 Z' },
  { group: 'inner', d: 'M425.3 135.8 C420.4 136.8 418.5 141.1 419.6 148.9 C420.4 154.4 420.3 157.4 419.2 161.9 C415.2 179.2 393.7 191.2 363.6 193.1 C349.8 194 347.2 195.1 347.2 200.4 C347.3 204.6 349.6 206.3 360.6 210.2 C380.9 217.5 389.5 216.7 404.6 206.1 C407.2 204.3 411 201.8 413 200.5 C440.4 183 447.6 174 447.2 157.8 C446.9 144.8 435.9 133.7 425.3 135.8 Z' },
  { group: 'inner', d: 'M355.6 151.4 C343 153.5 333.6 167 338.1 176.7 C340.7 182.2 343.1 182.6 364.3 181 C375.1 180.2 383.9 178 386.6 175.5 C397.4 165.4 375 148.1 355.6 151.4 Z' },
];

/** The stem. */
export const stemPath =
  'M385.6 397.6 C382 398.4 373.3 402.7 371.3 404.7 C367.6 408.3 367.2 411.9 369.4 420.6 C388.8 499 381.6 575.4 348.1 646.1 C341.8 659.4 342.5 662.8 352.6 669.6 C363.2 676.7 367.7 676 372.7 666.6 C394 627.2 408.1 575.4 411 526.5 C411.8 513.9 411.6 486.7 410.6 476.4 C410.4 474.2 410.2 471 410 469.2 C408.6 453.2 403.3 426 398.2 408.2 C395.6 399.3 391.9 396.2 385.6 397.6 Z';

/** The right leaf, drawn before the left one, as in the artwork. */
export const leafRightPath =
  'M570.1 423 C569.5 423.1 566.5 424.2 563.3 425.4 C553.9 429.2 545.6 431.8 531.9 435.3 C496.8 444.3 479 454.3 462.3 474.6 C450 489.5 439.3 515.1 438.3 532 C437.9 539.7 444.2 542.7 451 538.1 C452.2 537.3 456.6 534.3 460.9 531.4 C482.6 516.7 496.7 506.6 510.2 496 C517.2 490.5 520.4 489.9 522.5 493.5 C525.6 498.9 520.5 504.2 496.6 521.1 C495.2 522.1 492.4 524.1 490.2 525.6 C488.1 527.2 483.4 530.4 479.8 532.9 C467.4 541.2 455.2 549.9 453.6 551.4 C449.1 555.9 450.6 561.5 457.3 564.6 C485 577.5 522.8 577.1 544.1 563.6 C577.2 542.7 592.7 487.8 581.2 431.9 C579.8 424.9 575.9 421.8 570.1 423 Z';

/** The left leaf. */
export const leafLeftPath =
  'M242.8 460 C202.3 461.8 163.7 491.2 140.4 537.9 C135.2 548.4 138.2 554.2 149 554.2 C159.8 554.2 176.4 556.3 192.3 559.5 C244.6 570.1 277.9 562.4 300.1 534.6 C313.4 518 312.7 509.4 297.8 507.3 C281.4 504.9 268.8 506.4 241.9 513.7 C229.6 517.1 227.6 517.1 225.6 513.6 C223.3 509.6 225.1 506.2 230.6 504.1 C246.3 498.2 269.4 493.9 285.9 493.9 C298.5 493.8 299.8 493.4 301.5 489.8 C302.9 486.5 302 483.8 298.2 480.1 C283.8 466.3 263.9 459.1 242.8 460 Z';

/**
 * The whole plant's outline: **one filled path** over petals, stem and both leaves,
 * drawn last and on top of every fill.
 *
 * ⚠️ **Thirteen subpaths, and they have to stay in one path.** The first is the
 * plant's silhouette and the other twelve are the interior cells the fills show
 * through; they read as holes only because they share a path with the silhouette that
 * encloses them, under SVG's default `nonzero` fill rule. Split into separate paths, or
 * "simplified", the twelve become twelve ink blots over the bloom.
 *
 * ⚠️ **There is no bloom-only crop, and there must not be one.** No clip and no viewBox
 * separates the bloom from the foliage: cropping to the petals leaves a stub of stem and
 * the tips of both leaves poking out underneath. The rose is drawn whole at every size.
 */
export const outlinePath =
  'M391.9 43.2 C364.7 45 340.9 54.6 319.4 72.5 C314.5 76.5 313.2 76.6 306.9 73.8 C273.3 59 232.1 66.6 206.2 92.5 C170.8 128 159.4 169.9 173 214.9 C175.8 224.1 175.6 224.8 168.7 227.5 C106.6 251.9 114.6 349.3 180 364.4 C198.5 368.6 210.4 376.1 225 392.8 C255.7 427.8 295 437.6 341.9 422.2 C351.9 418.9 352.9 419.3 354.9 427 C363.7 461.1 368.4 526.5 361.8 524.2 C361.3 524.1 358.8 521.7 355.7 518.6 C348.7 511.6 343 507.1 333.9 501.4 C327.3 497.2 327.4 497.4 324.9 491.5 C310.2 457.2 274.6 438.1 235.6 443.6 C183.1 451.1 144.1 485 120.8 543.6 C112.1 565.5 115 570.8 135.8 571.2 C145.1 571.5 152.6 571.8 157.2 572.2 C165.8 573 168.2 573.3 173 574 C176 574.4 183.6 575.7 189.9 576.9 C221.5 582.6 233.5 583.3 251.4 580.2 C285.1 574.5 307.8 558 322.5 528.8 C325.2 523.4 327.2 523.4 333.9 528.8 C341.6 534.9 348.4 542.5 354.8 552.2 C359.1 558.6 359.4 559.9 358.2 565.9 C352.8 592.4 343.6 618.2 329.2 648.1 C321.2 664.6 322.1 668.6 335.7 678.4 C368.4 701.9 371.7 702 384.1 679.4 C396.9 656.1 407.7 628.5 414.9 600.9 C417.1 592.7 416.6 593.5 426.2 583.8 C437.6 572.4 436.2 572.8 446.8 578.2 C460.7 585.2 475.3 589.7 488.2 590.9 C489.2 591 491.8 591.2 494.1 591.4 C529.5 594.8 562.3 578.9 579.7 550 C602 512.7 606.6 459.9 591.9 411 C588.6 400.3 582.8 398 572.5 403.1 C561.4 408.7 549.9 412.8 530.9 417.8 C476 432.2 451.9 450.6 432.8 492.9 C428.5 502.2 427.6 501.6 426.9 488.6 C425.9 471.8 424 454.6 421.6 442.5 C421.4 441.5 420.8 437.9 420.1 434.6 C418.9 428.1 416.4 417 414.6 409.9 C412.4 401.1 412.8 400.8 423.1 403.5 C478.5 417.7 538.3 398.5 566.3 357.5 C580.8 336.4 586 315.9 586 280.8 C586 263.8 586.7 257.8 590 246 C607.9 183.1 581.3 135.6 526.8 133 C519.2 132.7 518.8 132.3 517.2 125 C506.4 73 454.4 39.1 391.9 43.2 Z M410 65.3 C434.2 66.8 456.9 76.2 476.8 92.8 C494.1 107.4 501 128.4 498.2 157.9 C495.7 185.6 483.6 208.2 462.5 225.1 C443.2 240.5 412.2 258.1 383.9 269.8 C343 286.5 305.5 296.4 284.7 295.9 C268.2 295.6 282.3 286.3 342 258.1 C400.6 230.5 439.9 205.9 452.7 188.9 C477.7 155.6 454 110.8 415.1 117.8 C409.5 118.8 408.1 118.4 402.1 114.9 C380.2 101.6 353 99.4 322.8 108.4 C312.6 111.5 314 107.2 327.7 93.7 C347.4 74.3 379.3 63.3 410 65.3 Z M278.4 89 C294.2 90.6 297.6 93 294.4 100.4 C288.9 112.9 283.7 119.2 272.6 126.4 C270.9 127.6 268.3 129.3 266.9 130.2 C247.4 143.1 236.4 180 240.7 218 C241.6 225.9 241.8 227.2 242.2 229.8 C242.8 233.9 244.5 242.9 245.6 248.7 C247.5 258 247.1 258.4 239.4 254.5 C207.8 238.7 193 220.6 188.5 192.4 C183.2 158.9 202.6 117.5 231.9 99.7 C246.1 91 261.9 87.4 278.4 89 Z M365.5 125.6 C386.4 127.8 404.2 140.1 404.2 152.5 C404.2 156.2 402.4 155.9 399.1 151.6 C386.1 134.6 360.8 129.2 340.6 139.3 C327.6 145.9 322.8 155.6 321.3 178.3 C320.8 186 319 186.6 312.1 181.5 C291.4 166.1 293.9 145 318 133.4 C330.3 127.5 350.7 124.1 365.5 125.6 Z M429.8 140.8 C444.2 145.5 446.9 163.2 435.3 177.1 C431.1 182.1 425.4 186.4 408 197.8 C406.1 199 403 201.1 401 202.5 C388 211.8 381.1 212.3 362.1 205.5 C353 202.2 351.5 201.5 351.5 200.4 C351.5 199 352.3 198.8 363.3 198.1 C405.1 195.5 429.6 175.3 424.5 147.8 C423.3 140.9 424.7 139.1 429.8 140.8 Z M276.3 153.3 C277.1 153.9 277.3 154.9 277.7 159.4 C279.3 180.9 290.1 195.6 313.9 209.2 C322.2 214 330.8 217.9 346.4 223.9 C351.6 225.9 352.7 227.1 351 228.8 C350.3 229.5 348.3 230.5 326.5 241.1 C320.1 244.2 308.7 249.9 301.1 253.8 C274 267.7 276.9 266.3 275.2 266.2 C272.3 266 271.2 263.9 267.8 251.4 C260.1 223.5 258.6 200.5 262.9 177.1 C265.2 164.3 272.9 150.7 276.3 153.3 Z M531.8 155.6 C552.8 158.2 568.8 172.7 574 194.1 C577.1 206.9 576.3 218.4 570.8 238.4 C566.2 254.7 565.6 259.6 565.7 277.8 C565.9 307.3 562.4 323.6 552.4 340.4 C536.6 367.1 500.9 385.2 462.9 385.9 C444.7 386.3 442.9 384.9 452.5 377.9 C473 362.9 485.9 344.9 494.2 319.5 C503.1 292.4 505.4 261.9 500.9 230.1 C499.2 218.3 499.3 217.7 503.4 210.2 C511 196.6 515.6 182.3 518.1 164.6 C519.5 155.4 521.1 154.3 531.8 155.6 Z M366 156.4 C377.2 158.3 388.5 168.7 383.3 172.1 C380 174.3 364.9 176.4 348.6 176.9 C342.7 177.1 341.4 175.4 342.6 169.2 C344.6 159.4 354 154.2 366 156.4 Z M480.8 240.8 C483.7 243 483.1 277 480 293.5 C472.1 334.6 445.5 365.9 413.9 371.2 C386.7 375.8 340.2 360.8 312.4 338.5 C302.7 330.8 294.8 322.5 294.8 320.2 C294.8 318.4 294.9 318.4 305.4 316.5 C345.9 309.3 389.3 293.9 429.1 272.5 C443.4 264.8 463.7 252 471.8 245.5 C473.1 244.4 474.9 243 475.7 242.3 C478.4 240.2 479.6 239.8 480.8 240.8 Z M189.6 246.1 C191.2 246.8 192.5 247.9 197.5 252.5 C209.8 263.8 227.9 274.8 246.5 282.1 C253.9 285.1 255.5 286.6 256 291.4 C257.4 303.9 259.6 309.8 266.7 320.4 C286.7 350.2 315.5 372 352.2 385.1 C360.4 388 360.9 388.4 359.2 390.3 C358 391.8 348.3 396.5 340.5 399.5 C311.1 410.8 281.1 408.8 259.2 394.4 C252.5 389.8 248.1 385.8 235.4 372.6 C218.2 354.7 209.5 349.4 186.5 343 C177.2 340.4 176.8 340.3 172.4 338.1 C141 322.6 138.2 271.5 167.7 252.3 C175.6 247.2 185.8 244.3 189.6 246.1 Z M389.8 402.8 C391.7 403.7 392.5 405.9 395.7 419 C400.3 437.1 403.8 456.8 405 470.2 C405.2 472 405.4 475.2 405.6 477.4 C411 537 396.8 609.9 370.1 660.9 C364.7 671.2 364.4 671.3 355.7 665.5 C347.5 660.1 347.4 659.4 352.8 647.9 C386.6 576.4 393.9 499 374.4 419.8 C372 410.1 372.4 409 379.8 405.4 C386.4 402.2 387.9 401.8 389.8 402.8 Z M574.1 428.2 C575.8 429.2 576.8 433.7 578.5 447.4 C585.1 499.6 567.7 547 536.4 562.1 C517.4 571.3 489.1 571.5 465.4 562.5 C455.8 558.9 454.1 557 457.7 554.3 C460.5 552.3 475.6 541.8 481.8 537.6 C485.8 534.9 490.9 531.4 493 529.9 C495.1 528.4 498 526.4 499.4 525.4 C525.3 507 530.5 501.1 527.8 493 C524.9 484.5 517.2 484 507.5 491.8 C493.8 502.5 480.9 511.8 457.1 527.9 C444.6 536.3 445.2 536 444 535 C443.1 534.4 443.2 532.1 444.2 526.8 C451.7 488.5 473.2 461.8 507.4 448.1 C514.4 445.2 520.8 443.2 533.4 440 C547.1 436.5 557.6 433.2 566.8 429.5 C571.5 427.6 572.8 427.4 574.1 428.2 Z M254.4 465.3 C262.9 466 274 469.6 282.2 474.3 C289.2 478.3 297 484.9 297 486.9 C297 488.8 296.9 488.8 285.8 488.9 C269.1 488.9 245.8 493.3 228.8 499.5 C219.5 502.9 216.6 511.4 222.6 517.9 C226.5 522.1 229.9 522.2 243.4 518.5 C268.9 511.4 280.9 510 296.9 512.1 C305.9 513.4 306.6 515.7 300.6 525.3 C285.9 548.5 259.7 560.6 227.4 559.2 C217.3 558.8 208.4 557.6 193.2 554.6 C175.1 551.1 160.2 549.3 148.9 549.2 C140.3 549.2 140.7 546.7 152 527.4 C176 486.1 216 461.9 254.4 465.3 Z';

/** The groups filled at a given count, centre-outwards — a prefix of `petalFillOrder`. */
export function filledGroups(petals: PetalCount): readonly PetalGroup[] {
  return petalFillOrder.slice(0, petals);
}

type RoseFills = {
  petals: Readonly<Record<PetalGroup, string>>;
  /** Stem and both leaves. */
  foliage: string;
  outline: string;
};

/**
 * Every colour the mark draws at a given petal count.
 *
 * Split out from the component because it is the part worth reading on its own: the
 * zero state and the fill order are both visible here without a renderer.
 */
export function roseFills(petals: PetalCount): RoseFills {
  const filled = new Set<PetalGroup>(filledGroups(petals));
  const fill = (group: PetalGroup) =>
    filled.has(group) ? roseColors.petal : roseColors.unfilledPetal;

  return {
    petals: {
      inner: fill('inner'),
      front: fill('front'),
      upperLeft: fill('upperLeft'),
      left: fill('left'),
      right: fill('right'),
    },
    foliage: roseColors.foliage,
    outline: roseColors.outline,
  };
}
