# VectorCraft Chat

Eigenständiger, lokaler KI-Chat zur Diskussion, Erstellung und Bearbeitung von Vektorkonstruktionen in VectorCraft. **Stand: 21. Oktober 2026; Version 0.2.0 (technischer Prototyp).**

## Ziel

Ein fortlaufender Dialog, in dem Ideen zunächst diskutiert und dann auf ausdrücklichen Wunsch als native VectorCraft-Aktionen ausgeführt werden. Nach der Ausführung soll die KI den Dokumentzustand erneut erfassen und bestehende Objekte gezielt weiterbearbeiten. Die App soll unabhängig von ChatGPT Work unter Windows und macOS laufen.

## Aktueller Stand

- Python-/Tkinter-Chatoberfläche, Standardfenster 540 × 490 px, Mindestfenster 420 × 360 px.
- OpenRouter Chat-Completions API mit dynamischer OpenRouter-Modellauswahl; API-Key über Betriebssystemschutz speicherbar (Windows DPAPI, macOS Schlüsselbund); Linux-Dateifallback.
- Direkter lokaler VectorCraft-Kontrollkanal (JSON-Zeilenprotokoll) unter 127.0.0.1:7979.
- Dokumentstatus und Befehlskatalog abfragen; begrenzte strukturierte Aktionen prüfen, explizite Freigabe erforderlich.
- Lokaler Chatverlauf als JSON in ~/.vectorcraft-chat/history.json.
- Startskripte für Windows und macOS. Kein Installer, kein nativer Build.

## Start

1. VectorCraft mit `--control 7979` starten. Der lokale Port hat **keine Authentifizierung**; nur während der Arbeit aktivieren.
2. Windows: `START-Windows.cmd`, Mac: `START-Mac.command`; Python 3 mit Tkinter wird benötigt.
3. OpenRouter-Key und gültige Modell-ID eingeben, Verbindung prüfen, Konstruktion diskutieren.
4. Nur gewünschte Aktionen freigeben; vorher eigene Dokumentkopie sichern.

## Diagnose und Modellwahl

„Key speichern“ legt den Schlüssel lokal ab (Windows DPAPI, macOS Schlüsselbund). „Modelle laden“ lädt die aktuellen OpenRouter-Modell-IDs. „Diagnose speichern“ schreibt eine JSON-Datei ohne Key, Chattexte und Dokumentinhalte. Bei einer OpenRouter-401-Antwort bitte Key prüfen und erneut speichern.

## Bekannte Einschränkungen

**Nicht produktionsreif.** Weder ein echter OpenRouter-End-to-End-Test noch die Ausführung an einer laufenden VectorCraft-Desktopinstanz wurde hier nachgewiesen. Das angezeigte 0,10-€-Budget ist **keine durchgesetzte Kostengrenze**. Visuelle Rückmeldung, robustes Change-Tracking, zuverlässiges Erhalten manueller Änderungen, Versionsvergleich und Installer fehlen.

Dokumentation: [Architektur](docs/ARCHITEKTUR.md), [Entwicklungsstand](docs/ENTWICKLUNGSSTAND.md), [Roadmap](docs/ROADMAP.md), [Tests](docs/TESTS.md), [Änderungen](CHANGELOG.md).


## 0.2.0 wichtige Einschränkung
Kein vollständiger Live-Test mit VectorCraft/OpenRouter hier möglich. Das eingestellte Budget stoppt Folgeanfragen nach Erreichen des erfassten Verbrauchs (USD konservativ als EUR behandelt), limitiert aber nicht eine bereits laufende Anfrage.
