"""Plate: a fast model covers for a slow one.
The prompt fires and both models start at once. The fast model thinks briefly and starts
acting; the slow model is still thinking. When the slow model is ready it takes over at the
first step the fast model hasn't done, and the fast model stops. Actions are quick in both.
Without the fast model, the slow model would do every step after its thinking: 27 s, not 19 s.
Run: python3 tools/plates/sync.py [out.svg]   (default: _includes/plates/sync.svg)"""
import os, sys

def X(t):                         # seconds -> x
    return 104 + t * 15.0

FAST_THINK, SLOW_THINK, T_END, T_OLD = 1.2, 6.0, 19.0, 27.0
fast_steps = [1.9, 3.2, 4.5, 5.6]                 # steps 1-4, done while the slow model thinks
slow_steps = [6.6 + i * 1.75 for i in range(7)]   # steps 5-11, the slow model picks up at 5
Y_AX, Y_FAST, Y_SLOW = 28, 82, 150
o = []
o.append('<style>'
         '.plate-sync .tl{stroke:var(--rule);stroke-width:.7;stroke-dasharray:1 3}'
         '.plate-sync .ax{stroke:var(--hair);stroke-width:.7}'
         '.plate-sync .ln{stroke:var(--ink);stroke-width:1.3;fill:none}'
         '.plate-sync .ghost{stroke:var(--hair);stroke-width:1.1;stroke-dasharray:2 3;fill:none}'
         '.plate-sync .think{fill:var(--card);stroke:var(--ink);stroke-width:1}'
         '.plate-sync .hatch{stroke:var(--muted);stroke-width:.7}'
         '.plate-sync .step{fill:var(--card);stroke:var(--ink);stroke-width:1.2}'
         '.plate-sync .num{font-size:11.5px;fill:var(--ink)}'
         '.plate-sync .hand{stroke:var(--red);stroke-width:1.1;fill:none;stroke-dasharray:3 2.5}'
         '.plate-sync .save{stroke:var(--red);stroke-width:1;fill:none}'
         '</style>')

# light timestamps on top
o.append(f'<path class="ax" d="M {X(0)} {Y_AX} H {X(T_OLD)}"/>')
for t in (0, 6, 12, 19, 27):
    o.append(f'<path class="ax" d="M {X(t):.1f} {Y_AX-3} V {Y_AX+3}"/>')
    o.append(f'<path class="tl" d="M {X(t):.1f} {Y_AX+6} V {Y_SLOW+14}"/>')
    o.append(f'<text class="sm" x="{X(t):.1f}" y="{Y_AX-8}" text-anchor="middle">{t} s</text>')
o.append(f'<text class="sm" x="{X(0)-6}" y="{Y_AX+4}" text-anchor="end">prompt</text>')

o.append(f'<text x="8" y="{Y_FAST+5}">fast model</text>')
o.append(f'<text x="8" y="{Y_SLOW+5}">slow model</text>')

def think(t0, t1, y, label):
    x0, x1 = X(t0), X(t1)
    o.append(f'<rect class="think" x="{x0:.1f}" y="{y-7}" width="{x1-x0:.1f}" height="14"/>')
    xs = x0 + 3
    while xs < x1 - 2:
        o.append(f'<path class="hatch" d="M {xs:.1f} {y+6} L {min(xs+9, x1-1):.1f} {y-6}"/>')
        xs += 5
    if label:
        o.append(f'<text class="sm" x="{(x0+x1)/2:.1f}" y="{y+24}" text-anchor="middle">{label}</text>')

def step(t, y, n):
    o.append(f'<circle class="step" cx="{X(t):.1f}" cy="{y}" r="8"/>')
    o.append(f'<text class="num" x="{X(t):.1f}" y="{y+4}" text-anchor="middle">{n}</text>')

# fast model: thinks a moment, then does steps 1-4, then stops
think(0, FAST_THINK, Y_FAST, '')
o.append(f'<text class="sm" x="{X(FAST_THINK/2):.1f}" y="{Y_FAST-14}" text-anchor="middle">thinks</text>')
o.append(f'<path class="ln" d="M {X(FAST_THINK)} {Y_FAST} H {X(SLOW_THINK)}"/>')
for i, t in enumerate(fast_steps):
    step(t, Y_FAST, i + 1)
o.append(f'<path class="ln" d="M {X(SLOW_THINK)} {Y_FAST-9} V {Y_FAST+9}"/>')
o.append(f'<text class="sm" x="{X(SLOW_THINK)+8}" y="{Y_FAST+4}">stops</text>')

# slow model: thinks while the fast one works, then takes over at step 5
think(0, SLOW_THINK, Y_SLOW, 'thinks')
o.append(f'<path class="ln" d="M {X(SLOW_THINK)} {Y_SLOW} H {X(T_END)}"/>')
for i, t in enumerate(slow_steps):
    step(t, Y_SLOW, i + 5)
o.append(f'<path class="ln" d="M {X(T_END)} {Y_SLOW-10} V {Y_SLOW+10}"/>')
o.append(f'<text x="{X(T_END)+8}" y="{Y_SLOW+5}">done</text>')

# the handover: slow picks up at the first step the fast model hasn't done
hx = X(SLOW_THINK)
o.append(f'<path class="hand" d="M {hx:.1f} {Y_FAST+10} C {hx:.1f} {Y_FAST+40}, {X(slow_steps[0]):.1f} {Y_SLOW-40}, {X(slow_steps[0]):.1f} {Y_SLOW-10}"/>')
o.append(f'<text class="red" x="{hx+14:.1f}" y="{(Y_FAST+Y_SLOW)/2+5:.1f}">takes over at step 5</text>')

# without the fast model, the slow model would do steps 1-11 after thinking
ys = Y_SLOW + 40
o.append(f'<path class="ghost" d="M {X(T_END)+50} {Y_SLOW} H {X(T_OLD)}"/>')
o.append(f'<circle class="hollow" cx="{X(T_OLD):.1f}" cy="{Y_SLOW}" r="3.5"/>')
o.append(f'<text class="sm" x="{X(T_OLD):.1f}" y="{Y_SLOW-12}" text-anchor="end">slow model alone</text>')
o.append(f'<path class="save" d="M {X(T_END)} {ys-5} V {ys} H {X(T_OLD)} V {ys-5}"/>')
o.append(f'<text class="red" x="{X((T_END+T_OLD)/2):.1f}" y="{ys+16}" text-anchor="middle">8 s saved</text>')

label = ('Timeline from the prompt to 27 seconds. Both models start at once. The fast model thinks briefly, then '
         'does steps 1 to 4 while the slow model is still thinking. At 6 seconds the slow model is ready, takes over '
         'at step 5, and the fast model stops. The slow model does steps 5 to 11 quickly and finishes at 19 seconds; '
         'alone it would have finished at 27 seconds, 8 seconds later.')
svg = f'<svg class="plate-sync" viewBox="0 0 540 222" role="img" aria-label="{label}">\n' + '\n'.join(o) + '\n</svg>\n'
here = os.path.dirname(os.path.abspath(__file__))
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, '..', '..', '_includes', 'plates', 'sync.svg')
open(out, 'w').write(svg)
