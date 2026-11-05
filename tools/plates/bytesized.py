import math, random, os
D=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','_includes','plates')+'/'
# bytes after each change in the bytesized README, plain C first
B=[67976,13800,7400,6256,5592,4268,4211,4107,4019,3566,3422,3375,3303,3166,3156,3041,2972,2946]
QR=2953
X0,X1=86,392; YT,YB=30,200; LO,HI=math.log10(2400),math.log10(80000)
def y(b): return YB-(math.log10(b)-LO)/(HI-LO)*(YB-YT)
def x(i): return X0+i*(X1-X0)/(len(B)-1)
o=[]
for lab,b in [("64 KB",65536),("16 KB",16384),("4 KB",4096)]:
    o.append(f'<path class="grid" d="M {X0-6} {y(b):.1f} H {X1+8}"/>')
    o.append(f'<text class="sm" x="{X0-12}" y="{y(b)+4:.1f}" text-anchor="end">{lab}</text>')
# red line: the most a QR code can hold
o.append(f'<path class="ret" d="M {X0-6} {y(QR):.1f} H 456"/>')
o.append(f'<text class="sm red" x="{X0-12}" y="{y(QR)+4:.1f}" text-anchor="end">QR limit</text>')
# staircase
d=f'M {x(0):.1f} {y(B[0]):.1f}'
for i in range(1,len(B)): d+=f' H {x(i):.1f} V {y(B[i]):.1f}'
o.append(f'<path class="track" d="{d}"/>')
for i,b in enumerate(B):
    cls='red-f' if i==len(B)-1 else 'body'
    o.append(f'<circle class="{cls}" cx="{x(i):.1f}" cy="{y(b):.1f}" r="{2.6 if i in (0,len(B)-1) else 1.8}"/>')
# a few notes
o.append(f'<text x="{x(0)+10:.1f}" y="{y(B[0])-4:.1f}">plain C, 67,976 bytes</text>')
for i,lab in [(2,"no libc"),(9,"unpacks itself")]:
    o.append(f'<text class="sm" x="{x(i)+6:.1f}" y="{y(B[i])-7:.1f}">{lab}</text>')
o.append(f'<text class="red" x="{x(17):.1f}" y="{y(B[-1])+22:.1f}" text-anchor="end">2,946 bytes</text>')
# a little QR code, the whole program
random.seed(3); N=21; S=3.4; QX,QY=454,y(QR)-S*N-14
o.append(f'<rect class="bx-r" x="{QX-4}" y="{QY-4:.1f}" width="{N*S+8}" height="{N*S+8}"/>')
cells=[]
def finder(cx,cy):
    for r in range(7):
        for c in range(7):
            if r in(0,6) or c in(0,6) or (2<=r<=4 and 2<=c<=4): cells.append((cx+c,cy+r))
for fx,fy in [(0,0),(N-7,0),(0,N-7)]: finder(fx,fy)
for r in range(N):
    for c in range(N):
        inf=(r<8 and c<8) or (r<8 and c>=N-8) or (r>=N-8 and c<8)
        if not inf and random.random()<.5: cells.append((c,r))
o.append('<path class="qr" d="'+''.join(f'M{QX+c*S:.1f} {QY+r*S:.1f}h{S}v{S}h-{S}z' for c,r in cells)+'"/>')
o.append(f'<text class="sm" x="{QX+N*S/2:.1f}" y="{QY-12:.1f}" text-anchor="middle">the whole program</text>')
style='''<style>
.plate-bytesized .qr{fill:var(--ink)}
.plate-bytesized .ret{animation:bsmarch 6s linear infinite}
@keyframes bsmarch{to{stroke-dashoffset:-42}}
@media (prefers-reduced-motion:reduce){.plate-bytesized .ret{animation:none}}
</style>'''
aria=("A staircase on a log scale: the engine shrinks from 67,976 bytes of plain C to 2,946 bytes over 18 checked changes, "
      "ending just under a red line at 2,953 bytes, the most a QR code can hold. Beside it, a QR code: the whole program.")
open(D+'bytesized.svg','w').write(f'<svg class="plate-bytesized" viewBox="0 0 540 218" role="img" aria-label="{aria}">\n{style}\n'+'\n'.join(o)+'\n</svg>\n')
