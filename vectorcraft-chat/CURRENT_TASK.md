# Aktuell freigegebener Auftrag – VC-RESET-01
Stand: 24.10.2026 · **FREIGEGEBEN, REFERENZARCHIV FEHLT IM REPOSITORY**

## Maßgebliche Entwicklungsentscheidung
Die fehlerhafte bisherige VectorCraft-Chat-App wird **nicht weiter repariert**. Kontrollierter Neustart auf Grundlage des am 14.10.2026 historisch erfolgreich verwendeten Python-Steuerprogramms. Der bisherige App-Code und seine Geschichte bleiben unverändert als Referenz erhalten.

## Genau EIN jetzt freigegebener Auftrag
Das **unveränderte Original** `VectorCraft-Mandala-Zentriert-v2.zip` auffinden, seine SHA-256-Prüfsumme bestätigen und es als unveränderliche Referenz in der neuen, getrennten Entwicklungsarbeit sichern.

Erwartete Prüfsumme: `09ab09949b987a71d7735dd456bca5795eddb60d98bf9cedf1661232ee23f6ae`.
Erwarteter Inhalt: `vectorcraft_mandala_zentriert.py`, `01_Pruefen.bat`, `02_Mandala_zentriert_erstellen.bat`, `ANLEITUNG.txt`.

**Blocker:** Das Originalarchiv ist bislang im Repository nicht nachgewiesen. Wenn es nicht zugänglich ist, ausdrücklich um die Originaldatei bitten. Weder Code noch ZIP-Inhalt aus Erinnerungen nachbauen.

## Ausführung
- Isolierter Arbeitsbranch: `vc-reset-reference-01` (erstellt aus `main`).
- Erlaubt: Quell-/Projektdateien lesen, das bereitgestellte Originalarchiv unverändert prüfen und als Referenz sichern; Prüfergebnis dokumentieren.
- Verboten: Reparatur der alten App; neues Frontend oder KI-Adapter; GitHub Actions, native Builds, OpenRouter/andere kostenpflichtige APIs, Releases und automatisch folgende Aufgaben.
- Keine Änderung des produktiven Quellcodes. `main` nicht für Experimente verwenden.
- Erfolg: Originalarchiv bytegenau mit erwarteter Prüfsumme gesichert; vier Quelldateien nachgewiesen; Code bleibt unverändert; Ergebnis in GitHub dokumentiert.
- Abschluss: Nach der Prüfung stoppen und berichten. Die nächste Aufgabe bedarf einer gesonderten Freigabe.

## Danach vorgesehen – **noch NICHT freigegeben**
Kleiner deterministischer Test mit echter VectorCraft-Engine über TCP 7979: Dreieck erzeugen, Objekt-ID prüfen, dasselbe Dreieck um 30° drehen. Erst danach KI-Anbindung.

## Quellen
- `vectorcraft-chat/PROJECT_STATE.md` – Ziel, Befunde, Entwicklungskontext.
- `vectorcraft-chat/docs/REFERENCE-2026-10-14.md` – historischer Nachweis und Abgrenzungen.
- `vectorcraft-chat/TODO.md` – umfangreiches **historisches** Reparatur-/Testprotokoll, **nicht** die aktive Auftragsliste.
- Globale Regeln: https://github.com/wibem1/AI-Development-Standards/blob/main/DEVELOPMENT_STANDARDS.md

GitHub Issues sind in diesem Repository deaktiviert (API 410); daher dient **diese Datei** als aktuelle verbindliche Aufgabenquelle. Änderungen an Dateien allein erzwingen keine technische Berechtigungssperre.
