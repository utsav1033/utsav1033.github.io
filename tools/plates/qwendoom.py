import os
D=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','_includes','plates')+'/'
o=[]
FX0,FX1,FY0,FY1=200,330,40,206
MY0,MY1=112,196   # the layers that hold the game
o.append(f'<text class="name" x="{(FX0+FX1)/2}" y="24" text-anchor="middle">the model</text>')
o.append(f'<rect class="bx" x="{FX0}" y="{FY0}" width="{FX1-FX0}" height="{FY1-FY0}"/>')
y=FY0+8
while y<=FY1-6:
    cls='mem' if MY0<=y<=MY1 else 'lay'
    o.append(f'<path class="{cls}" d="M {FX0+10} {y} H {FX1-10}"/>')
    y+=6
# bracket for the memory layers, on the left
o.append(f'<path class="leader" d="M {FX0-8} {MY0} H {FX0-12} V {MY1} H {FX0-8}"/>')
o.append(f'<text class="sm" x="{FX0-18}" y="{MY0+16}" text-anchor="end">its memory</text>')
o.append(f'<text class="sm" x="{FX0-18}" y="{MY0+32}" text-anchor="end">holds the game</text>')
# Doom, written in once
o.append('<rect class="bx" x="28" y="40" width="96" height="44"/>')
o.append('<text class="name" x="76" y="62" text-anchor="middle">Doom</text>')
o.append('<text class="sm" x="76" y="77" text-anchor="middle">code + map</text>')
o.append(f'<path class="guide" d="M 76 84 V 170 H {FX0-22}"/>')
o.append(f'<path class="arrow" d="M {FX0-22} 166 L {FX0-15} 170 L {FX0-22} 174 z"/>')
o.append('<text class="sm" x="28" y="196">written in once,</text>')
o.append('<text class="sm" x="28" y="212">before the first token</text>')
# the token loop, in red
LX=414
o.append(f'<path class="track-r loop" d="M {FX1} 72 H {LX-12} Q {LX} 72 {LX} 84 V 162 Q {LX} 174 {LX-12} 174 H {FX1+12}"/>')
o.append(f'<path class="arrow-r" d="M {FX1+12} 169 L {FX1+5} 174 L {FX1+12} 179 z"/>')
o.append(f'<text class="red" x="{LX+12}" y="112">each token</text>')
o.append(f'<text class="red" x="{LX+12}" y="130">is one CPU step</text>')
o.append(f'<text class="sm" x="{LX+12}" y="150">~3,700 a second</text>')
o.append(f'<text class="sm" x="{FX1+10}" y="64">token out</text>')
o.append(f'<text class="sm" x="{FX1+14}" y="194">back in</text>')
o.append(f'<text class="sm" x="{(FX0+FX1)/2}" y="226" text-anchor="middle">328 layers, nothing trained</text>')
o=[s for s in o if s]
style='''<style>
.plate-qwendoom .lay{stroke:var(--hair);stroke-width:.8}
.plate-qwendoom .mem{stroke:var(--ink);stroke-width:1.2}
.plate-qwendoom .arrow{fill:var(--hair)}
.plate-qwendoom .arrow-r{fill:var(--red)}
.plate-qwendoom .loop{stroke-dasharray:5 3;animation:qdmarch 5s linear infinite}
@keyframes qdmarch{to{stroke-dashoffset:-40}}
@media (prefers-reduced-motion:reduce){.plate-qwendoom .loop{animation:none}}
</style>'''
aria=("Doom's code and map are written once into the memory of a model, a tall stack of layers. "
      "Then, in red, each token the model writes goes back in as the next input, and each token is one step of a CPU.")
open(D+'qwendoom.svg','w').write(f'<svg class="plate-qwendoom" viewBox="0 0 540 240" role="img" aria-label="{aria}">\n{style}\n'+'\n'.join(o)+'\n</svg>\n')
