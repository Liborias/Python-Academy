## Export je nové rozhodnutí o formátu

CSV neuchovává datové typy tabulky. Ukládá text, oddělovače a uvozování. Příjemce proto potřebuje vědět, jak je číst. Naše dohoda je UTF-8, středník mezi sloupci a desetinná čárka. Zdrojové soubory necháme a výstup uložíme pod jiným názvem.

```python
from pathlib import Path
import pandas as pd
data = pd.read_csv("data.csv", sep=";", decimal=",", encoding="utf-8",
                   keep_default_na=False, dtype={"kod":"str", "nazev":"str", "hodnota":"float64"})
cesta = Path("vystup.csv")
data.to_csv(cesta, sep=";", decimal=",", encoding="utf-8", index=False)
print(cesta.read_text(encoding="utf-8"))
```

Path představuje cestu. To_csv vytvoří soubor, případný existující soubor pod stejným názvem přepíše. Sep určuje oddělovač, decimal zápis desetinných čísel a encoding kódování. `index=False` výslovně vynechá řádkové popisky. Bez něj by vznikl další sloupec, který se při dalším čtení snadno zamění za data. Hlavičku názvů datových sloupců naopak zachováme i u prázdné tabulky.

## Uvozování nepíšeme obyčejným join

Název může obsahovat středník, uvozovky nebo nový řádek. To_csv je podle potřeby uzavře do uvozovek a vnitřní uvozovky ošetří. Obyčejné spojení polí středníkem by mohlo změnit počet sloupců či řádků. Správný CSV čte parser, ne prosté split(";") na každém fyzickém řádku. Nový řádek uvnitř uvozovaného pole pořád patří k jednomu datovému záznamu.

## Text v paměti a výběr sloupců

Když to_csv nezadáme cestu, vrátí Unicode str s CSV. To se hodí pro kontrolu nebo další zpracování bez vytváření souboru. Kódování se vybírá až při převodu textu na bajty; proto zde nepřidáváme BOM.

`tabulka[sloupce].to_csv(...)` vybere přesně sloupce ze seznamu a jejich pořadí, zatímco původní tabulku nemění. Neexportovat index není totéž jako zahodit důležitý datový sloupec kod: ten v tabulce zůstává.

## UTF-8 BOM a automatické otevření v Excelu

Encoding="utf-8-sig" přidá na začátek souboru značku BOM. Ta některým verzím tabulkových programů pomůže rozpoznat UTF-8. Neurčuje však oddělovač ani typ sloupce. Excel může při automatickém otevření CSV dál považovat 001 za číslo; při importu proto zvolte pro kod text. V programu čteme s dtype kod str a keep_default_na=False, aby se neztratily nuly ani doslovné NA. Pro výměnu CSV si předem dohodněte kódování, oddělovač i typy; samotná přípona to neříká.

## Ověřit obsah, ne jen existenci souboru

Po exportu CSV znovu načteme podle stejné dohody a porovnáme s původními daty. `tabulka.reset_index(drop=True)` jen sjednotí index pro porovnání, neukládá tuto změnu do zdroje. `pd.testing.assert_frame_equal` ověří tabulky; při rozdílu vyvolá AssertionError. Check_exact=False a rtol/atol=1e-12 dovolí malý rozdíl při desetinné aritmetice, texty a pořadí přesto musí souhlasit. Try/except v Úkolu 5 převede zjištěný rozdíl či neplatné schéma na False; úspěch na True. Existence souboru není důkazem správných hodnot.

## Váš úkol

Tabulka má kod/nazev str a hodnota float64 bez chybějících hodnot, libovolný řádkový index. Text může obsahovat středník, uvozovky, nový řádek, diakritiku i doslovné NA. Uložte skutečné UTF-8 CSV bez BOM, se středníkem, desetinnou čárkou, hlavičkou a bez indexu. Zachovejte pořadí/kódy; prázdná tabulka má stále hlavičku. Rodič cesty existuje, vraťte Path stejné cesty a tabulku neměňte.

Dokončete `uloz_csv(tabulka, cesta)`.

Další úkoly vytvoří CSV text, vyberou pořadí sloupců, přidají BOM a ověří hotový soubor. V aplikaci stáhněte výsledek z panelu Soubory CSV a Excel; uvidíte tam i přiložený vstup data.csv. Po reloadu odkazy znovu vzniknou spuštěním kódu. V editoru soubory najdete v pracovní složce procesu. Kontroly zkoušejí skutečné bajty, diakritiku, nulové kódy, speciální znaky i prázdnou tabulku.
