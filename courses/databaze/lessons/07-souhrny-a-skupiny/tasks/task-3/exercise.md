## COUNT a chybějící hodnoty

Vytvořte **pocet_vyplnenych(con)** nad udalosti. Vrátí jednu n-tici (COUNT(*), COUNT(poznamka), COUNT(DISTINCT poznamka)). Tím odlišíme všechny řádky, vyplněné hodnoty a počet jejich různých hodnot.

NULL se v počtu sloupce nepočítá, prázdný text ano. Dvě stejné poznámky se při DISTINCT počítají jednou. Pro prázdnou tabulku vraťte (0, 0, 0). Nedoplňujte náhradní text před počítáním, sloučil by rozdílné případy.
