# VectorCraft Chat — eigenständige KI-Chatsteuerung

**Entwicklungsstand: 21.10.2026 — v0.1.3, experimentell, nicht funktionsfähig nach Nutzer-Praxistest.**

Ziel: eine kleine **eigenständige Chat-App** für Windows und Mac, mit der man eine Konstruktion in VectorCraft mit einer KI besprechen, ausführen, beurteilen und weiterbearbeiten kann. Nicht bloß ein einmaliger Prompt-zu-Zeichnung-Generator. Die KI muss den aktuellen Dokumentzustand kennen und bereits vorhandene Objekte gezielt verändern können.

## Aktueller Stand (bestätigt und nicht bestätigt)
- Lokale VectorCraft-Verbindung über `127.0.0.1:7979` im Nutzertest erfolgreich; Dokumenttitel „Vorlagenrekonstruktion“.
- OpenRouter-Anfrage erfolgt mit gespeichertem API-Key; letzte Diagnose hat Kosten, aber keine ausführbare Aktion vermerkt.
- Der Chat und das UI existieren als Python-Prototyp v0.1.3; die GUI hatte zuvor unbenutzbare Größen-/Layoutprobleme.
- API-Key-Speicherung, Modellliste und Diagnoseexport wurden implementiert, **nicht vollständig im Betrieb bestätigt**.
- Kein erfolgreicher Ende-zu-Ende-Test von „Konstruiere ein Dreieck“ bis zur sichtbaren Zeichnung nachgewiesen.
- Das Kostenlimit 0,10 € ist **nicht** technisch durchgesetzt.
- Der Quellcode von v0.1.3 liegt als separates ZIP aus dem Chat vor; diese Dokumentationsübernahme bedeutet nicht, dass der Quellcode bereits in diesem Verzeichnis eingecheckt wurde.

## Geplanter technischer Aufbau
Chat/UI → Dialog- und Aktionsplanung → ausgewählte validierte native VectorCraft-Kommandos → lokale Steuerungsschnittstelle.
Das Chatmodell soll das Dokument zunächst in kompakter Form inspizieren; bei Bedarf einzelne Objekte oder Commands nachladen. Nicht die vollständige Liste aller 1.026 verfügbaren Commands regelmäßig in den Prompt aufnehmen.

**Kein automatisch unkontrolliertes Ausführen:** Änderungen validieren, den aktuellen Dokumentzustand prüfen, gezielt ausführen und Rückmeldung/Fehler protokollieren. Dialog darf auch ohne Aktion stattfinden.

## Fehlerprioritäten
1. Funktionierenden Dreieck-Ende-zu-Ende-Test erstellen.
2. KI-Antwort von ausführbarer, schemavalidierter Aktionsstruktur trennen; ungültige JSON-Antworten sicher behandeln.
3. Vollständige Diagnosen für Anfrage-, Antwort-, Parser-, Validierungs- und Ausführungsschritte (ohne Schlüssel, sensible Promptinhalte standardmäßig ausschließen).
4. Dynamische Modellliste samt Auswahl zuverlässig laden.
5. Kostenlimit verbindlich prüfen; keine bloße Budgetanzeige.
6. Bearbeitung bestehender Objekte und Abgleich bei manuellen Änderungen.

## Upstream VectorCraft
Repository-Hauptteil enthält die VectorCraft-Anwendung. Lokaler Steuerungskanal `vectorcraft --control 7979`, JSON-Zeilenanfragen, siehe [docs/control-protocol.md](../docs/control-protocol.md); MCP-Dokumentation [docs/mcp.md](../docs/mcp.md). Diese Chat-App ist ein **separates Projekt im Unterverzeichnis**; Änderungen sollen VectorCraft selbst nicht beschädigen.

## Teststatus
Die für v0.1.3 gemeldeten 8 automatisierten Tests sind **kein** erfolgreicher End-to-End-Nachweis. Nutzer-Praxistest: App funktioniert nicht. Details in [Diagnose](docs/DIAGNOSE-2026-10-21.md).

## Referenz
GitHub ist ab diesem Commit die Dokumentationsbasis. Der v0.1.3-Quellcode muss noch vollständig ergänzt und gegen das im Chat vorhandene ZIP abgeglichen werden.
