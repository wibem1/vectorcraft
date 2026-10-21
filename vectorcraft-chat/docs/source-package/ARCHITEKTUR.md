# Architektur

`vectorcraft_chat.py` ist derzeit die vollständige App mit Tkinter-Oberfläche, JSON-Statusspeicherung, OpenRouter-Anfrage, Prüfung und Freigabe der KI-Aktionen und TCP-Client.

## Datenfluss

Benutzer ↔ Chatfenster → OpenRouter-API → Antwort plus optionaler `<vc_actions>`-Block → Parser und Zulässigkeitsprüfung → ausdrückliche Freigabe → TCP auf 127.0.0.1:7979 → VectorCraft-Steuerprotokoll → Dokument.

Die KI erhält einen gekürzten `document.inspect`-Status und einen Ausschnitt des `engine.commands`-Katalogs. Die App akzeptiert nur `engine.execute`, `document.inspect`, `ui.render` und `ui.inspect`; höchstens zwölf Aktionen pro Antwort. Schreib- und Löschaktionen sollen vermieden werden, aber dies ersetzt keine vollständige Sandbox.

VectorCraft-Dokumentation: `docs/control-protocol.md` und `docs/mcp.md` im Basisprojekt `wibem1/vectorcraft`. Alternativ zum MCP-Server verwendet dieser Prototyp den direkten JSON-Kontrollkanal.

## Geplante Trennung

Chat/Provider-Modul, Context/Document-Modul, sichere Action-Engine, History/Versionen und plattformspezifische GUI. Nicht als fertig implementiert betrachten.
