## Odkaz místo opakovaného názvu

Kategorie bude mít vlastní id a jedinečný název. Pomůcka si uloží kategorie_id, výpůjčka pomucka_id. Přejmenování kategorie pak nemusí přepisovat názvy ve všech pomůckách. Cizí klíč zajišťuje, že každý odkaz kromě NULL vede na existující řádek.

```python
import sqlite3
from contextlib import closing
with closing(sqlite3.connect(':memory:', autocommit=True)) as con:
    con.execute('PRAGMA foreign_keys = ON')
    print('Vynucování vazeb:', con.execute('PRAGMA foreign_keys').fetchone()[0])
    con.autocommit = False
    print('Transakční režim:', con.autocommit)
```

PRAGMA foreign_keys se zapíná na každém spojení zvlášť. Začít v autocommit=False by už otevřelo transakci a pozdější zapnutí by se neprojevilo. Proto nejprve True, zapnutí/ověření, potom False. Nový soubor sám zapnutí pro příští spojení nezapamatuje.

## Jak se zachová mazání

ON DELETE SET NULL u kategorie_id zachová pomůcku, jen ji odpojí od kategorie. Kategorie je volitelná, proto tento sloupec není NOT NULL. ON DELETE RESTRICT u pomucka_id nedovolí smazat pomůcku, na kterou odkazuje historie. Platí to i po vrácení výpůjčky.

Nové schéma má tři tabulky: kategorie(id,nazev), pomucky(id,nazev,kusy,kategorie_id), vypujcky(id,pomucka_id,clen,vraceno). Kusy jsou aktuálně dostupné množství. Vrácení je 0/1 a nové půjčení začíná na 0.

CHECK u kusy nově vyžaduje typeof(kusy)='integer' a nezápornost. Platí pro uloženou hodnotu po afinitě; API projektu ještě zvlášť ověří původní Python počet. NOT NULL řeší chybění, CHECK pravidlo hodnoty.

## Nové schéma je nový pokus

Připravené funkce používají relační schéma v čerstvé databázi. Staré soubory z lekcí 1–5 se automaticky nemění. CREATE IF NOT EXISTS není migrace a staré sloupce sám nedoplní. Pro projekt použijeme nový klub.sqlite3.

Vytvoření/změny s předaným con nechají transakci volajícímu. Jen spojeni_s_vazbami vytváří nové spojení, které pak musí zavřít jeho nový vlastník.

## Váš úkol

Vytvořte **spojeni_s_vazbami(cesta)**. Otevře nové spojení s autocommit=True, zapne PRAGMA foreign_keys=ON a dotazem PRAGMA foreign_keys ověří 1. Pak nastaví con.autocommit=False a vrátí živé spojení volajícímu.

Pokud se příprava nepodaří, vlastní spojení zavřete a chybu předejte. Pokud ověření vrátí jinou hodnotu než 1, vyvolejte RuntimeError. Začít rovnou s autocommit=False a teprve pak zapnout vazby nestačí: PRAGMA uvnitř aktivní transakce se neprojeví. Platí pro paměť i soubor a pro každé nové spojení zvlášť.
