#!/usr/bin/env python3
# Generates carmen.svg (plate-carmen). Run: python3 gen_carmen.py > carmen.svg
H = 264
o = []
A = o.append

PY = 86            # the draft's path
GT, GB = 70, 102    # gate bar extent
RAIL = 134         # return rail
gates = [  # x, label, tier (0 = upper row, 1 = lower row)
    (114, "static", 1),
    (160, "compile", 0),
    (206, "no-tolerance", 1),
    (252, "visible battery", 0),
    (298, "fresh fuzz", 1),
    (352, "hidden draw", 0),
    (404, "timing", 1),
]
TIER_Y = {0: 40, 1: 58}

A(f'<svg class="plate-carmen" viewBox="0 0 540 {H}" role="img" aria-label="Carmy, the model, writes three kernel drafts. Each passes seven gates in order: static, compile, no-tolerance checks, visible battery, fresh fuzz, a hidden draw of secret inputs whose results Carmy never sees, and timing against MLX. Failures return to Carmy with where and why; the winner is fused into Qwen 2.5 0.5B, 8 kernels to 2 per layer, decode 1.02 times faster. Below: of 75 planted bugs, a one-shape check lets 35 through; the judge catches all 75.">')
A('''<style>
.plate-carmen .gate{fill:none;stroke:var(--ink);stroke-width:1.4;stroke-linecap:square}
.plate-carmen .gate-r{fill:none;stroke:var(--red);stroke-width:1.4;stroke-linecap:square}
.plate-carmen .path{fill:none;stroke:var(--ink);stroke-width:1.2}
.plate-carmen .rail{fill:none;stroke:var(--ink);stroke-width:.9;stroke-dasharray:4 3}
.plate-carmen .drop{fill:none;stroke:var(--ink);stroke-width:.8}
.plate-carmen .seal{fill:none;stroke:var(--red);stroke-width:.8;stroke-dasharray:1.5 2.5}
.plate-carmen .drop-r{fill:none;stroke:var(--red);stroke-width:.8;stroke-dasharray:2 2}
.plate-carmen .head{fill:var(--ink);stroke:none}
.plate-carmen .head-r{fill:var(--red);stroke:none}
.plate-carmen .sheet{fill:var(--card);stroke:var(--ink);stroke-width:.9}
.plate-carmen .ln{fill:none;stroke:var(--hair);stroke-width:.8}
.plate-carmen .layers{fill:none;stroke:var(--ink);stroke-width:.7}
.plate-carmen .frame{fill:none;stroke:var(--ink);stroke-width:1}
.plate-carmen .bug{fill:var(--ink)}
.plate-carmen .esc{fill:var(--card);stroke:var(--muted);stroke-width:.9}
.plate-carmen .div{fill:none;stroke:var(--rule);stroke-width:.8}
.plate-carmen .pip{fill:var(--ink);opacity:0;animation:carmen-run 10s linear infinite;
  offset-path:path('M 60 86 H 252 V 134 H 38 V 112 V 86 H 60 H 448')}
@keyframes carmen-run{0%{offset-distance:0%;opacity:0}3%{opacity:1}96%{offset-distance:100%;opacity:1}100%{offset-distance:100%;opacity:0}}
@media all{.plate-carmen .pip{animation:none;opacity:0}}
</style>''')

# ---- Carmy: three stacked drafts
A('<text class="name" x="16" y="20">Carmy</text>')
A('<text class="sm" x="16" y="38">the LLM</text>')
for i, (dx, dy) in enumerate([(8, 0), (4, 4), (0, 8)]):
    x, y = 16 + dx, 66 + dy
    A(f'<rect class="sheet" x="{x}" y="{y}" width="34" height="38"/>')
    if i == 2:
        for k in range(5):
            w = 22 if k % 2 == 0 else 16
            A(f'<path class="ln" d="M {x+6} {y+8+k*6} h {w}"/>')

# ---- main path from drafts through the gates to the model
A(f'<path class="path" d="M 58 {PY} H 444"/>')
A(f'<path class="head" d="M 450 {PY} l -7 -3.2 v 6.4 z"/>')

# ---- gates
for x, label, tier in gates:
    red = label == "hidden draw"
    cls = "gate-r" if red else "gate"
    A(f'<path class="{cls}" d="M {x} {GT} V {PY-6} M {x} {PY+6} V {GB}"/>')
    ty = TIER_Y[tier]
    A(f'<path class="{"leader-r" if red else "guide"}" d="M {x} {ty+5} V {GT-3}"/>')
    A(f'<text class="{"red" if red else ""}" x="{x}" y="{ty}" text-anchor="middle">{label}</text>')

A('<path class="ray" d="M 114 20 V 14 H 208 M 304 14 H 404 V 20"/>')
A('<text class="name" x="256" y="19" text-anchor="middle">the judge</text>')
A('<text class="sm" x="490" y="38" text-anchor="middle">real model</text>')
# hidden draw: sealed off; its verdict goes to the report, never back to Carmy
hx = 352
A(f'<rect class="seal" x="{hx-17}" y="{GT-6}" width="34" height="{GB-GT+12}"/>')
A(f'<path class="drop-r" d="M {hx} {GB+6} V {RAIL+2}"/>')
A(f'<path class="head-r" d="M {hx} {RAIL+8} l -3 -6 h 6 z"/>')
A(f'<text class="sm red" x="{hx+9}" y="{RAIL+6}">never shown</text>')

# ---- fail path: visible gates drop to the return rail back to Carmy
for x, label, tier in gates[:5]:
    A(f'<path class="drop" d="M {x} {GB} V {RAIL}"/>')
    A(f'<circle class="body" cx="{x}" cy="{RAIL}" r="1.6"/>')
A(f'<path class="rail" d="M 298 {RAIL} H 38 V 116"/>')
A(f'<path class="head" d="M 38 112 l -3.2 7 h 6.4 z"/>')
A(f'<text class="sm" x="206" y="{RAIL+18}" text-anchor="middle">fail: where and why</text>')

# timing gate: label for what passes
A(f'<text class="sm" x="427" y="{PY+18}" text-anchor="middle">winner</text>')

# ---- the model: 24 layers
mx0, mx1, my0 = 456, 524, 65
A('<text class="name" x="490" y="20" text-anchor="middle">Qwen 0.5B</text>')
d = " ".join(f"M {mx0} {my0+i*2} H {mx1}" for i in range(24))
A(f'<path class="layers" d="{d}"/>')
A(f'<rect class="frame" x="{mx0-3}" y="{my0-4}" width="{mx1-mx0+6}" height="{24*2+6}"/>')
A(f'<text class="sm" x="490" y="{my0+70}" text-anchor="middle">8 kernels → 2</text>')
A(f'<text class="sm" x="490" y="{my0+86}" text-anchor="middle">decode 1.02×</text>')

# ---- division
A(f'<path class="div" d="M 16 166 H 524"/>')

# ---- 75 planted bugs: one-shape check vs the judge
def grid(y0, caught):
    for n in range(75):
        c, r = divmod(n, 3)
        x = 160 + c * 7
        y = y0 + r * 7
        if n < caught:
            A(f'<circle class="bug" cx="{x}" cy="{y}" r="2"/>')
        else:
            A(f'<circle class="esc" cx="{x}" cy="{y}" r="2"/>')

A('<text class="sm" x="160" y="190">75 planted bugs</text>')
A('<text x="16" y="214">one-shape check</text>')
grid(204, 40)
A('<text x="342" y="214">35 slip through</text>')
A('<text x="16" y="246">carmen’s judge</text>')
grid(236, 75)
A('<text x="342" y="246">all 75 caught</text>')

A('<circle class="pip" r="3"/>')
A('</svg>')
print("\n".join(o))
