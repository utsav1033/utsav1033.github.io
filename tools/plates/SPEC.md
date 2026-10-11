# Plate spec: shared by every diagram on utsav1033.github.io

The site is a portfolio for an AI engineer. It is typeset with old-book fonts on cream paper
(IM Fell English for headings, EB Garamond for text) but the layout is modern and plain. Each
diagram ("plate") sits in a framed box beside a short paragraph. The reader is a technical
founder skimming in 30 seconds: the plate must make the mechanism obvious at a glance.

## Look: a plate from an old scientific journal / engineering drawing
- Think 19th-century Nature or Philosophical Transactions figures, patent drawings, and
  Tufte. Precise hairlines, leader lines to labels, dotted construction guides, letter or
  numeral keys, generous white space. NOT slideware: avoid rows of rounded boxes with arrows.
- One accent: red (class `red` / var(--red)) marks the single most important thing.
  Everything else is ink, muted ink, or hairline.
- Strokes 0.7–1.4 units. Nothing within 8 units of the viewBox edge. Align to a grid.
- Text upright only, never italic. Minimum font-size 12.5. Labels at most ~4 words; no
  sentences inside the plate (the caption carries the explanation). Plain names in default
  text; proper names may use class `name` (IM Fell SC).

## Technical contract
- Output exactly one file: `<svg class="plate-NAME" viewBox="0 0 540 H" role="img" aria-label="…">`
  with H between 160 and 280. It renders at ~520–560 px wide, so 1 unit ≈ 1 px. On phones it
  keeps a 500 px min-width and scrolls sideways inside its frame.
- Colours ONLY via CSS variables: var(--ink) var(--muted) var(--hair) var(--rule) var(--red)
  var(--card) var(--paper). Fonts: var(--body) (default for svg text) and var(--fellsc).
  It must work in dark mode (variables flip automatically). No hard-coded colours.
- You may use the classes already in /home/user/utsav1033.github.io/assets/css/site.css
  (svg .sm .red .name .guide .hollow .body .ring .leader .leader-r .ret .ray .grid .faint
  .bx .bx-r .lnr .xmark …), and/or put a `<style>` element inside your svg with every rule
  scoped under `.plate-NAME`.
- Motion is optional: at most one slow loop (≥ 4 s), CSS only, scoped, and a
  `@media (prefers-reduced-motion:reduce)` rule that shows the meaningful final state.
- No scripts, no external images, no foreignObject.

## Verify before you finish
Render with:
  node /tmp/claude-0/-home-user-utsav1033-github-io/8a41bc09-45f3-5c9f-890c-ecb2d3df5626/scratchpad/plates/preview.js <your.svg> <out.png> "<title>" "<caption>"
It writes out.png (light), out-dark.png, out-anim.png and prints JSON with any overlapping
or out-of-bounds text. Look at the PNGs with the Read tool. Iterate until: zero overlaps,
nothing outside, it reads clearly in both themes, and a stranger would understand the
mechanism in five seconds.

## Report back
The file path, a title (≤ 4 words), a one-sentence caption (plain, not italic, ≤ 25 words),
and anything you were unsure about.
