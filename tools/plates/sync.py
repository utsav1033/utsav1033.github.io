# time -> x : 0 s at 116, 15 units per second
X=lambda t: 116+15*t
S=52; Y=110; F=170; A=212
o=[]
a=o.append
a('<svg class="plate-sync" viewBox="0 0 540 270" role="img" aria-label="Timeline over 27 seconds. The slow model writes plans while the fast model already acts. The sync layer skips plan steps already done, drops a plan made stale by a wrong step, and holds a send action at a red check before it runs. The task finishes at 19 seconds instead of 27.">')
a('<style>.plate-sync .skip{fill:var(--card);stroke:var(--muted);stroke-width:.8;stroke-dasharray:1.6 1.4}'
  '.plate-sync .strike{fill:none;stroke:var(--ink);stroke-width:1}'
  '.plate-sync .lane{fill:none;stroke:var(--hair);stroke-width:.8}'
  '.plate-sync .chan{fill:none;stroke:var(--rule);stroke-width:.8}'
  '.plate-sync .hold{fill:none;stroke:var(--red);stroke-width:1.1}'
  '.plate-sync .bar{fill:none;stroke:var(--ink);stroke-width:1.4}</style>')
# left labels
a(f'<text x="16" y="{S+4}">slow model</text><text class="sm" x="16" y="{S+21}">writes plans</text>')
a(f'<text class="name" x="16" y="{Y+5}">sync layer</text>')
a(f'<text x="16" y="{F+4}">fast model</text><text class="sm" x="16" y="{F+21}">acts on screen</text>')
# grid verticals at 5 s
for t in (5,10,15):
    a(f'<path class="grid" d="M {X(t)} 30 V {A}"/>')
# lanes
a(f'<path class="lane" d="M {X(0)} {S} H {X(27)}"/>')
a(f'<path class="chan" d="M {X(0)} {Y-8} H {X(27)} M {X(0)} {Y+8} H {X(27)}"/>')
a(f'<path class="lane" d="M {X(0)} {F} H {X(17)}"/>')
a(f'<path class="lane" d="M {X(18)} {F} H {X(19)}"/>')
# slow model plan writing
a(f'<path class="track" d="M {X(0)} {S} H {X(5)-4}"/><path class="track" d="M {X(5)+4} {S} H {X(12)}"/>')
a(f'<text class="sm" x="{(X(0)+X(5))/2}" y="{S-9}" text-anchor="middle">plan 1</text>')
a(f'<text class="sm" x="{(X(5)+X(12))/2}" y="{S-9}" text-anchor="middle">plan 2</text>')
a(f'<path class="guide" d="M {X(12)+4} {S} H {X(19)}"/>')
for t in (5,12):
    a(f'<circle class="body" cx="{X(t)}" cy="{S}" r="3"/><path class="ray" d="M {X(t)} {S+3} V {Y-6}"/>')
# packet 1: steps at 15-unit pitch from arrival
def sq(x,cls): a(f'<rect class="{cls}" x="{x-4}" y="{Y-4}" width="8" height="8"/>')
p1=[X(5),X(6),X(7),X(8)]
sq(p1[0],'skip'); sq(p1[1],'skip'); sq(p1[2],'body'); sq(p1[3],'body')
for x in p1[:2]:
    a(f'<path class="strike" d="M {x-6} {Y+6} L {x+6} {Y-6}"/>')
for x in p1[2:]:
    a(f'<path class="ray" d="M {x} {Y+4} V {F-3}"/>')
# packet 2: stale, dropped
p2=[X(12),X(13),X(14)]
for x in p2: sq(x,'hollow')
a(f'<path class="strike" d="M {p2[0]-8} {Y} H {p2[-1]+8}"/>')
# fast model actions
for t in (1.5,3,7,8,10.5,12,13.5,15):
    a(f'<circle class="body" cx="{X(t)}" cy="{F}" r="3"/>')
# wrong step
w=X(9.5)
a(f'<path class="strike" d="M {w-3.5} {F-3.5} L {w+3.5} {F+3.5} M {w-3.5} {F+3.5} L {w+3.5} {F-3.5}"/>')
a(f'<text class="sm" x="{w}" y="{F+19}" text-anchor="middle">wrong step</text>')
a(f'<path class="guide" d="M {w+3} {F-6} L {p2[0]-4} {Y+10}"/>')
# irreversible: send held at check
s0,s1=X(17),X(18)
a(f'<path class="hold" d="M {s0} {F-3} V {Y} H {s1} V {F}"/>')
a(f'<circle cx="{s0}" cy="{F}" r="3.4" style="fill:var(--red)"/>')
a(f'<circle cx="{(s0+s1)/2}" cy="{Y}" r="6" style="fill:var(--card);stroke:var(--red);stroke-width:1.1"/>')
a(f'<path class="hold" d="M {(s0+s1)/2-3} {Y} l 2.2 2.4 l 4 -5"/>')
a(f'<circle class="body" cx="{s1}" cy="{F}" r="3"/>')
a(f'<text class="red" x="{s0-6}" y="{F+19}" text-anchor="middle">send</text>')
# done + ghost
d=X(19)
a(f'<path class="bar" d="M {d} {F-9} V {F+9}"/>')
a(f'<path class="guide" d="M {d+4} {F} H {X(27)-5}"/><circle class="hollow" cx="{X(27)}" cy="{F}" r="4"/>')
a(f'<text class="sm" x="{(d+X(27))/2}" y="{F+21}" text-anchor="middle">without sync</text>')
# event keys
a(f'<text x="{p1[0]+8}" y="{Y-16}">skips done steps</text>')  # check
a(f'<text x="{p2[0]+8}" y="{Y-16}">drops stale plan</text>')
a(f'<text class="red" x="{s1+10}" y="{Y+28}">checks send</text>')
a(f'<text class="sm red" x="{s1+10}" y="{Y+44}">against task</text>')
# axis
a(f'<path class="ray" d="M {X(0)} {A} H {X(27)}"/>')
for t in (0,5,10,15,19,27):
    a(f'<path class="ray" d="M {X(t)} {A} V {A+5}"/>')
for t in (0,5,10,15):
    a(f'<text class="sm" x="{X(t)}" y="{A+19}" text-anchor="middle">{t}</text>')
a(f'<text x="{X(19)}" y="{A+19}" text-anchor="middle">19 s</text>')
a(f'<text class="sm" x="{X(27)}" y="{A+19}" text-anchor="middle">27 s</text>')
a(f'<text class="sm" x="16" y="{A+19}">time</text>')
a(f'<path class="ray" d="M {X(19)} {A+28} V {A+34} H {X(27)} V {A+28}"/>')
a(f'<text x="{(X(19)+X(27))/2}" y="{A+50}" text-anchor="middle">8 s saved</text>')
a('</svg>')
open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'..','..','_includes','plates','sync.svg'),'w').write('\n'.join(o)+'\n')
