import math, random
def f(x): return f"{x:.1f}"

# ---------- Plate I: Taskmaster trajectory ----------
def cubic(p0,p1,p2,p3,t):
    u=1-t; return (u**3*p0[0]+3*u*u*t*p1[0]+3*u*t*t*p2[0]+t**3*p3[0], u**3*p0[1]+3*u*u*t*p1[1]+3*u*t*t*p2[1]+t**3*p3[1])
P=[(36,150),(170,150),(330,120),(492,36)]
pts=[cubic(*P,i/400) for i in range(401)]
L=[0]
for i in range(1,401): L.append(L[-1]+math.dist(pts[i-1],pts[i]))
tot=L[-1]
def at(frac):
    d=frac*tot
    for i in range(1,401):
        if L[i]>=d: return pts[i], L[i]/tot
stops=[0.04+i*(0.92/6) for i in range(7)]
nodes=[at(s) for s in stops]
roman=['i','ii','iii','iv','v','vi','vii']
tm=['<g transform="translate(0,28)">']
tm.append(f'<path class="guide" d="M {P[0][0]} {P[0][1]} C {P[1][0]} {P[1][1]}, {P[2][0]} {P[2][1]}, {P[3][0]} {P[3][1]}"/>')
for k,((x,y),_) in enumerate(nodes):
    tm.append(f'<circle class="hollow" cx="{f(x)}" cy="{f(y)}" r="4"/>')
    tm.append(f'<path class="leader" d="M {f(x)} {f(y+7)} V {f(y+16)}"/><text class="sm" x="{f(x)}" y="{f(y+28)}" text-anchor="middle">{roman[k]}</text>')
(x3,y3),_=nodes[2]; (x7,y7),_=nodes[6]
tm.append(f'<path class="ret" d="M {f(x7-6)} {f(y7-6)} Q {f((x3+x7)/2)} {f(min(y3,y7)-70)} {f(x3+2)} {f(y3-8)}"/>')
tm.append(f'<text class="red" x="{f((x3+x7)/2+20)}" y="{f(min(y3,y7)-26)}" text-anchor="middle">return to iii: load it, don’t replay</text>')
# keyframes for the present body (walks forward, then jumps back to iii, then on to vi)
fr=[s for s in stops]
seq=[(0,fr[0]),(9,fr[1]),(18,fr[2]),(27,fr[3]),(36,fr[4]),(45,fr[5]),(54,fr[6]),(70,fr[2]),(84,fr[5])]
kf='@keyframes present{'+''.join(f'{p}%{{offset-distance:{d*100:.1f}%}}' for p,d in seq)+'100%{offset-distance:'+f'{fr[5]*100:.1f}'+'%}}'
tm_path=f'M {P[0][0]} {P[0][1]} C {P[1][0]} {P[1][1]}, {P[2][0]} {P[2][1]}, {P[3][0]} {P[3][1]}'
tm.append(f'<g class="present" style="offset-path:path(\'{tm_path}\');offset-rotate:0deg"><circle class="ring" r="10"/><circle class="body" r="4.6"/></g>')
tm.append('</g>')
tm.append('<g transform="translate(14,22)"><circle class="body" cx="0" cy="0" r="4"/><text x="10" y="4">the present step, the only one in context</text>'
          '<circle class="hollow" cx="0" cy="18" r="4"/><text x="10" y="22">a step saved to disk once it checked out</text></g>')
plate1='\n'.join(tm)

# ---------- Plate II: run tracing as an optics plate ----------
tr=[]
src=[(40,40,'Mac A'),(40,96,'Mac B'),(40,152,'Mac C')]
store=(190,96); lens_x=300; screen_x=430
for i,(x,y,n) in enumerate(src):
    tr.append(f'<circle class="hollow" cx="{x}" cy="{y}" r="5"/><text x="{x-12}" y="{y+4}" text-anchor="end">{n}</text>')
    tr.append(f'<path class="ray" id="r{i}" d="M {x+5} {y} L {store[0]-7} {store[1]}"/>')
tr.append(f'<path class="consent" d="M 45 46 Q 110 30 {store[0]-6} {store[1]-9}"/>')
tr.append(f'<text class="sm" x="96" y="26">words: only with consent</text>')
tr.append(f'<circle class="ring" cx="{store[0]}" cy="{store[1]}" r="11"/><circle class="body" cx="{store[0]}" cy="{store[1]}" r="3"/>')
tr.append(f'<path class="leader" d="M {store[0]} {store[1]+14} V 150"/><text x="{store[0]}" y="164" text-anchor="middle">diagnostics</text>')
tr.append(f'<path class="ray" d="M {store[0]+11} {store[1]} L {lens_x-6} {store[1]}"/>')
tr.append(f'<ellipse class="lens" cx="{lens_x}" cy="{store[1]}" rx="7" ry="44"/>')
tr.append(f'<path class="leader" d="M {lens_x} {store[1]+48} V 150"/><text x="{lens_x}" y="164" text-anchor="middle">one command</text>')
rows=[(56,'steps'),(76,'model calls'),(96,'tokens, timings'),(116,'reason it stopped')]
for y,lab in rows:
    tr.append(f'<path class="ray" d="M {lens_x+7} {store[1]} L {screen_x} {y}"/>')
tr.append(f'<path class="screen" d="M {screen_x} 40 V 152"/>')
for y,lab in rows:
    tr.append(f'<text x="{screen_x+8}" y="{y+4}">{lab}</text>')
tr.append(f'<text class="red" x="{screen_x+8}" y="140">failed at step v</text>')
for i,(x,y,n) in enumerate(src):
    tr.append(f'<circle class="body photon" style="offset-path:path(\'M {x+5} {y} L {store[0]-7} {store[1]} L {lens_x} {store[1]} L {screen_x} {116}\');animation-delay:{i*1.4:.1f}s" r="2.6"/>')
plate2='\n'.join(tr)

# ---------- Plate III: FlowGap as a star chart ----------
random.seed(7)
sc=[]
cx,cy=260,128
for r in (90,150,210):
    sc.append(f'<circle class="grid" cx="{cx}" cy="{cy+120}" r="{r}"/>')
for a in range(-60,61,30):
    t=math.radians(a-90); sc.append(f'<path class="grid" d="M {cx} {cy+120} L {f(cx+260*math.cos(t))} {f(cy+120+260*math.sin(t))}"/>')
# faint noise stars
for _ in range(46):
    x=random.uniform(14,506); y=random.uniform(12,214)
    sc.append(f'<circle class="faint tw" style="animation-delay:{random.uniform(0,6):.1f}s" cx="{f(x)}" cy="{f(y)}" r="{random.choice([0.7,0.9,1.1])}"/>')
cons=[('Reschedule',[(70,62),(96,44),(120,58),(112,84),(84,90)],[(0,1),(1,2),(2,3),(3,4),(4,0)],(96,112)),
      ('Billing',[(214,40),(240,30),(266,46),(252,70)],[(0,1),(1,2),(2,3)],(240,92)),
      ('Cancel',[(390,52),(414,40),(438,58),(424,82),(400,80)],[(0,1),(1,2),(2,3),(3,4)],(414,104))]
for k,(name,st,ed,lab) in enumerate(cons):
    for a,b in ed:
        (x1,y1),(x2,y2)=st[a],st[b]
        sc.append(f'<path class="cons draw" style="animation-delay:{k*0.5:.1f}s" d="M {x1} {y1} L {x2} {y2}"/>')
    for i,(x,y) in enumerate(st): sc.append(f'<circle class="star" cx="{x}" cy="{y}" r="{2.6 if i==0 else 1.9}"/>')
    sc.append(f'<text class="name" x="{lab[0]}" y="{lab[1]}" text-anchor="middle">{name}</text><text class="sm" x="{lab[0]}" y="{lab[1]+14}" text-anchor="middle">in the flow</text>')
gap=[(232,150),(254,140),(276,156),(262,176),(240,174),(286,180),(250,160)]
for i,(x,y) in enumerate(gap): sc.append(f'<circle class="star red-f" cx="{x}" cy="{y}" r="{2.6 if i==0 else 1.9}"/>')
sc.append('<g class="gapmark"><circle class="gapring" cx="259" cy="161" r="40"/>'
          '<path class="leader-r" d="M 299 168 L 352 182"/><text class="red" x="358" y="180">unnamed: no node in the flow</text>'
          '<text class="red sm" x="358" y="196">where 49% of calls went</text></g>')
plate3='\n'.join(sc)

# ---------- Plate IV: carmen as concentric gates ----------
cm=[]; cx,cy=200,124
R=[104,84,64,44,24]; names=['compiles','matches the answer key','fresh random inputs','secret inputs','timed against MLX']
for k in range(0,360,10):
    t=math.radians(k); r1=R[0]+3; r2=R[0]+(8 if k%30==0 else 5)
    cm.append(f'<path class="tick" d="M {f(cx+r1*math.cos(t))} {f(cy+r1*math.sin(t))} L {f(cx+r2*math.cos(t))} {f(cy+r2*math.sin(t))}"/>')
for k,r in enumerate(R):
    cm.append(f'<circle class="orbit" cx="{cx}" cy="{cy}" r="{r}"/>')
    th=math.radians(-72+k*16); px,py=cx+r*math.cos(th),cy+r*math.sin(th); ly=34+k*24
    cm.append(f'<circle class="body" cx="{f(px)}" cy="{f(py)}" r="1.6"/><path class="leader" d="M {f(px)} {f(py)} L 338 {ly-4}"/><text x="344" y="{ly}">{names[k]}</text>')
cm.append(f'<circle class="body" cx="{cx}" cy="{cy}" r="5"/><text class="sm" x="{cx}" y="{cy-10}" text-anchor="middle">model</text>')
def endp(r,deg): t=math.radians(deg); return cx+r*math.cos(t),cy+r*math.sin(t)
ax,ay=endp(64,208); bx,by=endp(44,146)
tracks=[('A',(28,30),(96,22),(ax,ay),'fail'),('B',(28,222),(100,236),(bx,by),'fail'),('C',(20,128),(110,176),(cx-5,cy),'pass')]
for i,(n,s,c,e,kind) in enumerate(tracks):
    cls='track-r' if kind=='fail' else 'track'
    cm.append(f'<path class="{cls} draw2" style="animation-delay:{i*1.6:.1f}s" d="M {s[0]} {s[1]} Q {c[0]} {c[1]} {f(e[0])} {f(e[1])}"/>')
    cm.append(f'<text x="{s[0]-4}" y="{s[1]+4}" text-anchor="end">{n}</text>')
    if kind=='fail':
        x,y=e; cm.append(f'<path class="xmark" style="animation-delay:{i*1.6+1.2:.1f}s" d="M {f(x-4)} {f(y-4)} L {f(x+4)} {f(y+4)} M {f(x+4)} {f(y-4)} L {f(x-4)} {f(y+4)}"/>')
cm.append('<text class="sm" x="344" y="176">A: a bug at length 257</text><text class="sm" x="344" y="192">B: fp16 rounding</text><text class="sm" x="344" y="208">C: 1.82× faster, into Qwen</text>')
plate4='\n'.join(cm)

import os
ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
OUT=os.path.join(ROOT,'_includes','plates')
P6='%.1f'%(stops[5]*100)
SVG={
 'taskmaster':('0 0 520 214','Seven steps along a course, each saved to disk. A dark body marks the one step held in context; it moves forward step by step, then returns to step three by loading it.',plate1),
 'tracing':('-46 0 586 172','Records from three Macs converge on the diagnostics store, pass through one command, and show on a screen: steps, model calls, tokens and timings, the reason it stopped, failed at step five.',plate2),
 'flowgap':('0 0 520 220','A star chart of calls. Three constellations are named Reschedule, Billing and Cancel and exist in the flow. A fourth, in red, has no name: no node in the flow, where 49 percent of calls went.',plate3),
 'carmen':('0 0 540 248','Five concentric gates around the model. Draft A stops at the fresh random inputs ring, draft B at the secret inputs ring, and draft C passes every ring to reach the model.',plate4)}
for name,(vb,label,body) in SVG.items():
    with open(os.path.join(OUT,name+'.svg'),'w') as fh:
        fh.write(f'<svg class="plate-{name}" viewBox="{vb}" role="img" aria-label="{label}">\n{body}\n</svg>\n')
with open(os.path.join(ROOT,'assets','css','plates-motion.css'),'w') as fh:
    fh.write('/* generated by tools/plates.py */\n'+kf+'\n@media (prefers-reduced-motion:reduce){.plate-taskmaster .present{animation:none;offset-distance:'+P6+'%}}\n')
print('wrote', ', '.join(SVG))
