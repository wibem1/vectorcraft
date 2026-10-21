# Native Windows and macOS integration

TODO reviewed before changes and build. Version remains 0.3.1-dev; no release.

## Scope

Close the native Windows/macOS verification gap using actual default-feature VectorCraft GUI and CLI builds on standard GitHub-hosted runners. The existing Linux real-engine workflow stays in place. Positive provider completions still use a local HTTP fixture, not a paid OpenRouter key. Packaging and a provider-enforced EUR cap remain separate open work.

## Changes

- Add `vectorcraft-chat-native.yml`, Windows and macOS jobs with `fail-fast: false`. Verify an actual Tk desktop before compiling. Build GUI and CLI with the normal release command, run regressions, then run the same complete native integration without engine/control mocks. Capture screenshot, JSON and native stderr per platform.
- Adapt screenshot capture to native Windows/macOS with Pillow ImageGrab; Linux retains ImageMagick. Native API assertions remain mandatory regardless of renderer or screenshot behavior.
- Mac test creates/unlocks its own temporary keychain, directs actual app save/read/delete there via `VECTORCRAFT_CHAT_KEYCHAIN`, and deletes the test keychain afterward. No login-keychain item is used. Default application behavior is unchanged when no override is set.
- Windows MCP subprocesses now use `CREATE_NO_WINDOW`, as native startup already did. The actual native test checks the flags on real bridge launches. Previously only the main application launch had this protection.
- Test a real OS rejection of an invalid executable on a second unused port, without subprocess simulation; verify the successfully started native app stays alive and has only one launch. Existing initial-document, reuse, triangle ID, 30-degree rotation, selection recovery, follow-up move, model selection, HTTP/JSON, stored key, diagnostic and accounting checks stay mandatory.

## Validation before Actions

Local discovery: 62 tests, 58 passed, four explicitly separate integration/live tests skipped. `git diff --check` clean. Cargo is absent locally; actual GUI/CLI compilation and native OS tests must be verified in Actions. No Windows/macOS native success is claimed at this point.

Primary references checked for CI labels and Keychain argument handling:

- https://docs.github.com/en/actions/reference/runners/github-hosted-runners
- https://github.com/apple-oss-distributions/Security/blob/main/SecurityTool/macOS/security.c

Append actual workflow IDs, logs, failures and results after execution. Do not mark the platform TODO complete merely because jobs were submitted.

## Zwischenstand der tatsächlichen OS-Prüfungen

- TODO vor Ergebnisübernahme erneut geprüft. [OS-Schlüsselspeicherlauf 39673786475](https://github.com/wibem1/vectorcraft/actions/runs/39673786475), Quellstand 7af0f8ff: **Windows und macOS SUCCESS**. Logs von Jobs 119478227927 und 119478228718 gelesen; Berichte heruntergeladen und geprüft. Tatsächliche App-Funktionen speichern, lesen, aktualisieren und löschen den Schlüssel über Windows-DPAPI bzw. einen isolierten echten macOS-Keychain. Kein Login-Keychain verwendet. [Dauerhafter Bericht](test-results/2026-10-21-os-key-stores.json).
- [Echter OpenRouter-Prüflauf 39673176326](https://github.com/wibem1/vectorcraft/actions/runs/39673176326), Job 119476079289: **NOT_CONFIGURED**, kein Repository-Testschlüssel, 0 Completion-Anfragen. Job technisch erfolgreich, ausdrücklich **kein bestandener positiver Live-Test**. JSON-Artefakt 12379243984 gelesen; der Schlüssel wurde nicht angefordert oder ausgegeben.
- [Native Plattformintegration 39672716335](https://github.com/wibem1/vectorcraft/actions/runs/39672716335): Windows-Job 119474489253 und macOS-Job 119474489807 haben echte Tk-Desktops bestätigt; beim Zwischenstand kompilieren beide noch GUI/CLI. Noch kein nativer Plattform-Erfolg behauptet. Neuer Linux-Lauf 39672716402 ebenfalls in Kompilation.
- Lokaler echter OS-Fehlerpfad zusätzlich geprüft: Linux weist eine ungültige ausführbare Datei zurück; Chat meldet ConnectionFailure, kein simulierter Prozess. Keine Veröffentlichung, Version weiterhin 0.3.1-dev.

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

Alle genannten JSON-/PNG-Artefakte wurden heruntergeladen; SHA256 stimmt mit GitHub-Metadaten überein. Dauerhafter zusammengeführter Nachweis: [native-platforms.json](test-results/2026-10-21-native-platforms.json). Die öffentliche Modellliste und HTTP-401 wurden im Linux-Job 119474489171 ebenfalls tatsächlich geprüft (16 Provider-Tests PASS); positive Modellantworten bleiben HTTP-Fixtures. Private Login-Keychains wurden absichtlich nicht verändert; der frühere fehlende Nachweis tatsächlicher macOS-Schlüsselspeicherung ist durch den isolierten echten OS-Keychain-Test abgedeckt.

Offen bleiben installierbare Chat-Pakete, ein positiver Live-Auftrag mit gültigem CI-Key, allgemeine freie Konstruktionen und eine garantierte providerseitige 0,10-€-Kostengrenze. Die geprüften Runner ersetzen keine Zusage für jede Windows-/Mac-Hardware; Apple Silicon und persönliche Windows-11-Installationen wurden hier nicht nativ ausgeführt. Das bestehende macOS-GUI-Paket liefert die CLI separat als ZIP; ein vollständiges Chat-Paket muss die Bridge mitbringen oder ihre Installation eindeutig prüfen. Erstbuildzeiten wurden mit 28m04s (Windows) und 33m58s (Mac) gemessen; Wiederverwendung nachgewiesen identischer Engine-Binaries ist ein künftiger CI-Optimierungspunkt. Kein Test wurde wegen Laufzeit entfernt.
