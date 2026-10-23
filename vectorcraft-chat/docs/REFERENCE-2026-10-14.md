# Referenzstand VectorCraft, 14.10.2026

Quelle: vom Nutzer am 23.10.2026 bereitgestellter Gesprächsexport (113 Seiten). Die früheren Diagnosen wurden hier nicht erneut live ausgeführt.

## Nachgewiesenes Verfahren
ChatGPT erzeugte Testskripte. Der Nutzer startete diese unter Windows; die **lokalen Skripte** kommunizierten per TCP/JSON mit VectorCraft auf 127.0.0.1:7979. Ein direkter Netzwerkzugriff der ChatGPT-Sitzung selbst ist nicht belegt.

## Ergebnisse laut damaligen Protokollen
- Verbindungstest: TCP erfolgreich, ui.inspect, engine.commands und document.inspect; 1.028 Befehle laut damaliger Diagnoseauswertung.
- Zeichentest v5: 20 Steuerbefehle erfolgreich, editierbare Formen und Text erzeugt, gezielte Farbänderung eines vorhandenen Objekts mit ID 3, andere Objekte unverändert; Speicherung und SVG-Export.
- Agententest v7: acht editierbare Objekte, gezielte Folgeänderungen, Export in VectorCraft, SVG und PNG. Diese Tests verwendeten **vordefinierte** Befehle und waren keine freie KI-Steuerung.
- Mandala: drei native radiale Live-Repeat-Ringe mit 12/8/8 Wiederholungen; anfangs sichtbare Verschiebung, danach Zentrierungsarbeiten. Die Referenz `VectorCraft-Mandala-Zentriert-v2.zip` wurde in der späteren Übergabeprüfung E01 mit SHA-256 `09ab09949b987a71d7735dd456bca5795eddb60d98bf9cedf1661232ee23f6ae` identifiziert.
- Offener Grenzfall: Live-Repeat-Objekte funktionierten geometrisch, aber interaktives Einfügen neuer Pfade oder Unterebenen in Repeat-Container war nicht bestätigt. Daraus entstand der separate Entwicklungswunsch live-repeat-editing.

## Grenzen der Evidenz
Kein Nachweis eines direkten ChatGPT-Netzwerkzugangs zum lokalen Rechner, keiner verlässlichen freien OpenRouter-Konstruktion, keiner heutigen Live-Ausführung und keiner garantierten Kostenobergrenze. Die damaligen Assistentenantworten sind Gesprächsbelege und ersetzen keine neue Engine-Prüfung.

## Verbindliche Konsequenz für den Neustart
Die bewährte lokale Skriptkommunikation unverändert als Ausgangsbasis erhalten. Erst einen einzelnen echten TCP/JSON-Test mit Objekt-ID und gezielter Folgeänderung prüfen; dann einen minimalen KI-Adapter ergänzen. Keinen Umbau der alten komplexen Chat-App beginnen.

Fundstellen im Gesprächsexport: Seiten 7–14, 93–97 und 108–113. Den privaten Gesprächsexport nicht in GitHub hochladen.
