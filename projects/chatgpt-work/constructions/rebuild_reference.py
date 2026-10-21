"""Reconstruct the supplied monochrome drawing as repeated native vector sectors."""
import math,json,copy
from pathlib import Path
import numpy as np
from PIL import Image

SRC=Path(r'C:\Users\wibem\Downloads\sacred-circles-of-light-the-spiritual-journey-through-mandala-design-free-vector.jpg')
im=Image.open(SRC).convert('L')
gray=np.asarray(im,dtype=float)
h,w=gray.shape;cx=cy=490.
yy,xx=np.indices(gray.shape);dx=xx-cx;dy=yy-cy
radius=np.hypot(dx,dy)
sector=(dy<=0)&(abs(dx)<=-dy/math.sqrt(3))

def contours(field):
    threshold=127.5;edges={}
    table={1:[(3,0)],2:[(0,1)],3:[(3,1)],4:[(1,2)],6:[(0,2)],7:[(3,2)],
           8:[(2,3)],9:[(2,0)],11:[(2,1)],12:[(1,3)],13:[(1,0)],14:[(0,3)]}
    active=(field>threshold)
    cases=(active[:-1,:-1].astype(int)+2*active[:-1,1:]+4*active[1:,1:]+8*active[1:,:-1])
    ys,xs=np.where((cases!=0)&(cases!=15))
    for y,x in zip(ys,xs):
        z=[field[y,x],field[y,x+1],field[y+1,x+1],field[y+1,x]]
        corners=[(x,y),(x+1,y),(x+1,y+1),(x,y+1)]
        def edge(e):
            i,j=e,(e+1)%4;t=(threshold-z[i])/(z[j]-z[i])
            return (round(corners[i][0]+t*(corners[j][0]-corners[i][0]),7),
                    round(corners[i][1]+t*(corners[j][1]-corners[i][1]),7))
        case=cases[y,x]
        if case==5:pairs=[(0,1),(2,3)] if sum(z)>4*threshold else [(0,3),(1,2)]
        elif case==10:pairs=[(0,3),(1,2)] if sum(z)>4*threshold else [(0,1),(2,3)]
        else:pairs=table[case]
        def value(px,py):
            u=px-x;v=py-y
            return z[0]*(1-u)*(1-v)+z[1]*u*(1-v)+z[2]*u*v+z[3]*(1-u)*v
        for ea,eb in pairs:
            a,b=edge(ea),edge(eb)
            vx,vy=b[0]-a[0],b[1]-a[1];length=math.hypot(vx,vy)
            if not length:continue
            mx,my=(a[0]+b[0])/2,(a[1]+b[1])/2
            nx,ny=-vy/length*.02,vx/length*.02
            if value(mx+nx,my+ny)<value(mx-nx,my-ny):a,b=b,a
            edges[a]=b
    loops=[]
    while edges:
        first=next(iter(edges));p=first;loop=[]
        while p in edges:
            loop.append(p);p=edges.pop(p)
            if p==first:break
        if p==first and len(loop)>=4:loops.append(loop)
    return loops

def simplify(points,tol=.25):
    def rdp(p):
        if len(p)<=2:return p
        a,b=p[0],p[-1];vx=b[0]-a[0];vy=b[1]-a[1];den=math.hypot(vx,vy)
        ds=[abs(vx*(a[1]-q[1])-(a[0]-q[0])*vy)/den if den else math.dist(a,q) for q in p]
        i=max(range(len(p)),key=lambda i:ds[i])
        return rdp(p[:i+1])[:-1]+rdp(p[i:]) if ds[i]>tol else [a,b]
    k=max(range(len(points)),key=lambda i:math.dist(points[0],points[i]))
    return rdp(points[:k+1])[:-1]+rdp(points[k:]+[points[0]])[:-1]

root=json.loads(Path('outputs/KI-Mandala-Liniara.vectorcraft').read_text(encoding='utf-8'))
doc=root['document'];counter=0
def uid():
    global counter
    counter+=1;return counter
black={'type':'solid','color':{'model':'rgb','r':0.,'g':0.,'b':0.}}
none={'type':'none'}
symbols=[];layers=[];sizes={};stats=[]
for name,lo,hi in [('Außenblätter',280,1000),('Verschränkter Mittelkranz',155,280),('Blüte und Innenrahmen',0,155)]:
    field=np.where(sector&(radius>=lo)&(radius<hi),255-gray,0.)
    loops=[simplify(p) for p in contours(field)]
    loops=[p for p in loops if len(p)>=3]
    xs=[p[0]-cx for loop in loops for p in loop];ys=[p[1]-cy for loop in loops for p in loop]
    x0,x1=min(xs),max(xs);y0,y1=min(ys),max(ys)
    mx,my=(x0+x1)/2,(y0+y1)/2;sw,sh=x1-x0,y1-y0
    subs=[]
    for loop in loops:
        anchors=[]
        for x,y in loop:
            anchors.append({'p':[(x-cx-mx)*20/sw,(y-cy-my)*20/sh]})
        subs.append({'closed':True,'anchors':anchors})
    art={'id':uid(),'name':name+' · Konturen','appearance':{'items':[{'kind':'fill','paint':black},{'kind':'stroke','paint':none,'width':0}]},
         'kind':{'type':'path','path':{'subpaths':subs}}}
    symbols.append({'name':name,'art':art});sizes[name]=[sw,sh]
    children=[]
    for i in range(6):
        theta=math.pi*i/3;co,si=math.cos(theta),math.sin(theta)
        children.append({'id':uid(),'name':f'{name} {i+1}',
                         'kind':{'type':'symbolinstance','symbol':name,
                                 'xf':[co*sw/20,si*sw/20,-si*sh/20,co*sh/20,cx+co*mx-si*my,cy+si*mx+co*my]}})
    layers.append({'id':uid(),'name':name,'kind':{'type':'layer','color':{'Preset':0},'template':False,'printable':True,'children':children}})
    stats.append({'symbol':name,'contours':len(subs),'anchors':sum(len(s['anchors']) for s in subs)})
paper={'id':uid(),'name':'Weißer Hintergrund','appearance':{'items':[{'kind':'fill','paint':{'type':'solid','color':{'model':'rgb','r':1.,'g':1.,'b':1.}}}]},
       'kind':{'type':'path','path':{'subpaths':[{'closed':True,'anchors':[{'p':[0,0]},{'p':[980,0]},{'p':[980,980]},{'p':[0,980]}]}]}}}
layers.insert(0,{'id':uid(),'name':'Hintergrund','kind':{'type':'layer','color':{'Preset':0},'template':False,'printable':True,'children':[paper]}})
doc.update(title='Sechsblättriges Mandala · nach Vorlage',layers=layers,symbols=symbols,next_id=counter+1,
           artboards=[{'id':1,'name':'Vorlagenrekonstruktion','rect':{'x0':0,'y0':0,'x1':980,'y1':980},'show_center_mark':False,'show_cross_hairs':False}],
           images={},metadata={},unknown={'symbolSizes':sizes,'currentSymbol':symbols[0]['name']})
doc.pop('symbolSizes',None);doc.pop('currentSymbol',None)
root['images']={}
Path('outputs/Mandala-nach-Vorlage.vectorcraft').write_text(json.dumps(root,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
Path('work/reference-reconstruction.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding='utf-8')
print(stats)
