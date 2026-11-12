## Přihlášení je stav tohoto běhu

Model z registrace je v ucty.py. Rozšíříme ho o ověření a uživatelské poznámky. Sezeni drží pouze (id, sjednocené jméno) nebo None. Heslo po ověření v sezení neuchovává. Nové spuštění začíná odhlášené.

```python
# Žádná identita znamená nepřihlášený stav.
uzivatel = None
print('Přihlášen:', uzivatel is not None)
```

Ověření totožnosti a oprávnění jsou dva kroky: správná fráze vytvoří identitu, dotazy poznámek pak vždy filtrují její id. Samotné skrytí tlačítka nebo uložení názvu v proměnné nechrání cizí řádky.

## Neúspěch nezanechá staré přihlášení

Před každým novým pokusem starou identitu zrušíme. Kdyby zůstala po chybném hesle, další akce by dál používaly předchozí účet. Neznámé jméno i nesprávná fráze mají obecný neúspěch. Pro neznámé platné jméno používáme veřejný náhradní záznam, aby také proběhl scrypt krok; neslibujeme tím shodný čas celé aplikace.

Poškozený JSON/ověřovací záznam neznamená přihlášení. Při ukládání poznámek ověříme celou dávku před transakcí; chyba druhého INSERT musí vrátit i první. Poznámky jsou běžný text v DB, nejsou šifrované.

## Váš úkol

Doplňte **Ucty.prihlaseni**, **zapis**, **cti** a metody **Sezeni.prihlas**, **importuj**, **seznam**. Prihlaseni sjednotí jméno, parametricky načte id/jmeno/overeni, JSON přečte nacti_overeni a použije over_heslo. Neexistující jméno ověřuje s NAHRADNI. Úspěch vrátí (id,jméno), jakýkoli neúspěch None. Chybný formát jména také None.

Zapis(ident, texty) validuje seznam přes over_poznamky, v jedné transakci provede parametrické executemany pro daného vlastníka a vrátí počet. Poznámka má 1–2000 znaků, obsahuje text a zachová původní mezery/nové řádky. Cti(ident) vrátí [(id_poznámky,text)] pouze vlastníka, v pořadí id.

Sezeni.prihlas nejprve zruší uzivatel, pak získá novou identitu a vrátí bool. Importuj bez identity vyvolá PermissionError, jinak uloží dávku pod id vlastníka. Seznam také vyžaduje identitu a vrátí jen její poznámky. Uloz(text) a odhlas jsou připravené. Sezení nevlastní spojení, to zavře model při skončení celé aplikace.

## Vlastní konzole

Uložte pracovní složku a dokončete reseni.py. V místním terminálu:

```powershell
python spust_ucty.py --help
python spust_ucty.py registrace Zofie
python spust_ucty.py prihlaseni Zofie
```

Help nic nevytvoří. Registrace vyžádá heslo dvakrát přes getpass, přihlášení jednou; při psaní se znaky nezobrazují. Heslo nepatří do příkazové řádky ani zdrojového kódu. Menu 1 vypíše vlastní poznámky, 2 přidá jednu, 3 odhlásí. Chyba CLI vrátí 2, Ctrl+C 130.

DB ucty.sqlite3 leží vedle spouštěče i při jiném cwd, --db CESTA před příkazem naváže na jiné umístění s existujícím rodičem. Mezi uloženými lekcemi použijte absolutní cestu ke stejné DB, schéma 22/23/25 se nemění. Webová ukázka používá paměť a nemá skrytý terminál getpass.

Je to místní cvičná aplikace. Nemění přihlašování webové Akademie a nechrání soubor před člověkem, který k němu má přístup v operačním systému.
