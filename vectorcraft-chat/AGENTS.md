# Arbeitsregeln — VectorCraft Chat (ergänzend zur root-AGENTS.md)

**Zuerst** `PROJECT_STATE.md` und `TODO.md` in diesem Verzeichnis lesen. Die umfangreiche root-`AGENTS.md` betrifft insbesondere die VectorCraft-Engine; deren technische und Lizenzregeln bleiben unverändert gültig.

- Ein Auftrag = ein kleines überprüfbares Ziel; keine eigenmächtige Ausweitung auf App-Umbau, neue Features oder Build-Infrastruktur.
- Unterscheide strikt: dokumentiert / implementiert / lokal geprüft / live gegen die echte Engine und den echten Provider erfolgreich.
- Vor API-Anfragen kostenlose Tests verwenden; keine bezahlten Wiederholungsschleifen. Budgetvorgaben an Work sind keine technisch garantierten Limits.
- Nicht nach jedem Codeexperiment eine App-Version bauen oder veröffentlichen. Nur positiv getestete Stände freigeben.
- GitHub primär als Projektgedächtnis: Code, `PROJECT_STATE.md`, vorhandene `TODO.md`. **GitHub Actions bleiben in der frühen Entwicklungsphase ausdrücklich gesperrt.** Die Freigabe darf erst erwogen werden, wenn ein klar abgegrenzter, stabiler Entwicklungsstand durch gründliche lokale Tests belegt ist: wesentliche Funktionen einschließlich echter Engine-Interaktion erfolgreich geprüft, Regressionen bestanden, Ergebnisse und offene Fehler in `PROJECT_STATE.md` dokumentiert und keine wesentlichen ungeprüften Kernfunktionen. Simulationen, bloße Builds und statische Prüfungen genügen nicht. **Erst nach Erfüllung dieser Voraussetzungen UND gesonderter ausdrücklicher Nutzerfreigabe für einen konkret benannten Workflow** darf GitHub Actions verwendet werden. Vorher keine Workflow-Starts, Reruns oder automatisch ausgelösten CI-/Paketläufe; insbesondere kein Ausweichen auf Actions bei fehlendem lokalem Engine-Zugang. Kleine kostenlose lokale Tests bevorzugen; wenn nicht möglich, Blocker dokumentieren und stoppen.
- Bei Fehlern nur eine Ursache isolieren, ohne gleichzeitig Funktionen zu erweitern. Nach zwei erfolglosen gezielten Versuchen zunächst Analyse statt weiterer Reparaturvarianten.
- Ein neuer Chat / Work-Auftrag bestätigt zuerst Quellstand, bekannte Nachweise, Blocker und den nächsten einzelnen Schritt; bereits geklärte Fragen nicht ohne neuen Beleg erneut untersuchen.
- Schließe jeden abgeschlossenen Schritt mit einer knappen Aktualisierung von `PROJECT_STATE.md` ab. Keine umfangreichen Tätigkeitsberichte und keine Parallelaufträge.

## Projektübergreifender Standard
Vor jedem neuen Entwicklungsauftrag zusätzlich die zentralen Regeln lesen: https://github.com/wibem1/AI-Development-Standards/blob/main/DEVELOPMENT_STANDARDS.md . Diese ergänzen bestehende VectorCraft-Engine-Regeln, ersetzen sie nicht.

## Verbindliche Aufgabenquelle
**Vor jeder Entwicklung `CURRENT_TASK.md` lesen.** Nur der dort freigegebene Auftrag darf ausgeführt werden. Ist er blockiert, stoppen und den Blocker benennen; nicht zur historischen `TODO.md` als Arbeitsauftrag wechseln. Andere Schritte benötigen eine neue Freigabe.
