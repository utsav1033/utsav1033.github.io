"""Plate: handing a task from the slow model to the fast one.
The slow model works first; when the fast model takes over, the slow one stops. The fast
model spends its first stretch thinking (planning), then acts quickly (each action < 450 ms)
and finishes at 19 s, where the slow model alone took 27 s.
Run: python3 tools/plates/sync.py [out.svg]   (default: _includes/plates/sync.svg)"""
import os, sys

def X(t):                    # seconds -> x
    return 112 + t * 14.6

T_HAND, T_ACT, T_END, T_OLD = 4.0, 8.0, 19.0, 27.0
Y_AX, Y_SLOW, Y_FAST = 28, 76, 130
o = []
o.append('<style>'
         '.plate-sync .tl{stroke:var(--rule);stroke-width:.7;stroke-dasharray:1 3}'
         '.plate-sync .ax{stroke:var(--hair);stroke-width:.7}'
         '.plate-sync .ln{stroke:var(--ink);stroke-width:1.3;fill:none}'
         '.plate-sync .ghost{stroke:var(--hair);stroke-width:1.1;stroke-dasharray:2 3;fill:none}'
         '.plate-sync .think{fill:var(--card);stroke:var(--ink);stroke-width:1}'
         '.plate-sync .hatch{stroke:var(--muted);stroke-width:.7}'
         '.plate-sync .act{stroke:var(--ink);stroke-width:1.6}'
         '.plate-sync .save{stroke:var(--red);stroke-width:1;fill:none}'
         '</style>')

# light timestamps on top
o.append(f'<path class="ax" d="M {X(0)} {Y_AX} H {X(T_OLD)}"/>')
for t in (0, 4, 8, 12, 16, 19, 23, 27):
    o.append(f'<path class="ax" d="M {X(t):.1f} {Y_AX-3} V {Y_AX+3}"/>')
    o.append(f'<path class="tl" d="M {X(t):.1f} {Y_AX+6} V {Y_FAST+12}"/>')
    o.append(f'<text class="sm" x="{X(t):.1f}" y="{Y_AX-8}" text-anchor="middle">{t} s</text>')

o.append(f'<text x="8" y="{Y_SLOW+5}">slow model</text>')
o.append(f'<text x="8" y="{Y_FAST+5}">fast model</text>')

# slow model: two slow steps, then it stops at the handoff
o.append(f'<path class="ln" d="M {X(0)} {Y_SLOW} H {X(T_HAND)}"/>')
for t in (1.2, 2.8):
    o.append(f'<rect class="body" x="{X(t)-4.5:.1f}" y="{Y_SLOW-4.5}" width="9" height="9"/>')
o.append(f'<path class="ln" d="M {X(T_HAND)} {Y_SLOW-7} V {Y_SLOW+7}"/>')
# what the slow model alone would have taken
o.append(f'<path class="ghost" d="M {X(T_HAND)+3} {Y_SLOW} H {X(T_OLD)}"/>')
o.append(f'<circle class="hollow" cx="{X(T_OLD):.1f}" cy="{Y_SLOW}" r="3.5"/>')
o.append(f'<text class="sm" x="{X(15.5):.1f}" y="{Y_SLOW-8}" text-anchor="middle">slow model alone</text>')

# the slow line hands over into the fast line
o.append(f'<path class="ln" d="M {X(T_HAND)} {Y_SLOW} C {X(T_HAND)} {Y_SLOW+30}, {X(T_HAND)+2} {Y_FAST-30}, {X(T_HAND)+2} {Y_FAST-6}"/>')
o.append(f'<text class="sm" x="{X(T_HAND)-6:.1f}" y="{Y_SLOW+28}" text-anchor="end">hands over</text>')

# fast model: thinks first (its planning time) ...
x0, x1 = X(T_HAND) + 2, X(T_ACT)
o.append(f'<rect class="think" x="{x0:.1f}" y="{Y_FAST-6}" width="{x1-x0:.1f}" height="12"/>')
xs = x0 + 4
while xs < x1 - 2:
    o.append(f'<path class="hatch" d="M {xs:.1f} {Y_FAST+5} L {min(xs+8, x1-1):.1f} {Y_FAST-5}"/>')
    xs += 5
o.append(f'<text class="sm" x="{(x0+x1)/2:.1f}" y="{Y_FAST+24}" text-anchor="middle">thinks</text>')

# ... then acts fast: many short actions, each under 450 ms
t, n = T_ACT + 0.25, 0
while t < T_END - 0.2:
    o.append(f'<path class="act" d="M {X(t):.1f} {Y_FAST-6} V {Y_FAST+6}"/>')
    t += 0.45; n += 1
o.append(f'<path class="ln" d="M {X(T_ACT)} {Y_FAST} H {X(T_END)}"/>')
o.append(f'<text class="sm" x="{X((T_ACT+T_END)/2):.1f}" y="{Y_FAST+24}" text-anchor="middle">acts: each action under 450 ms</text>')
o.append(f'<path class="ln" d="M {X(T_END)} {Y_FAST-10} V {Y_FAST+10}"/>')

# the saving
ys = Y_FAST + 42
o.append(f'<path class="save" d="M {X(T_END)} {ys-5} V {ys} H {X(T_OLD)} V {ys-5}"/>')
o.append(f'<text class="red" x="{X((T_END+T_OLD)/2):.1f}" y="{ys+16}" text-anchor="middle">8 s saved</text>')

label = ('Timeline from 0 to 27 seconds. The slow model takes two steps, then hands the task over at 4 seconds and stops; '
         'alone it would have finished at 27 seconds. The fast model first thinks until 8 seconds, then acts quickly, '
         'each action under 450 milliseconds, and finishes at 19 seconds: 8 seconds saved.')
svg = f'<svg class="plate-sync" viewBox="0 0 540 196" role="img" aria-label="{label}">\n' + '\n'.join(o) + '\n</svg>\n'
here = os.path.dirname(os.path.abspath(__file__))
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, '..', '..', '_includes', 'plates', 'sync.svg')
open(out, 'w').write(svg)
