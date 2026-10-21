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

- [x] Beim Start von VectorCraft Chat prüfen, ob die lokale Steuerschnittstelle auf `127.0.0.1:7979` erreichbar ist.
- [x] Falls VectorCraft noch nicht läuft, die installierte Anwendung selbstständig mit `--control 7979` starten.
- [x] Installationspfad unter Windows/macOS erkennen; gegebenenfalls einmalig auswählen und für spätere Starts speichern.
- [x] Falls VectorCraft bereits mit aktivem Kanal läuft, diese Instanz wiederverwenden (keinen zweiten Prozess starten).
- [x] Erreichbarkeit und tatsächliche Protokollantwort abwarten, dann erst die Konstruktionsfunktionen freigeben.
- [x] Kompakten Verbindungsstatus und Schaltfläche **„VectorCraft starten / verbinden“** anbieten.
- [x] Bei fehlendem Programm, blockiertem Port, Zeitüberschreitung oder Verbindungsabbruch verständliche Fehler anzeigen und eine speicherbare Diagnose ermöglichen.
- [ ] Windows- und macOS-Tests inklusive Start bei geschlossenem VectorCraft, vorhandener Instanz und fehlgeschlagenem Start automatisieren.
- [x] Kein separates BAT- oder offenes Konsolenfenster als Voraussetzung. Die Chat-App ist der einzige Einstiegspunkt.

**Status:** implementiert; echter nativer Linux-Start unter OpenGL und Vulkan erfolgreich geprüft. Windows/macOS-Lifecycle-Regressionen bestanden; echte native Prozessintegration dieser beiden Plattformen bleibt offen. Keine vollständige Release-Freigabe.

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

- Zusätzliche Verbindungsprüfung: Dokument-/Protokollfehler und leere Kataloge brechen jetzt vor Modellkatalog, bezahltem Request und Kostenreservierung ab. Der bisherige allgemeine Fehlerpfad konnte trotz fehlendem bestätigtem Zustand eine Anfrage senden. Neuer Regressionstest deckt RuntimeError, ValueError, OSError, null-Dokument und leeren Katalog ab. TODO vor Änderung erneut gelesen; erneute CI erforderlich.

## Zweiter nachgewiesener Startfehler: leeres natives Dokumentfenster

- TODO erneut vor Korrektur geprüft. Korrekturlauf 39661233784 / 119434447781 tatsächlich abgeschlossen und vollständige Logs ausgewertet: X11-Abhängigkeit behoben; native Anwendung rendert unter OpenGL und Vulkan, TCP-Kanal erreichbar. Kein vollständiger Integrationserfolg: Chat-Verbindung scheitert danach an `document.inspect` / `no document open`.
- Rust-Protokollquelle geprüft: `document.inspect` setzt ein aktives Dokument voraus; `ui.inspect` liefert dagegen immer `documents`, `activeDocument`, `opening` und `fileDialog`. Die bisherige Annahme einer null-Antwort war falsch.
- Chat prüft nun zuerst den nativen UI-Status und erstellt ausschließlich bei bestätigter leerer Dokumentliste ohne laufenden Öffnungsvorgang ein neues Dokument. Bestehende Dokumente bleiben erhalten; Fehler/unbekannte Zustände erzeugen kein Dokument. Regressionen und nativer Wiederverbindungserhalt ergänzt; keine Testvorbereitung durch externes `file.new`.
- Vollständige native Folge und Provider-Fixture müssen auf diesem Stand erneut unter Actions bestehen. Kein Release.

- TODO vor CI-Änderung gelesen. Rust-Cache um Workspace-Crates und einen getrennten Cache-Key erweitert (offizielles Action-Schema geprüft). Cargo-Build bleibt verpflichtend; unveränderter Rust-Code kann künftig wiederverwendet werden, statt ihn für jede Python-Korrektur vollständig neu zu übersetzen. Kein Test wird übersprungen.

## Tatsächlich laufende Prüfung des korrigierten Dokumentstarts

- Geprüfter Quellstand: `c97651bb02c67c842031e93df04327c089daa36a` (enthält Dokumentkorrektur `5f9b9e4f`).
- [Native Integration 39663769616](https://github.com/wibem1/vectorcraft/actions/runs/39663769616), Job `119443285040`: beim letzten Abruf noch Rust-Kompilation; **noch kein Testerfolg**.
- [Plattformprüfung 39663769551](https://github.com/wibem1/vectorcraft/actions/runs/39663769551): Linux `119443284998` und Windows `119443285327` erfolgreich. Je 62 Tests entdeckt, 58 bestanden und 4 explizite CI-Spezialtests ausgelagert. Linux zusätzlich 16 Provider-Tests bestanden, darunter echte öffentliche Modellliste und HTTP-401-Prüfung. Logs tatsächlich gelesen. macOS `119443285238` noch queued.
- Lokal: 62 Tests entdeckt, 58 bestanden, 4 ausdrücklich ausgelagert. `git diff --check` ohne Fehler. `cargo xtask ci` konnte lokal nicht starten (Cargo fehlt); kein vollständiger Rust-Workspace-Gate behauptet. Rust-Quellcode unverändert, echte GUI/CLI-Kompilation bleibt in Actions verpflichtend.
- Kein gültiger OpenRouter-Key in dieser Ausführungsumgebung: positive Live-Completion bleibt ungeprüft. Native Provider-Folge verwendet ausdrücklich einen lokalen HTTP-Testserver. Keine Veröffentlichung und keine manuellen App-Tests angefordert.

## Verifizierter Abschluss dieses Prüfschritts, 21.10.2026

- TODO vor Abschluss erneut gelesen. Anwendung bleibt **0.3.1-dev**, kein Release und keine manuellen Tests angefordert.
- Geprüfter Programmstand `c97651bb02c67c842031e93df04327c089daa36a`: [native GUI/Engine-Integration 39663769616](https://github.com/wibem1/vectorcraft/actions/runs/39663769616), Job `119443285040`, **SUCCESS**. Vollständiges Jobprotokoll gelesen: native Tests sowohl OpenGL als auch Vulkan tatsächlich bestanden (zwei ausdrückliche PASS-Meldungen, nicht nur die durch continue-on-error geglättete Schrittanzeige).
- Nachgewiesen: Chat startet die echte Anwendung genau einmal, wartet auf bestätigtes Protokoll, legt das erste Dokument an, verwendet die laufende Instanz wieder und bewahrt ein bestehendes Dokument. Dreieck ID **2**, 3 geschlossene Anker, 30°-Drehung, Modell-Folgeaktion über tatsächliches HTTP/JSON gegen lokalen Testserver und native TCP/MCP-Verbindung: Verschieben um (17, -11), weiterhin ID 2 und 30°. Schlüssel-Rundlauf, Modellauswahl, aktueller Objektkontext, 0,0002 USD Fixture-Kostenbuchung und keyfreie Diagnose bestanden. Tatsächliche externe Modellkosten: 0 USD.
- [Plattformlauf 39663769551](https://github.com/wibem1/vectorcraft/actions/runs/39663769551): **Windows, Linux und macOS SUCCESS**, einschließlich der neuen Dokument-/Kosten-Abbruchregressionen. Je 62 Tests entdeckt: Windows/Linux 58 bestanden + 4 explizite Spezialtests ausgelagert; macOS 57 bestanden + 5 ausgelagert (zusätzlich echter Login-Keychain-Rundlauf). Linux führt die beiden öffentlichen OpenRouter-HTTP-Prüfungen sowie Tk-/native Engine-Tests in getrennten Schritten aus; kein bezahlter Live-Auftrag behauptet.
- Actions-Artefakt `12377513103` heruntergeladen und SHA256 `9dc78829166e84425518a33c26df2506ab62eaa25b40ae5d36032e58da1dce8c` geprüft; nativer JSON-Bericht tatsächlich gelesen. Dauerhafter Bericht: [test-results/2026-10-21-native-startup.json](docs/test-results/2026-10-21-native-startup.json).
- Verbleibende Freigabeblocker: echte native Windows-/macOS-Integration, installierbare Pakete, positiver Live-OpenRouter-Auftrag mit gültigem Test-Key, tatsächlicher macOS-Keychain-Rundlauf und garantierte Kostenobergrenze. Dynamische Modellliste/401 sind echte öffentliche HTTP-Tests; die positive Modellantwort bleibt ausdrücklich eine lokale HTTP-Fixture.
- Neu erkannt: Das Chat-PNG ist teilweise vom ebenfalls gestarteten nativen Fenster verdeckt; daraus folgt kein visueller Layout-Erfolgsnachweis. Screenshot-Aufnahme künftig nach Anheben des Chat-Fensters prüfen. Die funktionalen Tests sind davon unabhängig vollständig bestanden.
- Linux-Paketabhängigkeiten separat prüfen: Die CI installiert nun die bestätigte X11-Tastaturbibliothek; bestehende Paketmanifeste dürfen diese dynamische Abhängigkeit nicht übersehen.

## Parallel eingegangene Screenshot-Korrektur (erhalten)


- TODO reviewed before this change. Source c97651bb passed [native run 39663769616](https://github.com/wibem1/vectorcraft/actions/runs/39663769616), job 119443285040; full logs inspected. Both OpenGL and Vulkan native startup/triangle/30-degree rotation/follow-up move passed. Headless exact geometry, identity, manual intervening edits and real PNG also passed.
- [Platform run 39663769551](https://github.com/wibem1/vectorcraft/actions/runs/39663769551): Windows, Linux **and macOS passed**. Native GUI execution remains Linux-only; platform lifecycle regressions do not establish native GUI success on Windows/macOS.
- Downloaded artifact 12377513103 and read native JSON: one launch, triangle ID 2, rotation 29.999999999999996°, 3 closed anchors, 3 provider fixture requests, accounted fixture cost $0.0002, external charge $0. The valid paid OpenRouter path remains untested.
- Visual artifact inspection found Chat partially obscured by the native window under Xvfb. Correct the test capture by raising Chat and processing repaint events before ImageMagick capture; require screenshot command success. Application behavior is unchanged; request one integration rerun to inspect unobscured visual evidence.
- Update README to describe automatic startup and the console-free Windows source launcher. No release and no manual user test.

- Commit b839127b liegt zusätzlich auf main; die Teständerung bleibt erhalten. Der Anwendungsquellcode ist gegenüber dem erfolgreich getesteten Stand c97651bb unverändert. Visuelle Korrektur muss im zusätzlich gestarteten Lauf geprüft werden.
