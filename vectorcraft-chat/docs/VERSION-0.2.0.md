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

## Nachtrag: Praxistest vom 21.10.2026, 16:24 — FEHLGESCHLAGEN

Die Nutzerdiagnose `VectorCraft-Chat-Diagnose-20261021-162358.json` belegt: `document.inspect` erfolgreich; Catalog 1.028 Commands, 22 ausgewählt, darunter `object.path.addAnchorPoints`, `select.object.openPaths`, `object.blend.spine.addAnchor` und `object.mesh.movePoint`. API-Aufruf erfolgreich: 3.217 Tokens und 0,00597375 USD. KI-Antwort mit 489 Zeichen, aber `action_parser: no action tag`; danach `no_actions` und `actions=0`. Kein VectorCraft-Zeichenbefehl ausgeführt. 0 dynamisch geladene Modelle.

**Nachgewiesene Schwächen im Code:** Der Command-Selector basiert auf Teilwortwertung und priorisiert bei „Dreieck“ gerade Bearbeitungsbefehle für Anker/Pfade statt zwingend notwendige Pfaderstellung; der Handlungsparser akzeptiert ausschließlich einen speziellen XML-artigen Aktionsblock, ohne eine robuste alternative Tool-Calling-Schnittstelle. Das Ende-zu-Ende-Ziel wurde erneut verfehlt. **v0.2.0 NICHT als funktionsfähig bezeichnen.**

**Nächste Entwicklungsbedingung:** zuerst den realen VectorCraft-Befehlskatalog nach Pfaderstellungsbefehlen und Parametern analysieren, gezielte kontraktbasierte Auswahl, echte Engine-Tests einschließlich Dreieck und Folgeänderung, erst danach neue öffentliche Testversion. Keine erneute Nutzer-Testversion allein auf Grundlage von Unit-Tests.
