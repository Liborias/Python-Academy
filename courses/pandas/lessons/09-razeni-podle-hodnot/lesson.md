## Řadíme hodnoty, nikoli názvy řádků

Sort_index z prvního modulu řadil popisky. `tabulka.sort_values(by="cena")` řadí celé řádky podle hodnot ceny. Ostatní hodnoty v řádku se přesunou spolu s ní. Index zůstává původní, takže nejlevnější položka může mít stále popisek V nebo číslo 17. Řazení neznamená nové očíslování.

Argument by pojmenuje sloupec. `ascending=True` znamená vzestupně, False sestupně. Tyto hodnoty jsou bool, nikoli texty "True" a "False". Pro číselné sloupce můžeme mluvit o nejnižší ceně nebo nejvyšším počtu. Technické řazení textu není automaticky české slovníkové řazení; v úkolech řadíme čísla.

## Shody a chybějící hodnoty

```python
prehled = tabulka.sort_values(
    by="cena", ascending=True, kind="stable", na_position="last"
)
```

Kind volí způsob řazení. Stable při shodné hodnotě zachová původní pořadí těchto řádků. To je důležité například u dvou čajů se stejnou cenou: bez výslovného pravidla by nebylo jasné, který bude první. Na_position="last" posune NaN na konec i při sestupném řazení. Volba "first" je naopak umístí na začátek. Chybějící cena tím nezíská nulovou cenu.

Stejně funguje sort_values na Series, jen nepředáváme by: řadí své hodnoty a zachová name i spojení s popisky. V posledním úkolu požadujeme NaN na začátku; čtěte proto konkrétní zadání, nespoléhejte na výchozí nastavení. Řazení bez inplace vrací výsledek a vstup nemění.

## Dva klíče

`tabulka.sort_values(by=["cena", "kusy"], ascending=[True, False], na_position="last")` řadí nejprve cenu vzestupně. Teprve při stejné ceně porovná kusy sestupně. Druhý klíč tedy nepřeváží rozdílnou cenu. Seznam směrů odpovídá seznamu klíčů na stejných pozicích. NaN je poslední v rámci každého klíče. V úkolu jsou dvojice klíčů jedinečné, takže neřešíme úplnou shodu obou hodnot. Parametr kind se u DataFrame uplatňuje pro řazení podle jediného sloupce; pravidlo pro dva klíče vyjadřujeme jejich seznamem a směry.

## Nejprve seřadit, potom zkrátit

Nejlevnější dvě položky získáme seřazením a teprve potom head(2). Samotné head vybere první řádky v aktuálním pořadí, nehledá minimum. Head(0) dává prázdný výsledek; head s příliš velkým počtem vrátí všechny řádky. V tomto úkolu zůstávají chybějící ceny na konci a mohou se do dostatečně dlouhého výsledku dostat také.

Pokud opravdu chceme nové pořadové číslo, použijeme `prehled.reset_index(drop=True)`. Reset_index vytvoří výchozí RangeIndex od nuly bez názvu; drop=True zahodí staré popisky, nepřidá je jako další datový sloupec. Hodnoty ani aktuální pořadí řádků se nezmění. Před odhozením indexu si vždy rozmyslete, zda jej nepotřebujete jako identifikátor. V našich dalších úkolech se původní index obvykle zachovává.

## Váš úkol

Dokončete `serad_tabulku(tabulka, sloupec, vzestupne)`. Sloupec existuje, je číselný a může obsahovat NaN; vzestupne je bool. Vraťte DataFrame řazený podle jeho hodnot v požadovaném směru, při shodě stabilně a s NaN vždy na konci. Zachovejte index i sloupce, vstup neměňte. Prázdná tabulka je platná.

Další zadání procvičí dva klíče, nejlevnější položky, nový index a řazení Series. Zkuste dvě shodné hodnoty a NaN; na nich poznáte, zda řazení odpovídá zadání.
