## Připravíme prostředí pro první databázi

SQLite ukládá data do běžného databázového souboru; nepotřebuje samostatně běžící server ani přihlášení. Python k němu přistupuje přes modul sqlite3 ze standardní knihovny. V prvním bloku nic dalšího neinstalujeme. Používáme Python 3.12 nebo novější kvůli výslovnému nastavení autocommit; ověřené prostředí je Python 3.14.8 a SQLite 3.53.1.

Ve VS Code, VSCodium nebo PyCharm otevřete složku projektu a vyberte stejnou .venv jako v terminálu. V hlavní Přípravě prostředí jsou kroky pro každý editor. Samotné rozšíření editoru není databázový stroj. Ověření lze spustit přímo v pracovním okně:

```python
import sys
import sqlite3
print('Používaný Python:', sys.executable)
print('SQLite:', sqlite3.sqlite_version)
```

První řádek výstupu ukáže konkrétní interpreter, druhý verzi SQLite, nikoli verzi Pythonu. Konzolové příklady fungují i bez grafické plochy a internetu.

## Co otevře connect

`sqlite3.connect`(cesta, autocommit=True) vrátí spojení Connection. Existující databázi otevře, chybějící soubor vytvoří, rodičovskou složku ale nevyrábí. Přípona .sqlite3 je zvyklost, ne podmínka. Nový soubor bez tabulek může mít zatím nulovou velikost.

Zvláštní cesta ':memory:' vytvoří databázi jen v paměti konkrétního spojení. Po jeho zavření data zmizí. Dvě taková spojení mají dvě nezávislé databáze. To je vhodné pro první pokusy, které nemají měnit vaše soubory.

## Od SQL příkazu k hodnotě

`execute` odešle text SQL stroji SQLite a vrátí Cursor. SELECT sqlite_version() vytvoří jeden výsledný řádek; fetchone ho převezme jako n-tici, například ('3.53.1',). Index 0 z ní získá samotný text. Nejde o číslo, se kterým bychom počítali.

Spojení vlastní ten, kdo ho otevřel. `closing` z contextlib zavolá při odchodu close i při chybě. Samotné with con není totéž: řeší potvrzení/vrácení transakce, ale spojení nezavře. Autocommit=True v úvodu ukládá jednotlivé úspěšné změny; skupinu změn probereme v lekci 5.

## Soubor, který zůstane mezi běhy

Ukázky používají paměť nebo dočasnou složku, po které se uklidí. Pro vlastní soubor uložte pracovní složku do editoru a předejte cestu vedle reseni.py, například pomocí Path a with_name. Běžné tlačítko Spustit v prohlížeči vytváří dočasnou kopii: není to trvalá paměť databáze. Při práci v editoru můžete projekt spustit příkazem python reseni.py.

## Váš úkol

Vytvořte **verze_databaze(cesta)**. Otevře skutečné SQLite spojení k předané cestě, SQL dotazem SELECT sqlite_version() získá verzi databázového stroje, spojení zavře a vrátí samotný text verze. Cesta může být Path, text souborové cesty nebo ':memory:'. Rodičovský adresář souboru už existuje.

SQLite při otevření vytvoří chybějící soubor. Existující tabulky ani data nemažte. Zjištění verze stroje samo není kontrola všech dat či správnosti schématu. Použijte například closing, aby se vlastní spojení zavřelo i při chybě. Import vašeho souboru nesmí databázi otevírat.
