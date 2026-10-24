# VectorCraft Chat — verbindlicher Projektstand

## Historischer Nachweis vom 14.10.2026 (am 23.10. anhand Gesprächsexports abgeglichen)

Der konkrete, quellenbasierte Bericht liegt in [docs/REFERENCE-2026-10-14.md](docs/REFERENCE-2026-10-14.md). Wichtigste Klarstellung: **ChatGPT erstellte die Steuerprogramme, ausgeführt wurden sie lokal vom Nutzer; die lokale TCP/JSON-Kommunikation war erfolgreich. Ein eigener direkter ChatGPT-Netzwerkzugang auf Port 7979 ist nicht belegt.** Zeichentest v5 und Agententest v7 verwendeten vorbereitete Befehle; die frei interpretierende KI-Steuerung blieb unbewiesen. Mandala-Live-Repeat-Geometrie funktionierte, interaktive Repeat-Containerbearbeitung war offen. Die Originalreferenz liegt weiterhin nicht im GitHub-Repository. Diese Ergänzung ist Dokumentation, kein neuer Live-Test und keine neue Release-Freigabe.

## Verbindliche Strategieentscheidung — 23.10.2026
**Beschlossen:** Die bisherige komplexe VectorCraft-Chat-App wird **nicht** als Reparaturprojekt fortgeführt. Stattdessen kontrollierter, kleiner Neustart ausgehend von dem historisch erfolgreich erprobten direkten Python-Steuerprogramm. Dies ist eine Strategieentscheidung, noch **keine** implementierte oder getestete Änderung.

- **Ziel:** Natürlicher KI-Auftrag → gültige VectorCraft-Aktionen → echte lokale Engine (TCP 127.0.0.1:7979) → sichtbare editierbare Konstruktion → gezielte Folgeänderung anhand derselben Objekt-ID.
- **Referenz:** `VectorCraft-Mandala-Zentriert-v2.zip`, historisch am 14.10. bestätigt. Archiv ist **noch nicht nachweislich im Repository enthalten**; SHA-256 laut Übergabetest: `09ab09949b987a71d7735dd456bca5795eddb60d98bf9cedf1661232ee23f6ae`. Zuerst unveränderte Referenz sichern und Verfügbarkeit prüfen. Historischer Erfolg ist kein heutiger Live-Test.
- **Schritt 1:** Minimale, isolierte TCP/JSON-Steuerung der echten Engine mit kleinem deterministischem Test belegen (Dreieck, Objekt-ID, 30° Drehung desselben Objekts). Wenn Referenz nicht im Repo liegt, Archiv anfordern statt nachzubauen.
- **Schritt 2:** Erst dann einen **minimalen KI-Adapter** bauen: natürliche Sprache → kleine, strukturierte, validierte Aktionsliste. Antwort vollständig? Abbruchgrund? unbekannte Befehle? Maximalumfang? Keine fehlerhafte Antwort ausführen. Mit gespeicherten Provider-Antworten kostenlos testen, danach gezielt eine echte Anfrage mit vorab geprüften Kosten.
- **Schritt 3:** KI-Adapter + echte Engine + überprüfbare Folgeänderung integrieren. Erst nach positivem End-to-End-Nachweis Chatoberfläche, Packaging, Windows/macOS.
- **Altprojekt:** Alter `vectorcraft-chat/`-Code und `TODO.md` bleiben unverändert als technische Referenz/Fehlergeschichte, sind **kein** Entwicklungsauftrag zur Fortsetzung des bisherigen Reparaturpfads. Einzelkomponenten nur nach isolierter Bewertung übernehmen. Neue Implementierung soll getrennt vom bisherigen App-Code entstehen; den konkreten Pfad erst beim ersten Entwicklungsauftrag wählen.
- **Arbeitsweise:** Globales Regelwerk `wibem1/AI-Development-Standards`; ein kleiner überprüfbarer Schritt; GitHub aktualisieren; keine unbelegten Releases, keine Build-/Work-/API-Schleifen. Keine parallele Bearbeitung derselben Basis.
- **Nächster Auftrag für neuen Chat:** Zuerst nur Übernahme und Verifikation der Referenzdateien / des minimalen technischen Startpunkts, dann den **ersten einzelnen Funktionstest** vorschlagen. Keine Wiederaufnahme des alten App-Reparaturplans. Keine Programmänderungen oder kostenpflichtigen Aufrufe, bevor dieser Schritt feststeht.

Stand: 2026-10-23 · Übergabe aus Chat · nur Dokumentation

## Ziel
Eine kleine, kostengünstige KI-Chatsteuerung für die bereits installierte VectorCraft-Anwendung: natürliche Anweisungen → gültige VectorCraft-Kommandos → sichtbare, editierbare Konstruktion → gezielte Folgeänderung desselben Objekts. Windows und macOS erst nach erfolgreichem Kernnachweis.

## Gesicherte Erkenntnisse
- Am 14.10.2026 funktionierte die direkte lokale VectorCraft-Steuerung über TCP 127.0.0.1:7979, mit `engine.execute`, `document.inspect` und `engine.commands`. Damalige Diagnosen meldeten erfolgreich erzeugte/bearbeitete Dokumente und Exporte.
- Referenz: `VectorCraft-Mandala-Zentriert-v2.zip` (ursprüngliche Sicherung, NICHT durch dieses Dokument im Repository abgelegt). SHA-256 des ursprünglichen ZIP laut abgeschlossener Übergabeprüfung E01: `09ab09949b987a71d7735dd456bca5795eddb60d98bf9cedf1661232ee23f6ae`.
- Inhalt der Referenz-ZIP: `vectorcraft_mandala_zentriert.py`, `01_Pruefen.bat`, `02_Mandala_zentriert_erstellen.bat`, `ANLEITUNG.txt`. Damals erfolgreich: drei native radiale Live-Repeat-Ringe mit Mittelpunkt (700,700); durch den Nutzer am 14.10. bestätigt. Eine erneute Live-Ausführung erfolgte im Übergabetest nicht.
- Ein Chat-zu-Chat-Übernahme-/Rückübergabetest E01 mit unverändertem Originalcode und SHA-256-Prüfung war erfolgreich. E01 belegt eine statische Übergabe, NICHT die erfolgreiche Weiterentwicklung.
- Der spätere VectorCraft-Chat-Prototyp hatte wiederholt Fehler in der KI-Antwortverarbeitung, Befehlsvalidierung, Token-/Kostenkontrolle und Integration. Das ist kein Beleg, dass die VectorCraft-Engine nicht funktioniert.
- Die bestehende Datei `vectorcraft-chat/TODO.md` dokumentiert technische Arbeiten, Testläufe und offene Freigabeblocker; ihre Aussagen sind zunächst historische Einträge, kein automatisch aktueller Freigabenachweis.

## Was ausdrücklich NICHT nachgewiesen ist
- Zuverlässige freie KI-Steuerung über OpenRouter bis zur sichtbaren Konstruktion und interaktiven Folgeänderung.
- Erfolgreiche, aktuelle End-to-End-Integrationstests der veröffentlichten Windows- und Mac-App.
- Dass das Mandala-Referenzarchiv bereits in diesem GitHub-Repository abgelegt ist.
- Verbindlich technisch erzwungene Limits für Work-Credits oder eine garantierte Euro-Obergrenze bei einem Provider.

## Ursachenanalyse / verbindliche organisatorische Erkenntnisse
- Unterschied zwischen funktionierendem deterministischem Steuerprogramm und noch unbewiesener freier KI-Interpretation beachten.
- Zu früher Ausbau von UI, Mehrmodellsteuerung, Diagnose, Packaging und Actions vergrößerte die Fehlerfläche.
- Syntaktisch geprüfter Code und erfolgreiche Builds ersetzen keinen echten Funktionstest.
- Wiederholte Chats/Work-Aufträge verloren verifizierte Erkenntnisse; mehrere Reparatur- und Buildschleifen erzeugten Kosten ohne nachgewiesenen Nutzen.
- GitHub dient als dauerhafter Speicher für Code und Projektzustand, nicht als Anlass für dauernde Actions-Läufe.

## Nächster Schritt (ausschließlich, ohne Codeänderung)
1. Ein neuer normaler Chat liest `vectorcraft-chat/AGENTS.md`, diese Datei und `vectorcraft-chat/TODO.md` sowie gezielt relevanten Code.
2. Er gibt eine knappe Übernahmeprüfung zurück: aktueller Quellstand, bereits belegte Funktionen, offene Beweise, genau EIN sinnvoller nächster Minimalkomponententest.
3. Keine Builds, keine kostenpflichtigen API-Aufrufe, keine Releases und keine App-Versionen bei dieser Übernahmeprüfung.
4. Erst nach gemeinsamer Auswertung einen kleinen Funktionsversuch planen. Die Referenz-ZIP muss, solange sie nicht im Repo liegt, bei Bedarf separat bereitgestellt werden.

## Disziplin für die nächsten Sitzungen
- Vor jeder Änderung TODO lesen; nur eine konkrete Funktion je Abschnitt.
- Keine parallelen Entwicklungsaufträge an demselben Quellstand.
- Keine ungetesteten Versionen ausgeben; ohne positiven Nachweis Status `nicht verifiziert`.
- Den letzten bestätigten Stand nicht überschreiben; bei Fehlschlag sauber zurückkehren.
- `PROJECT_STATE.md` nur bei einer relevanten neuen Erkenntnis oder am Ende eines abgeschlossenen Entwicklungsschritts aktualisieren.
- Kein automatischer Workflow-/Build-Retry. Kostenpflichtige KI-Calls nur mit ausdrücklichem Anlass und konservativer Kostenprüfung.

## Entwicklungsschritt 24.10.2026 — minimale Direktsteuerung
- Verbindliche Standards, AGENTS und TODO vor Änderungen gelesen. Der Altprojekt-Reparaturpfad bleibt gestoppt.
- Originalarchiv `VectorCraft-Mandala-Zentriert-v2(3).zip` aus der Übergabe lokal auf SHA-256 `09ab09949b987a71d7735dd456bca5795eddb60d98bf9cedf1661232ee23f6ae` geprüft: vier historische Dateien, Original nicht verändert. Das ZIP selbst liegt weiterhin nicht nachweislich in GitHub.
- Neuer isolierter Quellordner `vectorcraft-minimal-control/`: `vectorcraft_control.py` (Standard nur lesender TCP/JSON-Verbindungstest, `--execute` legt ausdrücklich neues Dokument an, zeichnet Dreieck, ermittelt ID, dreht dieselbe ID 30 Grad, prüft `document.node`) und `test_vectorcraft_control.py` (kostenlose Protokoll-Fixture). Keine OpenRouter-Integration, keine GUI und keine Release-Freigabe.
- Der zuvor lokal vorhandene ZIP-Vorläufer des Minimalcodes bestand drei Fixture-Tests am 24.10.; die neu in GitHub geschriebene Fassung ist noch **nicht als eigenständiger Testlauf geprüft**. Keine aktuelle Ausführung mit echter VectorCraft-Engine. Ein Mock-/Fixture-Erfolg ist kein nativer Funktionsnachweis.
- Quellcommits: `41a86b8`, `c15046f`. Kein Build, keine kostenpflichtige Anfrage.
- **Nächster einzelner Schritt:** neuen GitHub-Quellstand durch isolierten kostenlosen Test prüfen; anschließend nur den echten TCP/JSON-Dreiecktest mit nativer Engine in einer geeigneten Ausführungsumgebung durchführen. Ohne echten Nachweis keine KI-Anbindung freigeben.

## VC-RESET-02 – isolierte Direktsteuerungsprüfung (24.10.2026)
- Nutzerfreigabe `also los` als einzelner Auftrag in `vectorcraft-chat/CURRENT_TASK.md` auf Arbeitsbranch `vc-reset-control-02` dokumentiert. Produktiver `main` und historische App unverändert.
- Quellstand `vectorcraft-minimal-control/vectorcraft_control.py` und `test_vectorcraft_control.py` geprüft; `crates/engine/src/cmd/create.rs` bestätigt `path.create` mit SVG-`d` und `{id}` als Rückgabe. Frühere native Chat-Testquelle zeigt `document.node` und `object.rotate`.
- Lokaler, kostenloser Unit-/TCP-Fixture-Test des aus den GitHub-Dateien übertragenen Kernablaufs: **3 Tests bestanden** (ungültige IDs, fehlender Nullwinkel, TCP-Dreieck/30°/gleiche ID gegen lokalen Simulator). Ausgeführt mit `python -m unittest -v`, 0,504 s. Die lokale Übertragung war nicht als Bytevergleich zum GitHub-Python-Quelltext verifiziert; dieses Ergebnis ist ein Test des Kernablaufs, kein unabhängiger formaler Nachweis der exakten GitHub-Dateien.
- Echter Engine-Test **nicht ausgeführt**: diese Ausführungsumgebung hat keine `vectorcraft`-/`vectorcraft-cli`-Binary und kein `cargo`. Port 7979 des Nutzerrechners ist von hier aus nicht zugänglich. Keine GitHub Actions gestartet, kein OpenRouter, keine kostenpflichtigen Anfragen.
- **Ergebnis:** Fixture bestanden, native Ausführung blockiert, **keine Release-Freigabe**. Als nächster Test steht ausschließlich der native Dreieck/Objekt-ID/30°-Durchlauf in einer Umgebung mit echter Engine aus; bis dahin kein KI-Adapter.
