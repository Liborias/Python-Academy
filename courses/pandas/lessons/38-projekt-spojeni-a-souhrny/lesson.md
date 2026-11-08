## Platné měření nemusí mít známou stanici

Čistá data mají správný datum i teplotu, ale kod 999 není v katalogu. Vynechat jej bez záznamu by zastřelo původ výsledku. Left merge s indikátorem zachová levé řádky a dovolí oddělit spárované od nespárovaných. Katalog se má chovat jako jednoznačný číselník, ne rozmnožovat měření.

```python
import pandas as pd
from predchozi import vycisti_mereni
raw = pd.read_csv("mereni.csv", sep=";", encoding="utf-8", dtype="str", keep_default_na=False)
mista = pd.read_csv("mista.csv", sep=";", encoding="utf-8", dtype="str", keep_default_na=False)
cista = vycisti_mereni(raw)["cista"]
spoj = cista.merge(mista, on="kod", how="left", sort=False,
                    validate="many_to_one", indicator=True)
print(spoj[["radek", "kod", "nazev", "_merge"]])
```

On označuje hodnotový klíč kod. How="left" ponechá všechna čistá měření, sort=False jejich pořadí. Validate="many_to_one" dovolí opakované levé kódy, ale vyžaduje jedinečný pravý kod; duplicitní katalog vyvolá pd.errors.MergeError. Platí to i pro duplicitní stanici, kterou právě žádné měření nepoužívá. Nesmíme nejednoznačnost potichu opravit drop_duplicates.

Indicator vytvoří kategorii _merge. Both je skutečně spárovaný řádek, left_only chybějící protějšek. Nemícháme tuto informaci s chybějící hodnotou některého jiného sloupce. V našem katalogu jsou kod/nazev/oblast známé neprázdné texty, kod je jedinečný nebo se jeho nejednoznačnost odmítne.

## Výsledek podle stanice a podle dne

Po rozdělení vytvoříme souhrn ze spárovaných pozorování. Groupby podle dvojice kod/nazev vrátí pocet a prumer. Dvě různá místa se mohou jmenovat stejně; samotný název tedy není bezpečný identifikátor. Sort=True určí vzestupné pořadí klíčů, as_index=False ponechá klíče ve sloupcích. Size počítá záznamy, mean průměr jejich teplot. Nuly a záporné teploty normálně zahrneme.

Druhý souhrn použije den. Nevyrábíme chybějící kalendářní dny ani je nevyplňujeme nulovou teplotou. Počet je int64, průměr float64; prázdný vstup nebo žádný známý kód dá prázdné přehledy se správnými sloupci a typy. Průměr není součet teplot a pozdější celkový průměr nemá být průměrem nerovně velkých skupin.

## Váš úkol

Dokončete `spoj_a_shrn(cista, mista)`. Cista má formát z lekce 37. Vraťte čtyři DataFrame ve slovníku:

- Spojena: radek, den, kod, teplota, nazev, oblast; pouze spárované v levém pořadí.
- Nesparovana: radek, den, kod, teplota; pouze neznámé kódy v levém pořadí.
- Podle_mist: kod, nazev, pocet int64, prumer float64; řazení podle kod/nazev.
- Podle_dnu: den datetime64[us], pocet int64, prumer float64; řazení podle dne.

Klíče slovníku pište malými písmeny podle šablony: spojena, nesparovana, podle_mist, podle_dnu. Všechny tabulky mají RangeIndex. Vstupy zachovejte i při MergeError; chybné sloupce katalogu odmítněte ValueError. Katalog může být prázdný s hlavičkami, jeho známé texty neupravujte.

U vzoru je 6 spárovaných měření a 1 nespárované (pořadí 5, kod 999). Souhrny podle kódu: 001 má 3 měření a průměr 28/3, 010 má 2 a průměr 1, NA má 1 a průměr -2 °C. Nevyužitou stanici 777 nevymýšlíme jako nulové měření.
