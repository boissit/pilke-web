/**
 * The app's sparkle as pure geometry — the outline and the box it was drawn in.
 *
 * Copied verbatim from `pilke-app/src/components/svgs/Sparkle.tsx`, where it is
 * exported under this name precisely so that nothing draws a near copy of it. It
 * lives in a module of its own here for the same reason: three components on this
 * site draw this shape — the wordmark's sparkle, the tiled glimmer and the
 * currency's coin — and a hand-redrawn flourish in any of them would be a second
 * brand mark.
 */
export const sparkleShape = {
  width: 37,
  height: 61,
  path: 'M32.704 4.042a1.5 1.5 0 0 0-2.734-1.235c-.335.722-.678 1.488-1.036 2.286-1.87 4.174-4.134 9.227-7.595 13.425-4.044 4.906-9.633 8.521-18.08 7.847a1.5 1.5 0 0 0-.954 2.742c3.36 2.246 5.944 4.357 7.217 8.162 1.3 3.885 1.313 9.798-1.304 19.815a1.5 1.5 0 0 0 2.85.921c3.881-10.025 8.474-14.074 12.343-15.484 3.887-1.417 7.451-.32 9.579.823a1.5 1.5 0 0 0 1.589-2.537c-4.224-3.058-5.964-9.436-5.916-16.81.048-7.272 1.84-14.96 4.04-19.955Z',
} as const;
