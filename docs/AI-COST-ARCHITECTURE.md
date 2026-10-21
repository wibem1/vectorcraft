# VectorCraft – Kosten- und Interaktionsarchitektur (Beginn 21.10.2026)

Status: **technische Bestandsaufnahme und Messwerkzeuge; noch keine KI-Chat-Reparatur oder Produktfreigabe**.

## Abgrenzung

Das Repository `wibem1/vectorcraft` enthält die Rust-Zeichenanwendung und ihre lokale MCP-/Control-Schnittstelle. Die am 21.10.2026 getestete **VectorCraft-Chat v0.1.3** meldet hingegen `platform=win32`, `python=3.15.0`, OpenRouter-Modell `google/gemini-3.8-flash`, 468 geladene Modelle und ein Kostenlimit von 0,10 €. **Deren Python-Client, Prompt-Builder, OpenRouter-Request-Erzeugung und Kostenprüfung wurden im untersuchten GitHub-Tree nicht gefunden.** Änderungen am Rust-Server allein können dessen Tokenverbrauch daher nicht nachweislich beheben. Vor einer Optimierung muss der tatsächlich ausgeführte Client-Code eindeutig ins Repository aufgenommen bzw. zugeordnet werden.

## Verifizierte Anknüpfungspunkte im Rust-Code

- `crates/mcp/src/server.rs`: kompakte MCP-Server-Anweisungen; verweist auf `draw_shape`, `draw_path`, `render_preview`, `doc_inspect`, `command_list`, `command_run` und `command_batch`.
- `crates/mcp/src/tools.rs`: MCP-Werkzeugdefinitionen und JSON-Schemas. Der Server stellt bereits Werkzeuge bereit, mit denen der Client **nicht** jeden Engine-Befehl einzeln als KI-Tool veröffentlichen muss.
- `crates/mcp/src/resources.rs`: `vectorcraft://document` (Zusammenfassung), `vectorcraft://document/json` (gesamtes Modell), `vectorcraft://object/{id}` (gezieltes Objekt), `vectorcraft://command/{id}` (einzelner Befehl). Der Code warnt ausdrücklich davor, das ganze Dokument wiederholt zu senden.
- `docs/mcp.md`: Live-Steuerung über `vectorcraft --control 7979`, `vectorcraft-cli mcp --connect 127.0.0.1:7979`; lokale Engine unterstützt Änderungen und Inspektion.

Die Diagnosenennung `connection_command_count=1026` belegt die Größe eines **verfügbaren Befehlsbestands**, nicht 1.026 Aufrufe für ein Dreieck. Ob der Python-Client den gesamten Katalog bei jedem KI-Aufruf an OpenRouter schickt, ist **offen**.

## Reale Nutzungsbeobachtung (Diagnose vom 21.10.2026, 13:01)

| Messung | Anfrage 1 | Anfrage 2 | Summe |
| --- | ---: | ---: | ---: |
| Eingabetokens | 9.643 | 7.623 | 17.266 |
| Ausgabetokens | 1.235 | 1.396 | 2.631 |
| Gesamttokens | 10.878 | 9.019 | 19.897 |
| Anbieter-Kosten USD | 0,01186350 | 0,01095225 | 0,02281575 |

Diese USD-Abrechnung ist **kein Eurobetrag**. Für ein hartes Eurobudget muss eine nachvollziehbare Wechselkursgrundlage angegeben werden. Die Diagnose enthält keine Prompt-Texte und keinen Nachweis, welche Antwort eine konkrete geometrische Aktion ausführte.

## Verbindliche Zielarchitektur

1. **Die lokale Zeichnung ist die Wahrheit**: Objekt-IDs, Hierarchie, Auswahl, Gruppierung und Änderungen bleiben in der Rust-Engine. Chatverlauf ist niemals die alleinige Quelle.
2. **Zustand auf Anfrage**: vor einer Bearbeitung kurze `document.inspect`-Zusammenfassung mit Dokumentgeneration; gezielt einzelne Objekte abrufen. Vollständiges `document.json` nur bei begründetem Bedarf und nach Tokenprüfung.
3. **Visuelles Verständnis**: `render_preview` gezielt bei ästhetischer Beurteilung oder Unsicherheit; niemals pauschal bei jeder Aktion. Eine Vorschau muss die nach der letzten Änderung aktuelle Dokumentgeneration repräsentieren.
4. **Kleine Werkzeugoberfläche**: bei normalen Konstruktionsaufträgen ausschließlich die relevanten MCP-Werkzeuge und knappe Parameterbeispiele. `command_list`/Einzelkommando nur bei Bedarf; nie ohne Beleg 1.026 Schemata in den Prompt kopieren.
5. **Budgetwächter im Chat-Client**: vor *jedem* OpenRouter-Aufruf Eingabetokens/Maximalausgabe und USD-Preis (pro Modell dynamisch) konservativ schätzen; laufende Reservierung für noch nicht abgerechnete Requests; nach Antwort anhand der Anbieterabrechnung buchen; bei fehlenden Preisen/Wechselkurs nicht mit einer vorgetäuschten Garantie fortfahren.
6. **Erfolgsprüfung**: Rückgabe aus dem lokalen Befehl abwarten, Dokumentgeneration/Objekte prüfen, Fehler diagnostisch erfassen. Keine stillen Wiederholungsaufrufe.
7. **Transparenz**: pro Aufruf Prompt-Tokens nach Kategorie (System, Tools, Chat, Dokument, Bild), Output-Tokens, Kosten, Outcome, aktuelle Generation; keine API-Keys oder sensiblen Inhalte in Diagnoseexporten.

## Abnahmekriterien vor einer neuen Version

- Dreieck: 3 verschiedene Punkte, geschlossener Vektorpfad; nach Bearbeitung im Dokument nachweisbar.
- Manueller Eingriff: Selektion/Objektwerte ändern sich in VectorCraft, der nächste KI-Auftrag arbeitet mit dem neuen Stand.
- Komplexes Muster: parametrische Wiederholung lokal, nicht ein kostenpflichtiger Aufruf pro Element.
- Vorschau: eine explizite visuelle Beurteilung benutzt das aktuelle Bild; unveränderte Geometrieanfrage versendet nicht ungefragt ein Bild.
- Kosten: jedes Request vor dem Senden auf Budget geprüft, Ergebnisse nachvollziehbar; kein automatischer Wechsel auf ein teureres Modell.
- Sicherheit: Request-Protokolle dürfen weder API-Keys noch vollständige Dokumentinhalte enthalten.
- Release erst nach grünen Tests **und** nachgewiesenen niedrigen Kosten für einfache Konstruktionen auf einem echten Client.

## Nächste technische Arbeit (Blocker)

Den tatsächlich gestarteten Python-Chat-Client v0.1.3 samt OpenRouter-Request-Aufbau, Prompt-Generierung, Live-Zustandserfassung und Kostenprüfung im Repository lokalisieren. Danach zuerst einen reproduzierbaren Vorher/Nachher-Test für die Dreieckanfrage hinzufügen und genau diese Schicht korrigieren. Der Rust-MCP-Server stellt die notwendigen selektiven Lesewege bereits weitgehend bereit; eine komplette zweite Geometrie-Engine ist nicht erforderlich.

Begleitend liegt unter `Tools/cost_audit.py` ein **offline** arbeitender Diagnoseauswerter, der unveränderte Anbieter-Tokendaten aggregiert. Er führt **keine** API-Aufrufe aus und behauptet keine bereits erzielte Einsparung.

## Implementierungsstand 21.10.2026 – Selektions- und Budgetmodul

- `Tools/ai_client_cost_policy.py`: reine Client-Hilfsfunktionen mit vier expliziten MCP-Werkzeugprofilen (draw/edit/visual/discover); keine ungeprüfte Weitergabe aller Befehle.
- `compact_document`: überträgt nur explizit zugelassene Kurzfelder statt automatisch vollständige Objektbäume. Ist die Zusammenfassung zu groß, wird abgebrochen und eine gezieltere Abfrage verlangt.
- `CostGate`: konservatives Vorabreservieren und Abrechnen in Euro mit vom Client **explizit bereitzustellendem** Wechselkurs und Kostendeckel. Bei unbekannten Preisen kein automatisches Senden.
- `Tools/test_ai_client_cost_policy.py`: Tests für kleines Werkzeugset, bedarfsgerechte Bildwerkzeuge, große Dokumente und Budgetüberschreitung.
- GitHub Actions `AI cost audit tests`: **erfolgreich** für den Stand dieses Branches.

**Nicht integriert:** Die tatsächliche Python-Chat-Anwendung v0.1.3 ist weiterhin nicht in diesem Repository enthalten. Die Hilfsfunktionen werden von ihr deshalb noch nicht aufgerufen. Eine reale Einsparung, ein funktionierendes Dreieck und die Dokument-Synchronisierung im Chat sind noch nicht nachgewiesen. Der nächste Schritt muss an diesem Client erfolgen, nicht an einem Ersatz ohne Benutzersitzung.
