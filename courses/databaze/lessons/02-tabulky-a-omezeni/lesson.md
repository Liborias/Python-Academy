## Řádky potřebují společná pravidla

Tabulka je pojmenovaná sada řádků se sloupci. Pro klubovní sklad potřebujeme identifikátor, název a počet kusů. CREATE TABLE pravidla připraví; zatím nevkládá samotné pomůcky.

```sql
CREATE TABLE IF NOT EXISTS pomucky (
    id INTEGER PRIMARY KEY,
    nazev TEXT NOT NULL UNIQUE,
    kusy INTEGER NOT NULL DEFAULT 0 CHECK (kusy >= 0)
);
```

INTEGER PRIMARY KEY v SQLite umožní doplnit jedinečné celočíselné id, pokud ho nevložíme sami. Není nutné přidávat AUTOINCREMENT: ten řeší další pravidla opakovaného použití dřívějších id. Název má být TEXT, NOT NULL zakazuje chybějící hodnotu a UNIQUE stejný název podruhé.

DEFAULT 0 doplní kusy, když sloupec při INSERT vynecháme. Výslovné NULL se za výchozí nulu nenahradí. CHECK odmítne záporný počet; samo by ale NULL nezakázalo, proto je důležité i NOT NULL.

## Typová afinita není úplná validace

Běžná SQLite tabulka používá typové afinity a může některé předané hodnoty převádět. Tato zadání pracují s celočíselnými počty; INTEGER zde není slib, že každý libovolný Python objekt bude automaticky odmítnut. Přísnější režim a chování typů probereme při rozšíření SQL.

```python
import sqlite3
from contextlib import closing
with closing(sqlite3.connect(':memory:', autocommit=True)) as con:
    con.execute('CREATE TABLE pokus (id INTEGER PRIMARY KEY, poznamka TEXT)')
    con.execute('INSERT INTO pokus DEFAULT VALUES')
    print(con.execute('SELECT id, poznamka FROM pokus').fetchone())
```

Výsledek (1, None) ukazuje automatické id a chybějící poznámku. None není prázdný text. SQLite své chyby pravidel ohlásí jako sqlite3.IntegrityError.

## Opakovatelná příprava

IF NOT EXISTS znovu nevytvoří již existující tabulku. Zachová její data, ale také neopraví staré jiné schéma. Pozdější změnu struktury musíme navrhnout zvlášť. Nepoužívejte DROP TABLE jako běžnou součást vytvoření, smazal by i data.

Funkce této lekce dostávají con od volajícího. Připraví tabulku a vrátí None; neuzavírají spojení a nevolají commit/rollback. Volající tak může celou přípravu potvrdit či vrátit. S autocommit=True se jednotlivý CREATE potvrdí sám.

## Váš úkol

Vytvořte **vytvor_pomucky(con)**. Připraví tabulku pomucky s id INTEGER PRIMARY KEY, nazev TEXT NOT NULL UNIQUE a kusy INTEGER NOT NULL DEFAULT 0 CHECK (kusy >= 0). Použijte CREATE TABLE IF NOT EXISTS, aby opakované volání zachovalo data.

Id se má automaticky doplnit, pokud ho při vložení neuvedeme. Název nesmí být NULL a nesmí se opakovat, počet celých kusů nesmí být záporný ani NULL a výchozí je nula. Funkce nic nevrací. Spojení a transakce vlastní volající: nevolejte close, commit ani rollback. U existující tabulky se schéma tímto příkazem neaktualizuje; nejde o migraci.
