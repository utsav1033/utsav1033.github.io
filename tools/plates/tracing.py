# generates tracing.svg
X0, PX = 140, 30  # waterfall origin and px per second
def x(t): return X0 + t*PX
rows = [  # label, kind, start, end, ttft
 ("turn 1","m",0.0,1.6,0.8),
 ("open app","s",1.7,2.4,None),
 ("turn 2","m",2.5,4.3,3.4),
 ("click Send","s",4.4,4.8,None),
 ("turn 3","m",4.9,6.4,5.6),
 ("upload file","f",6.5,11.6,None),
]
o=[]
SMC='class="sm" '
REDC='class="red" '
A=o.append
A('<svg class="plate-tracing" viewBox="0 0 540 280" role="img" aria-label="Run records from many Macs leave each machine as counts and fixed error words, with spoken words only by consent, gather in one store, and one command prints a single run as a timeline of model turns and steps, the failed step marked in red.">')
A('''<style>
.plate-tracing .fr{fill:none;stroke:var(--hair);stroke-width:.8}
.plate-tracing .st{fill:none;stroke:var(--ink);stroke-width:.9}
.plate-tracing .wd{fill:none;stroke:var(--ink);stroke-width:.9;stroke-dasharray:1.4 2.6}
.plate-tracing .stp{fill:none;stroke:var(--ink);stroke-width:2.2}
.plate-tracing .stp-r{fill:none;stroke:var(--red);stroke-width:2.2}
.plate-tracing .cap{fill:none;stroke:var(--ink);stroke-width:1}
.plate-tracing .cap-r{fill:none;stroke:var(--red);stroke-width:1}
.plate-tracing .wait{fill:var(--card);stroke:var(--ink);stroke-width:.9}
.plate-tracing .strm{fill:var(--ink)}
.plate-tracing .ph{stroke:var(--muted);stroke-width:.8;opacity:0;animation:tr-ph 7s linear infinite}
@keyframes tr-ph{0%{transform:translateX(0);opacity:0}6%{opacity:.9}70%{transform:translateX(348px);opacity:.9}88%{transform:translateX(348px);opacity:.9}100%{transform:translateX(348px);opacity:0}}
@media (prefers-reduced-motion:reduce){.plate-tracing .ph{animation:none;opacity:0}}
</style>''')
# --- Macs and day files
for c in (26,50,74):
    A(f'<rect class="bx" x="18" y="{c-9}" width="22" height="14"/><path class="cap" d="M 13 {c+7.5} H 45"/>')
    A(f'<path class="leader" d="M 48 {c-1} H 58"/>')
    A(f'<path class="bx" d="M 61 {c-8} H 68 L 72 {c-4} V {c+6} H 61 Z"/><path class="leader" d="M 68 {c-8} V {c-4} H 72"/>')
A('<text class="sm" x="29" y="98" text-anchor="middle">Macs</text>')
A('<text class="sm" x="70" y="98" text-anchor="middle">day file</text>')
# boundary (uploader)
A('<path class="guide" d="M 118 12 V 86"/>')
A('<text class="sm" x="118" y="98" text-anchor="middle">uploader</text>')
# solid strands: counts + error words
SX,SY=268,52
for c in (28,56,84):
    A(f'<path class="st" d="M 76 {c-1} C 140 {c-1}, 190 {SY}, {SX} {SY}"/>')
    A(f'<circle class="body" cx="76" cy="{c-1}" r="1.6"/>')
A('<text class="sm" x="158" y="84">counts, error words</text>')
# dotted strand: words, consent only (inline label)
A('<path class="wd" d="M 76 19 H 126"/>')
A('<text class="sm" x="130" y="23">words, if consented</text>')
A('<path class="wd" d="M 240 19 H 282 Q 286 19 286 25 V 31"/>')
A('<circle class="hollow" cx="118" cy="19" r="3"/>')
# store cylinder
A('<path class="bx" d="M 268 36 V 66 A 18 5 0 0 0 304 66 V 36"/><ellipse class="bx" cx="286" cy="36" rx="18" ry="5"/>')
A('<path class="leader" d="M 268 46 A 18 5 0 0 0 304 46"/>')
A('<text class="sm" x="286" y="88" text-anchor="middle">store</text>')
# command
A('<path class="st" d="M 306 52 H 332"/>')
A('<rect class="bx" x="334" y="41" width="58" height="22"/>')
A('<text x="341" y="56.5">$ trace</text>')
A('<text class="sm" x="363" y="88" text-anchor="middle">one command</text>')
# fan out
for y,lab,cls in ((24,"per shortcut","sm"),(52,"failed runs","sm"),(80,"one run","")):
    A(f'<path class="{"st" if not cls else "leader"}" d="M 394 52 C 410 52, 414 {y-4}, 434 {y-4}"/>')
    A(f'<text {SMC if cls else ""}x="440" y="{y}">{lab}</text>')
A('<path class="st" d="M 462 85 V 104"/><path class="cap" d="M 459 100 L 462 104 L 465 100"/>')
# --- report frame
A('<rect class="fr" x="16" y="104" width="508" height="166"/>')
A('<text x="28" y="123">run 4f2a <tspan class="sm" dx="4">file expense, 11.6 s</tspan></text>')
# key
kx=226
A(f'<rect class="wait" x="{kx}" y="115" width="9" height="7"/><rect class="strm" x="{kx+9}" y="115" width="9" height="7"/>')
A(f'<text class="sm" x="{kx+23}" y="123">model call</text>')
A(f'<path class="stp" d="M {kx+94} 118.5 H {kx+112}"/><path class="cap" d="M {kx+94} 115 V 122 M {kx+112} 115 V 122"/>')
A(f'<text class="sm" x="{kx+117}" y="123">step</text>')
A('<text x="512" y="123" text-anchor="end"><tspan class="name">Verdict</tspan><tspan class="red" dx="6">step_failed</tspan></text>')
A('<path class="leader" d="M 16 131 H 524"/>')
# grid + axis
for s in range(0,13,2):
    A(f'<path class="grid" d="M {x(s)} 136 V 246"/>')
    A(f'<path class="tick" d="M {x(s)} 249 V 253"/>')
    A(f'<text class="sm" x="{x(s)}" y="264" text-anchor="middle">{s}{" s" if s==12 else ""}</text>')
A(f'<path class="leader" d="M {x(0)} 249 H {x(12)}"/>')
# rows
for i,(lab,k,a,b,tt) in enumerate(rows):
    cy=146+i*18
    red = k=="f"
    A(f'<text {REDC if red else ""}x="128" y="{cy+4.5}" text-anchor="end">{lab}</text>')
    if k=="m":
        A(f'<rect class="wait" x="{x(a)}" y="{cy-4}" width="{(tt-a)*PX}" height="8"/>')
        A(f'<rect class="strm" x="{x(tt)}" y="{cy-4}" width="{(b-tt)*PX}" height="8"/>')
    elif k=="s":
        A(f'<path class="stp" d="M {x(a)} {cy} H {x(b)}"/><path class="cap" d="M {x(a)} {cy-4} V {cy+4} M {x(b)} {cy-4} V {cy+4}"/>')
    else:
        mid=(x(a)+x(b))/2; g=38
        A(f'<path class="stp-r" d="M {x(a)} {cy} H {mid-g} M {mid+g} {cy} H {x(b)-4}"/>')
        A(f'<path class="cap-r" d="M {x(a)} {cy-4} V {cy+4}"/>')
        A(f'<text class="red" x="{mid}" y="{cy+4.5}" text-anchor="middle">timeout</text>')
        A(f'<path class="xmark" d="M {x(b)-4} {cy-4} l 8 8 M {x(b)-4} {cy+4} l 8 -8"/>')
A(f'<path class="ph" d="M {x(0)} 136 V 246"/>')
A('</svg>')
open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'..','..','_includes','plates','tracing.svg'),'w').write("\n".join(o)+"\n")
