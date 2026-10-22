Freigabe am 22.10.2026 auf ausdrückliche Anweisung des Projektinhabers nach Bekanntgabe des fehlenden Live-Testschlüssels.

Eigenständige portable Pakete mit gebündeltem Python/Tk, echter VectorCraft-Engine und CLI; die Chat-App startet VectorCraft automatisch. ZIP vollständig entpacken, dann VectorCraftChat.exe bzw. VectorCraftChat.app öffnen. macOS-Paket: Intel x64; Apple Silicon nicht nativ geprüft. Keine signierten Installer, keine Apple-Notarisierung.

Die Binärdateien werden unverändert aus dem erfolgreichen Paketlauf 39726542072 übernommen. Die interne App-Versionsanzeige bleibt daher 0.3.1-dev; die Veröffentlichung heißt 0.3.1 Preview 1. Keine Neuübersetzung und kein ungetesteter Binäraustausch.

Bestanden am Quellstand a38c87aa17b0f674cfc0970eb125920cde3f8aa9:
- Native Windows-/macOS-Intel-Integration: https://github.com/wibem1/vectorcraft/actions/runs/39726542081
- Gefrorene eigenständige Pakete: https://github.com/wibem1/vectorcraft/actions/runs/39726542072
- Headless-Engine: https://github.com/wibem1/vectorcraft/actions/runs/39726542201
- Plattformregressionen und öffentliche Provider-Prüfungen: https://github.com/wibem1/vectorcraft/actions/runs/39726542048
- Automatischer Start, Dreieck/Objekt-ID/30°, zusätzliche offene und geschlossene Pfade, gezielte Folgeänderung, Erhalt einer unabhängigen Zwischenbearbeitung und anderer Objekte, Betriebssystem-Schlüsselspeicherung, Modellwahl, Diagnose und Kostenbuchung.

Bekannte Einschränkungen:
- Der positive OpenRouter-Live-Test ist mangels GitHub-Secret OPENROUTER_API_KEY nicht bestanden. Positive Modellantworten in den Integrationstests stammen aus einer HTTP-Fixture; die Engine ist echt. Freie und komplexe natürlichsprachliche Konstruktionen sind damit nicht vollständig Ende zu Ende nachgewiesen. Der Nutzer benötigt seinen eigenen OpenRouter-Key in der App.
- 0,10 € ist eine konservative lokale Vorabprüfung, keine garantierte providerseitige Euro-Kostenobergrenze. Die Oberfläche weist darauf hin.
- Freigabe als Vorabversion aufgrund ausdrücklicher Nutzerentscheidung; keine Behauptung, alle ursprünglichen Freigabebedingungen seien erfüllt.

Die bisherige Freigabesperre wird für genau diese unveränderten, getesteten Pakete durch die ausdrückliche Nutzeranweisung „freigeben!“ aufgehoben. Weitere offene Punkte stehen in vectorcraft-chat/TODO.md. test-results.json und SHA256SUMS.txt liegen den Downloads bei.
