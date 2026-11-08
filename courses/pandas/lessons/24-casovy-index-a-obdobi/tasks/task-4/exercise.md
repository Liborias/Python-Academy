### Pravidelná denní mřížka

Vraťte float64 Series na denní mřížce od zacatek do konec včetně obou dnů (platné YYYY-MM-DD, zacatek <= konec). Vstup má jedinečný vzestupný DatetimeIndex datetime64[us], jen půlnoci, bez NaT/pásma. Chybějící dny doplňte NaN, nevytvářejte součty ani předchozí hodnoty. Zachovejte name Series i jméno indexu, výstupní index má jednotku us. Prázdný vstup je platný.

Doplňte `pravidelna_mrizka(serie, zacatek, konec)`. Vstupy neměňte. Šablona má zkušební volání a pod úkolem lze zobrazit možné řešení.
