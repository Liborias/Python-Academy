## Vlastní tracker na obrazovce

Hotové modely z 17–18 jsou v model.py/prehledy.py, rozložení v pohled.py. Okno předává hodnoty, SQL i transakce zůstávají v modelu. Formulář má datum, kg, cm, poznámku, volitelné Od/Do a přehled. Datum se při otevření nastaví na dnešek, výška 180 je upravitelný ukázkový vstup.

```python
# Pole vrací text; čárku převedeme jen pro číselný vstup.
text = '72,5'
print(float(text.replace(',', '.')))
```

`cti_cislo` v validace.py navíc ověří kladnou konečnou hodnotu. Více čárek nebo text jsou chyby, tisícové oddělovače nepodporujeme. Převod čárky se netýká poznámky. Při chybném datu nebo čísle necháme celý formulář vyplněný, aby jej člověk mohl opravit.

## Okno a vaše trvalá data

Spustit otevře skutečné Tk okno na počítači s Pythonem, nikoli uvnitř webové stránky. Ukázka používá paměť se dvěma fiktivními záznamy a po zavření se zahodí. Ověřte `python -m tkinter`; instalace Tk a volba stejné .venv v jednotlivých editorech jsou v Přípravě/NAVOD.md.

Pro vlastní evidenci uložte pracovní složku a dokončete reseni.py. V jejím terminálu:

```powershell
python spust_bmi.py --help
python spust_bmi.py
```

Help vypíše možnosti bez DB a okna. Druhý příkaz importuje vaši Aplikace a otevře nový prázdný bmi.sqlite3 vedle spouštěče. `--db CESTA` před příkazem vybere jiný soubor se stávajícím rodičem. Pro přechod mezi uloženými lekcemi použijte absolutní cestu ke stejnému bmi.sqlite3; schéma 17–20 se nemění. Nepoužívejte databáze jiných projektů. Běžný webový běh je dočasný.

## Váš úkol

Doplňte **Aplikace.obnov**, **pridej**, **filtruj** a **vse**. Obnov nejprve načte nový přehled i souhrn, teprve potom změní self.data, self.obdobi a widgety. Řádky zobrazí jako `id: datum | kg kg / výška cm | BMI hodnota`, kg/cm s formátem g, BMI se dvěma místy. Souhrn zobrazí „Počet: číslo | Průměr BMI: hodnota“, pro prázdný průměr pomlčku —.

Pridej převede hmotnost/výšku přes cti_cislo, zavolá model.pridej a zachová poznámku beze změny. ValueError vysvětlí v popisku, SQLite chyba oznámí „Měření se nepodařilo uložit do databáze.“ Při chybě nic nevymaže. Po úspěchu vyčistí hmotnost a poznámku, ponechá datum/výšku, obnoví aktuální období a oznámí „Uloženo měření ID číslo.“ Pokud selže až obnova po úspěšném uložení, oznámí „Měření uloženo, přehled se nepodařilo obnovit.“

Filtruj převede prázdné Od/Do na None, zkusí obnov a při ValueError ponechá původní přehled i rozepsaný filtr. SQLite chybu čtení oznámí „Přehled se nepodařilo načíst z databáze.“ Úspěch hlásí „Období použito.“ Vse obnoví neomezená data a teprve po úspěchu vyprázdní Od/Do, stav „Zobrazuji všechna měření.“ Při chybě zachová dosavadní stav.

Nově uložený záznam může být mimo vybrané období. To neznamená, že se ztratil; použijte Všechna měření. Po zavření a novém spuštění vlastní evidence záznamy zůstanou. Tracker nehodnotí zlepšení zdraví ani nenavrhuje cílovou hmotnost.
