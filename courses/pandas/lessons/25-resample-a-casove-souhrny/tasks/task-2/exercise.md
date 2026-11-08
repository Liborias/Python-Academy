### Počet záznamů v každém dni

Vraťte int64 Series počtů všech záznamů za kalendářní den, včetně záznamů s NaN. Vstup je float64 Series se vzestupným DatetimeIndex datetime64[us], bez NaT/pásma; opakované časy jsou platné. Dny bez záznamu mezi prvním a posledním dnem mají počet 0. Interval je zleva uzavřený a označený začátkem dne. Zachovejte name i index.name, prázdný vstup je platný.

Doplňte `denni_pocty(serie)`. Vstupy neměňte. Šablona má zkušební volání a pod úkolem lze zobrazit možné řešení.
