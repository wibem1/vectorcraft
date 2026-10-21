import json,subprocess
from pathlib import Path
p=Path('outputs/KI-Mandala-Liniara.vectorcraft');d=json.loads(p.read_text(encoding='utf-8'))['document']
first=d['layers'][2]['kind']['children'][0]['id']
args=[r'C:\Program Files\VectorCraft\vectorcraft-cli.exe','run','--in',str(p),'--cmd','select.set','--params',json.dumps({'ids':[first]}),'--cmd','symbol.edit','--cmd','paint.setStroke','--params',json.dumps({'color':'#265f74'}),'--cmd','symbol.update','--params',json.dumps({'name':'Federfächer · Linien'}),'--cmd','symbol.list']
r=subprocess.run(args,capture_output=True,text=True,encoding='utf-8');assert r.returncode==0,r.stderr
rows=[json.loads(x) for x in r.stdout.splitlines() if x.strip()]
listing=rows[-1]['result']['symbols']
assert sum(x['instances'] for x in listing)==212
assert next(x for x in listing if x['name']=='Federfächer · Linien')['instances']==32
Path('work/liniara-symbol-test.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print('PASS: symbol.edit -> stroke change -> symbol.update; 32 fan instances retained; 212 instances total.')
