import os, sys
S=56; F=118          # slow line, fast line
L0, L1 = 124, 524    # line extent
o=[]; a=o.append
a('<svg class="plate-sync" viewBox="0 0 540 168" role="img" aria-label="Two lines: the fast model takes many quick steps, the slow model fewer, later ones. A slow-model step the fast model already did is skipped. A send step is checked before it runs. The task drops from 27 to 19 seconds.">')
a('<style>.plate-sync .lane{fill:none;stroke:var(--hair);stroke-width:1}'
  '.plate-sync .skip{fill:var(--card);stroke:var(--muted);stroke-width:1;stroke-dasharray:2 1.6}'
  '.plate-sync .strike{fill:none;stroke:var(--ink);stroke-width:1.2}'
  '.plate-sync .chk{fill:var(--card);stroke:var(--red);stroke-width:1.3}'
  '.plate-sync .bar{fill:none;stroke:var(--ink);stroke-width:1.4}</style>')
# lines + labels
a(f'<text x="16" y="{S+5}">slow model</text><text x="16" y="{F+5}">fast model</text>')
a(f'<path class="lane" d="M {L0} {S} H {L1} M {L0} {F} H 436"/>')
# fast model: many quick steps
send=372
for x in (144,172,200,228,256,284,312,340,400):
    a(f'<circle class="body" cx="{x}" cy="{F}" r="4"/>')
# done bar + time note
a(f'<path class="bar" d="M 436 {F-10} V {F+10}"/>')
a(f'<text x="448" y="{F+5}">27 s → 19 s</text>')
# slow model: fewer, later steps
sk=252
def sq(x,cls): a(f'<rect class="{cls}" x="{x-5}" y="{S-5}" width="10" height="10"/>')
sq(sk,'skip')
a(f'<path class="strike" d="M {sk-8} {S+8} L {sk+8} {S-8}"/>')
sq(352,'body'); sq(452,'body')
# interaction 1: already done -> skipped
a(f'<path class="guide" d="M {sk-4} {S+8} L 176 {F-6}"/>')
a(f'<text x="{sk}" y="{S-16}" text-anchor="middle">already done, skipped</text>')
# interaction 2: send checked before it runs
a(f'<path class="ret" d="M {send} {S} V {F-9}"/>')
a(f'<circle class="chk" cx="{send}" cy="{F}" r="8"/>')
a(f'<path class="hold" style="fill:none;stroke:var(--red);stroke-width:1.3" d="M {send-3.6} {F+.3} l 2.6 2.8 l 4.8 -6"/>')
a(f'<text class="red" x="{send}" y="{F+30}" text-anchor="middle">send, checked first</text>')
a('</svg>')
out=sys.argv[1] if len(sys.argv)>1 else os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','_includes','plates','sync.svg')
open(out,'w').write('\n'.join(o)+'\n')
