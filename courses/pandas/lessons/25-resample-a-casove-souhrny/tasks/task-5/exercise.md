### Denní počet a průměr v jedné tabulce

Vraťte DataFrame s denními sloupci radky (všechny záznamy int64), dostupne (nechybějící hodnoty int64) a prumer (float64). Vstupní DatetimeIndex datetime64[us] je vzestupný bez NaT/pásma, opakované časy povolené; sloupec existuje a je float64, ostatní sloupce ignorujte. Prázdné dny mezi prvním a posledním dnem mají 0, 0, NaN. Použijte zleva uzavřené intervaly se štítky začátků dnů, zachovejte index.name. Prázdná tabulka se sloupci je platná.

Doplňte `denni_prehled(tabulka, sloupec)`. Vstupy neměňte. Šablona má zkušební volání a pod úkolem lze zobrazit možné řešení.
