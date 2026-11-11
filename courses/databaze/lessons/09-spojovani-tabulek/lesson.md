## Spojujeme související údaje

JOIN připojí k řádku odpovídající údaje jiné tabulky. INNER JOIN vrátí jen shody. LEFT JOIN zachová každý řádek levé tabulky, i když vpravo nic nenajde; pravé sloupce jsou pak NULL.

```python
import sqlite3
from contextlib import closing
with closing(sqlite3.connect(':memory:', autocommit=True)) as con:
    con.execute('CREATE TABLE leve (id INTEGER)')
    con.execute('CREATE TABLE prave (id INTEGER)')
    con.execute('INSERT INTO leve VALUES (1)')
    print(con.execute('SELECT l.id, p.id FROM leve AS l LEFT JOIN prave AS p ON l.id=p.id').fetchall())
```

Výsledek [(1, None)] vysvětluje i častou chybu v souhrnech. COUNT(*) po levém spojení napočítá řádek i u prázdné kategorie. COUNT(p.id) naopak počítá jen skutečné pomůcky.

## Počet řádků je součást významu

Kategorie může mít více pomůcek, pomůcka více výpůjček. Spojení s výpůjčkami tak může pomůcku zopakovat. Součet kusů po takovém spojení by mohl být násobný. Neřešte to slepým DISTINCT, který by zase mohl ztratit různá půjčení stejné pomůcky.

Pro otázku „nemá žádnou aktivní výpůjčku“ použijeme NOT EXISTS. Vnořený dotaz je navázaný na právě zkoumané p.id. Hledá existenci aktivního řádku, ne seznam všech vrácených půjčení. Pomůcka s jedním aktivním a jedním vráceným řádkem stále aktivní výpůjčku má.

Cvičné tabulky a vazby odpovídají lekci 8. Schéma a SQL funkce z předchozí lekce jsou přiložené beze změny definic. Výchozí row_factory=None, explicitní sloupce/pořadí, žádné potvrzení cizí transakce.

## Váš úkol

Vytvořte **pomucky_s_kategorii(con)**. INNER JOIN pomucky a kategorie vrátí (id_pomůcky, název, kusy, název_kategorie), v pořadí id pomůcky. Nezařazené pomůcky se v tomto konkrétním výběru neobjeví.

Spojujte pomocí p.kategorie_id=k.id, ne podle shody textových názvů. Tabulkové aliasy p/k zkrátí zápis a rozliší stejně pojmenované sloupce. Vstup má výchozí row_factory=None. Spojení/transakci neukončujte.
