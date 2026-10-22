# VectorCraft Chat – TODO

## VCCHAT.47 – nachgewiesener Freigabeblocker

Der tatsächlich neu gestartete [Live-Lauf 39726464472](https://github.com/wibem1/vectorcraft/actions/runs/39726464472), Job 119651382410, ist mit `NOT_CONFIGURED` fehlgeschlagen: Repository-Secret `OPENROUTER_API_KEY` fehlt. Vollständiges Protokoll gelesen; 0 Completion-Anfragen. Dieser fehlende Pflichtnachweis wird jetzt als Fehler statt als grüner Job markiert. Ein gültiger Testschlüssel muss über die GitHub-Secret-Verwaltung verfügbar gemacht werden; keine Schlüssel im Chat, Repository oder Diagnoseprotokoll speichern. Der bisherige Live-Probeauftrag verlangt nur „OK“ und ersetzt auch mit Schlüssel noch keinen vollständigen natürlichen Konstruktionsauftrag über die native Engine.

Anwendungsstand `a38c87aa17b0f674cfc0970eb125920cde3f8aa9`: lokal 67 Tests bestanden, 4 Spezialtests übersprungen. Echte Actions-Läufe ausgelöst: [Headless 39726542201](https://github.com/wibem1/vectorcraft/actions/runs/39726542201), [native Windows/macOS 39726542081](https://github.com/wibem1/vectorcraft/actions/runs/39726542081), [Pakete 39726542072](https://github.com/wibem1/vectorcraft/actions/runs/39726542072), [Regressionen 39726542048](https://github.com/wibem1/vectorcraft/actions/runs/39726542048). Zum dokumentierten Abruf noch laufend/wartend; ausdrücklich kein bestandener Plattformnachweis für diesen Stand. Historischer Headless-Lauf 39725452448 für 92b9b676 ist SUCCESS, darf nicht auf diese Änderungen übertragen werden.

[Maschinenlesbarer Nachweis](docs/test-results/2026-10-22-release-blocker.json). Allgemeine freie Konstruktionen und komplexe Live-Aufträge bleiben ungeprüft. Keine neue Version, kein Release, keine freigegebenen Downloadpakete. Kostenobergrenze bleibt eine konservative lokale Schätzung; keine providerseitige Garantie. Keine manuellen App-Tests angefordert.

## VCCHAT.45–46 – präzise Aufträge und Mehrfachobjektprüfung (22.10.2026)

TODO vor Änderung geprüft. Lokale Dreieck-/Dreh-Abkürzungen erkennen nur vollständig passende einfache Aufträge; Größen-, Farb-, Mehrfachobjekt- und explizite ID-Aufträge werden nicht mehr stillschweigend überschrieben. Allgemeine MCP-Pfade werden vor der Mutation validiert und danach über neue Objekt-ID, Ankerzahl und Geschlossenheit verifiziert. Native Suite erweitert um geschlossenen Vierpunktpfad und offenen Fünfpunktpfad, explizite Ziel-ID, echte unabhängige Zwischenbearbeitung und unveränderte andere Objekte. Die Suite läuft auch in beiden eingefrorenen Paketen.

Modellaktionen zum Verschieben, Drehen und Skalieren benötigen vor der Ausführung eine ausdrückliche ganzzahlige Ziel-ID; unvollständige Antworten werden abgewiesen statt auf das letzte Dreieck umgeleitet. Budgeteingabe über 0,10 € gesperrt. Oberfläche benennt ausdrücklich eine konservative Vorabprüfung ohne providerseitige Euro-Garantie; der ältere TODO-Punkt zur garantierten Obergrenze ist damit keine erfüllte Garantie. Ein positiver Live-OpenRouter-Ende-zu-Ende-Test bleibt Freigabebedingung. Lokal 71 Tests entdeckt, 67 bestanden, 4 native/Live-Spezialtests nicht lokal ausgeführt. Cargo ist lokal nicht installiert; Workspace-Gate nicht ausgeführt, Rust unverändert. Aktuelle native CI-Ergebnisse ausstehend. Keine Veröffentlichung.


## VCCHAT.41–43 – explizite Objekt-IDs (22.10.2026)

TODO vor Änderungen geprüft. Engine-Transformationen mit expliziter Objekt-ID werden jetzt über die verifizierende native MCP-Routine `transform_object` ausgeführt; dabei wird die ausdrücklich benannte Objekt-ID benutzt und vor und nach der Änderung geprüft. Die `id` wird nur als Zielangabe verwendet, nicht als Transformationsparameter. Ergänzende Regressionen für explizite Ziel-IDs, bisherige Dreieck-Kompatibilität und fremde Befehle wurden hinzugefügt. Quellstand `92b9b676`. Erneute CI-Prüfung läuft bzw. ist ausstehend, daher **keine neue Freigabe**. Weiter offen: freie allgemeine Konstruktionen, positiver Live-OpenRouter-Auftrag, garantierter providerseitiger 0,10-€-Deckel.

## CI-Nachtrag zu VCCHAT.35–38 (22.10.2026)

Der korrigierte Anwendungsstand `01e4af9d569030824399e48b9447f4103d1618e7` hat die Regressionen und Provider-Prüfungen [39724328678](https://github.com/wibem1/vectorcraft/actions/runs/39724328678) mit SUCCESS bestanden. Der Paketworkflow [39724328765](https://github.com/wibem1/vectorcraft/actions/runs/39724328765) meldet **Windows und macOS Intel SUCCESS**; Joblogs 119645071696 und 119645071711 gelesen, beide gefrorenen Kandidaten hochgeladen (Artefakte 12402891072 und 12402263480). Separate Headless- und native Plattformläufe 39724328635 / 39724328586 waren bei der Prüfung noch in_progress und werden ausdrücklich nicht als abgeschlossen gewertet. Neue freie KI-Komposition und positiver Live-OpenRouter-Auftrag weiterhin ungeprüft. **Keine Freigabe.**

## Fortsetzung VCCHAT.35–37 (22.10.2026)

TODO vor Änderungen geprüft. Eine nachgewiesene Zielverwechslungsgefahr bei freien KI-Folgeaktionen wurde korrigiert: Eine explizite Objekt-ID in `object.move`, `object.rotate` oder `object.scale` darf nicht durch die ID des zuletzt erstellten Dreiecks ersetzt werden. Für Kompatibilität bleibt die bisherige Dreieck-Folgeaktion ohne explizite Ziel-ID erhalten. Die Weiterleitung wird in `uses_verified_triangle_target` isoliert und durch drei Regressionstests für explizite, implizite und andere Befehle geprüft.

Die Änderungen sind zunächst **nicht als native Integration bestanden** zu werten, bevor aktuelle Actions-Logs vorliegen. Allgemeine freie Konstruktionen, positiver Live-OpenRouter-Auftrag und providerseitig garantierter 0,10-€-Deckel bleiben offen. Keine Release-Freigabe.

## Aktueller Abschluss: echte Engine und eigenständige Testpakete

TODO vor Änderung, Build und Abschluss geprüft. Headless und native Quelltests erneut erfolgreich; zusätzlich eigenständige Windows-/macOS-Intel-Testpakete samt echter Engine/CLI, gefrorener nativer Testsuite, HTTPS, Schlüsselablage und Archivabgleich erfolgreich. Keine Veröffentlichung, Version 0.3.1-dev. Positiver Live-Auftrag und garantierter Provider-Kostendeckel bleiben offen. Details: [Paketprotokoll](docs/PACKAGES-2026-10-21.md). Die folgenden älteren Abschnitte halten den jeweiligen historischen Zwischenstand fest.

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
- [x] Windows- und macOS-Tests inklusive Start bei geschlossenem VectorCraft, vorhandener Instanz und fehlgeschlagenem Start automatisieren (tatsächliche native CI: Windows Server 2025 x64 und macOS 15.7.9 Intel).
- [x] Kein separates BAT- oder offenes Konsolenfenster als Voraussetzung. Die Chat-App ist der einzige Einstiegspunkt.

**Status:** implementiert und tatsächlich unter Windows, macOS Intel und Linux geprüft; Referenzstand 1df86ea1, native Plattformintegration 39672716335 und Linux-Lauf 39672716402 erfolgreich. Pakete, positiver Live-OpenRouter-Auftrag und garantierte Kostenobergrenze bleiben offen. Keine vollständige Release-Freigabe.

## Weitere offene Hauptaufgaben

- [x] Vollständigen Chat-App-Quellcode und Buildskripte im Repository sichern; getestete portable Windows-/macOS-Intel-Builds als Actions-Artefakte (kein signierter Installer/Release).
- [x] Echten Headless-Engine-Test für Dreieck → Objekt-ID → Drehung in GitHub Actions erfolgreich ausführen und Logs prüfen.
- [ ] Freie KI-Konstruktionsaufträge robust und schemavalidiert in native VectorCraft-Aktionen überführen.
- [x] Interaktive Nachbearbeitung und Erhalt manueller Änderungen nachweisen (geprüfte Dreieck-/Transformationsfolge; freie Konstruktionen bleiben separat offen).
- [x] Dynamische Modellauswahl, API-Key-Speicherung und Diagnose im Betrieb prüfen (native Integration mit HTTP-Fixture; echte DPAPI-/isolierte Keychain-CRUD und Linux-Datei; positiver Live-OpenRouter-Auftrag bleibt separat offen).
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

- Konkrete Screenshot-Nachprüfung: [Run 39666190973](https://github.com/wibem1/vectorcraft/actions/runs/39666190973), Job `119451754906`, Quellstand b839127b; beim letzten Abruf noch Kompilation. Die vollständigen funktionalen Nachweise von c97651bb und die erfolgreiche Plattformmatrix bleiben davon getrennt dokumentiert. Kein Release.

## Abschluss der Screenshot-Nachprüfung, 21.10.2026

- TODO vor Abschluss erneut geprüft. [Run 39666190973](https://github.com/wibem1/vectorcraft/actions/runs/39666190973), Job 119451754906, Quellstand `b839127bec545dbead491f4be29f9ce4ab78abe3`: **SUCCESS**. Vollständiges Jobprotokoll gelesen: Kompilation, 58 Regressionen (4 separat ausgeführte Spezialtests), genaue Headless-Geometrie, Tk-/Engine-Callbacks und beide echten nativen Start-/Provider-Fixture-Folgen (OpenGL und Vulkan) bestanden. Kein Fehlertest entfernt oder durch eine Simulation ersetzt.
- Actions-Artefakt [12378482089](https://github.com/wibem1/vectorcraft/actions/runs/39666190973/artifacts/12378482089) heruntergeladen; SHA256 `3ab9c729ebc31ff35055532ac617dc2f399aaca80ece8abffcebff421db53710` stimmt. Nativen JSON-Bericht gelesen und Chat-PNG tatsächlich visuell geprüft: 540 × 490 Pixel, Fenster unverdeckt, Modell-/Key-/Port-/Budgetfelder, Verbindungs-/Diagnoseknöpfe, Verlauf und Eingabe vollständig sichtbar; Test-Key maskiert. Die zuvor verdeckte Aufnahme ist damit korrigiert.
- Nachlauf bestätigt erneut: genau ein nativer Start, Dreieck ID 2 mit drei geschlossenen Ankern, 30° und anschließender Bewegung bei gleicher Identität, drei HTTP-Fixture-Anfragen, 0,0002 USD verbuchte Fixture-Kosten, 0 USD externe Modellkosten. Dauerhafter Nachweis: [Screenshot-Nachlauf](docs/test-results/2026-10-21-screenshot-rerun.json).
- Zugehörige neue Plattformmatrix 39666191087: Windows/Linux erfolgreich; macOS wurde nach Warteschlange **abgebrochen**, also kein neuer macOS-Erfolg behauptet. Die vollständige erfolgreiche Dreiplattformmatrix 39663769551 gehört zum unveränderten Anwendungsquellcode c97651bb. Der Vergleich c97651bb → main enthält ausschließlich Dokumentation und die Screenshot-Testkorrektur.
- Native Windows-/macOS-Ende-zu-Ende-Starts, tatsächlicher macOS-Keychain-Rundlauf, gültige Live-OpenRouter-Completion, installierbare Pakete und garantierte providerseitige Euro-Kostengrenze bleiben offen. Keine neue Version veröffentlicht; keine manuellen App-Tests angefordert.

## Zusätzliche echte OpenRouter-Prüfung

TODO vor CI-Änderung gelesen. Ein separater Workflow prüft einen gegebenenfalls vorhandenen Repository-Testschlüssel OPENROUTER_API_KEY mit höchstens einer Completion eines aktuell ausdrücklich mit null Preisen ausgewiesenen Textmodells. Kein Retry; tatsächliche gemeldete Abrechnung muss null sein. Ohne Schlüssel lautet der Bericht NOT_CONFIGURED, ausdrücklich kein bestandener Live-Test. Keine Schlüssel oder Antworttexte im Nachweis. Native Builds bleiben davon unabhängig. Ergebnis wird nach dem tatsächlichen Lauf ergänzt.

- TODO erneut geprüft: separate schnelle OS-Schlüsselspeicher-Prüfung ergänzt, damit Speichern/Lesen/Aktualisieren/Löschen mit echtem Windows-DPAPI und isoliertem echtem macOS-Keychain nicht vom Rust-Build oder GPU-Start abhängen. Anwendungscode und native Integrationsassertionen unverändert. Noch kein Erfolg behauptet; Ergebnis nach Logprüfung ergänzen.

## Zwischenstand der tatsächlichen OS-Prüfungen

- TODO vor Ergebnisübernahme erneut geprüft. [OS-Schlüsselspeicherlauf 39673786475](https://github.com/wibem1/vectorcraft/actions/runs/39673786475), Quellstand 7af0f8ff: **Windows und macOS SUCCESS**. Logs von Jobs 119478227927 und 119478228718 gelesen; Berichte heruntergeladen und geprüft. Tatsächliche App-Funktionen speichern, lesen, aktualisieren und löschen den Schlüssel über Windows-DPAPI bzw. einen isolierten echten macOS-Keychain. Kein Login-Keychain verwendet. [Dauerhafter Bericht](docs/test-results/2026-10-21-os-key-stores.json).
- [Echter OpenRouter-Prüflauf 39673176326](https://github.com/wibem1/vectorcraft/actions/runs/39673176326), Job 119476079289: **NOT_CONFIGURED**, kein Repository-Testschlüssel, 0 Completion-Anfragen. Job technisch erfolgreich, ausdrücklich **kein bestandener positiver Live-Test**. JSON-Artefakt 12379243984 gelesen; der Schlüssel wurde nicht angefordert oder ausgegeben.
- [Native Plattformintegration 39672716335](https://github.com/wibem1/vectorcraft/actions/runs/39672716335): Windows-Job 119474489253 und macOS-Job 119474489807 haben echte Tk-Desktops bestätigt; beim Zwischenstand kompilieren beide noch GUI/CLI. Noch kein nativer Plattform-Erfolg behauptet. Neuer Linux-Lauf 39672716402 ebenfalls in Kompilation.
- Lokaler echter OS-Fehlerpfad zusätzlich geprüft: Linux weist eine ungültige ausführbare Datei zurück; Chat meldet ConnectionFailure, kein simulierter Prozess. Keine Veröffentlichung, Version weiterhin 0.3.1-dev.

## Getrennte native Layoutprüfung

TODO vor Ergänzung gelesen. Windows-Integration 39672716335 / 119474489253 ist tatsächlich erfolgreich; vollständige Logs und JSON gelesen, native Dreiecksgeometrie auch im Bild sichtbar. Das vordere VectorCraft-Fenster verdeckt dort jedoch Chat. Ein schneller eigener Desktop-Workflow prüft deshalb die echte App-Klasse mit Produktions-Theme und isoliertem Profil in ihrem getrennt gekennzeichneten Anfangszustand, maskiertes Key-Feld und sichtbare/ungeclippte Hauptbedienelemente. Anheben ausschließlich für die Testaufnahme. Keine Engine- oder Provider-Aufrufe in diesem Layouttest; er ersetzt keinen nativen Funktionstest. Anwendungscode und bereits bestandene Windows-Assertions bleiben unverändert. macOS-GUI-Build noch ausstehend. Aufnahmeergebnis nach tatsächlicher Ausführung ergänzen.

## Verifizierter Abschluss: native Plattformen und Oberfläche

TODO vor Abschluss erneut gelesen. Anwendungsstand `1df86ea1bea85a70b9933ea8783498d981262698` ist auf allen drei geprüften Plattformen erfolgreich. Die danach übernommenen Änderungen betreffen ausschließlich CI und Dokumentation; Anwendungs-/Engine-Quellcode ist unverändert. Version bleibt **0.3.1-dev**, keine Veröffentlichung.

| Prüfung | Tatsächliches Ergebnis |
|---|---|
| [Native Windows-/macOS-Integration 39672716335](https://github.com/wibem1/vectorcraft/actions/runs/39672716335) | Beide Jobs **SUCCESS**; vollständige Logs gelesen |
| Windows 119474489253 | Server 2025 x64, echter DX12-Softwareadapter; 62 Regressionen (58 bestanden, 4 getrennte Spezialtests) und echter nativer GUI-Test bestanden |
| macOS 119474489807 | macOS 15.7.9 Intel, echter Metal-Adapter; 62 Regressionen (57 bestanden, 5 getrennte Spezialtests) und echter nativer GUI-Test bestanden |
| [Linux 39672716402](https://github.com/wibem1/vectorcraft/actions/runs/39672716402) | Headless-Geometrie, Tk, beide nativen Renderer OpenGL/Vulkan einschließlich neuem OS-Fehlerpfad bestanden |
| [Echte Schlüsselspeicher 39673786475](https://github.com/wibem1/vectorcraft/actions/runs/39673786475) | Windows-DPAPI und isolierter tatsächlicher macOS-Keychain: Speichern/Lesen/Aktualisieren/Löschen **PASS** |
| [Desktop-Layout 39677833630](https://github.com/wibem1/vectorcraft/actions/runs/39677833630) | Windows und macOS **PASS**, beide PNGs tatsächlich visuell geprüft |
| [Positiver Live-OpenRouter-Test 39673176326](https://github.com/wibem1/vectorcraft/actions/runs/39673176326) | **NOT_CONFIGURED**, kein Repository-Testschlüssel, keine Completion gesendet |

In beiden echten nativen Plattformläufen: genau ein gestarteter VectorCraft-Prozess, bestätigtes Steuerprotokoll, erstes Dokument automatisch vorbereitet, laufende Instanz wiederverwendet und bestehendes Dokument erhalten. Dreieck **ID 2**, drei geschlossene Anker, **30°**, nach Abwahl weitere native Bewegung **(17, -11)** bei gleicher Identität. Tatsächlicher OS-Startfehler einer ungültigen ausführbaren Datei geprüft; keine Prozesssimulation. Windows-MCP-Brücken werden tatsächlich mit CREATE_NO_WINDOW gestartet. Reale App-Funktionen prüfen Modellwahl, gespeicherten Schlüssel, frischen Objektkontext, Diagnose und Kostenbuchung gemeinsam mit echter TCP/MCP-Engine und lokaler HTTP-Provider-Fixture: drei HTTP-Anfragen, 0,0002 USD Fixture-Buchung, **0 USD externe Modellkosten**.

Die kombinierten nativen Bildschirmaufnahmen zeigen das vordere VectorCraft-Fenster und verdecken Chat teilweise. Sie werden ausdrücklich nicht als unverdeckte Chat-Layoutprüfung gewertet. Der separate schnelle Layoutlauf startet dieselbe App-Klasse mit Produktions-Theme und isoliertem Profil im klar bezeichneten unverbundenen Anfangszustand, hebt sie für die Aufnahme an, prüft sichtbare Bedienelemente innerhalb der Fenstergrenzen und das maskierte Key-Feld. Beide unverdeckten 540×490-PNGs sind angesehen. Dieser Layouttest ruft weder Engine noch Provider auf und ersetzt keinen nativen Funktionstest.

Alle genannten JSON-/PNG-Artefakte wurden heruntergeladen; SHA256 stimmt mit GitHub-Metadaten überein. Dauerhafter zusammengeführter Nachweis: [native-platforms.json](docs/test-results/2026-10-21-native-platforms.json). Die öffentliche Modellliste und HTTP-401 wurden im Linux-Job 119474489171 ebenfalls tatsächlich geprüft (16 Provider-Tests PASS); positive Modellantworten bleiben HTTP-Fixtures. Private Login-Keychains wurden absichtlich nicht verändert; der frühere fehlende Nachweis tatsächlicher macOS-Schlüsselspeicherung ist durch den isolierten echten OS-Keychain-Test abgedeckt.

Offen bleiben installierbare Chat-Pakete, ein positiver Live-Auftrag mit gültigem CI-Key, allgemeine freie Konstruktionen und eine garantierte providerseitige 0,10-€-Kostengrenze. Die geprüften Runner ersetzen keine Zusage für jede Windows-/Mac-Hardware; Apple Silicon und persönliche Windows-11-Installationen wurden hier nicht nativ ausgeführt. Das bestehende macOS-GUI-Paket liefert die CLI separat als ZIP; ein vollständiges Chat-Paket muss die Bridge mitbringen oder ihre Installation eindeutig prüfen. Erstbuildzeiten wurden mit 28m04s (Windows) und 33m58s (Mac) gemessen; Wiederverwendung nachgewiesen identischer Engine-Binaries ist ein künftiger CI-Optimierungspunkt. Kein Test wurde wegen Laufzeit entfernt.

## Laufender Schritt: eigenständige Testpakete

TODO vor Änderung gelesen. Windows-/macOS-Intel-Kandidaten bündeln Python/Tk,
Chat, tatsächlich kompilierte Engine und CLI. Die eingefrorene Anwendung führt
über --self-test dieselbe echte native Integrationssuite aus, einschließlich
Dreieck, Objektidentität, 30° und Provider-Fixture-Folgeänderung. Pakete werden
nur nach bestandener Prüfung als Actions-Artefakt hochgeladen. Kein Release,
kein Versionssprung. Build und gefrorene Ausführung zunächst **ausstehend**.
PyInstaller-Aufbau anhand offizieller Dokumentation geprüft:
https://pyinstaller.org/en/stable/usage.html . Positive Live-Completion und
providerseitige Kostengarantie bleiben separat offen.

Paketprüfung vor CI-Abschluss: macOS-Lizenzen/Lesemich nach Contents/Resources
verschoben, damit keine unversiegelten Dateien im Bundle-Wurzelverzeichnis
liegen (Apple errSecCSUnsealedAppRoot). Zusätzlich strikte codesign-Verifikation
und SHA256-Manifest der tatsächlich getesteten Chat-/Engine-/CLI-Binaries.
Dies ist eine vorsorgliche Quellcodekorrektur, kein bereits beobachteter CI-Fehler.
Referenz: https://developer.apple.com/documentation/security/errseccsunsealedapproot .

Paket-Einstieg ergänzt: Nach dem nativen Selbsttest müssen auch automatische
Engine-/CLI-Erkennung ohne Pfad-Overrides, echter öffentlicher Modellkatalog
über HTTPS und echter HTTP-401-Pfad aus dem gefrorenen Prozess bestehen.
Absichtlich ungültiger Testschlüssel, keine bezahlte/positive Completion.
Dies prüft insbesondere SSL-/Runtime-Abhängigkeiten des eigenständigen Pakets.
Ergebnisse zunächst ausstehend; unveränderte Produktions-App-Klasse.

Tatsächliche Paketfehler gelesen: Windows 39679379961 / 119497548407
kompiliert und friert erfolgreich ein, hängt aber vor Anlage des Testprotokolls
und erreicht 300-s-Timeout; kein Paket hochgeladen. macOS 39679807472 /
119499018802 scheitert bei PyInstaller-BUNDLE: --icon NONE wird dort als
Dateiname behandelt. Korrektur: vorhandenes lizenziertes VectorCraft-ICNS unter
macOS; frühes Bootstrap-Log vor Import der App; Fehlerdiagnose über zusätzliche
Konsolen-EXE ausschließlich bei fehlgeschlagenem Windowed-Test. Kein Ersatz
des verpflichtenden Windowed-Erfolgs. Erneuter echter Paketlauf erforderlich.

CI-Laufzeitkorrektur: Fertige native Engine/CLI werden vor der Paketprüfung
separat gesichert. Der exakte Cache-Key enthält alle Git-Blobs außerhalb von
Chat/Workflowdefinitionen, Rust 1.95.0, Runner-Architektur und ImageVersion;
keine unscharfen Restore-Keys. SHA256-Prüfung aller Binaries vor Wiederverwendung.
Native Änderungen erzwingen Neubuild. Jeder Paketkandidat führt unabhängig vom
Cache weiterhin die echte native Engine-Suite aus. Damit sollen reine
Python-Paketkorrekturen nicht erneut vollständige Rust-Links erfordern.
Grundlage: https://github.com/actions/cache (getrennte restore/save Actions).

Überholte Paketläufe begrenzt: Neuer Kandidatenlauf beendet ausschließlich
ältere Läufe desselben Paket-Workflows auf demselben Branch; Headless- und native
Quelltests bleiben erhalten. Eigenes kleines Ubuntu-Job mit actions:write nur
für diesen Abbruch; native Buildjobs bleiben contents:read. Künftige Läufe
verwenden zusätzlich dieselbe Concurrency-Gruppe. So blockieren bekannte alte
Icon-/Bootstrap-Varianten keine Windows-/Mac-Runner für die Korrektur.


## Abschließende Prüfung hochgeladener Kandidaten

Paketlauf 39682760797: Windows und macOS Intel erfolgreich. Windows-Berichte und
vollständiges Archiv bereits lokal heruntergeladen, SHA256 geprüft und alle drei
Executables gegen das Testmanifest abgeglichen. Danach Verbindung der lokalen
Ausführungsumgebung verloren; die abschließende Prüfung beider hochgeladenen
Archive wird deshalb direkt in Actions ausgeführt. Der Audit prüft gefrorene
Berichte, echte native Identität/30°, OS-Schlüsseltest, echte öffentliche HTTPS-
Prüfungen ohne gültigen Key, alle Binary-SHA256, macOS-Ausführungsrechte und
Lizenzhinweise. Keine neue Version oder Veröffentlichung.


Archiv-Audit 39687971880 / 119526766785 tatsächlich SUCCESS: beide Paketarchive
heruntergeladen, alle drei Binary-Hashes gegen Testmanifest bestätigt; Mac-
Ausführungsrechte und Lizenzhinweise vorhanden. Gefrorene native Tests,
Pfaderkennung, 468 echte öffentliche Modelle und HTTP 401 auf beiden Plattformen
PASS. Audit gibt ergänzend die vollständigen gefrorenen Selbsttest-Logs aus,
damit diese trotz ausgefallener lokaler Umgebung direkt gelesen werden können.


## Verifizierter Paketabschluss

TODO vor Abschluss erneut geprüft. Quelle `6ba2c2c1`: Paketlauf [39682760797](https://github.com/wibem1/vectorcraft/actions/runs/39682760797) **Windows und macOS Intel SUCCESS**. Echte gefrorene Windowed-App mit gebündelter Engine und CLI: jeweils ein nativer Start, Dreieck ID 2, drei geschlossene Anker, 30°, Folgebewegung (17,-11), Instanz-/Dokumenterhalt, echter OS-Startfehler, DPAPI bzw. isolierter Keychain, Modellwahl, redigierte Diagnose, Fixture-Kostenbuchung. Keine Engine-Mocks. Pro Paket ein nativer Test ausgeführt, keiner übersprungen. Zusätzliche echte öffentliche HTTPS-Prüfungen: 468 Modelle und HTTP 401 mit ungültigem Key; keine positive Live-Completion und 0 USD externe Modellkosten.

Windows-Gesamtartefakte lokal heruntergeladen und SHA256 geprüft; alle drei archivierten Executables gegen Testmanifest bestätigt. Nach Verlust der lokalen Umgebung [unabhängiger Actions-Archivabgleich 39687971880](https://github.com/wibem1/vectorcraft/actions/runs/39687971880) erfolgreich: beide hochgeladenen ZIPs heruntergeladen, Binary-SHA256, macOS-Ausführungsrechte, Lizenzhinweise und Berichte geprüft. Dauerhafter [vollständiger JSON-Bericht](docs/test-results/2026-10-21-frozen-candidates.json). Keine Behauptung eines lokalen Mac-Gesamtarchiv-Downloads.

Version bleibt **0.3.1-dev**, kein Tag, kein Release. Offen: gültiger positiver OpenRouter-Live-Auftrag, allgemeine freie Konstruktionen, garantierte providerseitige 0,10-€-Grenze, signierte Installer/Notarisierung, Apple Silicon und Ausführung auf einer sauberen Nutzerinstallation. Keine manuellen App-Tests angefordert. Cargo-Workspace-Gate lokal nicht ausführbar (Cargo fehlte; später lokale Umgebung offline); Rust unverändert. Echte native Builds und Tests in Actions sind erfolgreich.

Vollständige gefrorene Selbsttest-Logs zusätzlich im erfolgreichen Audit 39688117575 / 119527252289 gelesen; Windows 17,731 s, Mac 53,169 s, jeweils PASS NATIVE und OK. Packaging-Lint 39688117539 / 119527252153 SUCCESS.
