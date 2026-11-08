### Prodejní řádky bez protějšku

Prodeje mají produkt str, kusy int64; ceník produkt str, cena float64 a jedinečný produkt. Klíče nechybějí, ale cena známého produktu může být NaN. Vraťte pouze původní prodejní sloupce u řádků, jejichž klíč v ceníku není, v původním pořadí s novým RangeIndex. Nezaměňujte chybějící cenu se chybějícím klíčem. Prázdné vstupy jsou platné, opakované prodeje zachovejte.

Doplňte `nesparovane_radky(prodeje, cenik)`. Vstupy neměňte. Šablona má zkušební volání a pod úkolem lze zobrazit možné řešení.
