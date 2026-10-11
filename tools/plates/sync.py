"""Plate: fast/slow model handoff. The slow model works first; once the fast model
starts, the slow model stops and its line merges into the fast one.
Run: python3 tools/plates/sync.py [out.svg]   (default: _includes/plates/sync.svg)"""
import os, sys

def X(t):            # seconds -> x
    return 120 + t * 19.0

T_HAND = 4.0         # the fast model starts here; the slow model stops
T_END = 19.0
Y_AX, Y_SLOW, Y_FAST = 26, 74, 124
o = []
o.append('<style>.plate-sync .tl{stroke:var(--rule);stroke-width:.7;stroke-dasharray:1 3}'
         '.plate-sync .ax{stroke:var(--hair);stroke-width:.7}'
         '.plate-sync .idle{stroke:var(--hair);stroke-width:.9;stroke-dasharray:2 3;fill:none}'
         '.plate-sync .ln{stroke:var(--ink);stroke-width:1.3;fill:none}'
         '.plate-sync .chk{fill:var(--card);stroke:var(--red);stroke-width:1.3}'
         '.plate-sync .tick{fill:none;stroke:var(--red);stroke-width:1.4}</style>')

# light timestamps on top
o.append(f'<path class="ax" d="M {X(0)} {Y_AX} H {X(T_END)}"/>')
for t in (0, 4, 8, 12, 16, 19):
    o.append(f'<path class="ax" d="M {X(t)} {Y_AX-3} V {Y_AX+3}"/>')
    o.append(f'<path class="tl" d="M {X(t)} {Y_AX+6} V {Y_FAST+16}"/>')
    o.append(f'<text class="sm" x="{X(t)}" y="{Y_AX-8}" text-anchor="middle">{t} s</text>')

# labels
o.append(f'<text x="10" y="{Y_SLOW+5}">slow model</text>')
o.append(f'<text x="10" y="{Y_FAST+5}">fast model</text>')

# slow model: works first, a couple of steps, then stops at the handoff
o.append(f'<path class="ln" d="M {X(0)} {Y_SLOW} H {X(T_HAND)}"/>')
for t in (1.3, 2.9):
    o.append(f'<rect class="body" x="{X(t)-4.5}" y="{Y_SLOW-4.5}" width="9" height="9"/>')
o.append(f'<path class="ln" d="M {X(T_HAND)} {Y_SLOW-7} V {Y_SLOW+7}"/>')
o.append(f'<text class="sm" x="{X(T_HAND)+8}" y="{Y_SLOW-10}">stops</text>')

# the slow line merges into the fast line
mx = X(T_HAND + 2.2)
o.append(f'<path class="ln" d="M {X(T_HAND)} {Y_SLOW} C {X(T_HAND)+26} {Y_SLOW}, {mx-24} {Y_FAST}, {mx} {Y_FAST}"/>')

# fast model: idle until the handoff, then one line carries the task
o.append(f'<path class="idle" d="M {X(0)} {Y_FAST} H {X(T_HAND)}"/>')
o.append(f'<path class="ln" d="M {X(T_HAND)} {Y_FAST} H {X(T_END)}"/>')
o.append(f'<circle class="hollow" cx="{X(T_HAND)}" cy="{Y_FAST}" r="5"/>')
o.append(f'<text class="sm" x="{X(T_HAND)}" y="{Y_FAST+22}" text-anchor="middle">takes over</text>')
steps = [7.4, 8.6, 9.8, 11.0, 12.2, 13.4, 17.6]
for t in steps:
    o.append(f'<circle class="body" cx="{X(t):.1f}" cy="{Y_FAST}" r="3.6"/>')

# the one irreversible step, checked before it runs
cs = X(15.4)
o.append(f'<circle class="chk" cx="{cs:.1f}" cy="{Y_FAST}" r="8"/>')
o.append(f'<path class="tick" d="M {cs-3.6:.1f} {Y_FAST+0.4} L {cs-0.8:.1f} {Y_FAST+3.2} L {cs+4:.1f} {Y_FAST-3.4}"/>')
o.append(f'<text class="red" x="{cs:.1f}" y="{Y_FAST+28}" text-anchor="middle">send, checked first</text>')

# done
o.append(f'<path class="ln" d="M {X(T_END)} {Y_FAST-9} V {Y_FAST+9}"/>')
o.append(f'<text x="{X(T_END)+10}" y="{Y_FAST+5}">done</text>')

label = ('Timeline from 0 to 19 seconds. The slow model works first and takes two steps; at 4 seconds the fast model '
         'takes over and the slow model stops, its line merging into the fast one. The fast model then moves quickly '
         'through its steps, checks the one send before it runs, and finishes at 19 seconds.')
svg = f'<svg class="plate-sync" viewBox="0 0 540 168" role="img" aria-label="{label}">\n' + '\n'.join(o) + '\n</svg>\n'
here = os.path.dirname(os.path.abspath(__file__))
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, '..', '..', '_includes', 'plates', 'sync.svg')
open(out, 'w').write(svg)
