from pathlib import Path
import shutil,zipfile
out=Path('outputs');package=out/'VectorCraft-Symbol-Experiment-0.4.2'
shutil.copytree('work/dist/VectorCraft-Symbol-Experiment-0.4.2',package,dirs_exist_ok=True)
(package/'source').mkdir(exist_ok=True)
for p in Path('work/app').glob('*.py'):shutil.copy(p,package/'source'/p.name)
shutil.copy('work/ANLEITUNG-0.4.2.txt',package/'ANLEITUNG.txt')
shutil.copy('work/engine-test.json',package/'engine-test.json')
shutil.copy('outputs/VectorCraft-Symbol-Experiment-0.4/PYTHON-LICENSE.txt',package/'PYTHON-LICENSE.txt')
(package/'TESTBERICHT.txt').write_text('Version 0.4.2\n\n14 automatisierte Tests bestanden: bisherige Zustands-/Fehlersperren sowie automatische Erkennung, Auswahlwechsel nach Bestätigung, Dokumentänderung nach Erkennung, verständliche Ablehnung ungeeigneter Objekte, Prüfung vor erneuter Auswahl.\n\nIntegration mit installierter VectorCraft-Engine im separaten headless MCP-Prozess bestanden: Symbol automatisch erkennen, symbol.edit, Farbe ändern, Auswahl leeren, gespeicherte Bearbeitungsform auswählen, symbol.update. Definition geändert und wieder zwei verknüpfte Instanzen bestätigt. Bericht: engine-test.json. Tabmetadaten liefert im headless Test ein Adapter. Kein Benutzer-Dokument verändert.\n\nGUI-Start und beide Reiter bei 620 x 480 geprüft. Alle sichtbaren Schaltflächen innerhalb des Fensters.\nEXE-Starttest bestanden (Exitcode 0).\n\nKein vollständiger manueller Durchlauf der Desktopoberfläche mit Sichtprüfung sämtlicher Instanzen. Zustandsprüfungen sind nicht atomar. Weitere Grenzen: ANLEITUNG.txt.\n',encoding='utf-8')
archive=out/'VectorCraft-Symbol-Experiment-0.4.2-Windows-x64.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
 for p in package.rglob('*'):
  if p.is_file():z.write(p,p.relative_to(out))
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
print('Paket geprüft:',archive,archive.stat().st_size)
