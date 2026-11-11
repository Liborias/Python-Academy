## Výsledek dotazu má tvar i pořadí

SELECT vybírá sloupce, FROM tabulku a WHERE podmínku. ORDER BY určuje pořadí, na které se může program spolehnout. Bez něj databáze neslibuje pořadí vložení ani pořadí id.

```python
import sqlite3
from contextlib import closing
with closing(sqlite3.connect(':memory:', autocommit=True)) as con:
    con.execute('CREATE TABLE jmena (nazev TEXT)')
    con.executemany('INSERT INTO jmena VALUES (?)', [('Šachy',), ('Lana',), ('Míče',)])
    print(con.execute('SELECT nazev FROM jmena ORDER BY nazev').fetchall())
    print(con.execute('SELECT nazev FROM jmena WHERE nazev = ?', ('Neexistuje',)).fetchone())
```

První řádek vrátí [('Lana',), ('Míče',), ('Šachy',)], druhý None. Obyčejné řazení textu v SQLite není české slovníkové řazení; v našem příkladu se pořadí jen shoduje s očekávaným.

## Fetchone a fetchall

`fetchone` vezme příští řádek, nebo None, pokud už žádný není. `fetchall` vezme všechny zbývající řádky jako seznam; prázdný výsledek je []. Vyčtený kurzor už stejné řádky znovu neposkytne. Vracení hotového seznamu zároveň oddělí výsledek od další práce s kurzorem.

V úkolech 1–3 a 5 dostáváte standardní spojení s výchozím row_factory=None, které vrací n-tice. Úkol 4 výslovně zkouší i spojení se sqlite3.Row a vytváří vlastní slovníky. Tvar výsledku proto posuzujeme spolu s nastavením spojení.

V zadáních uvádíme id, nazev, kusy výslovně. SELECT * závisí na všech sloupcích a jejich aktuálním pořadí; výslovný výběr tvoří srozumitelnější rozhraní funkce. Minimum ve WHERE zůstává parametrem stejně jako hodnoty při vkládání.

## Pojmenované sloupce a stránkování

`sqlite3.Row` umožňuje pojmenovaný přístup a lze ho převést na obyčejný slovník. Pro jeden dotaz nastavíme row_factory lokálního kurzoru; con.row_factory patří i dalším částem programu a nemáme ho bezdůvodně měnit.

LIMIT vybere nejvýše určitý počet, OFFSET vynechá řádky na začátku. Vždy je spojte s jednoznačným pořadím. V tomto úvodu se mezi stránkami data nemění; stabilitu stránek v měnících se datech řešíme později.

Čtecí funkce nic nepotvrzují ani nevracejí rollback a neuzavírají předané spojení. I nechtěný commit při čtení by mohl uložit cizí rozepsanou práci.

## Váš úkol

Vytvořte **vypis_pomucky(con)**. SQL dotazem vrátí seznam n-tic (id, nazev, kusy), řazený podle nazev vzestupně a pak id. Prázdná tabulka vrátí [].

Použijte výslovný seznam sloupců a ORDER BY. Bez něj pořadí není součást slibu databáze. Základní řazení textu v SQLite není české slovníkové řazení a rozlišuje velikost písmen. Spojení, jeho nastavení i cizí rozepsané změny zachovejte.
