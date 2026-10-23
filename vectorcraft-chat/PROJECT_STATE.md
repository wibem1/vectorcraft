# VectorCraft Chat — verbindlicher Projektstand
Stand: 2026-10-23 · Übergabe aus Chat · nur Dokumentation

## Ziel
Eine kleine, kostengünstige KI-Chatsteuerung für die bereits installierte VectorCraft-Anwendung: natürliche Anweisungen → gültige VectorCraft-Kommandos → sichtbare, editierbare Konstruktion → gezielte Folgeänderung desselben Objekts. Windows und macOS erst nach erfolgreichem Kernnachweis.

## Gesicherte Erkenntnisse
- Am 14.10.2026 funktionierte die direkte lokale VectorCraft-Steuerung über TCP 127.0.0.1:7979, mit `engine.execute`, `document.inspect` und `engine.commands`. Damalige Diagnosen meldeten erfolgreich erzeugte/bearbeitete Dokumente und Exporte.
- Referenz: `VectorCraft-Mandala-Zentriert-v2.zip` (ursprüngliche Sicherung, NICHT durch dieses Dokument im Repository abgelegt). SHA-256 des ursprünglichen ZIP laut abgeschlossener Übergabeprüfung E01: `09ab09949b987a71d7735dd456bca5795eddb60d98bf9cedf1661232ee23f6ae`.
- Inhalt der Referenz-ZIP: `vectorcraft_mandala_zentriert.py`, `01_Pruefen.bat`, `02_Mandala_zentriert_erstellen.bat`, `ANLEITUNG.txt`. Damals erfolgreich: drei native radiale Live-Repeat-Ringe mit Mittelpunkt (700,700); durch den Nutzer am 14.10. bestätigt. Eine erneute Live-Ausführung erfolgte im Übergabetest nicht.
- Ein Chat-zu-Chat-Übernahme-/Rückübergabetest E01 mit unverändertem Originalcode und SHA-256-Prüfung war erfolgreich. E01 belegt eine statische Übergabe, NICHT die erfolgreiche Weiterentwicklung.
- Der spätere VectorCraft-Chat-Prototyp hatte wiederholt Fehler in der KI-Antwortverarbeitung, Befehlsvalidierung, Token-/Kostenkontrolle und Integration. Das ist kein Beleg, dass die VectorCraft-Engine nicht funktioniert.
- Die bestehende Datei `vectorcraft-chat/TODO.md` dokumentiert technische Arbeiten, Testläufe und offene Freigabeblocker; ihre Aussagen sind zunächst historische Einträge, kein automatisch aktueller Freigabenachweis.

## Was ausdrücklich NICHT nachgewiesen ist
- Zuverlässige freie KI-Steuerung über OpenRouter bis zur sichtbaren Konstruktion und interaktiven Folgeänderung.
- Erfolgreiche, aktuelle End-to-End-Integrationstests der veröffentlichten Windows- und Mac-App.
- Dass das Mandala-Referenzarchiv bereits in diesem GitHub-Repository abgelegt ist.
- Verbindlich technisch erzwungene Limits für Work-Credits oder eine garantierte Euro-Obergrenze bei einem Provider.

## Ursachenanalyse / verbindliche organisatorische Erkenntnisse
- Unterschied zwischen funktionierendem deterministischem Steuerprogramm und noch unbewiesener freier KI-Interpretation beachten.
- Zu früher Ausbau von UI, Mehrmodellsteuerung, Diagnose, Packaging und Actions vergrößerte die Fehlerfläche.
- Syntaktisch geprüfter Code und erfolgreiche Builds ersetzen keinen echten Funktionstest.
- Wiederholte Chats/Work-Aufträge verloren verifizierte Erkenntnisse; mehrere Reparatur- und Buildschleifen erzeugten Kosten ohne nachgewiesenen Nutzen.
- GitHub dient als dauerhafter Speicher für Code und Projektzustand, nicht als Anlass für dauernde Actions-Läufe.

## Nächster Schritt (ausschließlich, ohne Codeänderung)
1. Ein neuer normaler Chat liest `vectorcraft-chat/AGENTS.md`, diese Datei und `vectorcraft-chat/TODO.md` sowie gezielt relevanten Code.
2. Er gibt eine knappe Übernahmeprüfung zurück: aktueller Quellstand, bereits belegte Funktionen, offene Beweise, genau EIN sinnvoller nächster Minimalkomponententest.
3. Keine Builds, keine kostenpflichtigen API-Aufrufe, keine Releases und keine App-Versionen bei dieser Übernahmeprüfung.
4. Erst nach gemeinsamer Auswertung einen kleinen Funktionsversuch planen. Die Referenz-ZIP muss, solange sie nicht im Repo liegt, bei Bedarf separat bereitgestellt werden.

## Disziplin für die nächsten Sitzungen
- Vor jeder Änderung TODO lesen; nur eine konkrete Funktion je Abschnitt.
- Keine parallelen Entwicklungsaufträge an demselben Quellstand.
- Keine ungetesteten Versionen ausgeben; ohne positiven Nachweis Status `nicht verifiziert`.
- Den letzten bestätigten Stand nicht überschreiben; bei Fehlschlag sauber zurückkehren.
- `PROJECT_STATE.md` nur bei einer relevanten neuen Erkenntnis oder am Ende eines abgeschlossenen Entwicklungsschritts aktualisieren.
- Kein automatischer Workflow-/Build-Retry. Kostenpflichtige KI-Calls nur mit ausdrücklichem Anlass und konservativer Kostenprüfung.
