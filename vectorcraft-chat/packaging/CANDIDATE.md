# VectorCraft Chat – CI-Testkandidat, kein Release

Python/Tk, Chat, native VectorCraft-Engine und MCP-CLI sind enthalten.
Windows: gesamten Ordner entpacken, VectorCraftChat.exe öffnen.
macOS Intel: VectorCraftChat.app vollständig behalten und öffnen.
Die Engine wird automatisch gestartet. Kein separater Python-Start erforderlich.

Unsignierter Windows-Testkandidat / nur ad hoc signierte macOS-App: keine
Developer-ID, keine Notarisierung und keine allgemeine Installationsfreigabe.
OpenRouter benötigt einen eigenen Schlüssel. Die lokale Kostenprüfung ersetzt
keine garantierte providerseitige 0,10-€-Grenze. Positive Live-Completion ist
mangels CI-Testschlüssel noch nicht geprüft; native Folgeaktionen nutzen im Test
bewusst eine lokale HTTP-Fixture. Keine externen Modellkosten im Pakettest.

--self-test AUSGABEVERZEICHNIS ist ein expliziter automatisierter Testmodus:
eigener Engine-Prozess, temporäres Profil, temporäre Schlüssel, echter nativer
Dreieck-/30°-/Folgeänderungstest; Testberichte im Ausgabeverzeichnis.

Zusätzlich prüft der Pakettest automatische Binary-Pfaderkennung, den echten
öffentlichen OpenRouter-Katalog über HTTPS und die echte HTTP-401-Antwort
mit absichtlich ungültigem Schlüssel; kein positiver Live-Auftrag.
