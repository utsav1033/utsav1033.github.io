import random, math
random.seed(7)
import os; D=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','_includes','plates')+'/'
TX=292; NX=312; LX=324
rows=[("Book appointment",70,(150,48)),("Reschedule / cancel",96,(62,66)),("Insurance / TPA",122,(200,108)),
      ("Billing &amp; payment",148,(90,122)),("Clinic info",174,(184,160)),("Prescription refill",200,(58,180))]
GY=232; GC=(132,218)
o=[]
def cloud(c,n,s,cls,r=1.6):
    pts=[]
    while len(pts)<n:
        x=random.gauss(c[0],s); y=random.gauss(c[1],s*0.8)
        if math.hypot(x-c[0],y-c[1])<s*1.9: pts.append((x,y))
    return ''.join(f'<circle class="{cls}" cx="{x:.1f}" cy="{y:.1f}" r="{r}"/>' for x,y in pts)
def lead(c,t,r0):
    dx,dy=t[0]-c[0],t[1]-c[1]; L=math.hypot(dx,dy)
    return (c[0]+dx/L*r0, c[1]+dy/L*r0, t[0]-dx/L*5, t[1]-dy/L*5)
# frame corner ticks
for x,y,sx,sy in [(14,32,1,1),(246,32,-1,1),(14,250,1,-1),(246,250,-1,-1)]:
    o.append(f'<path class="leader" d="M {x} {y+8*sy} V {y} H {x+8*sx}"/>')
o.append('<text class="sm" x="14" y="22">298 calls, embedded</text>')
o.append(f'<text class="sm" x="{TX-8}" y="22">declared flow</text>')
# noise
for _ in range(9):
    o.append(f'<circle class="faint" cx="{random.uniform(26,236):.1f}" cy="{random.uniform(42,244):.1f}" r="1.3"/>')
# leaders first (under dots)
for name,y,c in rows:
    a=lead(c,(TX-1,y),17)
    o.append(f'<path class="guide m" d="M {a[0]:.1f} {a[1]:.1f} L {a[2]:.1f} {a[3]:.1f}"/>')
a=lead(GC,(TX-1,GY),25)
o.append(f'<path class="ret flow" d="M {a[0]:.1f} {a[1]:.1f} L {a[2]:.1f} {a[3]:.1f}"/>')
for name,y,c in rows:
    o.append(cloud(c,12,8.5,'body',1.5))
o.append(cloud(GC,13,8,'red-f',1.7))
o.append(f'<circle class="gapring" cx="{GC[0]}" cy="{GC[1]}" r="22"/>')
o.append(f'<text class="red" x="{GC[0]-30}" y="{GC[1]-4}" text-anchor="end">no node</text>')
o.append(f'<text class="sm" x="{GC[0]-30}" y="{GC[1]+12}" text-anchor="end">13 calls</text>')
# tree
o.append(f'<path class="ray" d="M {TX} 40 V 200"/>')
o.append(f'<path class="lnr" stroke-dasharray="3 2.5" d="M {TX} 200 V {GY} H {NX-5}"/>')
o.append(f'<circle class="body" cx="{TX}" cy="40" r="3"/>')
o.append(f'<text x="{TX+12}" y="45">Classify intent</text>')
for name,y,c in rows:
    o.append(f'<path class="ray" d="M {TX} {y} H {NX-4}"/><circle class="hollow" cx="{NX}" cy="{y}" r="4"/>')
    o.append(f'<text x="{LX}" y="{y+5}">{name}</text>')
o.append(f'<circle class="ghost" cx="{NX}" cy="{GY}" r="5"/>')
o.append(f'<text class="red" x="{LX}" y="{GY+5}">Lab reports</text>')
o.append(f'<text class="sm red" x="{LX+70}" y="{GY+5}">drafted node</text>')
style='''<style>
.plate-flowgap .ghost{fill:var(--card);stroke:var(--red);stroke-width:1.2;stroke-dasharray:2.4 1.8}
.plate-flowgap .m{stroke:var(--muted);stroke-width:.8;stroke-dasharray:1.2 2.6}
.plate-flowgap .flow{animation:fgmarch 6s linear infinite}
@keyframes fgmarch{to{stroke-dashoffset:-42}}
@media all{.plate-flowgap .flow{animation:none}}
</style>'''
aria=("Left: 298 call transcripts embedded and clustered into intent clouds. Six clouds map by dotted lines onto the six nodes of the declared flow under Classify intent. "
      "A seventh cloud, in red, matches no node (13 calls) and is wired in as a dashed, drafted node: Lab reports.")
svg=f'<svg class="plate-flowgap" viewBox="0 0 540 256" role="img" aria-label="{aria}">\n{style}\n'+'\n'.join(o)+'\n</svg>\n'
open(D+'flowgap.svg','w').write(svg)
