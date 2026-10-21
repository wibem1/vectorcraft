---
name: vectorcraft-drawing
description: Zeichnungen in der lokal laufenden VectorCraft-Anwendung über den direkten Steuerkanal erstellen und prüfen. Für Aufträge wie „Zeichne in VectorCraft …“.
---

# VectorCraft zeichnen

Diese wiederverwendbare Arbeitsanweisung gilt für Zeichenaufträge, nicht für Änderungen am VectorCraft-Core. Sie installiert keinen Dienst und keine globale Chat-Erinnerung. Die Regeln der Repository-AGENTS.md bleiben gültig.

## Einstieg

1. Repositorywurzel von wibem1/vectorcraft und aktuellen Branch feststellen. Zuständige AGENTS.md lesen, danach PROJECT_STATUS.md, projects/chatgpt-work/README.md sowie docs/DIRECT_CONTROL.md und docs/PROVENANCE.md unter projects/chatgpt-work/. Vor Dateiänderungen auch untergeordnete AGENTS.md prüfen.
2. Lokale Werkzeuge müssen auf dem Rechner mit der laufenden VectorCraft-Anwendung ausgeführt werden können. Ein GitHub-Connector oder Cloud-Terminal allein genügt nicht: dessen 127.0.0.1 ist nicht der Windows-Rechner. Fehlt der lokale Zugriff, die fehlende Voraussetzung konkret nennen; keine Ausführung behaupten und keine öffentliche Portfreigabe/Tunnel einrichten.
3. Bevorzugt direkt JSON-Zeilen an 127.0.0.1:7979 senden. Das alte Reglerfenster ist nicht nötig. Protokoll aus docs/control-protocol.md und aktuelle Befehlsbeschreibungen aus engine.commands verwenden. Keine historischen IDs, Windows-Pfade oder aktiven Dokumente voraussetzen. control-app/legacy.py dokumentiert den bewährten Client, ist aber keine pauschale Ausführungsfreigabe für historische Skripte.
4. Sinnvolle Gestaltungsentscheidungen selbst treffen. Nur fehlende notwendige Maße, ein mehrdeutiges Änderungsziel oder fehlende Rechte/Zugriffe klären.

## Vor jedem Eingriff

- Anwendung/Version und lauschenden lokalen Prozess soweit mit lokalen Werkzeugen möglich prüfen. Erfolgreiches Verbinden oder passende Befehlsnamen identifizieren VectorCraft nicht eindeutig: Schwesteranwendungen benutzen denselben Port. Bei Bind-Fehlern oder unklarer Prozessidentität stoppen und die tatsächliche VectorCraft-Instanz ermitteln; nicht versuchsweise auf andere Ports schreiben.
- Zuerst ui.inspect, document.inspect und engine.commands lesen. Kein Schreibbefehl als Verbindungstest. Dialoge, noch laufende Öffnungs-/Speicheraufträge und unerwarteten Zustand auflösen, bevor geschrieben wird.
- Neue Konstruktion standardmäßig in einem neuen Tab erstellen. Vor dem Anlegen die bisherige Tabübersicht und das aktive Dokument erfassen. Ein vorhandenes Werk nur ändern, wenn der Auftrag es eindeutig bezeichnet.
- Für ein vorhandenes Änderungsziel unmittelbar vor dem Eingriff Titel, aktiven Tabindex, verfügbaren Pfad, Revision, Auswahl, relevante Objekt-IDs und Symboldefinitionen abgleichen. Fehlt ein Feld, es nicht erfinden: ergänzend Dokument-JSON und dessen kanonischen SHA-256 erfassen. Mehrdeutige/gleichnamige Tabs nicht anhand des Titels allein auswählen.
- Vor Änderungen native Sicherung und JSON-Zustand im lokalen, nicht öffentlichen Aufgabenordner schreiben; Existenz, Größe und Prüfsumme kontrollieren. Dokument-JSON allein ersetzt keine native Sicherung. document.save ohne Pfad kann Bytes liefern; bei einem bestehenden Pfad die tatsächliche Semantik vorab prüfen und das Original nicht durch einen unbedachten Save überschreiben.
- Während der Ausführung keine parallele manuelle Bearbeitung desselben Dokuments. Die Zustandsabfrage und der folgende Schreibbefehl sind NICHT atomar; Tabindex, Titel, Revision und Hash sind KEINE stabile Dokument-UUID. Bei zwischenzeitlichen Abweichungen neu prüfen, nicht weiterschreiben.

## Konstruieren

- Dimensionen, endliche Koordinaten, positive Größen, Instanz-/Objektzahlen und erwartete Begrenzungen vorab berechnen und begrenzen. Parameter anhand des laufenden engine.commands-Verzeichnisses prüfen.
- Zusammengehörige Änderungen möglichst als command.batch / kontrollierte Undo-Gruppe durchführen. Rückgaben einschließlich erzeugter IDs prüfen; IDs nie aus historischen Beispielen übernehmen. Nach jedem Batch Ziel und Zustand erneut prüfen.
- Neue native Daten können kompakt serialisiert über engine.execute → document.open mit name und dataBase64 in einem weiteren Tab geöffnet werden. Den zurückgegebenen Tab und den tatsächlichen Zustand prüfen. Keine Arbeit mit app.open und erfundenen Pfaden.
- Anfrage einschließlich Base64 und JSON-Hülle vor dem Senden auf UTF-8-Bytegröße prüfen: deutlich unter 4 MiB bleiben. Kein mehrzeiliges JSON auf dem Draht. Große Daten nicht durch willkürliches Aufteilen in ungültige Protokollzeilen senden.
- Wiederholte Motive bei Bedarf als gemeinsame Symboldefinitionen/Instanzen anlegen. symbol.edit {id} liefert name und ids; symbol.update {name, ids} aktualisiert die Definition. symbol.replace ersetzt nur die Zuordnung. Zentrierung, Normierung und document.unknown.symbolSizes kontrollieren. Bei Farbänderungen Transformationen/Koordinaten vor und nach der Änderung vergleichen; keine neue Normalisierung unbesehen übernehmen.
- Keine alten Konstruktionsskripte blind ausführen. Insbesondere color_liniara.py war ein zurückgerollter Fehlversuch. Die offene 0.5-Reglerproblematik bei manuellen Transformationen bleibt offen.

## Transport, Fehler und Dateien

- Anfrage-ID und boolesches ok der Antwort validieren; nur bei Erfolg result verwenden. Zeit- und Größenlimits setzen, Verbindungen schließen. Keine automatische Wiederholung von Schreibbefehlen nach Timeout, Verbindungsabbruch, ungültiger Antwort oder unklarem Ergebnis. Erst Dokument und laufende Jobs abgleichen; keinen weiteren Eingriff oder pauschales Undo in ein möglicherweise anderes Ziel schicken.
- Bei erkanntem Fehler nur dann Undo/Rollback nutzen, wenn Ziel und eigener letzter Eingriff eindeutig verifiziert sind; danach Zustand erneut vergleichen. Sonst Diagnose sichern und die konkrete Unklarheit melden.
- Steuerport ohne Authentifizierung nur lokal und während der Arbeit aktivieren. Bestehende automation-read-root / automation-write-root respektieren; bei verweigertem Dateizugriff keine Wurzeln pauschal erweitern. Auch per Base64 gelesene/geschriebene Daten nur im vereinbarten lokalen Aufgabenbereich ablegen.
- Eigene Ausgaben unter einem neuen, kollisionsfreien Aufgabennamen ablegen; Originale und historische Archive erhalten. Vorhandene Dateien nicht still überschreiben. Keine Backups oder Live-Dokumente automatisch in Git aufnehmen.

## Prüfen und abschließen

1. Nachherzustand lesen: Ziel, Objekt-/Symbolzahlen, Grenzen und die für den Auftrag relevanten Eigenschaften prüfen. Bei Änderungen unbeabsichtigte Koordinaten-/Transformationsänderungen ausschließen.
2. Mit ui.render oder document.export rendern und das Bild tatsächlich ansehen. ui.screenshot benötigt einen präsentierten Frame; falls das scheitert, Render nutzen und die fehlende UI-Prüfung benennen. Ohne Bildansicht keine visuelle Prüfung behaupten.
3. Native .vectorcraft, SVG und PNG in einem neuen lokalen Ausgabeordner sichern. Antworten können dataBase64 liefern; Bytes dekodieren und Dateien auf Existenz/Größe sowie geeignete Struktur prüfen. Native Datei möglichst in separatem Prüf-Tab erneut öffnen und Struktur/Symbole kontrollieren, ohne das Original zu ersetzen. Tabwechsel vor und nach jeder Prüfung erfassen.
4. Kurzer Abschluss: erzeugtes Werk, Speicherorte, tatsächlich geprüfte Eigenschaften und verbleibende Grenzen. Nicht „getestet“ schreiben, wenn nur historisches Protokoll gelesen wurde.

## Herkunft und Veröffentlichung

Keine Adobe-Software/-Ressourcen oder GPL-/AGPL-Code verwenden. Assets nur mit erlaubter Herkunft; vor einem Asset-Commit ASSETS.md, gegebenenfalls Lizenztext und NOTICE pflegen. Die fremde JPEG-Vorlage und alle direkten Kontur-, SVG-, PNG- und VectorCraft-Ableitungen aus dem alten Chat bleiben ausschließlich im lokalen Vollbackup: nicht lesen/hochladen/rekonstruieren, um sie für neue Aufgaben wiederzuverwenden. Keine pauschalen ZIPs oder rekursiven Add-Befehle. Ein neuer Zeichenauftrag ist keine Veröffentlichungsfreigabe. Details in projects/chatgpt-work/docs/PROVENANCE.md.

## Geltungsbereich

Dieses Skill-Verzeichnis ist für Hosts mit Repository-Skill-Unterstützung vorbereitet. Nur wenn der Host es tatsächlich entdeckt bzw. die Projektanweisung es lädt, steht es in neuen Chats bereit. Work-Einrichtung und lesender Abnahmetest: projects/chatgpt-work/docs/WORK_SETUP.md. Keine Änderung an globalen Einstellungen, Anwendungscode oder bestehenden Artefakten.
