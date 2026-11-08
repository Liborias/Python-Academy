### Ověřit skutečný obsah CSV

Tabulka má kod/nazev str a hodnota float64 bez chybějících hodnot, libovolný řádkový index. Text může obsahovat středník, uvozovky, nový řádek, diakritiku i doslovné NA. Soubor existuje a používá UTF-8/středník/desetinnou čárku. Vraťte bool, zda obsahuje stejné sloupce, pořadí řádků a hodnoty. Původní řádkový index se neexportuje. Čísla porovnejte s tolerancí 1e-12, text přesně; chybné schéma vraťte jako False. Tabulku ani soubor neměňte.

Doplňte `over_csv(tabulka, cesta)`. Pod zadáním lze zobrazit možné řešení.
