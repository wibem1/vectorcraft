# Sicherungsumfang

## Zuerst unverändert gesichert

Vor der Organisation wurden 134 vorhandene Dateien mit insgesamt 96.888.633 Bytes in ein separates lokales Verzeichnis kopiert. Quell- und Zielbytes wurden pro Datei per SHA-256 verglichen. Das ursprüngliche `SNAPSHOT_MANIFEST.json` und alle Originaldateien bleiben im lokalen Vollbackup.

Der öffentliche Ausschnitt unter `archive/2026-10-21/` enthält 130 dieser Dateien bytegleich. Sein `PUBLIC_SNAPSHOT_MANIFEST.json` nennt die aufgenommenen Dateien und die vier ausschließlich lokal aufbewahrten Assets. Es wird kein vollständiges privates Backup als ZIP ins öffentliche Repository hochgeladen.

## Zusätzlich gesichert

Fünf geöffnete eigene Projektzeichnungen wurden lesend erfasst und unter `live-capture/` abgelegt. `CAPTURE_INDEX.json` dokumentiert Titel, Revision, Symbolstatus und den wiederhergestellten aktiven Tab. Die aktuelle externe Vorlagenrekonstruktion ist nicht öffentlich erfasst.

Diese Kopien sind zusätzliche Zustandsaufnahmen. Die zuvor gelieferten Dateien unter `artwork/` und im historischen Archiv wurden dafür nicht überschrieben.

## Was erhalten ist

- Die vier veröffentlichten eigenen Mandalas jeweils als `.vectorcraft`, SVG und PNG.
- Separate Steuerprogramme 0.4, 0.4.1, 0.4.2 und 0.5 als unveränderte portable Windows-ZIPs; darin sind die benötigten Laufzeitdateien enthalten.
- Frühere vorhandene Symbol-Experiment-Eingangsarchive einschließlich 0.3.1, deren Quellstand als Ausgangsbasis diente.
- Quellen der Programme und Tests, Konstruktionsskripte, Anleitungen, Diagnosen und Zustandsvergleiche.
- Erfolgreiche und verworfene Versuche; verworfene Skripte werden nicht als empfohlene Einstiegspunkte ausgegeben.
- Asset-Herkunft und zugehörige Projekt-/Paketlizenztexte.

Ungepackte DLL-/Runtime-Duplikate, `__pycache__`, PyInstaller-Build-Caches und lokal installierte Abhängigkeiten werden nicht zusätzlich versioniert. Sie sind keine neuen Projektfunktionen; die ausgelieferten Programme bleiben durch die ursprünglichen ZIP-Pakete gesichert.

## Ausgeschlossen von GitHub

- Die externe Mandala-JPEG-Vorlage.
- Ihre direkte Rekonstruktion `Mandala-nach-Vorlage.vectorcraft`, `.svg` und `.png`.
- Vollständige private Backup-ZIPs und spätere lokale Zustandsaufnahmen dieser Rekonstruktion.

Die Korrektur des Anwenders am 2026-10-21 – keine Rechte an der Vorlage – ersetzt die unmittelbar davor irrtümlich erteilte Freigabe. Im öffentlichen Archiv stehen keine entsprechenden Bild-/Konturdaten. Der allgemeine Rekonstruktionsalgorithmus bleibt als eigener Code erhalten; die dafür nötige nicht freigegebene Eingabedatei wird nicht mitgeliefert.

## Wiederherstellung und künftige Arbeit

1. Den Sicherungsbranch aus GitHub auschecken und `tools/verify_backup.py` ausführen.
2. Gewünschte native Zeichnung aus `artwork/` öffnen. Eine zusätzliche eigene Kopie vor weiteren Eingriffen speichern.
3. Historische Windows-Programme nur aus dem vollständig entpackten gewünschten ZIP starten.
4. Sitzungs-Konstruktionsskripte zuerst lesen: viele setzen konkrete Dokumente, IDs und lokale Windows-Pfade voraus. Kein unbeaufsichtigtes Wiederabspielen gegen ein beliebiges Dokument.
5. Für neue Arbeit einen neuen Branch verwenden; bestätigte Ergebnisse und Fehler im Projektstatus nachtragen.

`FILE_MANIFEST.json` enthält die für diese GitHub-Sicherung vorgesehenen Dateien mit Größe, SHA-256 und Git-Blob-ID. Das Manifest selbst ist als zusätzliche Git-Datei versioniert; es kann sich nicht sinnvoll selbst per SHA-256 aufführen.
