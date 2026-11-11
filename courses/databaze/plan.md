## Databáze a projekty: od souboru ke klubovní evidenci

**Připraveno prvních 15 z 32 lekcí.** Úvod má obtížnost 2/4, celek 4/4:
základní funkce Pythonu stačí pro první SQL, později přibudou vazby, transakce,
Tkinter a spolupráce součástí. Předpoklady jsou doporučení, nic se nezamyká.

Každá z pěti samostatných lekcí má tři přepínatelné ukázky, pět úkolů
s vlastním zadáním/šablonou/kontrolou/možným řešením a tři kvízové otázky.
V prvním bloku je **15 ukázek a 25 úkolů**. Témata 6–9 přidávají tři ukázky/pět úkolů na lekci a projekt 10 jeden souvislý krok. První dva bloky mají **28 ukázek a 46 úkolů**. Evidence kroužků 11–15 přidává pět návazných kroků, celkem **33 ukázek a 51 úkolů**. Navazující projekty tvoří souvislé kroky,
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

## Modul 4 — BMI tracker (lekce 16–20, plán)

16. Výpočet, jednotky a meze interpretace.
17. Záznam měření s datem do SQLite.
18. Výpisy a časové souhrny.
19. Dokončení samostatného trackeru.
20. Testy, export a kopie databáze.

## Modul 5 — Místní účty a soubory (lekce 21–25, plán)

21. Standardní scrypt, salt a kontrola hesla.
22. Registrace a jedinečnost uživatele.
23. Místní přihlášení a propojení s databázovou vrstvou.
24. Volitelný převod textu na řeč offline.
25. Komprese zlib a přenos textu přes base64; význam a omezení.

## Modul 6 — Malé nástroje a předání (lekce 26–30, plán)

26. Luhn a zkušební kontrolní číslice.
27. Volitelný QR kód a export vlastních dat.
28. Vlastní testy modelu a izolované databáze.
29. Cesty, backup API, čisté prostředí a předání.
30. Vlastní varianta projektu a závěrečné ověření.

## Modul 7 — Volitelná serverová databáze (lekce 31–32, plán)

31. PostgreSQL: jiné připojení a psycopg 3.
32. Správa spojení a connection pool, srovnání s SQLite.

Pozdější témata zatím nejsou implementovaná. Tkinter vyžaduje místní grafickou
plochu, offline řeč dostupné systémové hlasy a QR další knihovnu. Volitelné
PostgreSQL potřebuje vlastní dostupný server a nastavení přístupu.
Pro prvních patnáct lekcí se neinstalují pip balíčky; pro okna je potřeba dostupný systémový Tk.
Odhad celku 20–30 hodin plus procvičení. Dalším krokem je BMI tracker 16–20.
