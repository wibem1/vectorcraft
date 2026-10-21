# Prüfstand

## Historisch bestätigt

- 24 automatisierte Python-Tests im zuletzt gelieferten Steuerprogramm 0.5: 14 Symbol-/Zustandstests und 10 Mandala-Tests.
- Separate Tests mit installierter VectorCraft-Engine im headless MCP-Prozess: `symbol.edit`, Fülländerung, `symbol.update`, verknüpfte Instanzen; radiale Kopien, Radius-/Drehungsänderungen, Batch-Rollback und ein gemeinsamer Undo-Schritt.
- GUI-Prüfungen: schnelles Ändern bündeln, zuletzt eingestellte Werte nach laufendem Aufruf übernehmen, Live-Pause, Beenden ohne Dokumentänderung, anstehende Aktualisierung beim Schließen stornieren, kompakte Oberfläche und EXE-Start.
- Direkte Konstruktion, Renderprüfung und Symbolzahlen der veröffentlichten Mandalas; Geometrieerhalt der endgültigen Farbvariante.

Die Originalberichte stehen unverändert in `archive/2026-10-21/`, `diagnostics/` und den historischen ZIP-Paketen. Historische Aussagen werden nicht in einen aktuellen vollständigen Produkt-/Plattformtest umgedeutet.

## Prüfung dieser Sicherung

Die 24 isolierten Python-Tests wurden am 21.10.2026 erneut erfolgreich ausgeführt. `git diff --check` meldete keine Fehler. Die folgenden Archivprüfungen werden zusätzlich im Abschlussbericht und Dateimanifest festgehalten.

1. Alle ursprünglichen lokalen Sicherungskopien per SHA-256 vergleichen.
2. Nicht freigegebene Vorlage und Rekonstruktion aus dem öffentlichen Dateisatz ausschließen; auch ZIP-Inhalte prüfen.
3. Sämtliche übertragenen Dateien über das Dateimanifest prüfen; ZIP-CRCs sowie native JSON-/SVG-Strukturen kontrollieren.
4. Die 24 isolierten Python-Tests erneut ausführen. Keine schreibenden Tests gegen die laufenden Benutzerzeichnungen.
5. Geöffnete eigene Dokumente nur lesend erfassen und den ursprünglichen Tab wiederherstellen.
6. Zentralen Assetnachweis und `git diff --check` prüfen.
7. Nach GitHub-Übertragung jeden vorgesehenen Repositorypfad, jede Größe und jede Git-Blob-ID mit dem Remote-Baum vergleichen. Der lokale Abschlussbericht enthält zusätzlich den Commit und die Remote-Prüfung.

## Nicht ausgeführt

`cargo xtask ci` kann in dieser Umgebung nicht ausgeführt werden, weil Cargo nicht vorhanden ist. Es wurden keine Rust-Engine-/UI-Dateien, Cargo-Manifeste oder WASM-Build-Konfigurationen geändert. Die Archivprüfung ersetzt keinen Rust-/WASM-CI-Lauf.

Es wurde kein neues Feature implementiert und keine manuelle Vollprüfung aller Funktionen auf allen Plattformen durchgeführt. Die archivierten EXE-Versionen werden als ursprüngliche Lieferstände aufbewahrt, nicht neu gebaut.
