## Stejný počet řádků není samozřejmost

Jestliže má prodej dva odpovídající řádky v ceníku, merge vytvoří dvě spárované kombinace. Když se klíč opakuje na obou stranách, počet může růst násobením. Následný součet tržby pak vypadá jako běžný výpočet, ale započítává zmnožené položky. Nejdřív proto pojmenujeme očekávaný vztah tabulek.

`validate="many_to_one"` dovoluje mnoho levých řádků pro produkt, ale vyžaduje nejvýše jeden pravý řádek pro tento klíč. `validate="one_to_one"` vyžaduje jedinečnost na obou stranách. Použít lze také zkratky m:1 a 1:1. Při porušení merge vyvolá `pd.errors.MergeError`. V těchto úkolech se nesmí chyba zamést pod koberec automatickým drop_duplicates; zdrojovou nejednoznačnost má zpracovatel skutečně zjistit.

```python
spojene = prodeje.merge(
    cenik, on="produkt", how="left", sort=False, validate="many_to_one"
)
```

Kontroluje se celý pravý klíč, i když duplicitní produkt právě není mezi prodeji. Jedinečnost je předpoklad ceníku jako zdroje, ne jen náhoda současného výběru. Validate neznamená, že každý levý klíč najde protějšek; na to potřebujeme další kontrolu. Ani při odmítnutí vstupní tabulky neměníme.

## Outer a indikátor původu

Outer spojení vrátí sjednocení klíčů z obou tabulek. V úkolech je řadíme vzestupně a používáme nový RangeIndex. `indicator=True` přidá sloupec _merge se třemi štítky: left_only, right_only a both. Ukáže, zda klíč pochází jen zleva, jen zprava nebo se spároval na obou stranách.

Indikátor má typ categorical: používá pevnou sadu těchto tří kategorií. Pro výběr stačí porovnání s textem, například `spojene["_merge"] == "left_only"`. Není potřeba jej převádět na číslo. Ve vstupech sloupec _merge nesmí kolidovat s naším novým indikátorem; úkoly tuto podmínku zaručují.

## Chybějící cena není totéž co chybějící produkt

Ceník může mít produkt s neznámou cenou NaN. Po spárování je cena stále NaN, ale klíč existuje a indikátor má both. Filtr cena.isna by proto nesprávně smíchal chybějící protějšek s chybějící hodnotou známého produktu. V úkolu s nespárovanými prodeji vracíme jen původní prodejní sloupce těch řádků, které mají left_only, v původním pořadí a s novým indexem.

Pandas navíc může spárovat chybějící klíč s chybějícím klíčem, což se liší od běžného očekávání ze SQL NULL. Nevykládáme takové spárování automaticky jako správný produkt. Zdejší úkoly mají neprázdné známé klíče; ukázka tento rozdíl záměrně demonstruje. U vlastních dat musíme předem stanovit, co s neznámými identifikátory uděláme.

## Dva stavy s jiným významem

V objednávce může stav znamenat zaplaceno a ve skladu dostupnost. Nechceme jeden z nich zahodit. `suffixes=("_objednavka", "_sklad")` při merge pojmenuje překrývající se neklíčové sloupce stav_objednavka a stav_sklad. Pořadí dvojice odpovídá levé a pravé tabulce. Klíč zůstane jednou pod původním názvem.

## Váš úkol

Dokončete `overene_ceny(prodeje, cenik)`. Schéma je produkt str/kusy int64 a produkt str/cena float64 jako minule; klíče nechybějí, ale ceník může být nejednoznačný. Vraťte left spojení s RangeIndex, levým pořadím a sloupci produkt, kusy, cena. Pokud je v ceníku jakýkoli duplicitní produkt, vyvolejte MergeError. Opakované prodeje jsou platné, prázdné vstupy také. Vstupy zachovejte i při chybě.

Další úkoly procvičí vztah 1:1, indikátor, nespárované řádky a vlastní suffixes. Po spojení zkontrolujte význam klíče, počet řádků, nespárované položky a teprve potom součty.
