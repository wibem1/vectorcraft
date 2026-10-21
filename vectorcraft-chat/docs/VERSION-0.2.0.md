# VectorCraft Chat 0.2.0 — Entwicklungsstand 21.10.2026

## Status: experimentelle Reparaturversion (kein erfolgreicher Windows-Praxistest)

Die neue Version 0.2.0 wurde auf Basis des realen 0.1.3-Quellcodes erstellt. Das ZIP `VectorCraft-Chat-0.2.0-Quellcode.zip` wurde in der Chat-Sitzung bereitgestellt; **der vollständige Quellcode ist noch nicht in GitHub eingecheckt**. Diese Notiz enthält nur die nachgeprüften Änderungen und offenen Einschränkungen.

### Reparaturen
- Statt 1.026 Befehle an die KI zu geben, werden maximal 22 nach Auftrag ausgewählte VectorCraft-Commands inklusive Parameterbeschreibung im Kontext übermittelt.
- KI-Antworten mit ungültigem Aktions-JSON oder nicht existierenden Commands werden vor der Ausführung abgelehnt.
- Beim Ausführen werden lokale VectorCraft-Rückmeldungen erfasst und der Dokumentzustand vorher/nachher erneut geprüft.
- Diagnose protokolliert API-Antwortmetadaten, Befehlsauswahl, Parserstatus, Ausführung und Fehler; API-Schlüssel und vollständiger Chattext werden nicht in den Diagnoseexport übernommen.
- Sitzungskosten aus OpenRouter-`usage.cost` werden addiert. Neue API-Anfragen werden gestoppt, wenn die aufsummierten USD-Kosten das numerische €-Budget erreichen. **Dies ist KEINE zuverlässige harte Obergrenze pro Anfrage und KEINE korrekte Währungsumrechnung.** Ein Lauf kann das Budget überschreiten.
- Bei einem ausdrücklich geforderten Konstruktionsauftrag ohne vorgeschlagene Aktion wird sichtbar darauf hingewiesen, dass nichts gezeichnet wurde.
- Geprüft: `python -m unittest -q test_app`: **12 Tests bestanden**, `python -m py_compile vectorcraft_chat.py`: bestanden. ZIP-CRC geprüft.

### Noch offen / nicht behaupten
- Keine End-to-End-Ausführung mit echter OpenRouter-Verbindung und laufendem VectorCraft in diesem Umfeld durchgeführt.
- Erstellen eines echten Dreiecks und anschließende visuelle Prüfung **nicht bestanden beziehungsweise noch nicht getestet**.
- Native Installer oder EXE für Windows/macOS **nicht vorhanden**; Python + Tkinter nötig.
- Kostenlimit 0,10 € noch nicht verbindlich technisch durchgesetzt.
- Dynamische Modellliste und Betriebssystem-Key-Speicherung waren in v0.1.3 implementiert, müssen auf dem Windows-Gerät weiter getestet werden.
- Fortlaufende Kontexttreue und manuelle Änderungen erhalten: noch nicht nachgewiesen.

### Priorisierter nächster Test
1. Windows: VectorCraft mit `--control 7979` starten.
2. VectorCraft Chat 0.2.0 mit gültigem API-Key und Modell öffnen.
3. „Konstruiere ein Dreieck“ senden. Prüfen, ob eine ausführbare Aktion vorgeschlagen wurde und ob sie nach Bestätigung ein editierbares Objekt erzeugt.
4. „Drehe das Dreieck um 30 Grad“ senden und auf gezielte Veränderung desselben Objekts prüfen.
5. Bei Fehler: „Diagnose speichern“ und JSON bereitstellen. Die Diagnose nennt dann die Phase der Fehlerentstehung.

### Historischer Bezug
Siehe [Fehlerdiagnose v0.1.3](DIAGNOSE-2026-10-21.md).
