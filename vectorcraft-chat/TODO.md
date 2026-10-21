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

## Prüfung 21.10.2026 — native Startdiagnose

- TODO vor Änderung erneut gelesen; die Punkte für automatischen Start bleiben offen, bis der echte native Integrationslauf besteht.
- Die beiden jüngsten Commits zum Renderer (OpenGL/Vulkan) liefern über die hier verfügbaren GitHub-Connector-Abfragen keine auswertbaren Workflow-Läufe. Daraus folgt **kein Testerfolg**.
- CI wurde um GPU-Treiber-, Bibliotheks- und Binary-Abhängigkeitsdiagnosen sowie Backtraces für beide Renderer erweitert (Commit `89ca207`).
- Nächster erforderlicher Schritt: tatsächliche CI-Läufe samt stderr-Artefakt auswerten, Fehler beheben und denselben nativen Test erneut ausführen. Keine Veröffentlichung, keine manuellen Nutzer-Tests.

## Tatsächlich gestarteter CI-Wiederholungslauf (21.10.2026)

- Die verbindliche TODO-Prüfung wurde vor dem nächsten Prüfschritt durchgeführt.
- Über die GitHub-Actions-Schnittstelle wurde das zuvor gescheiterte native Job `119331400903` tatsächlich erneut angefordert; GitHub bestätigte `success: true` für den **Startauftrag**, nicht für den Test.
- [Run 39631724096](https://github.com/wibem1/vectorcraft/actions/runs/39631724096) hat den neuen Job `119431947623`; beim ersten Abruf war er `in_progress`.
- Dieser Rerun testet den historischen Workflow-Stand, nicht die danach hinzugefügten OpenGL-/Backtrace-Diagnosen. Der Fehler bleibt ein Release-Blocker bis zur vollständigen erfolgreichen Prüfung des aktuellen Stands.

## Fortsetzung: native Startursache und durchgehender Provider-Test

- TODO vor Änderungen und Teststart erneut geprüft. Run 39631724096 / Job 119431947623 kompiliert beim ersten Abruf noch den historischen Stand.
- Vollständiges Fehlerprotokoll von Run 39658864183, Job 119426286283 gelesen: `libxkbcommon-x11.so` fehlt. Die bereits auf main eingegangene Korrektur d12e2939 installiert und prüft diese Bibliothek vor dem Build. Tatsächlicher Korrekturlauf: 39661233784 / 119434447781; Ergebnis zunächst ausstehend.
- Nativen Integrationstest erweitert: dynamischer Modellkatalog, gespeicherter Test-Key, echter HTTP-Request/JSON-Parser gegen lokalen Provider-Testserver, frischer Objektkontext, Modellaktion über native TCP/MCP-Verbindung, Abwahl und Wiederselektion desselben Objekts, Verschieben um (17, -11), Kostenbuchung und geheimnisfreie Diagnose. Keine Engine-Mocks. Provider ist ausdrücklich eine HTTP-Fixture; kein echter bezahlter OpenRouter-Auftrag.
- Automatischer Start auf Windows/macOS, gültige Live-Completion, native Pakete und garantierte Kostenobergrenze bleiben offen. Kein Release. Ergebnisse werden nach tatsächlicher Ausführung ergänzt.
