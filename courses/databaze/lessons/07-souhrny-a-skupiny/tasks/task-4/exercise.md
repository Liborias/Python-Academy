## Skupiny vybrané pomocí HAVING

Vytvořte **silne_kategorie(con, minimum)**. Vrátí (kategorie, součet_kusů) pro skupiny, jejichž součet je alespoň minimum. Řadí podle součtu sestupně, pak podle kategorie vzestupně s NULL první při shodě. Minimum je předané celé číslo a musí být SQL parametr.

HAVING pracuje s hotovým souhrnem skupiny. WHERE by filtrovalo jednotlivé řádky dřív a mohlo by součet změnit. Požadujeme i přesnou rovnost hranice, nula je platné minimum. Data ani transakci neměňte.
