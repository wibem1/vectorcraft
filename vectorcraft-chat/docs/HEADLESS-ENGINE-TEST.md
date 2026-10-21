# Echte VectorCraft-Engine — automatisierter Headless-Test

Stand 2026-10-21. **Test eingerichtet, noch kein erfolgreicher GitHub-Actions-Lauf nachgewiesen.**

## Implementierung
- GitHub Actions: [vectorcraft-chat-headless.yml](../../.github/workflows/vectorcraft-chat-headless.yml)
- Prüfskript: [smoke_headless.py](../tests/smoke_headless.py)
- GitHub Actions kompiliert `vectorcraft-cli` aus diesem Repository mit Rust 1.95.0 und führt `vectorcraft-cli mcp --headless` aus.
- JSON-RPC-Verbindung mit `initialize`, `notifications/initialized`, danach `tools/call`.
- Anhand des echten Dokumentbaums vor/nach `draw_path` wird die neu hinzugekommene Objekt-ID ermittelt.
- Mit `run_command select.set` wird nur dieses Objekt selektiert; `inspect_document` kontrolliert die Auswahl.
- `run_command object.rotate {angle:30}` dreht das ausgewählte Objekt; erneute Dokumentinspektion verlangt das Fortbestehen derselben ID.
- Alle Schritte ohne API-Key und ohne Modellkosten.

## Grenzen
- Noch keine automatische geometrische Winkelmessung oder Pixelprüfung der Drehung; nur erfolgreicher Befehl und fortbestehende Objektidentität.
- Die echte Engine könnte bei Einzelheiten des Antwortformats von den Annahmen des Smoke-Tests abweichen; solche Fehler sollen in Actions sichtbar werden und **nicht** als App-Erfolg gelten.
- Das Skript ist unabhängig von der experimentellen Python-Chatoberfläche. Ein erfolgreicher Headless-Test allein gibt die App noch nicht frei.
- Workflow-Ausführung und Erfolg müssen anhand des tatsächlichen GitHub-Actions-Laufs überprüft werden.

## Aufruf
GitHub: *Actions* → *VectorCraft Chat real headless engine* → *Run workflow*, alternativ Änderung der Workflow-/Testdatei auf main. Lokal auf Linux mit kompiliertem Binary:

```bash
cargo build --locked --release -p vectorcraft-cli
python3 vectorcraft-chat/tests/smoke_headless.py target/release/vectorcraft-cli
```

**Freigabekriterium:** erfolgreicher echter Engine-Test, anschließend Fehlerfälle/Rendering-Prüfung und Integration in den Chat.
