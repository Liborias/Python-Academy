## Databáze a projekty: od souboru ke klubovní evidenci

**Připraveno všech 32 lekcí.** Úvod má obtížnost 2/4, celek 4/4:
základní funkce Pythonu stačí pro první SQL, později přibudou vazby, transakce,
Tkinter a spolupráce součástí. Předpoklady jsou doporučení, nic se nezamyká.

Každá z pěti samostatných lekcí má tři přepínatelné ukázky, pět úkolů
s vlastním zadáním/šablonou/kontrolou/možným řešením a tři kvízové otázky.
V prvním bloku je **15 ukázek a 25 úkolů**. Témata 6–9 přidávají tři ukázky/pět úkolů na lekci a projekt 10 jeden souvislý krok. První dva bloky mají **28 ukázek a 46 úkolů**. Evidence kroužků 11–15 přidává pět návazných kroků, první tři bloky mají **33 ukázek a 51 úkolů**. BMI tracker 16–20 přidává sedm ukázek a pět návazných úkolů, první čtyři bloky mají **40 ukázek a 56 úkolů**. Místní účty a soubory 21–25 přidávají devět ukázek a pět úkolů, celkem **49 ukázek a 61 úkolů**. Navazující projekty tvoří souvislé kroky,
bez nesouvisejících variant, vždy s možným řešením.

## Prostředí

SQLite je v modulu sqlite3 standardní knihovny. První blok nepotřebuje pip
balíčky, server, účet ani internet. Python 3.12+ kvůli výslovnému autocommit;
ověřeno Python 3.14.8/SQLite 3.53.1. Ve VS Code/VSCodium/PyCharm a terminálu
vyberte stejnou .venv, postup je v Přípravě před kurzem.
python tools/setup_env.py --courses databaze může ověřit/připravit projektové
prostředí bez dalších povinných balíčků; běžné příklady fungují i bez grafiky.

Ukázky používají :memory: nebo TemporaryDirectory. Pro vlastní trvalý soubor
uložte pracovní složku a spusťte ji v editoru s vlastní cestou. Webový běh
je dočasný. `closing` zavírá spojení, `with con` řeší commit/rollback:
životnost spojení a hranice transakce nejsou totéž.

## Modul 1 — SQLite: od spojení k transakci

**Hotovo: lekce 1–5.**

1. Připojení, verze stroje, paměť a soubor, vlastnictví spojení.
2. Tabulky, INTEGER PRIMARY KEY, NOT NULL, UNIQUE, DEFAULT a CHECK.
3. Parametrizované INSERT/UPDATE/DELETE, lastrowid, rowcount a konflikty.
4. SELECT/WHERE/ORDER BY, fetchone/fetchall, Row a LIMIT/OFFSET.
5. Autocommit, commit/rollback, dávka a přesun jako jeden celek.

Výstup: skutečné funkce nad fiktivním klubovním skladem.
Hodnoty jsou oddělené od textu SQL, i apostrofy a čeština zůstanou zachované.
Kontrola používá skutečný SQLite stroj a ověří i návrat neúspěšné transakce
a viditelnost změn druhým spojením. Přijetí řešení nezávisí na přesném zápisu SQL.

## Modul 2 — Dotazy a vztahy (lekce 6–10)

**Hotovo: lekce 6–10.** NULL/COALESCE, doslovné hledání proti LIKE a skutečné typové afinity; souhrny/COUNT/AVG/GROUP BY/HAVING; cizí klíče zapnuté před transakcí a SET NULL/RESTRICT; INNER/LEFT JOIN, prázdné kategorie a aktivní historie. Závěrečná Evidence vlastní celé transakce půjčení/vrácení i spojení. Ukázka běží v paměti, spust_klub.py z uložené složky pracuje s klub.sqlite3 a poskytuje skutečné CLI příkazy. Staré schéma z 1–5 se nemigruje. Každý úkol má možné řešení, projekt je jeden celek.

6. NULL, typové afinity, porovnávání a textové filtry.
7. Souhrny COUNT/SUM, GROUP BY a HAVING.
8. Cizí klíče a důsledné zapnutí vazeb na každém spojení.
9. JOIN/LEFT JOIN a vztahy mezi tabulkami.
10. Souvislý konzolový mini-projekt klubovní evidence.

## Modul 3 — Evidence kroužků s Tkinterem (lekce 11–15)

**Hotovo: lekce 11–15.** Jeden návazný projekt s řešením každého kroku. Model vlastní SQLite spojení a transakce; GUI předává hodnoty, po chybě zachová vstupy. Výběr používá skutečné id i po mazání. Přihlášky hlídají kapacitu, duplicity, ochranu před smazáním a souhrny včetně prázdných kroužků. Závěr píše šest vlastních unittest případů, které kontrola zkusí i nad porouchanými modely.

Pro okna 12–14 ověřte `python -m tkinter`: potřebujete Tk a místní grafickou plochu. Bez nových pip balíčků. Ukázka používá paměť, uložený `spust_krouzky.py` nový `krouzky.sqlite3` vedle skriptu. --help nevytváří okno ani soubor; --db CESTA mění cestu. V závěru `python reseni.py` spustí izolované testy, spouštěč otevře hotové GUI z 14. Staré soubory jiných projektů se nemigrují.

11. Datová vrstva aplikace a oddělení SQL od widgetů.
12. Formulář a přidání kroužku.
13. Výběr, úpravy a mazání.
14. Přihlášky členů, vazby a zobrazení souvisejících údajů.
15. Dokončení okenní evidence, chyby a vlastní testy.

## Modul 4 — BMI tracker (lekce 16–20)

**Hotovo: lekce 16–20.** Samostatný projekt s řešením každého kroku; výpočetní lekce má tři přepínatelné ukázky. Kg/cm, konečná čísla, nezaokrouhlený výpočet a hranice pásem; skutečné datum a původní hodnoty v SQLite, více měření stejného dne; období včetně mezí, průměr jednotlivých BMI a změna kg podle data,id. Okno 19 zachová vstupy při chybě a podporuje desetinnou čárku. Závěr přidá UTF-8 CSV, SQLite backup včetně paměťové DB a tři izolované unittest. BMI je orientační dospělý ukazatel, ne individuální zdravotní hodnocení.

Bez nových pip balíčků; pro okno Tk a grafická plocha. Ukázky jsou dočasné. Uložený `spust_bmi.py` pracuje s vlastním `bmi.sqlite3` vedle sebe, --db CESTA naváže na předchozí složku. Export/zaloha/--help/overeni.py v 20 nevyžadují Tkinter. CSV a záloha se zapisují přes dočasný soubor, cíl se nahradí jen po úspěchu; zdrojová DB nesmí být cílem. Všechny příkazy vysvětlují lekce a NAVOD.md.

16. Výpočet, jednotky a meze interpretace.
17. Záznam měření s datem do SQLite.
18. Výpisy a časové souhrny.
19. Dokončení samostatného trackeru.
20. Testy, export a kopie databáze.

## Modul 5 — Místní účty a soubory (lekce 21–25)

**Hotovo: lekce 21–25.** Pevný scrypt profil n=131072/r=8/p=1, nová sůl, ověření přes compare_digest; registrace s Unicode casefold a UNIQUE; sezení s vlastním id a poznámkami. Chybný pokus zruší starou identitu, dávka se uloží celá nebo vůbec. Samostatná témata scrypt/kodek mají tři ukázky, každý krok má možné řešení a tři kvízy.

Volitelná offline řeč 24 běží standardně jako náhled. Skutečné --mluv vyžaduje systémový hlas (Windows System.Speech, macOS say, Linux espeak-ng/espeak cs), bez pip či online API. Kodek 25 vysvětluje UTF-8/zlib/Base64, verzi a omezené rozbalení; přenáší jen vlastní poznámky, ne hesla. Místní konzole spust_ucty.py používá nový ucty.sqlite3 vedle spouštěče, --db naváže na jinou uloženou složku. Heslo čte getpass, nikdy argument příkazu. Export/import ověří přihlášení a import přidá jednu validovanou dávku.

Bez dalších pip balíčků. Scrypt spotřebuje přibližně 128 MiB pracovní paměti; podporu musí mít daný Python. Nejde o přihlášení webové Akademie, soubor DB dál chrání operační systém. Všechny pokyny v lekcích a NAVOD.md.

21. Standardní scrypt, salt a kontrola hesla.
22. Registrace a jedinečnost uživatele.
23. Místní přihlášení a propojení s databázovou vrstvou.
24. Volitelný převod textu na řeč offline.
25. Komprese zlib a přenos textu přes base64; význam a omezení.

## Modul 6 — Malé nástroje a předání (lekce 26–30)

**Hotovo: lekce 26–30.** Sedm ukázek/pět úkolů s možnými řešeními a třemi kvízy.
Prvních šest bloků má **56 ukázek a 66 úkolů**. Obecný Luhn zachová ASCII/úvodní nuly,
půjčovna navíc vyžaduje existující kladné id bez úvodních nul. Kontrolní číslice
není identita ani oprávnění; QR obsah je otevřený text.

Vlastní unittest sada odhalí šest cílených poruch modelu. Cesty oddělují adresář
spouštěče od cwd; záloha používá SQLite backup API a atomické nahrazení cíle.
Závěr propojí karty/aktivní výpůjčky/CSV/QR a osm testů. Uložená konzole
spust_pujcovnu.py používá vlastní pujcovna.sqlite3 vedle sebe, --db před příkazem
naváže na jinou uloženou složku. Projekt z 10 se nemigruje, začněte novou DB.
Předání obsahuje všechny helpery a NAVOD.md, data zvlášť a novou .venv.

Jádro je standardní knihovna. Pouze QR potřebuje volitelný qrcode[pil]>=8.2,<9:
python -m pip install "qrcode[pil]>=8.2,<9" do stejné .venv, nebo v kořeni
Akademie python tools/setup_env.py --courses databaze --extras. Bez knihovny
se ukáže postup a ostatní části běží dál. Generování PNG funguje offline.
Ověřeno qrcode8.2/Pillow, čtení skutečných PNG nezávislým dekodérem.

26. Luhn a zkušební kontrolní číslice.
27. Volitelný QR kód a export vlastních dat.
28. Vlastní testy modelu a izolované databáze.
29. Cesty, backup API, čisté prostředí a předání.
30. Vlastní varianta projektu a závěrečné ověření.

## Modul 7 — Volitelná serverová databáze (lekce 31–32)

**Hotovo: lekce31–32.** Dvě souvislá zadání s možnými řešeními, šest ukázek
pro různé případy, tři kvízy v každé. Celkem **62 ukázek a 68 úkolů**.
Výukové ukázky/kontrola jsou označená simulace bez síťového připojení;
skutečný PostgreSQL vyžaduje zvlášť server a psycopg[binary,pool]>=3.2,<4.
Stejná .venv pro VS Code/VSCodium/PyCharm/terminál. NAVOD.md popisuje instalaci
Windows/macOS/Linux, roli a DB, PG* nastavení a význam příkazů.

Parametry %s oddělené od SQL, RETURNING id, autocommitTrue a explicitní
transaction, kurzor a spojení s různými vlastníky. Pool min1/max3, explicitní
open(wait=True), timeout převzetí3/připojení5/úvod8 sekund. Převzetí se vrací
i při chybě, funkce pool nezavírá. Vnější transakce zahrnuje všechny INSERT,
vnořená31 používá savepoint. Rollback řádků nevrací PostgreSQL sekvenci.

Uložený spust_postgres.py připojí skutečný server až s --pripojit, --heslo
čte getpass. Bez flagu pouze simulace. Init/pridat/prehled, stejné schéma
31/32, žádná migrace SQLite. Pokus_davky.py32 ověří dvouřádkový zápis a rollback
pozdějšího konfliktu; první dva fiktivní řádky v DB zůstanou. Pool nesdílíme
mezi procesy a pro jednorázový skript není automaticky výhodnější.

Ověřeno Python3.14.8/PostgreSQL17.11/psycopg3.3.9/pool3.3.3, skutečné SQL,
trvalost/rollback, souběžné přehledy, timeout max3 a uložené CLI.

31. PostgreSQL: jiné připojení a psycopg 3.
32. Správa spojení a connection pool, srovnání s SQLite.

Všech32 lekcí je připravených, status draft do připomínek studentů. Tkinter
vyžaduje místní grafickou plochu, offline řeč dostupný systémový hlas a QR
volitelnou knihovnu. PostgreSQL potřebuje vlastní server a psycopg klienta,
není podmínkou předchozích lekcí. Odhad20–30 hodin plus vlastní úpravy.
Dalším krokem je revize, vlastní varianta projektu a zpětná vazba.
