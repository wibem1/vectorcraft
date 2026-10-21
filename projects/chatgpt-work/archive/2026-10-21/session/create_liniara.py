import json, math, copy
from pathlib import Path

root=json.loads(Path('outputs/KI-Mandala-Sonnenrosette.vectorcraft').read_text(encoding='utf-8'))
doc=root['document']; counter=0
INK='#163b50'; TEAL='#258b88'; GOLD='#ad7c38'; PAPER='#f5f0e6'
def uid():
    global counter
    counter+=1;return counter
def paint(color):
    if color is None:return {'type':'none'}
    return {'type':'solid','color':{'model':'rgb','r':int(color[1:3],16)/255,'g':int(color[3:5],16)/255,'b':int(color[5:7],16)/255}}
def appearance(color=INK,width=1,fill=None):
    return {'items':[{'kind':'fill','paint':paint(fill)}, {'kind':'stroke','paint':paint(color),'width':width}]}
def path(anchors,closed=False,color=INK,width=1,fill=None):
    return {'id':uid(),'appearance':appearance(color,width,fill),
            'kind':{'type':'path','path':{'subpaths':[{'anchors':anchors,'closed':closed}]}}}
def bezier(start,segments,closed=False,color=INK,width=1,fill=None):
    a=[{'p':list(start)}]
    for c1,c2,end in segments:
        a[-1]['out']=list(c1);a.append({'p':list(end),'in':list(c2)})
    return path(a,closed,color,width,fill)
def line(points,color=INK,width=1,closed=False):return path([{'p':list(p)} for p in points],closed,color,width)
def circle(x,y,r,color=INK,width=1,fill=None):
    k=.5522847498307936*r
    return path([{'p':[x+r,y],'in':[x+r,y-k],'out':[x+r,y+k]},
                 {'p':[x,y+r],'in':[x+k,y+r],'out':[x-k,y+r]},
                 {'p':[x-r,y],'in':[x-r,y+k],'out':[x-r,y-k]},
                 {'p':[x,y-r],'in':[x-k,y-r],'out':[x+k,y-r]}],True,color,width,fill)
def group(name,children):return {'id':uid(),'name':name,'kind':{'type':'group','clip':False,'children':children}}
def layer(name,children):return {'id':uid(),'name':name,'kind':{'type':'layer','color':{'Preset':0},'template':False,'printable':True,'children':children}}
symbols=[];sizes={}
def symbol(name,w,h,children):
    art=group(name,children)
    def normalize(n):
        if n['kind']['type']=='path':
            for sub in n['kind']['path']['subpaths']:
                for a in sub['anchors']:
                    for key in ('p','in','out'):
                        if key in a:a[key]=[a[key][0]*20/w,a[key][1]*20/h]
        for c in n['kind'].get('children',[]):normalize(c)
    normalize(art);symbols.append({'name':name,'art':art});sizes[name]=[w,h]

# Six true shared definitions. All linework inside the motifs stays editable.
petals=[]
for j in range(8):
    w=57-j*6.2
    petals.append(bezier((0,112),[((-w,55),(-w,-65),(0,-116)),((w,-65),(w,55),(0,112))],True,
                         INK if j%2==0 else TEAL,1.3 if j==0 else .75))
for y in range(-72,80,22):
    w=33*(1-(y/135)**2)
    petals.append(bezier((0,y+20),[((-w*.6,y+10),(-w,y-8),(-w,y-20))],color=GOLD,width=.8))
    petals.append(bezier((0,y+20),[((w*.6,y+10),(w,y-8),(w,y-20))],color=GOLD,width=.8))
petals.append(line([(0,106),(0,-109)],GOLD,.8))
symbol('Federfächer · Linien',120,240,petals)

arches=[]
for j in range(7):
    w=53-j*6.5;tip=-99+j*6;base=99-j*6
    arches.append(bezier((0,base),[((-w,42),(-w,-47),(0,tip)),((w,-47),(w,42),(0,base))],True,
                         GOLD if j%3==0 else INK,1 if j==0 else .75))
arches.append(line([(0,-91),(0,91)],TEAL,.9))
symbol('Spitzbogen · Maßwerk',116,210,arches)

core=[]
for j in range(5):
    w=25-j*4
    core.append(bezier((0,53),[((-w,23),(-w,-24),(0,-54)),((w,-24),(w,23),(0,53))],True,TEAL if j%2 else INK,.85))
core.append(line([(0,-50),(0,50)],GOLD,.75))
symbol('Kernblatt · Linien',56,116,core)

lancets=[]
for j in range(4):
    w=19-j*4
    lancets.append(bezier((0,48),[((-w,12),(-w,-20),(0,-49)),((w,-20),(w,12),(0,48))],True,INK if j%2==0 else GOLD,.8))
lancets.append(line([(0,-45),(0,45)],TEAL,.7))
symbol('Randlanzette',44,104,lancets)

bridges=[]
for j in range(5):
    offset=j*4
    bridges.append(bezier((-56,20-offset),[((-34,-28+offset),(34,-28+offset),(56,20-offset))],color=GOLD if j%2 else TEAL,width=.8))
bridges.append(bezier((-48,10),[((-64,-9),(-37,-31),(-25,-13)),((-14,5),(-43,12),(-41,-4))],color=INK,width=.9))
bridges.append(bezier((48,10),[((64,-9),(37,-31),(25,-13)),((14,5),(43,12),(41,-4))],color=INK,width=.9))
symbol('Bogenbrücke · Arabeske',132,66,bridges)

pearls=[line([(0,-15),(0,15)],GOLD,.7),circle(0,-15,2.5,INK,.7),circle(0,15,2.5,INK,.7),circle(0,0,3,TEAL,.7)]
symbol('Perlenachse',18,38,pearls)

def instances(name,count,radius,scale=1,offset=0):
    out=[];w,h=sizes[name]
    for j in range(count):
        theta=2*math.pi*j/count+math.radians(offset)
        co,si=math.cos(theta),math.sin(theta)
        out.append({'id':uid(),'name':f'{name} {j+1:02}',
                    'kind':{'type':'symbolinstance','symbol':name,
                            'xf':[co*w/20*scale,si*w/20*scale,-si*h/20*scale,co*h/20*scale,
                                  800+radius*math.sin(theta),800-radius*math.cos(theta)]}})
    return out

background=path([{'p':[0,0]},{'p':[1600,0]},{'p':[1600,1600]},{'p':[0,1600]}],True,None,0,PAPER)
background['name']='Papierhintergrund'
geometry=[]
def wave(base,amp,k,phase,color,width):
    n=384;h=2*math.pi/n;anchors=[]
    for i in range(n):
        a=i*h;r=base+amp*math.cos(k*a+phase);dr=-amp*k*math.sin(k*a+phase)
        x=800+r*math.cos(a);y=800+r*math.sin(a)
        dx=dr*math.cos(a)-r*math.sin(a);dy=dr*math.sin(a)+r*math.cos(a)
        anchors.append({'p':[x,y],'in':[x-dx*h/3,y-dy*h/3],'out':[x+dx*h/3,y+dy*h/3]})
    return path(anchors,True,color,width)
for r in [35,42,149,156,166,302,306,568,574,610,615,710,716,727]:
    geometry.append(circle(800,800,r,GOLD if r%2 else INK,.6 if r%2 else .85))
for phase in (0,math.pi):geometry.append(wave(315,20,24,phase,TEAL,.75))
for j in range(4):geometry.append(wave(583,12,32,j*math.pi/2,INK if j%2 else GOLD,.7))
for i in range(144):
    a=2*math.pi*i/144
    r1=716 if i%6==0 else 721
    geometry.append(line([(800+r1*math.cos(a),800+r1*math.sin(a)),(800+726*math.cos(a),800+726*math.sin(a))],INK,.65))
for r,step,col in [(191,5,GOLD),(282,7,TEAL)]:
    pts=[(800+r*math.cos(2*math.pi*((i*step)%24)/24),800+r*math.sin(2*math.pi*((i*step)%24)/24)) for i in range(24)]
    geometry.append(line(pts,col,.55,True))
layers=[layer('01 · Papier',[background]),layer('02 · Guilloche und Konstruktionslinien',geometry),
        layer('03 · 32 Federfächer',instances('Federfächer · Linien',32,437)),
        layer('04 · 24 Maßwerkbögen',instances('Spitzbogen · Maßwerk',24,215,1,7.5)),
        layer('05 · 12 Kernblätter',instances('Kernblatt · Linien',12,87,1,15)),
        layer('06 · 32 Arabeskenbrücken',instances('Bogenbrücke · Arabeske',32,545,1,5.625)),
        layer('07 · 48 Randlanzetten',instances('Randlanzette',48,655)),
        layer('08 · 64 Perlenachsen',instances('Perlenachse',64,602,1,2.8125))]
center=[]
for i in range(12):
    a=i*math.pi/6
    center.append(line([(800+13*math.cos(a),800+13*math.sin(a)),(800+30*math.cos(a),800+30*math.sin(a))],TEAL,.9))
center.extend([circle(800,800,10,INK,1),circle(800,800,4,GOLD,.8,GOLD)])
layers.append(layer('09 · Zentrum',center))
doc.update(title='Liniara – Symbolmandala',layers=layers,symbols=symbols,next_id=counter+1,
           artboards=[{'id':1,'name':'Liniara','rect':{'x0':0,'y0':0,'x1':1600,'y1':1600},'show_center_mark':False,'show_cross_hairs':False}],
           images={},metadata={},symbolSizes=sizes,currentSymbol='Federfächer · Linien',
           unknown={'symbolSizes':sizes,'currentSymbol':'Federfächer · Linien'})
Path('outputs/KI-Mandala-Liniara.vectorcraft').write_text(json.dumps(root,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
print('Created',len(symbols),'shared symbol definitions and',sum(len(l['kind']['children']) for l in layers[2:8]),'instances; native bytes',Path('outputs/KI-Mandala-Liniara.vectorcraft').stat().st_size)
