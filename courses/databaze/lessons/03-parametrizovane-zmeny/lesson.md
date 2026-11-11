## Příkaz má strukturu, hodnoty mají vlastní místo

INSERT přidá řádek, UPDATE změní vybrané řádky a DELETE je odstraní. Základní pravidlo je stejné: názvy tabulek a sloupců patří do pevného textu SQL, konkrétní hodnoty předáváme odděleně.

```python
import sqlite3
from contextlib import closing
with closing(sqlite3.connect(':memory:', autocommit=True)) as con:
    radek = con.execute('SELECT :a + :b', {'a': 2, 'b': 3}).fetchone()
    print(radek[0])
```

Výstup 5 ukazuje pojmenované parametry. V ukázkách použijeme také otazníky a n-tici hodnot. SQLite zajistí předání typu i apostrofů; jméno O'Neil nepotřebuje vaše ruční nahrazování uvozovek.

Skládat SQL z uživatelského textu přes f-string by dovolilo změnit význam příkazu. V našich pokusech text podobný příkazu uložíme jako obyčejný název. Zástupné ? je pro hodnotu, ne pro název tabulky nebo sloupce.

## Co vrací kurzor

Po INSERT je lastrowid identifikátor právě vloženého řádku. Není to počet pomůcek a nemusí odpovídat počtu řádků, protože id mohou mít mezery. Po UPDATE/DELETE použijeme rowcount. UPDATE přiřazující stejnou hodnotu počítá v SQLite také nalezený řádek.

`executemany` opakuje jeden příkaz nad více sadami parametrů, může je číst z generátoru. Samo ale neznamená transakci celé dávky. Když třetí řádek selže, dřívější mohly být provedené. V lekci 5 z nich uděláme jeden celek.

## Který konflikt chceme ošetřit

ON CONFLICT(nazev) DO NOTHING řeší právě jedinečný název. Nesmí tiše zamést pod koberec záporný počet nebo chybějící název. Vlastní chybu SQLite zatím předáváme volajícímu, který rozhodne o zprávě nebo rollback.

Schema.py obsahuje přesné funkce z předchozí lekce a podklady.py připraví vlastní cvičná data. Pomocné funkce sami nevytvářejí spojení, nevynucují commit a nemažou existující řádky. Vaše funkce přebírají již otevřené con a neukončují ho.

## Váš úkol

Vytvořte **pridej_pomucku(con, nazev, kusy)**. Parametrizovaným INSERT vloží záznam do pomucky a vrátí skutečné id nového řádku. Id nezadáváme ručně, získáte ho z lastrowid vráceného kurzoru.

Všechny hodnoty zachovejte přesně, včetně apostrofů a mezer. Neměňte jiné řádky. Chybu pravidel tabulky nechte jako sqlite3.IntegrityError projít volajícímu. Spojení nezavírejte a sami nevolejte commit/rollback; hranici transakce zatím určuje volající.
