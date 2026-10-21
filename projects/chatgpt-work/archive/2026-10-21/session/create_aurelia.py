import math
from pathlib import Path
from xml.sax.saxutils import escape

OUT=Path('outputs')
BG='#071b29'; GOLD='#d6ad63'; LIGHT='#f3d9a0'; TEAL='#42b9b0'; BLUE='#123d49'
parts=[]
def add(s):parts.append(s)
def path(d,stroke=GOLD,width=1.4,fill='none',extra=''):
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" {extra}/>'
def circle(r,stroke=GOLD,width=1,fill='none',extra=''):
    add(f'<circle cx="0" cy="0" r="{r}" stroke="{stroke}" stroke-width="{width}" fill="{fill}" {extra}/>')
def point(r,a):return (r*math.cos(a),r*math.sin(a))
def xy(p):return f'{p[0]:.4f},{p[1]:.4f}'
def repeat(name,n,offset=0):
    add(f'<g id="{name}-Kreis">')
    for i in range(n):add(f'<use href="#{name}" transform="rotate({360*i/n+offset:.5f})"/>')
    add('</g>')
def radial_wave(base,amp,k,phase,t):return point(base+amp*math.sin(k*t+phase),t)
def wave_d(base,amp,k,phase,start=0,end=2*math.pi,steps=1000):
    return 'M'+' L'.join(xy(radial_wave(base,amp,k,phase,start+(end-start)*i/steps)) for i in range(steps+1))
def weave(base,amp,k,name):
    add(f'<g id="{name}">')
    for phase,col in [(0,GOLD),(math.pi,TEAL)]:
        d=wave_d(base,amp,k,phase)
        add(path(d,BG,15));add(path(d,col,7));add(path(d,LIGHT if phase==0 else '#9de4d4',1.1))
    for j in range(2*k):
        t=j*math.pi/k;phase=0 if j%2==0 else math.pi;col=GOLD if j%2==0 else TEAL
        mask=wave_d(base,amp,k,phase,t-.020,t+.020,30)
        bridge=wave_d(base,amp,k,phase,t-.040,t+.040,40)
        add(path(mask,BG,15));add(path(bridge,col,7));add(path(bridge,LIGHT if j%2==0 else '#9de4d4',1.1))
    add('</g>')

add('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1600" height="1600" viewBox="0 0 1600 1600">')
add('<title>Aurelia – KI-Konstruktion mit verschränkten Bändern und radialem Maßwerk</title>')
add('<defs>')
add('<g id="Krone">')
add(path('M0,-603 C-25,-636 -30,-678 0,-718 C30,-678 25,-636 0,-603Z',GOLD,1.8,BLUE))
add(path('M0,-624 C-13,-648 -17,-678 0,-701 C17,-678 13,-648 0,-624Z',TEAL,1.2))
add(path('M0,-641 L0,-695 M-10,-664 Q0,-675 10,-664',LIGHT,.8))
add('<circle cx="0" cy="-707" r="3" fill="#f3d9a0"/>')
add('</g>')
add('<g id="Lotus">')
add(path('M0,-314 C-62,-346 -86,-433 0,-490 C86,-433 62,-346 0,-314Z',GOLD,1.8,'#0b303b'))
add(path('M0,-333 C-39,-370 -48,-427 0,-470 C48,-427 39,-370 0,-333Z',TEAL,1.3,'#14515a'))
add(path('M0,-350 C-19,-390 -23,-423 0,-452 C23,-423 19,-390 0,-350Z',LIGHT,.8))
add(path('M0,-346 L0,-465 M0,-388 Q-17,-390 -30,-409 M0,-408 Q18,-409 31,-428 M0,-431 L-16,-443',GOLD,.9))
add('<circle cx="0" cy="-326" r="3.2" fill="#d6ad63"/>')
add('</g>')
add('<g id="Innenblatt">')
add(path('M0,-88 C-43,-126 -66,-207 0,-265 C66,-207 43,-126 0,-88Z',GOLD,1.7,'#0a2734'))
add(path('M0,-115 C-28,-151 -37,-202 0,-244 C37,-202 28,-151 0,-115Z',TEAL,1.3,'#15535a'))
add(path('M0,-131 C-12,-160 -20,-202 0,-230 C20,-202 12,-160 0,-131Z',LIGHT,.8))
add(path('M0,-134 L0,-236 M0,-171 Q-18,-167 -25,-183 M0,-188 Q19,-187 26,-202',GOLD,.8))
add('</g>')
add('<g id="Arabeske">')
add(path('M0,-581 C-18,-604 -57,-608 -47,-631 C-36,-652 -13,-629 -30,-619 C-41,-612 -47,-630 -35,-632 M0,-581 C18,-604 57,-608 47,-631 C36,-652 13,-629 30,-619 C41,-612 47,-630 35,-632',GOLD,1.4))
add(path('M0,-586 C-7,-599 -10,-611 0,-621 C10,-611 7,-599 0,-586Z',TEAL,1.1))
add('</g>')
add('<g id="Perlenblatt">')
add(path('M0,-494 Q-13,-510 0,-525 Q13,-510 0,-494Z',LIGHT,1.1,'#134c52'))
add('<circle cx="0" cy="-510" r="2.2" fill="#f3d9a0"/>')
add('</g>')
add('<g id="Zentralblatt">')
add(path('M0,-15 C-25,-28 -28,-62 0,-87 C28,-62 25,-28 0,-15Z',GOLD,1.5,'#16515a'))
add(path('M0,-25 C-11,-41 -14,-59 0,-73 C14,-59 11,-41 0,-25Z',LIGHT,.8))
add('</g>')
add('</defs>')
add(f'<rect width="1600" height="1600" fill="{BG}"/>')
add('<g transform="translate(800 800)">')
add('<g id="Himmelsrand">')
for r,w in [(740,.7),(732,1.5),(724,.6),(599,.8),(591,1.5),(580,.6)]:circle(r,width=w)
for i in range(144):
    a=2*math.pi*i/144
    r1=724 if i%6==0 else 729
    add(path('M'+xy(point(r1,a))+' L'+xy(point(737,a)),GOLD,1.4 if i%6==0 else .7))
for i in range(72):
    p=point(748,2*math.pi*i/72)
    add(f'<circle cx="{p[0]:.4f}" cy="{p[1]:.4f}" r="{2.3 if i%3==0 else 1}" fill="{GOLD}"/>')
add('</g>')
repeat('Krone',24)
repeat('Arabeske',24,7.5)
add('<g id="Geometrisches-Grundnetz">')
for step,r in [(5,455),(7,225)]:
    pts=[point(r,2*math.pi*((i*step)%24)/24-math.pi/2) for i in range(25)]
    add(path('M'+' L'.join(map(xy,pts)),GOLD,.7,extra='opacity="0.48"'))
add('</g>')
repeat('Lotus',24)
for r in [318,309,300]:circle(r,width=.8)
for i in range(96):
    a=2*math.pi*i/96
    add(path('M'+xy(point(302,a))+' L'+xy(point(315,a)),TEAL,.8))
weave(541,33,12,'Aeusseres-Flechtband-24-Kreuzungen')
repeat('Perlenblatt',48,3.75)
repeat('Innenblatt',16,11.25)
weave(279,20,8,'Inneres-Flechtband-16-Kreuzungen')
add('<g id="Filigraner-Sternkranz">')
for r in [99,108,116]:circle(r,width=1)
for i in range(48):
    a=2*math.pi*i/48
    add(path('M'+xy(point(99,a))+' L'+xy(point(115,a)),TEAL,.8))
pts=[point(135 if i%2==0 else 119,math.pi*i/16-math.pi/2) for i in range(32)]
add(path('M'+' L'.join(map(xy,pts))+'Z',GOLD,1.1))
add('</g>')
repeat('Zentralblatt',8)
circle(25,width=1.8,fill=BG)
circle(19,TEAL,.9)
for i in range(8):
    a=i*math.pi/4
    add(path('M'+xy(point(6,a))+' L'+xy(point(15,a)),GOLD,1.2))
circle(5,width=.8,fill=GOLD)
add('</g></svg>')
svg='\n'.join(parts).replace('href="#','xlink:href="#')
(OUT/'KI-Mandala-Aurelia.svg').write_text(svg,encoding='utf-8')
print('Generated',len(svg),'bytes')
