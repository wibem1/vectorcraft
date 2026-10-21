# VectorCraft Chat Changelog

## 0.2.0 (2026-10-21)
- Katalog auf auftragsbezogene Auswahl reduziert.
- Fehler- und Ausführungsdiagnose verbessert.
- Nicht existierende KI-Befehle werden vor Freigabe abgelehnt.
- Ausführungsresultat gegen Dokumentinspektion geprüft.
- API-Verbrauch über die Sitzung aufsummiert; weiteres Senden ab erreichtem Budget gesperrt. **Keine garantierte Provider-Hardcap pro Anfrage.**
- Kein kompletter VectorCraft-End-to-End-Test in diesem Ausführungsumfeld.

## 0.3.1-dev (21.10.2026)
- Vorläufiger Folgeauftrag „Drehe das Dreieck um 30 Grad“ mit gezielter Objektauswahl (`select.set`) und nativer Rotation (`object.rotate`).
- Objekt-ID nach `draw_path` aus der `inspect_document`-Selektion lesen; Abbruch bei fehlender oder nicht eindeutiger Zuordnung.
- Regressionstests für Eingabeerkennung, ID-Prüfung und fehlende Inspektionsdaten.
- Kein echter Engine-/Windows-Praxistest; keine Freigabe.
