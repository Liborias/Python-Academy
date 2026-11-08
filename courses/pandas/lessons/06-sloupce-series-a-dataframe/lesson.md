## Stejná data, jiný tvar

V předchozím bloku jsme tabulku vytvořili a načetli ze souboru. Teď se chceme ptát jen na některé údaje. DataFrame má dvě osy: řádky a sloupce. Series má jednu osu. Rozdíl ovlivňuje další operace, proto patří typ výsledku do zadání stejně jako jeho hodnoty.

`tabulka["teplota"]` vybere jeden sloupec jako Series. Její index pochází z řádků tabulky, name z názvu sloupce a dtype z typu jeho hodnot. Například výběr teploty umožní vypočítat mean stejně jako v lekci 2. Zápis s názvem v hranatých závorkách funguje i pro sloupec s mezerou; nemusíme se spoléhat na tečkový zápis atributu.

## Proč někdy píšeme dvě hranaté závorky

```python
serie = tabulka["teplota"]
prehled = tabulka[["teplota"]]
vybrane = tabulka[["teplota", "misto"]]
```

První příkaz vybírá jeden název a vrací Series. Druhý předává seznam s jediným názvem, proto vrací DataFrame s jedním sloupcem. Vnější závorky znamenají výběr z tabulky, vnitřní vytvářejí Python seznam. Třetí příkaz vybírá dva sloupce v zadaném pořadí: teplota bude vlevo, i kdyby ve vstupu byla jinde. Pořadí řádků se nemění.

Prázdný seznam `tabulka[[]]` vrátí tabulku se stejným řádkovým indexem a žádnými sloupci. Není to totéž co tabulka bez řádků. U jedinečných vstupních názvů lze v seznamu název zopakovat a sloupec se zopakuje i ve výsledku. Neexistující název by vyvolal KeyError; naše zadání zaručují existující názvy.

## Názvy nejsou hodnoty

`tabulka.columns.tolist()` vytvoří běžný seznam názvů sloupců. Samotné columns je objekt Index; tolist převede popisky do seznamu. Hodnoty řádků se tím nečtou. Srovnejte jej s `tabulka.index.tolist()`, která by vracela popisky řádků.

`tabulka.rename(columns={"teplota": "teplota_c"})` vrátí tabulku s novým názvem sloupce. Argument columns určuje, kterou osu přejmenováváme. To se liší od přejmenování indexu a od name celé Series v prvním bloku. Hodnoty, jejich typy a pořadí zůstanou stejné. V úkolu nové názvy nekolidují s ostatními sloupci.

## Původní data si ponechte

Výběr a rename použité bez inplace původní tabulku neupravují. Ve vzoru používáme copy pro výslovnou kopii vybraných dat. V pandas 3 se změny odvozeného objektu řídí Copy-on-Write; podrobně si to vyzkoušíme v lekci 10. Žádný dnešní úkol nemá měnit předaný vstup. Není potřeba konkrétní postup kopírovat znak po znaku: rozhoduje výsledek podle zadání.

## Váš úkol

Dokončete `vyber_sloupec(tabulka, sloupec)`. Vstup je DataFrame s jedinečnými textovými názvy sloupců a název existujícího sloupce. Vraťte jej jako Series se stejným indexem, name, dtype a pořadím hodnot. Tabulka může být bez řádků, sloupec však existuje. Vstup neměňte.

Další úkoly procvičí seznam sloupců, jednosloupcový DataFrame, rename a seznam názvů. Před spuštěním si vždy řekněte, kolik os bude mít výsledek. Pod každým úkolem lze zobrazit jedno možné řešení.
