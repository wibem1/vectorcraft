import sys,json,base64,math,copy
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent/'app'))
import legacy
from vc_workflow import nodes

before=legacy.command('document.json')
ov=legacy.call('document.inspect',{'depth':0})
assert ov['title']=='Liniara – Symbolmandala'
old=nodes(before)
palettes={
 'Federfächer · Linien':['#16566a','#6252a5','#238d89','#ca6353','#3c75a6','#b57f32'],
 'Spitzbogen · Maßwerk':['#724585','#3774ad','#cb6655','#a34f78','#298b8b','#b88931'],
 'Kernblatt · Linien':['#b84f68','#da784b','#d4a13b','#754c9e','#278988'],
 'Randlanzette':['#26788b','#8257a7','#d16850','#2a91a0','#b58531'],
 'Bogenbrücke · Arabeske':['#ad7c2e','#2b9896','#a44f7e','#3a73a4','#d0744e'],
 'Perlenachse':['#af7e2d','#9f4d7d','#337fb0','#27958f']}

def leaves(node):
    if node['kind']['type']=='path':yield node
    for child in node['kind'].get('children',[]):yield from leaves(child)

def world_points(doc,node):
    sym=next(s for s in doc['symbols'] if s['name']==node['kind']['symbol'])
    a,b,c,d,e,f=node['kind']['xf']
    result=[]
    for p in leaves(sym['art']):
        for sub in p['kind']['path']['subpaths']:
            for anchor in sub['anchors']:
                x,y=anchor['p'];result.append((a*x+c*y+e,b*x+d*y+f))
    return result

replaced={}
legacy.command('edit.undoGroup.begin',{'label':'Liniara · erweiterte Farbpalette'})
try:
    for name,palette in palettes.items():
        representative=next(n for n in old.values() if n['kind'].get('symbol')==name)
        legacy.command('select.set',{'ids':[representative['id']]})
        edited=legacy.command('symbol.edit',{'id':representative['id']})
        current=nodes(legacy.command('document.json'))
        commands=[]
        line_index=0
        for top in edited['ids']:
            for leaf in leaves(current[top]):
                color=palette[line_index%len(palette)]
                commands.append({'command':'paint.setStroke','params':{'id':leaf['id'],'color':color}})
                line_index+=1
        commands.append({'command':'symbol.update','params':{'name':name,'ids':edited['ids']}})
        result=legacy.command('command.batch',{'label':'Farben '+name,'commands':commands})
        replaced[representative['id']]=result['results'][-1]['id']
    # Fine construction lines receive matching accents; paper stays untouched.
    commands=[]
    static=before['layers'][1]['kind']['children']
    colors=['#497fa6','#b78b39','#527e9c','#a45f89','#368d88','#bf7256']
    for i,node in enumerate(static):
        commands.append({'command':'paint.setStroke','params':{'id':node['id'],'color':colors[i%len(colors)]}})
    commands.append({'command':'select.set','params':{'ids':[]}})
    legacy.command('command.batch',{'label':'Farbige Guilloche-Linien','commands':commands})
    after=legacy.command('document.json');ns=nodes(after)
    # Recoloring must preserve the visible geometry and every symbol instance.
    instances=[n for n in old.values() if n['kind']['type']=='symbolinstance']
    assert len(instances)==212
    for original in instances:
        updated=ns[replaced.get(original['id'],original['id'])]
        p=world_points(before,original);q=world_points(after,updated)
        assert len(p)==len(q)
        assert all(abs(x-u)<1e-6 and abs(y-v)<1e-6 for (x,y),(u,v) in zip(p,q))
    listing=legacy.command('symbol.list')
    assert len(listing['symbols'])==6 and sum(x['instances'] for x in listing['symbols'])==212
    legacy.command('edit.undoGroup.end')
except BaseException:
    legacy.command('edit.undoGroup.end',{'cancel':True})
    raise
legacy.command('view.fitArtboard')
native=legacy.command('document.save',{})
Path('outputs/KI-Mandala-Liniara-Farben.vectorcraft').write_bytes(base64.b64decode(native['dataBase64']))
preview=legacy.command('document.export',{'format':'png','scale':.8})
Path('outputs/KI-Mandala-Liniara-Farben.png').write_bytes(base64.b64decode(preview['dataBase64']))
svg=legacy.command('document.export',{'format':'svg'})
Path('outputs/KI-Mandala-Liniara-Farben.svg').write_bytes(base64.b64decode(svg['dataBase64']))
Path('work/liniara-color-check.json').write_text(json.dumps({'symbols':listing,'geometry_unchanged':True,'instances_checked':212,'palettes':palettes},ensure_ascii=False,indent=2),encoding='utf-8')
print('Recolored all six definitions and construction lines; 212 instance geometries verified unchanged.')
