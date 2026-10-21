# VectorCraft Chat 0.3.1-dev — Fortschritt, 21. Oktober 2026

**Status: nicht freigegebener Entwicklungsstand.** Der v0.3.1-dev-Quellcode liegt als ZIP-Artefakt in der zugehörigen Chat-Sitzung; dieses Dokument ist die GitHub-Statusnotiz, kein Beleg eines nach GitHub übertragenen Quellcodes.

## Implementierte Änderungen
- Direkter MCP-Pfad `draw_path` für ein gleichseitiges Dreieck (aus v0.3.0-dev).
- Neue Folgeoperation: „Drehe das Dreieck um 30 Grad“ (auch andere ausdrücklich angegebene Gradwerte); die App speichert die nach dem Zeichnen gemeldete Objekt-ID.
- MCP-Abfolge: `inspect_document` → `run_command select.set {ids:[id]}` → erneutes `inspect_document` für die Auswahlprüfung → `run_command object.rotate {angle}`.
- Fehlschlag ohne bestätigte Objekt-ID und Abbruch bei abweichender Selektion; kein stillschweigendes Drehen eines fremden Objekts.
- Die Umsetzung verwendet die dokumentierten MCP-Tools; ihr Rückgabeformat wird konservativ ausgewertet.

## Tests
- `python -m unittest -q test_app`: **17 bestanden** (14 bisherige + 3 Regressionstests).
- `python -m py_compile vectorcraft_chat.py`: bestanden.
- ZIP-Integrität: bestanden.
- Simulation des MCP-Transportes mit Testserver aus den bisherigen Tests vorhanden.
- **Nicht bestanden, weil nicht ausgeführt:** Test mit echter Rust-Engine in Headless-Modus, Live-VectorCraft auf Windows, vollständiger Ablauf Zeichnen → Objektidentität → Drehen → Ergebnisprüfung.

## Einschränkungen
- Ob `inspect_document` unmittelbar nach `draw_path` das neue Objekt eindeutig selektiert, muss die echte Engine bestätigen. Solange das nicht nachgewiesen ist, bleibt die folgende Drehung experimentell.
- Die übrigen freien KI-Konstruktionsaufträge benutzen teilweise weiterhin den bisherigen störanfälligen Befehlsplaner.
- Der Cost Cap von 0,10 € ist weiterhin keine zuverlässige harte Budgetgrenze.
- Keine installierbare EXE und kein Mac-Build. Kein neues Nutzer-Testrelease empfohlen.

## Nächster Schritt
Authentische VectorCraft-CLI und Rust-Engine in einer Build-Umgebung installieren/kompilieren. Als Abnahmebedingung einen Test, der `draw_path` ausführt, das neue Objekt über `inspect_document` identifiziert, es via `select.set` + `object.rotate` verändert und Ergebnis sowie Objektidentität bestätigt. Danach den gesamten v0.3.1-Quellcode mit Build-Workflow in GitHub einchecken.
