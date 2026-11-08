### Jeden klíč na každé straně

Proveďte outer spojení podle předaného str klíče, bez chybějících klíčů. Ostatní sloupce jsou odlišné float64. Výsledek obsahuje sjednocení klíčů vzestupně, levé sloupce a pak pravé neklíčové sloupce, s RangeIndex. Vyžadujte jedinečnost klíče na obou stranách pomocí validate="one_to_one": při duplicitě na kterékoli straně vyvolejte pd.errors.MergeError bez změny vstupů. Prázdné tabulky jsou platné.

Doplňte `spoj_jednoznacne(leva, prava, klic)`. Vstupy neměňte. Šablona má zkušební volání a pod úkolem lze zobrazit možné řešení.
