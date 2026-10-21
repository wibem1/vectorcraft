# Funktionierende direkte Steuerung

## Beobachteter Aufbau

```text
Anweisung des Anwenders im Chat
  → ChatGPT Work / Codex mit freigegebenen lokalen Werkzeugen
  → lokale Python-Skripte bzw. CLI-Aufrufe
  → JSON-Zeilen über 127.0.0.1:7979
  → laufendes VectorCraft 0.11.0 unter Windows
  → Dokumentzustand und gerenderte Ansicht zur Prüfung
```

Die direkte Verbindung ist werkzeuggestützt. Sie ist weder eine in VectorCraft eingebaute KI noch eine permanente Live-Bildschirmüberwachung. Die Bilder wurden jeweils aktiv gerendert und angesehen. Das alte Reglerfenster ist für diesen Arbeitsweg nicht erforderlich.

Die offizielle [OpenAI-Dokumentation zu ChatGPT Work](https://learn.chatgpt.com/docs/get-started-with-work) beschreibt die Nutzung verfügbarer lokaler Dateien, Apps und Werkzeuge auf dem Desktop. **Die konkrete VectorCraft-Anbindung ist unser hier getesteter lokaler Workflow**, keine dort zugesicherte spezielle VectorCraft-Integration. Dokumentationsstand: 2026-10-21.

## Start und Protokoll

```powershell
& 'C:\Program Files\VectorCraft\vectorcraft.exe' --control 7979
```

Beispiel einer einzelnen Anfrage, UTF-8 und mit abschließendem Zeilenumbruch:

```json
{"id":1,"method":"engine.execute","params":{"command":"symbol.list","params":{}}}
```

Die Antwort enthält die Anfrage-ID und `ok`; erfolgreiche Ergebnisse stehen unter `result`. `control-app/legacy.py` enthält den tatsächlich verwendeten Socket-Client. Er verwendet keine OpenAI-API-Schlüssel. Das sagt nichts über die Abrechnung des verwendeten ChatGPT-Angebots aus.

Bestätigte Aufrufe:

- `document.inspect`, `ui.inspect`: Übersicht, Revision, Auswahl, aktive Dokumente.
- `engine.commands`: verfügbare Befehle und Parameterschemata.
- `engine.execute` mit `document.json`, `document.open`, `symbol.list`, `object.transform`, `select.set`, `command.batch`, Symbolbefehlen und Exporten.
- `document.open` mit `name` und `dataBase64`: erzeugte native Vektordatei ohne Änderung am Originaldokument in einem weiteren Tab öffnen.
- `document.export` ohne Zielpfad: SVG-/PNG-Bytes unter `dataBase64` empfangen und lokal speichern.
- `document.save` ohne bekannten Dateipfad: native Bytes empfangen; nicht mit dem sicheren Speichern eines bestehenden Benutzerpfads gleichsetzen.
- `view.fitArtboard`: neue Konstruktion vollständig anzeigen.

## Bewährter Arbeitsablauf

1. Aktuelles Dokument, Auswahl und Symbolbibliothek auslesen; Ziel eindeutig prüfen.
2. Vorherzustand lokal sichern. Für größere neue Konstruktionen einen neuen Dokument-Tab verwenden.
3. Vektorgeometrie und Wiederholungen berechnen. Wiederkehrende Motive bei Bedarf als echte gemeinsame Symboldefinitionen und Instanzen anlegen.
4. Änderungen übertragen; zusammengehörige Eingriffe nach Möglichkeit in `command.batch` oder einer kontrollierten Undo-Gruppe ausführen.
5. Nachherzustand auslesen, Symbolzahlen und Geometrie kontrollieren.
6. In VectorCraft rendern und das Bild visuell prüfen.
7. Native Datei, SVG, Vorschau und erforderliche Diagnose sichern.

Dies ist ein beobachteter Arbeitsablauf, noch kein universelles, kontextunabhängiges ausführbares Produkt. Die historischen Skripte haben unterschiedliche Voraussetzungen.

## Symbole

`symbol.edit {id}` ersetzt eine gewählte Instanz durch bearbeitbare Geometrie und liefert `{name, ids}`. Danach übernimmt `symbol.update {name, ids}` die Änderungen in die gemeinsame Definition und erzeugt wieder eine Instanz. `symbol.replace` tauscht die Symbolzuordnung vorhandener Instanzen und definiert das Symbol nicht neu.

Bei selbst erzeugten nativen Dokumenten wurden natürliche Symbolgrößen erfolgreich mit `document.unknown.symbolSizes` hinterlegt. Die Ursprungszentrierung und Normalisierung müssen stimmen. Ein verworfener Farbversuch zeigte, dass Auflösen/Neunormalisieren bei problematischen Ausgangsdefinitionen unerwartete Koordinatenänderungen verursachen kann. Für Liniaras Farbvariante wurden deshalb nur die Farbwerte in einer Kopie der gemeinsamen nativen Definitionen geändert und die Geometrie separat verglichen.

## Grenzen und Fehlerbehandlung

- Der Steuerport ist lokal und hat gemäß VectorCraft-Protokoll keine Authentifizierung. Nur während der beabsichtigten Arbeit aktivieren; die vorhandenen App-Regeln für Automations-Dateizugriffe weiter beachten.
- Bei Timeout kann ein Schreibbefehl bereits laufen oder fertig sein. Zustand prüfen, nicht blind erneut senden.
- Die maximale Anfragezeile beträgt im dokumentierten Protokoll 4 MiB. Ein eingerücktes großes natives Dokument überschritt diese Grenze; dieselbe Datei in kompakter JSON-Form konnte geöffnet werden. Der historische Client bezeichnet solche Antworten teils nur als „ungültige Protokollantwort“.
- Dokumentprüfung und anschließender Befehl sind nicht gemeinsam atomar. Während der Ausführung nicht parallel am selben Ziel weiterarbeiten.
- Die externe Vorlagenrekonstruktion ist nur lokal gesichert. Keine Veröffentlichung ihrer Konturen oder Vorschauen.

Primärquellen im Repository: [`docs/control-protocol.md`](../../../docs/control-protocol.md), [`crates/engine/src/cmd/brushsym.rs`](../../../crates/engine/src/cmd/brushsym.rs), [`crates/ui-egui/src/control.rs`](../../../crates/ui-egui/src/control.rs). Für die ursprüngliche Sicherungsbasis gilt der in `PROJECT_STATUS.md` genannte Commit.
