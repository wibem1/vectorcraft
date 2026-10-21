from pathlib import Path
import shutil,zipfile
out=Path('outputs');package=out/'VectorCraft-Symbol-Experiment-0.5'
shutil.copytree('work/dist/VectorCraft-Symbol-Experiment-0.5',package,dirs_exist_ok=True)
(package/'source').mkdir(exist_ok=True)
for p in Path('work/app').glob('*.py'):shutil.copy(p,package/'source'/p.name)
for name in ['check_live_ui.py','check_compact.py']:
 s=Path('work',name).read_text(encoding='utf-8-sig')
 s='from pathlib import Path\n'+s.replace("sys.path.insert(0,'work/app')","sys.path.insert(0,str(Path(__file__).parent))")
 (package/'source'/name).write_text(s,encoding='utf-8')
shutil.copy('work/ANLEITUNG-0.5.txt',package/'ANLEITUNG.txt')
shutil.copy('work/ANLEITUNG-0.5.txt',out/'VectorCraft-0.5-Anleitung.txt')
for name in ['engine-test.json','mandala-engine-test.json']:shutil.copy(Path('work')/name,package/name)
shutil.copy('outputs/VectorCraft-Symbol-Experiment-0.4/PYTHON-LICENSE.txt',package/'PYTHON-LICENSE.txt')
(package/'TESTBERICHT.txt').write_text('VectorCraft Symbol-Experiment 0.5 – Prüfbericht\n\n24 automatisierte Tests bestanden: 14 bestehende Symbol-/Zustandstests, 10 neue Mandala-Tests. Geprüft wurden neue verknüpfte Kopien, Ersetzen ausschließlich eigener Instanzen, Vorlagenerhalt, manuelle Änderungen, Dokument-/Definitionswechsel, ungültige Werte, veraltete Auswahl nach Erkennung, Timeout ohne Wiederholung, Schreibfehler, unveränderte Einstellungen ohne Befehl und Beenden ohne Dokumentänderung.\n\nIntegration mit installierter VectorCraft-Engine in einem separaten headless MCP-Prozess bestanden: Symbol automatisch erkennen, symbol.edit, Farbe ändern, Auswahl wiederherstellen, symbol.update. Danach Mandala mit vier Kopien erstellen und auf sechs Kopien mit anderem Radius und 30 Grad Motivdrehung ändern. Positionen und Transformationsmatrizen numerisch geprüft. Alte Kopien entfernt, beide vorher vorhandenen Instanzen unverändert erhalten. Fehler in einem command.batch rollt die gesamte Änderung zurück. Ein Rückgängig-Schritt stellt die vorherige Mandala-Anordnung wieder her; anschließende Zustandsprüfung erkennt die ungültige Zuordnung.\n\nBerichte: engine-test.json und mandala-engine-test.json. Tabmetadaten liefert im headless Test ein Adapter. Kein bestehendes Benutzer-Dokument verändert.\n\nGUI-Steuerung geprüft: schnelle Änderungen gebündelt; während eines laufenden Aufrufs geänderte Werte gehen nicht verloren; Live ausschalten verhindert weitere automatische Updates; Beenden sendet keine Zeichenbefehle; vor dem Schließen wird eine wartende Aktualisierung storniert.\n\nAlle drei Reiter und sichtbaren Schaltflächen bei 620 x 480 innerhalb des Fensters; Protokoll weiterhin nutzbar. EXE-Starttest erfolgreich (Exitcode 0).\n\nKein vollständiger manueller Durchlauf der Desktopoberfläche mit Sichtprüfung aller Instanzen. Zustandsprüfung und Befehl sind nicht atomar; während der Ausführung nicht parallel weiterarbeiten. Dokumentidentität kann ohne stabile UUID nicht vollkommen erkannt werden. Details: ANLEITUNG.txt.\n\nKein Eingriff in das VectorCraft-Repository.\n',encoding='utf-8')
archive=out/'VectorCraft-Symbol-Experiment-0.5-Windows-x64.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
 for p in package.rglob('*'):
  if p.is_file():z.write(p,p.relative_to(out))
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None
 assert any(n.endswith('/mandala.py') for n in z.namelist())
print('Paket und CRC geprüft:',archive,archive.stat().st_size)
