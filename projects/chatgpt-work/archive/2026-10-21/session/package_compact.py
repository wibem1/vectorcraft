from pathlib import Path
import shutil,zipfile
out=Path('outputs'); package=out/'VectorCraft-Symbol-Experiment-0.4.1'
shutil.copytree('work/dist/VectorCraft-Symbol-Experiment-0.4.1',package,dirs_exist_ok=True)
shutil.copytree('outputs/VectorCraft-Symbol-Experiment-0.4/source',package/'source',dirs_exist_ok=True)
shutil.copy('work/app/vectorcraft_experiment.py',package/'source/vectorcraft_experiment.py')
for name in ['PYTHON-LICENSE.txt','engine-test.json']:
 shutil.copy(out/'VectorCraft-Symbol-Experiment-0.4'/name,package/name)
s=Path('work/ANLEITUNG.txt').read_text(encoding='utf-8').replace('VectorCraft-Symbol-Experiment-0.4.exe','VectorCraft-Symbol-Experiment-0.4.1.exe')
s='NEU IN 0.4.1: Kompaktes Startfenster 720 x 600, verkleinerbar bis 620 x 480.\nDie beiden Schritte stehen im Reiter Symbol bearbeiten; weitere Funktionen\nim Reiter Diagnose / Werkzeuge. Verbindung und Export bleiben direkt erreichbar.\nOffene Sitzungen aus 0.4 bleiben aus Sicherheitsgründen gesperrt.\n\n'+s
(package/'ANLEITUNG.txt').write_text(s,encoding='utf-8')
s='Ergänzung 0.4.1: Kompakte Oberfläche geprüft. Beide Reiter und sämtliche\nsichtbaren Schaltflächen passen bei 620 x 480 ins Fenster; Protokoll bleibt\nnutzbar. Starttest der gebauten EXE erfolgreich (Exitcode 0).\nDie Engine-/Workflow-Logik wurde gegenüber 0.4 nicht verändert.\n\n'+Path('work/TESTBERICHT.txt').read_text(encoding='utf-8')
(package/'TESTBERICHT.txt').write_text(s,encoding='utf-8')
archive=out/'VectorCraft-Symbol-Experiment-0.4.1-Windows-x64.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
 for p in package.rglob('*'):
  if p.is_file():z.write(p,p.relative_to(out))
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
print(archive,archive.stat().st_size,'bytes; CRC passed')
