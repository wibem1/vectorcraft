import sys,json,math,base64
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent/'app'))
import legacy
from vc_workflow import nodes

doc=legacy.command('document.json')
overview=legacy.call('document.inspect',{'depth':0})
assert overview['title']=='KI-Mandala – Sonnenrosette'
source=nodes(doc)[2]
assert source['kind']['type']=='symbolinstance'
xf=source['kind']['xf']
cx=cy=700
steps=[];rings=[]
for count,radius,scale,offset in [(12,385,.72,0),(12,210,.50,15),(6,65,.25,0),(1,0,.16,0)]:
    indexes=[]
    for i in range(count):
        theta=2*math.pi*i/count+math.radians(offset)
        co,si=math.cos(theta)*scale,math.sin(theta)*scale
        x=cx+radius*math.sin(theta);y=cy-radius*math.cos(theta)
        matrix=[co,si,-si,co,x-co*xf[4]+si*xf[5],y-si*xf[4]-co*xf[5]]
        indexes.append(len(steps))
        steps.append({'command':'object.transform','params':{'ids':[2],'copy':True,'matrix':matrix}})
    rings.append(indexes)
steps.append({'command':'edit.clear','params':{'ids':[2]}})
dot_indexes=[]
for color,offset,r in [('#8cc63f',0,6),('#f7931e',10,4)]:
    steps.extend([{'command':'select.set','params':{'ids':[]}},
                  {'command':'paint.setFill','params':{'color':color}},
                  {'command':'paint.setStroke','params':{'none':True}}])
    for i in range(18):
        theta=math.radians(20*i+offset)
        x=cx+550*math.sin(theta);y=cy-550*math.cos(theta)
        dot_indexes.append(len(steps))
        steps.append({'command':'shape.ellipse','params':{'x':x-r,'y':y-r,'width':2*r,'height':2*r}})
r=legacy.command('command.batch',{'label':'KI-Sonnenrosette konstruieren','commands':steps})
results=r['results']
groups=[]
for label,indices in zip(['Äußerer Ring · 12 Motive','Innerer Ring · 12 Motive','Herz · 6 Motive','Zentrum'],rings):
    ids=[results[i]['ids'][0] for i in indices]
    if len(ids)>1:
        rr=legacy.command('command.batch',{'label':label,'commands':[{'command':'select.set','params':{'ids':ids}},
                                                                    {'command':'object.group','params':{}}]})
        gid=rr['results'][1]['id']
    else:gid=ids[0]
    legacy.command('object.setProps',{'id':gid,'name':label})
    groups.append(gid)
dot_ids=[results[i]['id'] for i in dot_indexes]
rr=legacy.command('command.batch',{'label':'Punktekranz gruppieren','commands':[{'command':'select.set','params':{'ids':dot_ids}},
                                                                             {'command':'object.group','params':{}}]})
legacy.command('object.setProps',{'id':rr['results'][1]['id'],'name':'Punktekranz'})
legacy.command('select.set',{'ids':[]})
Path('work/ai-rosette-state.json').write_text(json.dumps(legacy.state(),ensure_ascii=False,indent=2),encoding='utf-8')
preview=legacy.command('document.export',{'format':'png','scale':.7,'background':'white'})
Path('outputs/KI-Mandala-Sonnenrosette.png').write_bytes(base64.b64decode(preview['dataBase64']))
native=legacy.command('document.save',{})
if native.get('dataBase64'):
    Path('outputs/KI-Mandala-Sonnenrosette.vectorcraft').write_bytes(base64.b64decode(native['dataBase64']))
svg=legacy.command('document.export',{'format':'svg'})
Path('outputs/KI-Mandala-Sonnenrosette.svg').write_bytes(base64.b64decode(svg['dataBase64']))
print('Constructed:',legacy.canonical(legacy.command('symbol.list')))
