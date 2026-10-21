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
- [x] Echten Headless-Engine-Test für Dreieck → Objekt-ID → Drehung in GitHub Actions erfolgreich ausführen und Logs prüfen.
- [ ] Freie KI-Konstruktionsaufträge robust und schemavalidiert in native VectorCraft-Aktionen überführen.
- [x] Interaktive Nachbearbeitung und Erhalt manueller Änderungen nachweisen (geprüfte Dreieck-/Transformationsfolge; freie Konstruktionen bleiben separat offen).
- [ ] Dynamische Modellauswahl, sichere API-Key-Speicherung und Diagnose im Betrieb prüfen.
- [ ] Kostengrenze 0,10 € pro Auftrag technisch zuverlässig absichern.

## Prüfung dieses Entwicklungsschritts, 21.10.2026

- TODO vor dem Zusammenführen und vor dem Abschluss erneut geprüft; automatische Startfunktion bewusst offen gelassen, keine Release-Freigabe.
- Vollständiger Python-App-Quellcode, Startskripte und CI liegen im Repository. Installierbare native Pakete sind noch offen; deshalb bleibt der kombinierte Quellcode-/Build-Punkt ungecheckt.
- Geprüfter Programmstand: `5629006d6d0886a95abc17d0258246c35c92c127`.
- [Echte Engine und Tk-Oberfläche](https://github.com/wibem1/vectorcraft/actions/runs/39624046757): **PASS**. ID 2 bleibt erhalten; exakte 30°-Drehung, Verschieben, Skalieren, weitere Drehung, zwischenzeitliche Änderung und unverändertes anderes Objekt ID 3; PNG und JSON als Actions-Artefakt.
- [App-/Provider-Prüfungen](https://github.com/wibem1/vectorcraft/actions/runs/39624046765): Windows und Linux **PASS**; macOS zum Abschluss noch **queued**, also nicht bestanden behauptet. Windows-DPAPI tatsächlich geprüft. macOS-Keychain-Rundlauf nicht geprüft.
- Unter Linux wurden über die getrennten Schritte sämtliche 37 entdeckten Tests ausgeführt: 34 normale Regressionen, 2 echte öffentliche HTTP-Prüfungen, 1 Tk-/Engine-Integrationstest. Windows: 34 Regressionen bestanden, 3 bewusst ausgelagert/übersprungen.
- Echte OpenRouter-Modellliste und HTTP-401-Pfad geprüft. Modellantworten/Aktionsvorschläge verwenden kontrollierte HTTP-Fixtures; ein bezahlter Auftrag mit gültigem API-Key wurde nicht ausgeführt.
- Kostenfehler behoben: USD/EUR-Vergleich, fehlende Abrechnung, Parserfehler, Neustart und kaputtes Kostenprotokoll. Konservative Vorabprüfung statt garantierter providerseitiger 0,10-€-Deckelung; dieser TODO-Punkt bleibt offen.
- Freigabeblocker: automatischer Start, ausstehende macOS-Prüfung/Paketbuilds, gültiger OpenRouter-Ende-zu-Ende-Auftrag und garantierte Kostenobergrenze. Kein neuer Release und keine manuellen App-Tests angefordert.

Details: [Entwicklungsprotokoll](docs/SESSION-2026-10-21.md).

## Laufender Schritt: automatischer Start

TODO vor Implementierung und Build geprüft. Start/Verbindung, Instanzwiederverwendung, Pfaderkennung, Bereitschaftssperre und Fehlerdiagnose sind implementiert; lokale Lifecycle-Tests bestanden. Die echte native GUI-Prüfung sowie Windows/macOS/Linux-CI werden mit diesem Commit angefordert. Punkte bleiben bis zur Logprüfung offen. Details: [Startprotokoll](docs/STARTUP-2026-10-21.md). Keine neue Version freigegeben.
