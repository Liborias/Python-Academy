### Souhrny kalendářních měsíců

Vraťte float64 součty za kalendářní měsíc se štítkem na jeho začátku (MS), zleva uzavřený interval. Vstup má vzestupný DatetimeIndex datetime64[us], bez NaT/pásma, časy se mohou opakovat. Vyžadujte min_count=1: prázdné měsíce mezi prvním a posledním měsícem i měsíce se samými NaN mají NaN, nikoli nulu. Zachovejte name a index.name. Měsíc nenahrazujte 30 dny. Prázdný vstup je platný.

Doplňte `mesicni_soucty(serie)`. Vstupy neměňte. Šablona má zkušební volání a pod úkolem lze zobrazit možné řešení.
