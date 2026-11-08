## Jedno číslo na skupinu nemusí stačit

U produktu chceme vědět nejen průměrnou tržbu na řádek, ale také počet dostupných údajů, minimum a maximum. `seskupene[hodnota].agg(["count", "mean", "min", "max"])` provede více agregací nad vybraným sloupcem. Výsledkem je DataFrame se čtyřmi sloupci v uvedeném pořadí; v indexu zůstane skupinový klíč.

Řetězce count, mean, min a max zde pojmenovávají podporované agregace pandas. Count dává počet známých hodnot, mean aritmetický průměr a min/max krajní dostupné hodnoty. Chybějící hodnoty se při těchto výpočtech vynechávají. Skupina bez známého údaje má count 0 a ostatní výsledky NaN. Prázdný výsledek má stále připravené sloupce a jejich datové typy.

## Názvy, které vysvětlují význam

```python
prehled = tabulka.groupby("produkt", as_index=False, dropna=False, sort=True).agg(
    radky=("trzba", "size"),
    dostupne=("trzba", "count"),
    prumer=("trzba", "mean"),
)
```

To je pojmenovaná agregace. Vlevo před = je název výsledného sloupce. Dvojice vpravo říká, z kterého zdrojového sloupce počítáme a jakou operací. Radky=("trzba", "size") počítá všechna místa ve skupině, i když tržba chybí; dostupne používá count a může být menší. Výsledné názvy a jejich pořadí tedy určujeme přímo v zápisu. As_index=False ponechá produkt jako sloupec a vytvoří RangeIndex.

Klíč nesmí kolidovat s názvem, který právě vytváříme. V úkolech je to zaručené. Při práci s vlastním zdrojem si názvy nejprve prohlédněte. Dropna=False a sort=True mají stejný význam jako v předchozí lekci: chybějící klíče zahrnout a skupiny seřadit technicky podle klíče.

## Jiný výpočet z jiného sloupce

Není potřeba počítat všechno z jedné hodnoty. Zápis `prumer=("cena", "mean"), maximum=("kusy", "max")` vytvoří průměr ceny a maximum počtu kusů. Každý výsledek musí mít srozumitelný název a jednotku. Průměr ceny na řádek není automaticky průměr zaplacený za jeden kus, pokud řádky obsahují různé počty kusů. Proto později v projektu počítáme tržbu jako cena krát kusy na každém řádku.

## Dva klíče v obyčejné tabulce

`groupby(["den", "produkt"], as_index=False, dropna=False, sort=True)` seskupuje podle kombinace dne a produktu. Stejný produkt v jiném dni tedy patří do jiné skupiny. Oba klíče zůstanou sloupci, teprve za nimi jsou pojmenované výsledky. Tak lze začít bez zavádění víceúrovňového indexu. Zahrneme i kombinaci s chybějícím klíčem a seřadíme podle obou klíčů.

## Řazení hotového výsledku

Groupby se sort=True řadí klíče, nikoli velikost průměru. Chceme-li nahoře nejvyšší průměr, použijeme až na hotový přehled sort_values. V úkolu při shodě průměru rozhoduje kód skupiny vzestupně, NaN je vždy na konci a reset_index(drop=True) dá nové pořadové číslování. To je samostatná prezentační volba, původní zdroje nemění.

## Váš úkol

Dokončete `statistiky_skupin(tabulka, klic, hodnota)`. Existující různé názvy vybírají str klíč a float64 hodnotu. Vraťte DataFrame se sloupci count, mean, min, max v tomto pořadí. Klíč bude index se jménem klic, skupiny vzestupně a chybějící skupina zahrnutá na konci. Count je int64, ostatní float64; prázdný vstup je platný. NaN v hodnotách vynechávejte a vstup neměňte.

Další úkoly procvičí vlastní názvy, různé hodnotové sloupce, dva klíče a pořadí přehledu. U každého sloupce dokážete vysvětlit, které vstupní řádky a hodnoty jej vytvořily.
