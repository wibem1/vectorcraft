import sys,json,copy,base64
from pathlib import Path
sys.path.insert(0,'work/app')
import legacy
from vc_workflow import nodes
before=legacy.command('document.json')
assert legacy.call('document.inspect',{'depth':0})['title']=='Liniara – Symbolmandala'
# Work directly on shared definitions, preserving every coordinate and transform.
after=copy.deepcopy(before)
palettes={
'Federfächer · Linien':['#16566a','#6252a5','#238d89','#ca6353','#3c75a6','#b57f32'],
'Spitzbogen · Maßwerk':['#724585','#3774ad','#cb6655','#a34f78','#298b8b','#b88931'],
'Kernblatt · Linien':['#b84f68','#da784b','#d4a13b','#754c9e','#278988'],
'Randlanzette':['#26788b','#8257a7','#d16850','#2a91a0','#b58531'],
'Bogenbrücke · Arabeske':['#ad7c2e','#2b9896','#a44f7e','#3a73a4','#d0744e'],
'Perlenachse':['#af7e2d','#9f4d7d','#337fb0','#27958f']}
def leaves(n):
 if n['kind']['type']=='path':yield n
 for c in n['kind'].get('children',[]):yield from leaves(c)
def color(n,c):
 for item in n['appearance']['items']:
  if item['kind']=='stroke':item['paint']={'type':'solid','color':{'model':'rgb','r':int(c[1:3],16)/255,'g':int(c[3:5],16)/255,'b':int(c[5:7],16)/255}}
for s in after['symbols']:
 for i,n in enumerate(leaves(s['art'])):color(n,palettes[s['name']][i%len(palettes[s['name']])])
colors=['#497fa6','#b78b39','#527e9c','#a45f89','#368d88','#bf7256']
for i,n in enumerate(after['layers'][1]['kind']['children']):color(n,colors[i%len(colors)])
for old,new in zip(before['symbols'],after['symbols']):
 for a,b in zip(leaves(old['art']),leaves(new['art'])):assert a['kind']==b['kind']
oldnodes=nodes(before);newnodes=nodes(after)
assert all({k:v for k,v in oldnodes[i]['kind'].items() if k!='children'}=={k:v for k,v in newnodes[i]['kind'].items() if k!='children'} for i in oldnodes)
assert len([n for n in newnodes.values() if n['kind']['type']=='symbolinstance'])==212
root=json.loads(Path('outputs/KI-Mandala-Liniara.vectorcraft').read_text(encoding='utf-8'))
after['title']='Liniara – Farbenspiel';root['document']=after
p=Path('outputs/KI-Mandala-Liniara-Farben.vectorcraft');p.write_text(json.dumps(root,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
print(legacy.command('document.open',{'name':p.name,'dataBase64':base64.b64encode(p.read_bytes()).decode()}))
legacy.command('view.fitArtboard')
listing=legacy.command('symbol.list');assert len(listing['symbols'])==6 and sum(s['instances'] for s in listing['symbols'])==212
native=legacy.command('document.save',{});p.write_bytes(base64.b64decode(native['dataBase64']))
r=legacy.command('document.export',{'format':'png','scale':.8});Path('outputs/KI-Mandala-Liniara-Farben.png').write_bytes(base64.b64decode(r['dataBase64']))
r=legacy.command('document.export',{'format':'svg'});Path('outputs/KI-Mandala-Liniara-Farben.svg').write_bytes(base64.b64decode(r['dataBase64']))
print('Verified: geometry unchanged, six definitions and 212 linked instances.')

