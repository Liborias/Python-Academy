## Spojení je prostředek, který si půjčujeme

Otevření připojení zahrnuje síť a ověření. Malý jednorázový skript si vystačí s jedním spojením. Dlouho běžící aplikace může použít **connection pool**, který drží omezený počet spojení a na jednotlivé operace je půjčuje. Pool nevytváří databázový server a nezaručuje rychlejší program při každé úloze.

```python
# Limit souběžně půjčených spojení není počet všech úloh aplikace.
max_spojeni = 3
ulohy = ['přidat', 'přehled', 'další přehled', 'další přidání']
print('Úloh:', len(ulohy), 'limit spojení:', max_spojeni)
```

Ukázky i kontrola v Akademii jsou znovu **označená simulace**. Nepředstírají měření výkonu ani skutečný souběh serveru. Opravdový pool a PostgreSQL vyzkoušíte v uložené složce podle NAVOD.md z předchozí lekce.

## Kdo co zavírá

Vlastník vytvoří ConnectionPool a po poslední práci ho zavře. **with pool.connection(timeout=3) as con** převezme spojení a po bloku ho vrátí do poolu, také při výjimce. Uvnitř funkce nevolejte con.close ani pool.close. Do dlouhého čekání na vstup nebo síťové API si spojení nepůjčujte zbytečně brzy.

Helper nastaví autocommit=True, min_size=1 a max_size=3. Vytvoří pool s open=False a výslovně zavolá open(wait=True, timeout=8), aby bylo připojení ověřené před prací. Při neúspěchu pool uklidí. Connect_timeout=5 omezuje navazování jednotlivého spojení, timeout=3 čekání na volné spojení a osm sekund úvodní připravení poolu. Jsou to různé okamžiky, nikoli jeden společný limit celé dávky.

## Pool není transakce dávky

Samostatné pridej_pg z 31 používá vlastní transakční blok. Kdybychom každou položku zavolali samostatně bez vnější transakce, první by se mohla potvrdit před konfliktem u druhé. Dávka má proto **jedno převzetí spojení a vnější con.transaction()**.

Volání pridej_pg uvnitř tohoto bloku vytvoří v psycopg vnořený transakční blok se savepointem. Vnořený úspěch nepotvrdí celou vnější transakci. Výjimku necháme projít ven a vnější blok vrátí všechny změny dávky. Už před půjčením spojení ověříme všechny vstupní dvojice. Záměrně nečekáme souvislá id: rollback řádků nevrací sekvenci identity zpět.

## Váš úkol

Doplňte **prehled_z_poolu(pool, minimum=0)** a **pridej_davku(pool, pomucky)**. Přehled ověří minimum pomocníkem pocet_kusu ještě před převzetím, půjčí jedno spojení s timeout=3 a zavolá prehled_pg z 31. Vrátí jeho výsledek a spojení uvolní.

Dávka nejprve použije priprav_davku: list nebo tuple nejvýše 100 dvojic název/počet, stejná pravidla jako v 31, oříznuté názvy. Prázdná dávka vrátí [] bez převzetí spojení. Jinak jedno převzetí, vnější transaction a jednotlivé pridej_pg z podkladu pg_model.py. Vraťte list skutečných id v pořadí vstupu. Chyba při pozdějším INSERT vrátí celou dávku, výjimka se předá dál a pool musí být znovu použitelný.

Neukrývejte výjimky do prázdného výsledku. Timeout při vyčerpaném poolu je chyba, prázdný přehled může být normální výsledek. Správná implementace nemusí mít stejný zápis jako možné řešení.

## Vyzkoušení skutečného poolu

Stejná .venv a volitelný psycopg[binary,pool]>=3.2,<4 z 31. Uložený spouštěč importuje právě vaše funkce a používá stejné libpq proměnné. Pro navázání na 31 nastavte stejnou databázi; SQL schéma je stejné. Znovu jej nevytvářejte pod jiným názvem omylem.

```powershell
python spust_postgres.py --help
python spust_postgres.py
python spust_postgres.py --pripojit --heslo init
python spust_postgres.py --pripojit --heslo pridat "Míč" 3
python spust_postgres.py --pripojit --heslo prehled
```

Help pouze vypíše volby a bez parametrů běží simulace. Init připraví tabulku, pokud ještě není. Pridat v této lekci předá vaší dávce jednu dvojici, prehled použije vaši funkci nad poolem. Víceřádkovou dávku ověří dodaný pokus_davky.py: přidá dva řádky s novými fiktivními názvy, pak zkusí nový řádek následovaný duplicitním. Po konfliktu musí být celá druhá dávka vrácená. Dva záznamy z úspěšné první dávky v cvičné DB zůstanou. NAVOD.md vysvětluje instalaci serveru a přístup bez hesla ve zdrojích.

Každý tento krátký CLI proces pool vytvoří a zavře. Výhoda opakovaného půjčování se projeví uvnitř déle běžícího procesu, ne sdílením poolu mezi různými spuštěními příkazu. Pro jednořádkový CLI z 31 je obyčejné spojení často přehlednější.

```powershell
python pokus_davky.py --pripojit --heslo
```

Bez přepínače i tento pokus spustí jen simulaci. Se skutečným připojením vypíše přidělená id, zachytí očekávaný konflikt UNIQUE a ověří nepřítomnost neúplného řádku i další použití poolu. Před pokusem musí proběhnout init.

## Co si z kurzu odnést

Pro vlastní malou místní evidenci může stačit SQLite. PostgreSQL přidá správu serveru, rolí, síťového přístupu a záloh; zvolte ho podle potřeb projektu. Pool řeší životnost a omezení počtu spojení, transakce správnost celého zápisu. Prošli jste všemi 32 lekcemi; další krok je vlastní varianta projektu, zpětná vazba a opakování míst, která se zatím nedaří.
