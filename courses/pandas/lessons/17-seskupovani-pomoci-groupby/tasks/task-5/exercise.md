### Seskupení jako obyčejná tabulka

Vraťte DataFrame se sloupci [klic, hodnota] a novým RangeIndex bez názvu. Str klíč zůstane sloupcem; pro každou skupinu sečtěte float64 hodnotu s min_count=1. Zahrňte chybějící klíč, klíče vzestupně a chybějící poslední. Skupina bez známého údaje má NaN. Názvy jsou existující a různé, prázdný vstup je platný.

Doplňte `seskup_do_tabulky(tabulka, klic, hodnota)`. Vstupy neměňte. Šablona má zkušební volání a pod úkolem lze zobrazit možné řešení.
