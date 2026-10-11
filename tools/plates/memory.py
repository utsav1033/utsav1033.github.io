import sys
P=[]
a=P.append
H=266
def arrow(x,y,d,cls='ray',s=4):
    # open chevron head at (x,y) pointing d
    if d=='r': return f'<path class="{cls}" d="M {x-s} {y-s*0.75} L {x} {y} L {x-s} {y+s*0.75}"/>'
    if d=='l': return f'<path class="{cls}" d="M {x+s} {y-s*0.75} L {x} {y} L {x+s} {y+s*0.75}"/>'
    if d=='d': return f'<path class="{cls}" d="M {x-s*0.75} {y-s} L {x} {y} L {x+s*0.75} {y-s}"/>'
    if d=='u': return f'<path class="{cls}" d="M {x-s*0.75} {y+s} L {x} {y} L {x+s*0.75} {y+s}"/>'
def crop(x1,y1,x2,y2,k=7):
    return (f'<path class="mk" d="M {x1} {y1+k} V {y1} H {x1+k} M {x2-k} {y1} H {x2} V {y1+k} '
            f'M {x2} {y2-k} V {y2} H {x2-k} M {x1+k} {y2} H {x1} V {y2-k}"/>')
def cube(cx,cy,s,cls='ray'):
    # isometric cube hairline
    h=s*0.5
    pts=[(cx,cy-s),(cx+s*0.87,cy-h),(cx+s*0.87,cy+h),(cx,cy+s),(cx-s*0.87,cy+h),(cx-s*0.87,cy-h)]
    d='M '+' L '.join(f'{x:.1f} {y:.1f}' for x,y in pts)+' Z'
    d+=f' M {cx-s*0.87:.1f} {cy-h:.1f} L {cx} {cy} L {cx+s*0.87:.1f} {cy-h:.1f} M {cx} {cy} V {cy+s}'
    return f'<path class="{cls}" d="{d}"/>'

a(f'<svg class="plate-memory" viewBox="0 0 540 {H}" role="img" aria-label="A small belief state held in context drives the agent, which acts in the app; each change is verified, appended as a proven diff to a long ledger on disk, and folded back into the belief state. Rewinding loads the belief state from the ledger up to an earlier step instead of replaying the session.">')
a('<style>.plate-memory .mk{fill:none;stroke:var(--muted);stroke-width:.8}'
  '.plate-memory .tape{fill:var(--card);stroke:var(--ink);stroke-width:1}'
  '.plate-memory .ent{stroke:var(--ink);stroke-width:.7}'
  '.plate-memory .ent-r{stroke:var(--red);stroke-width:.9}'
  '.plate-memory .gate{fill:var(--card);stroke:var(--ink);stroke-width:1.1}'
  '.plate-memory .chk{fill:none;stroke:var(--ink);stroke-width:1.3}'
  '.plate-memory .slot{fill:none;stroke:var(--ink);stroke-width:.8;stroke-dasharray:1.5 2}'
  '.plate-memory .head{fill:var(--ink);animation:mhead 7s ease-in-out infinite}'
  '.plate-memory .dot{fill:var(--ink);offset-rotate:0deg;animation:mdot 7s linear infinite}'
  '@keyframes mdot{0%{offset-distance:0%;opacity:0}5%{opacity:1}70%{offset-distance:100%;opacity:1}74%,100%{offset-distance:100%;opacity:0}}'
  '@keyframes mhead{0%,70%{opacity:0}76%,96%{opacity:1}100%{opacity:0}}'
  '@media all{.plate-memory .dot{display:none}.plate-memory .head{animation:none;opacity:1}}'
  '</style>')

# ---- context region
a(crop(24,30,170,132))
a('<text class="sm" x="24" y="148">context</text>')
bx1,by1,bx2,by2=56,50,138,108
# fixed-size dimension line above belief box
cxm=(bx1+bx2)/2
a(f'<path class="leader" d="M {bx1} 36 V 46 M {bx2} 36 V 46 M {bx1} 41 H {cxm-19} M {cxm+19} 41 H {bx2}"/>')
a(f'<text class="sm" x="{cxm}" y="45" text-anchor="middle">fixed</text>')
a(arrow(bx1,41,'l','leader',3)); a(arrow(bx2,41,'r','leader',3))
a(f'<rect class="bx" x="{bx1}" y="{by1}" width="{bx2-bx1}" height="{by2-by1}" rx="1"/>')
a(cube((bx1+bx2)/2,(by1+by2)/2,15))
a(f'<text x="{(bx1+bx2)/2}" y="25" text-anchor="middle">belief state</text>')

# ---- act arrow to app
ay=62
wx1,wy1,wx2,wy2=268,36,352,90
a(f'<path class="ray" d="M {bx2} {ay} H {wx1}"/>'); a(arrow(wx1,ay,'r'))
a(f'<text class="sm" x="{(bx2+wx1)/2}" y="{ay-6}" text-anchor="middle">act</text>')
# app window
a(f'<rect class="bx" x="{wx1}" y="{wy1}" width="{wx2-wx1}" height="{wy2-wy1}" rx="2"/>')
a(f'<path class="leader" d="M {wx1} {wy1+10} H {wx2}"/>')
for i in range(3): a(f'<circle class="hollow" cx="{wx1+7+i*7}" cy="{wy1+5}" r="1.8" style="stroke-width:.7"/>')
a(cube((wx1+wx2)/2+2,(wy1+10+wy2)/2+1,15))
a(f'<text x="{wx2-6}" y="{wy1-6}" text-anchor="end">app</text>')

# ---- verify gate
gx,gy,gr=472,ay,11
a(f'<path class="ray" d="M {wx2} {ay} H {gx-gr}"/>'); a(arrow(gx-gr,ay,'r'))
a(f'<circle class="gate" cx="{gx}" cy="{gy}" r="{gr}"/>')
a(f'<path class="chk" d="M {gx-5} {gy+0.5} L {gx-1.5} {gy+4} L {gx+5} {gy-4}"/>')
a(f'<text x="{gx}" y="{gy-gr-8}" text-anchor="middle">verify</text>')

# ---- ledger tape
tx1,tx2,ty1,ty2=40,476,180,198
brk1,brk2=258,272
step=6
a(crop(24,158,516,240))
a('<text class="sm" x="24" y="256">disk</text>')
a(f'<text x="{tx1}" y="{ty1-8}">ledger</text>')
a(f'<rect class="tape" x="{tx1}" y="{ty1}" width="{tx2-tx1}" height="{ty2-ty1}"/>')
# break gap: paper-coloured band with two slanted lines
ents=[]
x=tx1+step
while x<brk1-2: ents.append(x); x+=step
x=brk2+4
while x<tx2-step: ents.append(x); x+=step
kx=tx1+step*16  # rewind target entry
d=' '.join(f'M {e} {ty1} V {ty2}' for e in ents if e!=kx)
a(f'<path class="ent" d="{d}"/>')
a(f'<rect x="{brk1}" y="{ty1-3}" width="{brk2-brk1}" height="{ty2-ty1+6}" style="fill:var(--card)"/>')
a(f'<path class="ray" d="M {brk1-2} {ty2+4} L {brk1+4} {ty1-4} M {brk2-4} {ty2+4} L {brk2+2} {ty1-4}"/>')
# newest entry (head) + slot being appended
hx=tx2-step
a(f'<rect class="head" x="{hx}" y="{ty1}" width="{step}" height="{ty2-ty1}"/>')
# append line from gate down to head
a(f'<path class="ray" d="M {gx} {gy+gr} V {ty1-2}"/>'); a(arrow(gx,ty1-2,'d'))
a(f'<text class="sm" x="{gx-8}" y="{(ty1+gy)/2+20}" text-anchor="end">append</text>')
a(f'<text class="sm" x="{gx-8}" y="{(ty1+gy)/2+36}" text-anchor="end">if proven</text>')
# update: junction on append line back to belief
uy=98
a(f'<circle class="body" cx="{gx}" cy="{uy}" r="2.2"/>')
a(f'<path class="ray" d="M {gx} {uy} H {bx2}"/>'); a(arrow(bx2,uy,'l'))
a(f'<text class="sm" x="{(bx2+wx1)/2}" y="{uy+16}" text-anchor="middle">update</text>')
# step numerals
a(f'<text class="sm" x="{tx1+step}" y="{ty2+20}" text-anchor="middle">1</text>')
a(f'<text class="sm" x="{hx+step/2}" y="{ty2+20}" text-anchor="middle">500</text>')
# ---- rewind (red): bracket under 1..k, mark entry k, arrow up into belief
a(f'<path class="ent-r" d="M {kx} {ty1-4} V {ty2+4}" style="stroke-width:1.4"/>')
a(f'<path class="lnr" d="M {tx1+2} {ty2+3} V {ty2+6} H {kx} V {ty2+3}"/>')
a(f'<text class="red" x="{kx}" y="{ty2+20}" text-anchor="middle">120</text>')
rx=118
a(f'<path class="ret" d="M {kx} {ty1-6} C {kx} {150}, {rx} {150}, {rx} {by2+3}"/>')
a(arrow(rx,by2+3,'u','lnr'))
a(f'<text class="red" x="{kx+12}" y="152">rewind: load, not replay</text>')
# moving dot along loop belief->app->gate->ledger head
a(f'<circle class="dot" r="2.6" style="offset-path:path(\'M {bx2} {ay} H {gx} V {ty1+9}\')"/>')
# grows dimension under ledger
a(f'<path class="leader" d="M {tx1} 224 V 232 M {tx1} 228 H 210 M 320 228 H {tx2+16}"/>'); a(arrow(tx2+16,228,'r','leader',3))
a(f'<text class="sm" x="265" y="232" text-anchor="middle">grows every step</text>')
a('</svg>')
open(sys.argv[1],'w').write('\n'.join(P)+'\n')
