# Databáze a projekty: SQLite 1–5

Použijte Python 3.12 nebo novější (ověřeno Python 3.14.8/SQLite 3.53.1).
SQLite je ve standardním modulu sqlite3, první blok nepotřebuje pip balíčky,
server, účet ani internet. Projektovou .venv zvolte stejně v terminálu
a ve VS Code/VSCodium/PyCharm. Ve složce projektu můžete ověřit:

    python -c "import sys, sqlite3; print(sys.executable); print(sqlite3.sqlite_version)"
    python reseni.py

První příkaz ukáže interpreter a verzi databázového stroje, druhý spustí váš
program. Příprava před kurzem vysvětluje vytvoření .venv a výběr editoru.
Pomocné schema.py/podklady.py ponechte vedle reseni.py, pokud je lekce používá.

Hlavní ukázky používají :memory: nebo TemporaryDirectory; po zavření se
cvičná data uklidí. Pro vlastní trvalý soubor nejprve uložte pracovní složku
a v editoru nahraďte cestu ':memory:' například za Path(__file__).with_name('sklad.sqlite3').
U souborových ukázek nahraďte TemporaryDirectory svou stálou cestou.
Běžné webové spuštění vytváří dočasnou kopii programu, není trvalým úložištěm.
SQLite soubor není textový CSV; jeho obsah čteme SQL přes sqlite3.

V prvních čtyřech lekcích je autocommit=True: samostatný úspěšný zápis se uloží.
Pátá výslovně vyžaduje autocommit=False a stanoví hranici celé transakce.
`with con` řeší commit/rollback, spojení nezavírá. `closing(con)` jej na konci
zavře, ale nenahrazuje uložení rozepsané transakce. V pomocných funkcích
s předaným con z lekcí 2–4 spojení ani transakci neukončujte, vlastní je volající.

Příklady používají vlastní fiktivní klubová data. První blok nemaže vaše
databázové soubory, neprovádí automatické migrace ani nenavazuje síťová spojení.
Přesné zadání a možné řešení každého úkolu je v aplikaci.
