# Dauerhaft mit VectorCraft arbeiten

Stand: 21.10.2026. Diese Änderung ergänzt ausschließlich Arbeitsanweisungen.
Sie ändert weder VectorCraft-Core noch Steuerfenster oder historische Konstruktionen.

## Was künftig genügt

In einem eingerichteten Projektchat:

> Zeichne in VectorCraft ein zwölfzähliges blau-goldenes Mandala mit verknüpften Symbolmotiven.

Ohne anderes Ziel wird ein neues Dokument verwendet. Für Änderungen das Werk eindeutig nennen,
zum Beispiel: „Ändere in VectorCraft Liniara: nur die Farben, Geometrie unverändert.“
Die Vorgeschichte muss nicht jedes Mal mitgeschickt werden.

Das gilt erst nach der folgenden Einrichtung und dem erfolgreichen lesenden Abnahmetest.
Ein beliebiger neuer Chat liest nicht automatisch GitHub. Ein Repository-Link allein schafft
weder dauerhaft geladenen Kontext noch Zugriff auf die lokale Windows-Anwendung.

## Einmalig auf dem Rechner mit VectorCraft

1. Repository wibem1/vectorcraft lokal bereitstellen. Diese Konfiguration liegt auf
   feature/vectorcraft-work-start-2026-10-21, ausgehend vom Sicherungscommit
   dccac125aa9f8eb30269c5a3c793261d5c2ba5ca. Den Branch in einer sauberen separaten
   Arbeitskopie auschecken; bestehende uncommittete Arbeit und das lokale Vollbackup erhalten.
   Hauptbranch und archive/chatgpt-work-2026-10-21 werden durch diese Einrichtung nicht verändert.
2. In Work/Codex ein wiederverwendbares Projekt für genau diese lokale Arbeitskopie öffnen
   und Dateizugriff sowie lokale Befehlsausführung nach den verfügbaren Host-Funktionen einrichten.
   Der ausführende Prozess muss den Rechner mit VectorCraft erreichen. Ein GitHub-Connector
   dient nur dem Repositoryzugriff. Cloud-127.0.0.1 erreicht nicht den Windows-Desktop.
3. Wenn der Host AGENTS.md und Repository-Skills unterstützt, deren tatsächliches Laden mit dem
   Test unten prüfen. Andernfalls den folgenden Block einmalig in die dauerhaften
   Projektanweisungen des Hosts übernehmen. Den Platzhalter durch den absoluten lokalen
   Repositorypfad ersetzen. Diese Änderung im Repository kann keine Work-Projekteinstellung
   im Benutzerkonto setzen. Hat die verwendete Work-Oberfläche keine dauerhaften
   Projektanweisungen mit lokalem Dateizugriff, ist die kurze Eingabe allein dort nicht gewährleistet.
4. VectorCraft mit dem lokalen Steuerport starten. Installationspfad prüfen; im gesicherten
   Windows-Aufbau war dies:

   ```powershell
   & 'C:\Program Files\VectorCraft\vectorcraft.exe' --control 7979
   ```

   Bei bereits laufender Instanz zuerst deren Start-/Portzustand prüfen und offene Arbeit sichern;
   nicht ungefragt beenden oder eine konkurrierende Instanz starten. Port-Bindefehler ernst nehmen.
   Für Dateizugriffe die in docs/control-protocol.md beschriebenen Automationswurzeln verwenden:
   --automation-read-root und --automation-write-root müssen auf bestehende vereinbarte lokale
   Ordner zeigen. Ein ausgelassener Root gewährt keinen entsprechenden Dateizugriff.
   Nicht das gesamte Laufwerk freigeben. Kein zusätzlicher Server, kein API-Schlüssel und kein
   Reglerfenster sind für den direkten Weg nötig.

### Block für dauerhafte Projektanweisungen

```text
Dieses Projekt ist die lokale Arbeitskopie von wibem1/vectorcraft unter:
<ABSOLUTER LOKALER REPOSITORYPFAD>
Bei „Zeichne in VectorCraft …“ arbeite mit lokalen Werkzeugen auf dem VectorCraft-Rechner.
Lies zuerst die zuständigen AGENTS.md, PROJECT_STATUS.md und
.agents/skills/vectorcraft-drawing/SKILL.md in dieser Arbeitskopie.
Befolge den darin beschriebenen direkten Ablauf über 127.0.0.1:7979.
Neue Konstruktion standardmäßig in neuem Dokument; vor Eingriffen Ziel prüfen und sichern.
Keine Core-Änderungen. Historische Artefakte und Copyright-Ausschlüsse erhalten.
Fehlen lokale Werkzeuge oder Dateien, benenne genau die fehlende Einrichtung.
Behaupte niemals, ein neuer Chat könne global automatisch GitHub oder lokale Apps lesen.
```

Die maßgebliche [Arbeitsanweisung](../../../.agents/skills/vectorcraft-drawing/SKILL.md)
bleibt im Repository. Kein Kopieren der alten gesamten Chat-Historie erforderlich.

## Einmaliger lesender Abnahmetest in einem NEUEN Projektchat

> Prüfe die VectorCraft-Einrichtung nur lesend: nenne die geladene Arbeitsanweisung,
> Repositorypfad und Branch, prüfe den lokalen VectorCraft-Prozess und 127.0.0.1:7979,
> lies ui.inspect, document.inspect und engine.commands. Ändere und speichere nichts.

Erwartung: Der neue Chat nennt diese Arbeitsanweisung, die richtige lokale Arbeitskopie,
die echte VectorCraft-Instanz, aktive Tabs und das Befehlsverzeichnis. Keine Dokumente anlegen,
keine Auswahl ändern, keine Dateien speichern. Wenn ein Teil fehlt, die Einrichtung genau
an dieser Stelle korrigieren; ein erfolgreiches GitHub-Lesen genügt nicht.
Danach als ersten Schreibtest ein neues einfaches Werk beauftragen und anhand der
Arbeitsanweisung sichern, rendern und überprüfen.

## Je weiterer Sitzung

Dasselbe eingerichtete Projekt und die passende Arbeitskopie wählen, VectorCraft mit lokalem
Steuerport bereitstellen; dann genügt „Zeichne in VectorCraft …“. Keine dauerhafte
Bildschirmbeobachtung. Nach Arbeitsende den Steuerport durch reguläres Beenden der Anwendung
nach Sicherung der eigenen Arbeit deaktivieren. Nach Rechner-/Pfad-/Hostwechsel Abnahmetest
wiederholen. Die Anweisung ersetzt keine tatsächlich verfügbaren Werkzeuge.

## Sicherung, Prüfstand und Grenzen dieser Einrichtung

Basis ist der unveränderte Sicherungsbranch. Bestehende Artefakte, FILE_MANIFEST.json und
Copyright-Ausschlüsse bleiben unverändert; das Manifest beschreibt weiterhin den historischen
Sicherungsumfang und nicht neue Anweisungsdateien. Keine Grafik und kein neues Asset hinzugefügt.

Am 21.10.2026 wurden Repositorybaum und vorhandene AGENTS.md geprüft, Protokoll und
control.rs mit der Arbeitsanweisung abgeglichen sowie relative Links, unveränderte
Upstream-Anweisungen und die Beschränkung der Änderung auf Anweisungsdateien geprüft.
Die endgültige Git-Baumprüfung wird nach Erstellung auf dem separaten Branch vorgenommen.
plan/ ist laut Upstream lokal/gitignored und war über GitHub nicht verfügbar.

In diesem Chat war kein lokales Ausführungswerkzeug verfügbar („No usable execution
environment is available“). Daher kein Live-Socket-, Work-Neuchat-, Python-, Render- oder
Rust-/WASM-Test und kein cargo xtask ci; das Upstream-Qualitätsgate bleibt ausstehend.
Die Prüfung der Dokumente ersetzt diese Tests nicht. Die Projektanweisung muss einmalig
im tatsächlichen Work-Host hinterlegt bzw. dessen automatische Erkennung bestätigt werden.
Es wird kein erfolgreicher End-to-End-Betrieb dieser neuen Konfiguration behauptet.

Rücknahme: Den Arbeitsbranch verlassen bzw. ausschließlich diese Anweisungsergänzungen
zurücknehmen und den einmalig eingefügten Work-Projektblock entfernen. Keine historischen
Archive oder Benutzerzeichnungen löschen.
