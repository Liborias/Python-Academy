### CSV nejprve jako text

Tabulka má kod/nazev str a hodnota float64 bez chybějících hodnot, libovolný řádkový index. Text může obsahovat středník, uvozovky, nový řádek, diakritiku i doslovné NA. Vraťte CSV jako obyčejný Unicode str, bez zápisu do souboru. Středník, desetinná čárka, hlavička a žádný index/BOM. Správně uvozujte speciální znaky. Prázdný vstup dává text hlavičky. Tabulku neměňte.

Doplňte `csv_text(tabulka)`. Pod zadáním lze zobrazit možné řešení.
