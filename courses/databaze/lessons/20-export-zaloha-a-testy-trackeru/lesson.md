## Tabulka k přenosu a celá databáze

CSV obsahuje vybraný přehled; jiný program jej umí přečíst, ale neobsahuje schéma a pravidla databáze. Záloha SQLite naopak uchová celou DB včetně tabulek a id. Otevřenou databázi proto nekopírujeme prostým čtením souboru: použijeme Connection.backup.

```python
# CSV knihovna cituje středník, uvozovky i nový řádek v jedné hodnotě.
import csv
from io import StringIO
soubor = StringIO(newline='')
csv.writer(soubor, delimiter=';').writerow(['poznámka', 'A; B\nC'])
soubor.seek(0)
print(next(csv.reader(soubor, delimiter=';')))
```

Poslední prvek je jedna hodnota s novým řádkem. Ruční spojování středníkem či split po řádcích by ji rozbilo. Píšeme UTF-8 a newline='', oddělovač středník; čísla mají desetinnou tečku jako Python. Zobrazení na dvě místa se nepřenáší do uložené přesnosti.

## Dokončený soubor až po úspěchu

`soubory.py` poskytuje bezpecny_cil. Připraví dočasný soubor ve stejné složce, vrátí dvojici (dočasný Path, cílový Path) a teprve po úspěšném opuštění bloku provede os.replace. Při chybě starý cíl zůstane, dočasný se odstraní. Cíl může při úspěchu nahradit předchozí export či zálohu; nesmí ale přepsat právě otevřenou zdrojovou databázi. Helper chrání i shodnou cestu přes odkaz.

Záložní cílové spojení má autocommit=True a před nahrazením souboru se zavře. Zdrojový model vlastní celé transakce veřejných operací, nevkládejte do jeho con jiné rozpracované zápisy. Backup se tak spouští nad potvrzenými daty. Platí i pro paměťovou DB, kde není soubor ke kopírování.

## Váš úkol

Rozšiřte Tracker z prehledy.py o **export_csv(cesta, od=None, do=None)** a **zaloha(cesta)**. Export načte přehled období, v bezpecny_cil otevře dočasný soubor s encoding='utf-8', newline='', použije csv.writer delimiter=';' a hlavičku id, datum, hmotnost_kg, vyska_cm, bmi, poznamka. Zapíše nezměněné řádky přehledu a vrátí počet datových řádků bez hlavičky. Prázdný export má hlavičku a počet 0. Chybný filtr nezmění starý soubor.

Zaloha použije bezpecny_cil(cesta, self.cesta), otevře cílové SQLite spojení k dočasnému souboru s autocommit=True, zavolá self.con.backup a spojení zavře. Vrátí absolutní cílový Path. Chyby nepohlcuje, stará záloha při nich musí zůstat. Původní DB a záloha jsou po dokončení nezávislé.

## Ověření a skutečné spuštění

Uložený spust_bmi.py nyní importuje váš Tracker z reseni.py a hotové GUI z 19. Bez příkazu otevře okno; export/záloha a help nepotřebují grafickou plochu ani import Tkinteru:

```powershell
python spust_bmi.py --help
python spust_bmi.py export mereni.csv --od 2026-04-01 --do 2026-04-30
python spust_bmi.py zaloha kopie.sqlite3
python overeni.py
```

Export vypíše počet řádků, zaloha absolutní cestu. `--db CESTA` patří před příkaz, výchozí bmi.sqlite3 je vedle spouštěče. Rodič cílového souboru už musí existovat. Chyba CLI má návratový kód 2. Chcete-li použít vlastní měření z 19, předejte cestu k její DB.

`overeni.py` obsahuje tři izolované unittest: prázdný export, poznámku s problematickými znaky a zálohu nezávislou na pozdějších změnách. Importuje váš Tracker, používá TemporaryDirectory a addCleanup. Vaše vlastní data se nečtou ani nemění. OK znamená úspěch, FAILED vyžaduje opravu; návratový kód testů je 0/1. Hlavní ukázka reseni.py předvede export i obnovu v dočasné složce a vaše soubory neovlivní.
