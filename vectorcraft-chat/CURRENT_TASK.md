# Aktuell freigegebener Auftrag – VC-RESET-02
Stand: 24.10.2026 · FREIGEGEBEN DURCH NUTZER ("also los")

## Ausgangspunkt
VC-RESET-01 ist abgeschlossen: unverändertes Archiv `vectorcraft-reset/VectorCraft-Mandala-Zentriert-v2.zip` auf Branch `vc-reset-reference-01`, Git-Blob `921b8112f78a72a9a00af40e7e9ee601fa24f871`; dokumentierte SHA-256 `09ab09949b987a71d7735dd456bca5795eddb60d98bf9cedf1661232ee23f6ae`. Der historische Mandala-Code bleibt unverändert.

## Genau ein Auftrag
Die minimale, direkte Python-TCP/JSON-Steuerung kostenlos prüfen und soweit notwendig isoliert korrigieren: neues VectorCraft-Dokument, Dreieck, Objekt-ID, 30° Drehung **derselben** ID, überprüfter Endzustand an echter Engine. Zunächst schnelle kostenlose Unit-/Fixture-Prüfungen, dann nur bei verfügbarer nativer Engine genau ein echter Integrationstest. Ergebnisse ehrlich trennen.

## Grenzen
- Branch `vc-reset-control-02`; `main` unverändert.
- Nur `vectorcraft-minimal-control/`, Auftrags- und Projektdokumentation ändern. Keine Reparatur von `vectorcraft-chat/`, kein KI-Adapter, kein Frontend, kein Packaging, kein Release.
- Keine OpenRouter-/bezahlten Anfragen, keine unbegrenzten Workflow-Retries. GitHub Actions nur gezielt für echten Test, sofern geeigneter Workflow verfügbar.
- Bei fehlender echter Engine ausdrücklichen Blocker festhalten und nach den tatsächlich möglichen Prüfungen stoppen.
- Nie einen Fixture-Test als nativen Nachweis bezeichnen.

## Abschluss
Testergebnisse, Quellcommit, offene Blocker im Branch dokumentieren; dann stoppen. Nächster Schritt braucht neue Freigabe.
