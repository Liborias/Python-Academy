## Projekt musí jít spustit i odjinud

Aktuální pracovní adresář nemusí být složka programu. Výchozí vlastní DB proto odvodíme od souboru spouštěče, ne od cwd. Explicitní relativní --db naopak znamená cestu vůči aktuálnímu adresáři, jak je běžné v terminálu.

```python
# With_name vymění jméno souboru a zachová jeho rodičovskou složku.
from pathlib import Path
print(Path('projekt/app.py').with_name('pujcovna.sqlite3'))
```

Cesty nejprve pouze vypočítáme, bez vytváření složek či DB. Rodič už musí existovat. Absolutní --db pomůže navázat na záznamy v jiné uložené lekci. Půjčovna používá relační schéma z 10, nový projekt ale začněte novým pujcovna.sqlite3, jiné DB se nemigrují.

## Kopie databáze a čistá složka

Zálohu vytvoří Connection.backup, ne prosté kopírování otevřeného souboru. Funguje i z paměti. Cílové spojení s autocommit=True zavřeme, pak teprve helper nahradí cílový soubor. Chyba zachová starý cíl. Zdroj nesmí být cílem, ani přes shodný soubor/odkaz.

Před předáním spusťte testy. Předejte složku se všemi .py helpery a NAVOD.md, na druhém místě připravte novou .venv a vyberte ji v editoru i terminálu. Cizí .venv se nekopíruje. Vlastní *.sqlite3, *.sqlite3-wal, *.sqlite3-shm, .venv a __pycache__ běžně patří do .gitignore vlastního projektu, ne do veřejného repozitáře. Případná fiktivní data předávejte samostatně a pracujte s kopií. Není potřeba vytvářet ZIP.

## Váš úkol

Doplňte **cesty_projektu(soubor, db=None)** a **zaloha_projektu(model, cesta)**. Cesty vrátí {'koren': absolutní rodič souboru, 'db': absolutní Path databáze}. Bez db bude pujcovna.sqlite3 vedle souboru; zadanou db rozviňte expanduser a resolve vůči cwd. Výpočet nic nezapisuje.

Zaloha použije bezpecny_cil(cesta, model.cesta), připojí se k dočasnému souboru s autocommit=True, zavolá model.con.backup, spojení zavře a vrátí absolutní Path cíle. Chyby předává, starý cíl musí zůstat při neúspěchu. Veřejné metody modelu potvrzují celé operace; před backup nevkládejte do con jiné rozpracované změny.

V uložené dokončené složce:

```powershell
python spust_pujcovnu.py --help
python overeni.py
python spust_pujcovnu.py pridat "Míč" 2
python spust_pujcovnu.py prehled
python spust_pujcovnu.py zaloha kopie.sqlite3
```

Help nevytvoří DB, overeni.py provede šest izolovaných testů. Spouštěč používá vaše cesty/zálohu z reseni.py a hotový model z 28. DB vedle něj je vaše vlastní prázdná evidence, webová ukázka je dočasná. --db CESTA patří před příkaz, chyby mají kód 2. Novým procesem zkuste otevřít zálohu.


## Ověření v nové složce

Zkopírujte celou dokončenou pracovní složku na nové místo. V terminálu této
složky na Windows spusťte:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe overeni.py
.\.venv\Scripts\python.exe spust_pujcovnu.py --help
```

První příkaz vytvoří nové izolované prostředí z vašeho Pythonu. Další dva
použijí přímo jeho interpret, takže aktivace není nutná. Testy vytvoří jen
dočasná data, help vypíše příkazy. Na macOS/Linux použijte python3 -m venv .venv
a místo .\.venv\Scripts\python.exe cestu .venv/bin/python. Tuto .venv
vyberte také ve VS Code, VSCodium nebo PyCharm podle přípravy před kurzem.
QR je až volitelný doplněk; vlastní půjčovna, CSV a záloha fungují bez něj.

Příkaz pridat uloží nový předmět a počet dostupných kusů, prehled je znovu
načte. Zaloha vytvoří samostatný soubor, originál dál zůstává pracovní DB.
Ověřte jej příkazem python spust_pujcovnu.py --db kopie.sqlite3 prehled.
Tím skutečně otevřete kopii novým procesem. Samotná existence souboru ještě
nepotvrzuje, že záloha obsahuje správná data.
