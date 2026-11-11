## Chybí hodnota, nebo je jen prázdná?

V SQLite NULL znamená chybějící údaj. Není to nula, prázdný text ani text 'NULL'. Běžné porovnání s NULL nevrací jednoduše ano/ne, ale opět NULL, tedy neznámý výsledek. WHERE ponechá jen řádky s pravdivou podmínkou.

```python
import sqlite3
from contextlib import closing
with closing(sqlite3.connect(':memory:', autocommit=True)) as con:
    print(con.execute("SELECT NULL = NULL, NULL IS NULL, COALESCE(NULL, 'chybí')").fetchone())
```

Výsledek je (None, 1, 'chybí'). IS NULL je správná otázka na chybějící hodnotu. COALESCE vybírá první hodnotu, která není NULL; hodí se pro zobrazení náhradního textu a samotná data nemění.

## Dva rozdílné způsoby hledání

Instr hledá doslovný podřetězec. LIKE přijímá vzor: % znamená libovolnou posloupnost a _ jeden znak. Parametrizace zachová strukturu příkazu, ale zástupné znaky uvnitř vzoru zůstávají zástupnými. Proto jsou doslovné hledání a hledání vzorem dvě odlišná zadání.

Výchozí LIKE rozlišuje ASCII a ostatní Unicode jinak. Není to nástroj pro úplné české porovnávání bez velikosti písmen. V této lekci nebudeme měnit PRAGMA case_sensitive_like ani vymýšlet vlastní kolaci.

## Co znamená typová afinita

SQLite popisuje skutečný uložený typ přes typeof: null/integer/real/text/blob. Běžná tabulka může hodnotu podle afinity sloupce převést. INTEGER tak může změnit text '003' na celé 3, zatímco sloupec bez uvedeného typu jej nechá jako text. Poslední úkol tento rozdíl změří přímo v enginu.

Pomocné schema.py obsahuje stejné definice z lekce 2, podklady.py jen připraví vlastní čerstvá data. Funkce s předaným con nezavírají spojení a neukončují transakci volajícího.

## Váš úkol

Vytvořte **bez_poznamky(con)**. Z tabulky udalosti vrátí seznam (id, popis) pouze tam, kde je poznamka NULL, v pořadí id. Prázdný text ani doslovný text 'NULL' se za chybějící hodnotu nepovažují. Použijte skutečný SQL dotaz.

Spojení dostáváte od volajícího, nezavírejte ho a nevolejte commit/rollback. To platí pro všechny čtecí funkce tohoto bloku. Výchozí row_factory je None, výsledné řádky jsou n-tice.
