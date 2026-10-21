# Tests und Freigabestatus

`python -m unittest -v test_app` führt die in der Version enthaltenen Unittests aus. Tests beweisen **keinen** End-to-End-Betrieb mit echtem VectorCraft oder OpenRouter.

Vor einem Release notwendig: Verbindung zum lokalen Steuerprotokoll, Freigabelogik, absichtlicher Fehler einer Teilaktion, Wiedereinlesen der Objekte, Kosten-/Budgetabbruch, Fenstergröße 420 × 360, Windows- und Mac-Start, gespeicherter und erneut geladener Verlauf.

Bei jeder Änderung Testprotokoll mit Datum/Plattform/Commit sichern.
