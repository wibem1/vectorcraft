# Arbeitsregeln — VectorCraft Chat (ergänzend zur root-AGENTS.md)

**Zuerst** `PROJECT_STATE.md` und `TODO.md` in diesem Verzeichnis lesen. Die umfangreiche root-`AGENTS.md` betrifft insbesondere die VectorCraft-Engine; deren technische und Lizenzregeln bleiben unverändert gültig.

- Ein Auftrag = ein kleines überprüfbares Ziel; keine eigenmächtige Ausweitung auf App-Umbau, neue Features oder Build-Infrastruktur.
- Unterscheide strikt: dokumentiert / implementiert / lokal geprüft / live gegen die echte Engine und den echten Provider erfolgreich.
- Vor API-Anfragen kostenlose Tests verwenden; keine bezahlten Wiederholungsschleifen. Budgetvorgaben an Work sind keine technisch garantierten Limits.
- Nicht nach jedem Codeexperiment eine App-Version bauen oder veröffentlichen. Nur positiv getestete Stände freigeben.
- GitHub primär als Projektgedächtnis: Code, `PROJECT_STATE.md`, vorhandene `TODO.md`. Actions nur für gezielte, notwendige Prüfungen und ohne automatische Wiederholungen.
- Bei Fehlern nur eine Ursache isolieren, ohne gleichzeitig Funktionen zu erweitern. Nach zwei erfolglosen gezielten Versuchen zunächst Analyse statt weiterer Reparaturvarianten.
- Ein neuer Chat / Work-Auftrag bestätigt zuerst Quellstand, bekannte Nachweise, Blocker und den nächsten einzelnen Schritt; bereits geklärte Fragen nicht ohne neuen Beleg erneut untersuchen.
- Schließe jeden abgeschlossenen Schritt mit einer knappen Aktualisierung von `PROJECT_STATE.md` ab. Keine umfangreichen Tätigkeitsberichte und keine Parallelaufträge.
