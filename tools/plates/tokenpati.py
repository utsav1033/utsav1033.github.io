import os
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '_includes', 'plates') + '/'

# tokenpati's own maths (src/budget.rs) on an M4 with 16 GiB, Q4_K_M, 8k context:
#   weights = params * 0.56 B * 1.10 ; kv = 2 * layers * kv_heads * head_dim * 8192 * 2 B
GIB = 1024 ** 3
def w(params_b): return params_b * 1e9 * 0.56 * 1.10 / GIB
def kv(layers, heads, dim): return 2 * layers * heads * dim * 8192 * 2 / GIB
ROWS = [  # name, weights, kv, tok/s, verdict
    ("Qwen3 8B", w(8.2), kv(36, 8, 128), "18 tok/s", "runs fast"),
    ("Qwen3 14B", w(14.8), kv(40, 8, 128), "10 tok/s", "runs"),
    ("Mistral Small 24B", w(24.0), kv(40, 8, 128), "", "too big"),
]
X0, PX = 36, 19.0           # x of 0 GiB, px per GiB
USABLE, TOTAL = 12.0, 16.0  # Apple GPUs get ~75% of unified memory
XU, XT = X0 + USABLE * PX, X0 + TOTAL * PX
RY = [70, 122, 174]         # bar tops
BH = 13
H = 252

o = []
a = o.append
aria = ("Three models measured against the usable memory of an Apple M4 with 16 GiB. Each bar is weights plus KV cache. "
        "Qwen3 8B fits and runs fast at 18 tokens a second; Qwen3 14B fits and runs at 10; "
        "Mistral Small 24B needs 15 GiB, crosses the 12 GiB usable line, and is too big.")
a(f'<svg class="plate-tokenpati" viewBox="0 0 540 {H}" role="img" aria-label="{aria}">')
a('<defs><pattern id="tp-hatch" width="4" height="4" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
  '<path d="M 0 0 V 4" class="tp-h"/></pattern></defs>')
a('<style>'
  '.plate-tokenpati .tp-h{stroke:var(--ink);stroke-width:.8}'
  '.plate-tokenpati .wt{fill:url(#tp-hatch);stroke:var(--ink);stroke-width:1}'
  '.plate-tokenpati .kv{fill:var(--card);stroke:var(--ink);stroke-width:1}'
  '.plate-tokenpati .over{fill:var(--red);opacity:.22}'
  '.plate-tokenpati .lim{fill:none;stroke:var(--red);stroke-width:1.1;stroke-dasharray:4 3}'
  '.plate-tokenpati .bound{fill:none;stroke:var(--hair);stroke-width:.9}'
  '</style>')

# header
a(f'<text class="name" x="{X0}" y="24">Apple M4</text>')
a(f'<text class="sm" x="{X0 + 74}" y="24">16 GiB unified · 4-bit · 8k context</text>')

# chip boundary and usable line
a(f'<path class="bound" d="M {XT} 40 V {RY[-1] + BH + 12}"/>')
a(f'<text class="sm" x="{XT}" y="{RY[-1] + BH + 26}" text-anchor="middle">16 GiB</text>')
a(f'<path class="lim" d="M {XU} 40 V {RY[-1] + BH + 12}"/>')
a(f'<text class="red" x="{XU}" y="{RY[-1] + BH + 26}" text-anchor="middle">usable 12</text>')

for (name, wt, k, tps, verdict), y in zip(ROWS, RY):
    total = wt + k
    big = total > USABLE
    a(f'<text x="{X0}" y="{y - 7}">{name}</text>')
    a(f'<text class="sm" x="{X0 + (XU - X0) - 6}" y="{y - 7}" text-anchor="end">{total:.1f} GiB</text>')
    xw = X0 + wt * PX
    a(f'<rect class="wt" x="{X0}" y="{y}" width="{xw - X0:.1f}" height="{BH}"/>')
    a(f'<rect class="kv" x="{xw:.1f}" y="{y}" width="{k * PX:.1f}" height="{BH}"/>')
    if big:
        a(f'<rect class="over" x="{XU}" y="{y}" width="{X0 + total * PX - XU:.1f}" height="{BH}"/>')
    # verdict column
    vx = XT + 28
    if tps:
        a(f'<text x="{vx}" y="{y + 11}">{tps}</text>')
        a(f'<text class="sm" x="{vx}" y="{y + 27}">{verdict}</text>')
    else:
        a(f'<text class="red" x="{vx}" y="{y + 11}">{verdict}</text>')
        a(f'<text class="sm" x="{vx}" y="{y + 27}">never downloads</text>')

# key and the speed rule
ky = H - 18
a(f'<rect class="wt" x="{X0}" y="{ky - 10}" width="16" height="10"/>')
a(f'<text class="sm" x="{X0 + 22}" y="{ky}">weights</text>')
a(f'<rect class="kv" x="{X0 + 84}" y="{ky - 10}" width="16" height="10"/>')
a(f'<text class="sm" x="{X0 + 106}" y="{ky}">KV cache</text>')
a(f'<text class="sm" x="{XT + 28}" y="{ky}">speed ≈ bandwidth ÷ bytes</text>')

a('</svg>')
open(D + 'tokenpati.svg', 'w').write('\n'.join(o) + '\n')
print('\n'.join(f'{n}: {w_:.2f} + {k:.2f} = {w_ + k:.2f} GiB' for n, w_, k, _, _ in ROWS))
