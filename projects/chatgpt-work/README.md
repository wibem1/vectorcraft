# VectorCraft mit direkter ChatGPT-Work-Steuerung

Dieser Projektbereich sichert die Arbeit vom 20.–21. Oktober 2026. Er ergänzt das bestehende Repository, ohne dessen Engine, Rust-Anwendung oder Build-Konfiguration zu ändern.

**Dauerhaft einrichten: [Work-Projektstart](docs/WORK_SETUP.md)** – einmalige Einrichtung, kurze künftige Eingabe und lesender Abnahmetest.

**Einstieg: [PROJECT_STATUS.md](../../PROJECT_STATUS.md)**

- [Direkte Steuerung: Aufbau und bestätigter Ablauf](docs/DIRECT_CONTROL.md)
- [Mandalas und Vorschaubilder](docs/ARTWORK_CATALOG.md)
- [Sicherungsumfang und Wiederherstellung](docs/BACKUP_SCOPE.md)
- [Tests und Grenzen](docs/VERIFICATION.md)
- [Herkunft, Lizenzen und lokale Ausschlüsse](docs/PROVENANCE.md)
- [Offene Aufgaben](docs/NEXT_STEPS.md)
- [Dateimanifest](FILE_MANIFEST.json)

## Ordner

| Bereich | Inhalt |
|---|---|
| `artwork/` | Geprüfte eigene Mandalas als native Zeichnung, SVG und PNG |
| `control-app/` | Unveränderter letzter Quellstand des separaten Steuerfensters 0.5 und Tests |
| `constructions/` | Ausgewählte unveränderte Konstruktions-/Rekonstruktionsskripte der Sitzung; Kontext prüfen |
| `diagnostics/` | Eingangsdiagnosen, Vorherzustände, Testberichte und Befehlsverzeichnis |
| `live-capture/` | Zusätzliche lesende Sicherung offener eigener Zeichnungen, mit Index |
| `archive/2026-10-21/` | Unveränderte historische Dateien und ZIP-Pakete; öffentlich erlaubter Teil des ersten Backups |
| `tools/` | Ausschließlich Sicherungs-/Prüfwerkzeuge dieser Organisation |
| `licenses/` | Projekt- und Paketlizenztexte |

Das separate Python-Steuerfenster ist kein eingebautes KI-Modul. Der bevorzugte Arbeitsweg der Sitzung war die direkte Umsetzung von Wortanweisungen aus dem Chat über lokale Werkzeuge. Es wird kein neuer Hintergrunddienst installiert.
