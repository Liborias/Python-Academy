## Když už databáze není soubor

SQLite běží uvnitř Pythonu a pracuje se souborem nebo pamětí. PostgreSQL je samostatný server: klient pošle SQL přes připojení, server provede dotaz a vrátí řádky. Server může obsluhovat více programů a má vlastní role, oprávnění a správu. I server na stejném počítači je jiná služba než Python.

Tento závěr je **volitelný**. Lekce 1–30 fungují dál bez serveru. Příklady a tlačítko Zkontrolovat zde používají **označenou simulaci** dvou konkrétních dotazů. Pomůže s parametry a životností spojení; skutečné SQL, oprávnění, souběh a izolaci tím neověříme. Uložený spouštěč má pro server výslovný přepínač.

```python
# Databáze a přihlášená role jsou dva samostatné údaje, i když se jmenují stejně.
nastaveni = {'databaze': 'akademie', 'role': 'akademie'}
print(nastaveni['databaze'], nastaveni['role'])
```

## Co se při přechodu mění

- **Připojení:** SQLite dostane cestu k souboru nebo :memory:, PostgreSQL host, port, databázi, roli a ověření.
- **Parametry hodnot:** SQLite používá ?, psycopg používá %s pro všechny typy hodnot.
- **Přidělené id:** místo SQLite lastrowid použijeme PostgreSQL identity a RETURNING id.
- **Kontext spojení:** with sqlite con řeší transakci a nezavírá spojení; with psycopg.connect(...) řeší výsledek a spojení také zavře.
- **Záloha:** SQLite má backup API pro souborovou databázi, PostgreSQL vlastní nástroje, například pg_dump.

V této lekci dostane funkce už otevřené spojení s autocommit=True. Příkaz mimo transakční blok by se ihned potvrdil. **with con.transaction()** výslovně vymezí operaci: při úspěchu commit, při chybě rollback. Spojení přitom nezavře, protože je vlastní volající. Kurzor uvnitř bloku přenáší příkazy a čte výsledky; jeho kontext jej po použití zavře.

Hodnoty předáváme zvlášť, například tuple (nazev, kusy). Zástupné %s se neuzavírá do SQL uvozovek a nepoužívá se Pythonové % ani f-string. Pro jednu hodnotu patří do tuple čárka: (minimum,). Apostrof či text podobný SQL zůstane hodnotou. Parametry jsou pro hodnoty, nikoli libovolné názvy tabulek.

RETURNING id vrátí skutečně přidělené id jako řádek. Neodhadujeme ho z počtu řádků a nepoužíváme SQLite lastrowid. V PostgreSQL se hodnoty sekvence mohou spotřebovat i při rollbacku: mezery v id jsou běžné.

## Váš úkol

Doplňte **pridej_pg(con, nazev, kusy)** a **prehled_pg(con, minimum=0)** nad tabulkou akademie_pomucky. Helpery nazev_pomucky a pocet_kusu ověří a vrátí upravené hodnoty: okraje názvu se oříznou, název má 1–100 znaků, počet je int 0–1000000, nikoli bool. Neplatný vstup odmítněte před SQL a transakcí.

Pridat použije INSERT s oddělenými parametry %s, RETURNING id a vrátí celé id z fetchone. Přehled vrátí list tuple (id, nazev, kusy), filtr kusy >= minimum včetně meze a ORDER BY id. Prázdný výsledek je []. Každá funkce má vlastní con.transaction(), chybu předává a předané spojení nezavírá. Tabulku nevytváří ani nemaže; připraví ji samostatné init. Možné řešení ukazuje jednu cestu, například jinak spravovaný kurzor může být také správný.

## Skutečný server krok za krokem

1. Ve stejné .venv jako VS Code, VSCodium či PyCharm nainstalujte psycopg.
2. Nainstalujte/spusťte vlastní místní PostgreSQL, vytvořte samostatnou roli a cvičnou DB.
3. V terminálu nastavte PGHOST, PGPORT, PGDATABASE a PGUSER. Heslo zadávejte až do skrytého dotazu getpass.
4. Uložte dokončenou pracovní složku a spusťte níže uvedené příkazy. **NAVOD.md** obsahuje konkrétní postup pro Windows, macOS i Linux a význam každého příkazu.

```powershell
python -m pip install "psycopg[binary,pool]>=3.2,<4"
python -c "import psycopg, psycopg_pool; print(psycopg.__version__)"
python spust_postgres.py --help
python spust_postgres.py --pripojit --heslo init
python spust_postgres.py --pripojit --heslo pridat "Karty O'Neil" 2
python spust_postgres.py --pripojit --heslo prehled --minimum 1
```

Pip nainstaluje klienta, binární libpq a pool; nenainstaluje databázový server. Ověření importu vypíše verzi. Init připraví tabulku a ponechá existující data, pridat vloží jeden řádek a prehled ho načte v novém procesu. Samostatný přepínač --heslo vyžádá heslo bez echa, nikdy se za něj nepíše hodnota. Bez --pripojit běží pouze simulace. Nenastavené připojení se odmítne, nic se nehledá v původní SQLite DB.

Pro novou cvičnou DB vytvoří pg_podpora tabulku s BIGINT identity id, jedinečným TEXT názvem a nezáporným INTEGER počtem. SQLite soubor se automaticky nepřenáší. Předávání či zálohování serveru má vlastní nástroje; SQLite backup ani kopírování jeho souboru se na PostgreSQL nepoužije.
