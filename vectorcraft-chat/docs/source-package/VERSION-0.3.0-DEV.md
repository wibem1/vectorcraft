# VectorCraft Chat 0.3.0-dev — interner Reparaturstand

**Nicht als funktionsfähige Version freigegeben.** Stand 21.10.2026.

## Implementiert
- Deterministischer Dreieck-Plan: Drei Eckpunkte für ein gleichseitiges Dreieck, als geschlossener Vektorpfad statt aus falschen Kommandos ausgewählten Bearbeitungsoperationen.
- Ausführung des Plans über dokumentiertes VectorCraft MCP-Tool `draw_path` via `vectorcraft-cli mcp --connect 127.0.0.1:7979`.
- Bestätigung vor Ausführung, kein OpenRouter-Aufruf für diesen elementaren Vorgang.
- Vorhandene Chat-App, API-Key, Modellauswahl, Diagnose und übrige Funktionalität unverändert weitgehend übernommen.

## Tests
`python -m unittest -q test_app.py`: 14 Tests bestanden, darunter gleichseitige Dreiecksgeometrie und ein kompletter MCP-stdio-Handshake plus `tools/call(draw_path)` an simuliertem MCP-Server.
`python -m py_compile vectorcraft_chat.py`: bestanden.

## Nicht getestet / noch fehlerhaft
- Echter VectorCraft-Engine-End-to-End-Test (CLI und Rust-Engine sind in dieser Laufzeit nicht installiert).
- Folgeänderung (Rotation) derselben Objekt-ID noch nicht implementiert.
- Freie KI-gesteuerte Konstruktion weiterhin unzuverlässig; der allgemeine Chatpfad enthält noch die problematische Auswahl aus internen Kommandos.
- Kostenlimit nicht hart durchgesetzt; Modellabruf bislang nicht zuverlässig bestätigt.

Eine Endversion darf erst nach realen Headless-Tests und Folgeänderung veröffentlicht werden.
