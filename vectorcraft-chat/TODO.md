# VectorCraft Chat – TODO

## Verbindliche Regel für jedes neue Update

**Vor jeder Änderung, jedem Build und jeder Versionsfreigabe ist diese TODO-Liste zu prüfen.**

- [ ] Vor Beginn der Entwicklung alle offenen Punkte und ihre Prioritäten lesen.
- [ ] Für das Update festhalten, welche TODO-Punkte umgesetzt werden und welche bewusst offen bleiben.
- [ ] Nach der Umsetzung die Liste aktualisieren: erledigte Punkte nur nach erfolgreicher Prüfung abhaken; neue Aufgaben und erkannte Fehler hinzufügen.
- [ ] Tests und ihren tatsächlichen Status dokumentieren; einen nicht ausgeführten Test niemals als bestanden bezeichnen.
- [ ] Vor Veröffentlichung erneut alle offenen TODO-Punkte auf mögliche Release-Blocker prüfen.
- [ ] In jedem Release-Bericht auf diese TODO-Liste verweisen und erledigte, offene und blockierende Punkte benennen.

**Ein Update ohne dokumentierte TODO-Prüfung darf nicht als abgeschlossen oder freigegeben gelten.**

## Priorität: Automatischer VectorCraft-Start aus der Chat-App

- [ ] Beim Start von VectorCraft Chat prüfen, ob die lokale Steuerschnittstelle auf `127.0.0.1:7979` erreichbar ist.
- [ ] Falls VectorCraft noch nicht läuft, die installierte Anwendung selbstständig mit `--control 7979` starten.
- [ ] Installationspfad unter Windows/macOS erkennen; gegebenenfalls einmalig auswählen und für spätere Starts speichern.
- [ ] Falls VectorCraft bereits mit aktivem Kanal läuft, diese Instanz wiederverwenden (keinen zweiten Prozess starten).
- [ ] Erreichbarkeit und tatsächliche Protokollantwort abwarten, dann erst die Konstruktionsfunktionen freigeben.
- [ ] Kompakten Verbindungsstatus und Schaltfläche **„VectorCraft starten / verbinden“** anbieten.
- [ ] Bei fehlendem Programm, blockiertem Port, Zeitüberschreitung oder Verbindungsabbruch verständliche Fehler anzeigen und eine speicherbare Diagnose ermöglichen.
- [ ] Windows- und macOS-Tests inklusive Start bei geschlossenem VectorCraft, vorhandener Instanz und fehlgeschlagenem Start automatisieren.
- [ ] Kein separates BAT- oder offenes Konsolenfenster als Voraussetzung. Die Chat-App ist der einzige Einstiegspunkt.

**Status:** beschlossen, noch nicht implementiert. Keine Version als funktionsfähig freigeben, bevor echte Integrations- und Engine-Tests bestanden sind.

## Weitere offene Hauptaufgaben

- [ ] Vollständigen Chat-App-Quellcode samt Builds im Repository sichern.
- [ ] Echten Headless-Engine-Test für Dreieck → Objekt-ID → Drehung in GitHub Actions erfolgreich ausführen und Logs prüfen.
- [ ] Freie KI-Konstruktionsaufträge robust und schemavalidiert in native VectorCraft-Aktionen überführen.
- [ ] Interaktive Nachbearbeitung und Erhalt manueller Änderungen nachweisen.
- [ ] Dynamische Modellauswahl, sichere API-Key-Speicherung und Diagnose im Betrieb prüfen.
- [ ] Kostengrenze 0,10 € pro Auftrag technisch zuverlässig absichern.
