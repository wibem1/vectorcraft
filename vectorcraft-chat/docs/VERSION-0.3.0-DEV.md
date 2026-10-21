# VectorCraft Chat 0.3.0-dev — technischer Zwischenstand 21.10.2026

**NICHT FREIGEGEBEN:** Es fehlt weiterhin der vollständige Test mit der echten VectorCraft-Engine. Die folgenden Änderungen liegen als separates Quellcode-ZIP in der Chat-Sitzung, **noch nicht im GitHub-Quellcode**.

## Befund zu 0.2.0
Die KI erhielt 22 ungeeignete Commands, antwortete ohne Aktionsblock. Der Schlüsselwort-Selector bevorzugte u. a. addAnchorPoints. Keine Zeichenoperation ausgeführt.

## Korrekturansatz
Die VectorCraft-MCP-Dokumentation beschreibt ein echtes Zeichenwerkzeug `draw_path` mit `points`, `closed`, `fill`, `stroke`, `strokeWidth`. Der neue experimentelle Build umgeht deshalb für den einfachen Auftrag „Konstruiere ein Dreieck“ sowohl die umfangreiche Command-Auswahl als auch kostenpflichtiges Sprachmodell-Reasoning: Er berechnet drei gleichseitige Eckpunkte und schlägt einen expliziten MCP-draw_path-Aufruf vor.

MCP-Verbindung: `vectorcraft-cli mcp --connect 127.0.0.1:7979`, stdio JSON-RPC 2.0, `initialize`, `notifications/initialized`, `tools/call`. Windows-CLI aus installiertem VectorCraft (Standardpfad), alternativ Umgebungsvariable `VECTORCRAFT_CLI`. Das UI fordert weiterhin Bestätigung vor der Zeichenaktion.

## Automatisierte Tests
- 14 Tests erfolgreich, einschließlich Dreieck-Geometrie und MCP-Protokoll-Handshake + draw_path an simuliertem MCP-Server.
- Syntaxprüfung des Python-Skripts erfolgreich.
- ZIP-Integritätsprüfung erfolgreich.

## Offene Bedingungen vor Veröffentlichung
1. **Echte Rust-Engine fehlt in der Testumgebung:** noch kein Headless- und Live-Ende-zu-Ende-Test mit VectorCraft.
2. Folgeauftrag „Drehe das Dreieck um 30 Grad“ noch nicht als verlässliche Operation auf derselben Objekt-ID umgesetzt.
3. Freie KI-Anfragen verbleiben vorerst im bisherigen fehleranfälligen Pfad.
4. Kostenkontrolle von 0,10 Euro ist noch keine durchgesetzte harte Grenze.
5. Quellcode von 0.3.0-dev muss noch im Repository hinterlegt werden.

**Status: technisch überprüfter Entwicklungsstand, keine fertige nutzbare Version.** Frühere Falschangaben über „funktioniert“ werden vermieden.
