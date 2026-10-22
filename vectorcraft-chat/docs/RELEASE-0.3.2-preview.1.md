Korrekturupdate vom 22.10.2026 für die zuvor freigegebene Vorabversion.

Behebt den in beiden Nutzerdiagnosen nachgewiesenen Fehler „Zusatzpreis nicht unterstützt: image“, der reine Textaufträge vor dem API-Aufruf blockierte. Der öffentliche Katalog von google/gemini-3.8-flash wurde tatsächlich geprüft: Bild-, Audio-, Audio-Cache-, Websuche- und Reasoning-Preise sind vorhanden. Ungenutzte Bild-/Audio-Eingabepreise werden nur bei bestätigter reiner Textausgabe und reinem Texteingang ausgeschlossen. Websuche wird im Request ausdrücklich deaktiviert, :online gesperrt und Reasoning konservativ zusätzlich reserviert. Unbekannte Zusatzkosten und ungültige Preise bleiben gesperrt. Die Diagnose trennt Vorprüfung vom tatsächlichen API-Aufruf.

Sichtbare App-Version: 0.3.2-preview.1. ZIP vollständig entpacken, dann VectorCraftChat.exe bzw. VectorCraftChat.app öffnen. Die echte Engine und CLI sind enthalten und starten automatisch. Vor dem Start die alte Chat-App schließen. Einstellungen und gespeicherter Schlüssel werden weiterverwendet.

Quellstand: 3999cfb35844239d1fbf3eb6d65f4c789411ebcf.
Veröffentlichung nur nach SUCCESS der exakten Paket- und Regressionsläufe:
- Windows-/macOS-Intel-Pakete einschließlich echter nativer Engine und nichtnull multimodaler Preisfelder: https://github.com/wibem1/vectorcraft/actions/runs/39749645269
- Regressionen: https://github.com/wibem1/vectorcraft/actions/runs/39749644906

Unveränderte Einschränkungen der freigegebenen Preview: Kein positiver Live-OpenRouter-Nachweis mit gültigem CI-Key. Positive Provider-Antworten der nativen Tests sind HTTP-Fixtures, keine echten Modellantworten. Keine garantierte providerseitige Euro-Kostengrenze. Kein Apple-Silicon-Nativnachweis, keine Developer-ID/Notarisierung, keine signierten Installer. Die Korrektur beseitigt den konkret diagnostizierten Vorprüfungsfehler und behauptet keine allgemeine Fehlerfreiheit freier Konstruktionen.

Prüfsummen und tatsächlich überprüfte native Berichte: SHA256SUMS.txt und test-results.json.

Die gefrorenen Windows-/macOS-Pakete führen die vollständige gemeinsame native Testsuite aus, mit exakt den ausgelieferten Binärdateien; kein übersprungener nativer Test. Die Engine selbst wurde nicht geändert. Zusätzliche Quellbuilds 39749645011 und 39749644996 laufen unabhängig weiter und werden nicht als bereits bestanden ausgewiesen. Sie bauen dieselbe unveränderte Rust-Engine nochmals; die Veröffentlichung wartet nicht auf diese doppelten Builds, nachdem die eigentlichen Pakete mit ihren echten Engine-Binaries erfolgreich geprüft wurden. Kein fehlgeschlagener Test wurde übergangen.
