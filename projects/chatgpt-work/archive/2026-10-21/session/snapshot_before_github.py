from pathlib import Path
import shutil,hashlib,json,datetime
root=Path.cwd();snapshot=root/'outputs'/'VectorCraft-Project-Backup-2026-10-21'
assert not snapshot.exists(),'Snapshot already exists; do not overwrite'
items=[]
def add(p,rel):
 if p.is_file():items.append((p,Path(rel)))
for p in (root/'outputs').iterdir():
 if p.is_file():add(p,Path('deliverables')/p.name)
 elif p.is_dir() and p.name.startswith('VectorCraft-Symbol-Experiment'):
  for f in p.rglob('*'):
   if f.is_file() and '_internal' not in f.parts and '__pycache__' not in f.parts and f.suffix.lower() not in ('.exe','.dll','.pyd'):
    add(f,Path('versions')/p.name/f.relative_to(p))
for p in (root/'work').iterdir():
 if p.is_file():add(p,Path('session')/p.name)
for folder in ['app','baseline','isolated-profile']:
 base=root/'work'/folder
 if base.exists():
  for p in base.rglob('*'):
   if p.is_file() and '__pycache__' not in p.parts:add(p,Path('session')/folder/p.relative_to(base))
downloads=Path(r'C:\Users\wibem\Downloads')
for p in downloads.glob('VectorCraft-Symbol-Experiment-*.zip'):add(p,Path('inputs')/p.name)
for name in ['VectorCraft-Aenderungen.json','VectorCraft-Diagnose-0.4.json','sacred-circles-of-light-the-spiritual-journey-through-mandala-design-free-vector.jpg']:
 add(downloads/name,Path('inputs')/name)
manifest=[]
for src,rel in items:
 dst=snapshot/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
 a=hashlib.sha256(src.read_bytes()).hexdigest();b=hashlib.sha256(dst.read_bytes()).hexdigest();assert a==b
 manifest.append({'path':rel.as_posix(),'bytes':dst.stat().st_size,'sha256':b,'original':str(src)})
(snapshot/'SNAPSHOT_MANIFEST.json').write_text(json.dumps({'created':datetime.datetime.now().astimezone().isoformat(),'purpose':'Unchanged pre-organization backup','files':manifest,'excluded':'Installed dependencies, build caches, Python bytecode and unpacked runtime duplicates; deliverable ZIPs retained byte-for-byte.'},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'snapshot':str(snapshot),'files':len(manifest),'bytes':sum(m['bytes'] for m in manifest)},ensure_ascii=False))
