import json,subprocess
from pathlib import Path
p=Path('outputs/KI-Mandala-Liniara.vectorcraft');d=json.loads(p.read_text(encoding='utf-8'))
d['document']['unknown']={'symbolSizes':d['document']['symbolSizes'],'currentSymbol':d['document']['currentSymbol']}
Path('work/liniara-unknown-test.vectorcraft').write_text(json.dumps(d,separators=(',',':')),encoding='utf-8')
r=subprocess.run([r'C:\Program Files\VectorCraft\vectorcraft-cli.exe','run','--in','work/liniara-unknown-test.vectorcraft','--cmd','symbol.list'],capture_output=True,text=True,encoding='utf-8');print(r.stdout)
