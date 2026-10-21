# VectorCraft – bestätigter Projektstand

Stand: **21. Oktober 2026**. Arbeitsbereich: [`projects/chatgpt-work/`](projects/chatgpt-work/README.md).

Diese Sicherung dokumentiert bestehende Ergebnisse. **Keine neuen Funktionen und keine Änderungen am ursprünglichen VectorCraft-Quellcode.** Basis ist `main` bei `0a33cff3f6e2a1e9e672f4c3816f58cd8d3d032e`; eigener Branch: `archive/chatgpt-work-2026-10-21`.

## Was bestätigt funktioniert

- Direkte Steuerung der laufenden Windows-Anwendung VectorCraft 0.11.0 über JSON-Zeilen auf `127.0.0.1:7979`. ChatGPT Work/Codex führt dafür freigegebene lokale Werkzeuge und Python-Hilfsskripte aus. Die KI steckt nicht in VectorCraft und benötigt das alte Reglerfenster für diesen Weg nicht.
- Zeichnungen auslesen, neue Dokumente öffnen, Konstruktionen erzeugen, rendern, visuell prüfen und als `.vectorcraft`, SVG und PNG sichern.
- Symbolbearbeitung in zwei Schritten: `symbol.edit` löst eine Instanz in Geometrie auf; `symbol.update` mit gespeichertem Namen und expliziten IDs aktualisiert die gemeinsame Definition. `symbol.replace` hat eine andere Bedeutung und ist kein Ersatz für `symbol.update`.
- Steuerfenster 0.4.2: automatische Symbolerkennung, kompakte Oberfläche, Bearbeitungsobjekte wieder auswählen, Diagnose-Export. Der Anwender bestätigte den erfolgreichen Ablauf einschließlich Aktualisierung aller Instanzen.
- Steuerfenster 0.5: Anzahl, Radius, Motivdrehung und Mittelpunkt eines zusätzlichen Mandalas über Regler verändern. Atomare `command.batch`-Aktualisierungen; der Anwender bestätigte die Grundfunktion.

## Gesicherte Konstruktionen

| Zeichnung | Bestätigte Struktur | Dateien |
|---|---|---|
| Sonnenrosette | 31 verknüpfte Symbolinstanzen, versetzte Ringe und Punktekranz | [Galerie / Dateien](projects/chatgpt-work/docs/ARTWORK_CATALOG.md#sonnenrosette) |
| Aurelia | komplexes Flechtmandala, 1.356 Elemente; Pfade und Gruppen, **keine** gemeinsam verknüpften Symbolmotive | [Galerie / Dateien](projects/chatgpt-work/docs/ARTWORK_CATALOG.md#aurelia) |
| Liniara | sechs Symboldefinitionen, insgesamt 212 Instanzen; feines Linienmandala | [Galerie / Dateien](projects/chatgpt-work/docs/ARTWORK_CATALOG.md#liniara) |
| Liniara – Farbenspiel | sechs Definitionen / 212 Instanzen; zusätzliche Farben, Koordinaten unverändert | [Galerie / Dateien](projects/chatgpt-work/docs/ARTWORK_CATALOG.md#liniara--farbenspiel) |
| Rekonstruktion einer externen Vorlage | lokal erfolgreich als Vektorkonturen, drei Symbolfamilien / 18 Instanzen; kein eingebettetes Rasterbild | **Nur lokales Vollbackup, nicht öffentlich** |

Die zuletzt korrigierte Erklärung des Anwenders gilt: **Es bestehen keine Veröffentlichungsrechte an der externen Bildvorlage.** Weder Vorlage noch PNG/SVG/VectorCraft-Nachzeichnung sind in diesem GitHub-Stand enthalten. Details: [Herkunft und Ausschlüsse](projects/chatgpt-work/docs/PROVENANCE.md).

## Sicherung und Nachweise

- Vor der Organisation: unveränderte lokale Kopie von **134 Dateien / 96.888.633 Bytes**, je Datei mit SHA-256 verglichen.
- Öffentliches Archiv: **130 dieser Dateien**, unverändert; vier nicht freigegebene Assets bleiben ausschließlich lokal.
- Zusätzlich fünf geöffnete eigene Projektzeichnungen lesend erfasst, ursprünglichen aktiven Tab danach wiederhergestellt. Die fremde Vorlagenrekonstruktion wurde aus der öffentlichen Live-Erfassung ausgeschlossen.
- Historische Windows-ZIPs 0.4, 0.4.1, 0.4.2 und 0.5, frühere Eingangsarchive, Quellstände, Diagnosen und Anleitungen sind erhalten. Ungepackte DLL-/Runtime-Duplikate, Build-Caches und installierte Abhängigkeiten werden nicht zusätzlich versioniert.
- [Dateimanifest](projects/chatgpt-work/FILE_MANIFEST.json): Größen, SHA-256 und Git-Blob-IDs. [Sicherungsumfang](projects/chatgpt-work/docs/BACKUP_SCOPE.md) beschreibt Originale, Arbeitskopien und Ausschlüsse.
- [Verifikation](projects/chatgpt-work/docs/VERIFICATION.md) trennt historische Tests, aktuelle Archivprüfung und nicht ausgeführte Prüfungen.

## Offene Probleme – nicht als erledigt betrachten

1. **Manuelles Verschieben/Drehen beendet die Reglerarbeit in 0.5.** Der aktuelle Code ersetzt seine eigenen Kopien und sperrt bei manuellen Abweichungen. Ein Erhalt individueller Transformationen wurde besprochen, aber **nicht implementiert**. Es gibt keine bestätigte 0.5.1.
2. Direkte KI-Konstruktion und Reglerprogramm sind getrennte Arbeitsweisen. Kein gemeinsames KI-Bedienfeld, kein autonomer Hintergrunddienst und keine kontinuierliche Bildschirmbeobachtung.
3. Einige Konstruktionsskripte sind unveränderte Sitzungsartefakte: absolute Windows-Pfade, vorausgesetzte aktive Dokumente, historische Objekt-IDs und feste Ausgabeordner. **Nicht blind gegen eine laufende Zeichnung ausführen.** Ihre Übertragbarkeit wurde nicht als Produktfunktion bestätigt.
4. `archive/.../session/color_liniara.py` ist ein **verworfenes Experiment**: Bei einer Farbänderung über Auflösen/Neunormalisieren wurde eine Koordinatenabweichung erkannt und die Undo-Gruppe zurückgerollt. Erfolgreich war `color_definitions.py` mit Änderung der Definitionen in einer Kopie der nativen Dokumentstruktur. Beide Stände bleiben als Diagnose erhalten.
5. Native Symboldateien benötigen natürliche Größen unter `document.unknown.symbolSizes`; nur gleichnamige zusätzliche Felder auf der falschen Ebene reichen im getesteten Importweg nicht. Zentrierung und Normierung der Symbolkunst müssen bei Definitionseingriffen geprüft werden.
6. Prüfungen vor/nach einem Schreibbefehl sind nicht gemeinsam atomar. Titel, Tabindex, Pfad, Revision und Objekt-IDs sind kein perfekter Ersatz für eine stabile Dokument-UUID. Bei unklarem Ergebnis keine automatische Wiederholung.
7. Kein aktueller vollständiger Rust-/WASM-CI-Lauf: In dieser Umgebung ist Cargo nicht verfügbar. Die ursprünglichen Engine-/UI-Quellen wurden nicht verändert.
8. Die veröffentlichbaren Originalwerke bleiben von der nicht freigegebenen externen Vorlage getrennt. Keine pauschale Behauptung, jede beliebige Grafik verlustfrei rekonstruieren zu können.

## Nächste Arbeitsschritte – nur geplant

1. Diesen Sicherungsbranch prüfen; anschließend gegebenenfalls gezielt in `main` übernehmen.
2. Künftige Aufgaben und bestätigte Fehler auf GitHub festhalten. Das Repository hat derzeit Issues deaktiviert; keine Einstellung wurde dafür verändert. Bis zur bewussten Entscheidung dient [der Aufgabenstand](projects/chatgpt-work/docs/NEXT_STEPS.md) als versioniertes Arbeitsbuch.
3. Vor Änderungen einen eigenen Branch verwenden, Sicherungen und Dateinachweise fortführen.
4. Falls beauftragt: individuelle Transformationen in der Mandala-Steuerung erhalten; erst Verhalten definieren und Regressionen abdecken.
5. Falls beauftragt: die bewährte direkte Steuerung in wiederverwendbare, kontextprüfende Werkzeuge überführen und Sitzungs-Skripte portabel machen.

**Auftrag dieser Änderung bleibt ausschließlich Sicherung, Organisation und Dokumentation.**
