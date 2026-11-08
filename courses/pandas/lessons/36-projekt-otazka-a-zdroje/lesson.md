## Otázka před prvním výpočtem

Závěrečná Analytická dílna bude zkoumat vlastní smyšlená měření teplot z několika stanic. Otázka zní: jaké průměry mají známé stanice a kolik záznamů jsme odmítli nebo nedokázali spárovat? Není to předpověď počasí ani reprezentativní výzkum. Chceme dohledatelný postup, kterému rozumí i další člověk.

Lekce 36–42 tvoří jeden navazující projekt. Každý krok má vlastní možné řešení a přiložené ověřené předchozí funkce v predchozi.py. Můžete tedy pokračovat i bez kopírování kódu přes několik obrazovek. V editoru lze potom podklady nahradit vlastními dřívějšími řešeními, pokud splňují stejná rozhraní. Zde nepřidáváme nesouvisející varianty úkolů.

## Prostředí a zdroje

Použijte stejnou projektovou .venv jako dosud: `python tools/setup_env.py --courses pandas`. Potřebujeme pandas, pro pozdější graf Matplotlib a pro Excel openpyxl. VS Code, VSCodium a PyCharm vyberou tentýž interpreter. Soubory .py běží i bez okna a bez internetu; notebook je volitelný až v lekci 41. Ověřená kombinace: Python 3.14.8/pandas 3.1.1/Matplotlib 3.11.2/openpyxl 3.1.5.

Mereni.csv obsahuje den, textový kod stanice a teplota v °C, případně poznámku. Mista.csv mapuje jedinečný kod na nazev a oblast. Přečtěte přiložený datovy_slovnik.md: popisuje jednotky, význam řádku, chybějící údaje a pravidla. README vymezuje otázku a omezení zdroje. Oba dokumenty lze po běhu stáhnout, stejně jako CSV. V editoru je tlačítko pro pracovní soubor zkopíruje vedle reseni.py; v jiném editoru otevřete tuto složku ručně.

## Identifikátor není číslo

001 a NA jsou v tomto projektu skutečné textové kódy. Proto čteme dtype="str" a keep_default_na=False; výchozí převody by mohly ztratit nuly nebo považovat NA za neznámý údaj. Teplotu i datum nejprve ponecháme jako původní text, abychom později mohli vysvětlit odmítnutí.

```python
import pandas as pd
raw = pd.read_csv("mereni.csv", sep=";", encoding="utf-8", dtype="str", keep_default_na=False)
povinne = ["den", "kod", "teplota"]
print("Počet záznamů:", len(raw))
print("Jedinečné sloupce:", raw.columns.is_unique)
print("Povinné sloupce přítomné:", set(povinne).issubset(raw.columns))
```

Sep určuje středník a encoding UTF-8. Len vrátí počet datových záznamů, nikoli počet fyzických řádků textu: uvozovaný nový řádek může být uvnitř jedné položky CSV. Columns.is_unique ověří jedinečnost názvů. Set vytvoří množinu požadovaných názvů a issubset zjistí, zda nechybí žádný z nich; pořadí neřeší. Další poznámkový sloupec je v pořádku.

## Schéma a platné hodnoty jsou různé kontroly

Přítomnost sloupce teplota ještě neznamená, že je každá hodnota číselná. Tady ověříme jen strukturu; datumy a čísla posoudíme v dalším kroku. Ani prázdná tabulka se správnými sloupci není chyba schématu. Dva stejně pojmenované sloupce ale dělají výběr nejednoznačným, proto je odmítneme.

## Váš úkol

Dokončete `over_schema(tabulka, povinne)`. Vraťte bool: True jen pro DataFrame s jedinečnými názvy sloupců, který obsahuje všechny položky seznamu povinne. Další sloupce dovolte, nevyžadujte řádky ani stejné pořadí názvů. U jiného typu než DataFrame vraťte False. Typ zjistí isinstance(tabulka, pd.DataFrame). Tabulku ani seznam neměňte.

Zkuste chybějící název, jiný výběr povinných polí a prázdnou tabulku. Pod úkolem je možné řešení; kontrola nevyžaduje konkrétní zápis podmínky.
