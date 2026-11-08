## Popisek drží hodnotu u správného místa

Při aritmetice Series jsme zjistili, že pandas pracuje s indexem, nikoli jen s pořadím. Teď dostaneme seznam míst, pro která chceme přehled, i když některá měření chybí. `serie.reindex(popisky)` vrátí Series právě podle nového seznamu. Existující popisek dostane svou hodnotu, nový popisek NaN. Pořadí určuje seznam a může obsahovat i opakování.

Na rozdíl od loc reindex umí vytvořit místo pro dosud neexistující popisek. Zdrojový index však v našem úkolu musí být jedinečný, aby bylo jasné, kterou hodnotu použít. Reindex sám nesčítá a neodstraňuje původní NaN. Pokud popisek není v požadavku, do výsledku se nedostane.

## Připojení tabulek pod sebe

```python
vsechny = pd.concat([prvni, druha], ignore_index=True)
```

Concat dostane seznam objektů a výchozím směrem připojí jejich řádky pod sebe. Nejprve jsou všechny řádky první tabulky, potom druhé. Ignore_index=True vytvoří nový RangeIndex od nuly; původní kolidující čísla ani názvy řádků se nepoužijí. Sloupce se zarovnají podle názvů, nikoli podle pozice. V úkolu mají obě tabulky stejné schéma, takže typy zůstávají stejné.

Concat neodstraňuje duplicity a neověřuje, zda je každý záznam jedinečný. To je samostatné rozhodnutí z lekce 14. Stejně vypadající řádek může být další platný prodej a nesmí zmizet jen při připojování dat.

## Vedle sebe podle indexu

`pd.concat([prvni, druha], axis=1, join="outer")` připojí sloupce vedle sebe a řádky zarovná podle jejich indexových popisků. Outer znamená sjednocení popisků: místo přítomné jen v jedné tabulce nezmizí, druhá strana tam bude mít NaN. V úkolu pak sort_index seřadí výsledné textové popisky. Obě tabulky mají jedinečné indexy a různé názvy sloupců, aby byl výsledek jednoznačný.

Změna axis tedy mění i to, která druhá osa se zarovnává. Při připojení řádků se zarovnávají sloupce, při připojení sloupců řádky. Kdybychom index zahodili před spojením vedle sebe, mohli bychom přidat večerní teplotu jinému místu.

## Průnik není sjednocení

`pd.concat([prvni, druha], join="inner", ignore_index=True)` připojí řádky, ale ponechá jen společné sloupce. Jejich pořadí určí první tabulka. Pokud není společný žádný sloupec, výsledkem může být tabulka s řádky, ale bez datových sloupců; počet řádků se přesto sčítá. Není to stejné jako merge podle společného hodnotového klíče, které přijde v další lekci.

U dvou Series může concat zachovat původní indexy. V posledním úkolu proto ignore_index nepoužijeme: opakovaný popisek zůstane opakovaný a pořadí se nemění. Takový výsledek už nemusí splňovat předpoklad jedinečného indexu pro další reindex; pravidla indexu průběžně kontrolujeme.

## Váš úkol

Dokončete `zarovnej_mereni(serie, popisky)`. Vstup je float64 Series s jedinečným textovým indexem bez názvu a libovolným name. Vraťte hodnoty podle seznamu popisků, nové popisky jako NaN, zachovejte name a float64. Seznam může být prázdný nebo opakovat popisek. Původní Series ani seznam neměňte.

Další úkoly procvičí připojování řádků, sloupců, průnik sloupců a Series se zachovanými popisky. U každého výsledku zkontrolujte počet řádků, počet sloupců a to, která osa určila přiřazení hodnot.
