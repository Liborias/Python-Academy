# Volitelný PostgreSQL inventář

Python 3.12+, ověřováno na 3.14.8. Lekce 1–30 dál fungují bez PostgreSQL.
V prohlížeči i při python reseni.py je vždy označená výuková simulace dvou
konkrétních dotazů. Není to SQL stroj, připojení ani test skutečné izolace.
Proměnné PG* samy skutečné připojení nezapnou.

## Stejná .venv v editoru a terminálu

Ve VS Code/VSCodium vyberte Python: Select Interpreter a .venv. V PyCharm
Settings > Project > Python Interpreter zvolte stejné existující prostředí.
Ověřte python -c "import sys; print(sys.executable)". Příprava před kurzem
popisuje Windows/macOS/Linux i výběr editoru podrobně.

Pro skutečné připojení v aktivní .venv:
    python -m pip install "psycopg[binary,pool]>=3.2,<4"
    python -c "import psycopg, psycopg_pool; print(psycopg.__version__)"
Pip stáhne psycopg 3, jeho binární libpq a samostatný pool. Internet je potřeba
pro instalaci. Veškeré další příkazy používají stejnou .venv. V kořeni Akademie
lze použít python tools/setup_env.py --courses databaze --extras; nainstaluje
volitelné QR i PostgreSQL. Instalace knihovny sama server nenainstaluje.

## Místní server

Vyhraďte novou cvičnou DB, nepoužívejte důležitá data. PostgreSQL je samostatná
služba. Soubor SQLite nelze otevřít jako PostgreSQL a tento kurz jej nemigruje.

Windows: oficiální instalátor z https://www.postgresql.org/download/windows/,
zvolte server a příkazové nástroje. pgAdmin je volitelný. Služba musí běžet;
pokud psql není v PATH, použijte SQL Shell (psql) nebo plnou cestu k psql.exe
z bin složky instalace. V PowerShellu ji při mezerách spouští operátor &.
Instalátor vás vyzve k vlastnímu heslu administrátora postgres.

macOS s Homebrew:
    brew install postgresql@17
    brew services start postgresql@17
    $(brew --prefix postgresql@17)/bin/psql postgres
První dva příkazy nainstalují server a spustí místní službu, poslední otevře
SQL konzoli. U Homebrew bývá administrátorem účet macOS, nikoli role postgres.
Pokud psql není v PATH, používejte uvedenou plnou cestu.

Debian/Ubuntu pro systémový server:
    sudo apt update
    sudo apt install postgresql postgresql-client
    sudo systemctl start postgresql
    sudo -u postgres psql
První příkaz obnoví seznam balíčků, druhý instaluje server a klienta, třetí
spustí službu a poslední otevře konzoli jako administrátor. V systému bez
systemd použijte správce služeb dané distribuce. Python může zůstat ve .venv.

Na Windows v SQL Shell nebo tam, kde je role postgres:
    psql -h 127.0.0.1 -p 5432 -U postgres -d postgres -W
-h host, -p port, -U role a -d databáze určují cíl. -W vyžádá heslo interaktivně;
heslo se nepíše do příkazu. Na macOS použijte výše uvedené psql s místním účtem.

V administrátorské konzoli jednou:
    CREATE ROLE akademie LOGIN;
    \password akademie
    CREATE DATABASE akademie OWNER akademie;
    \q
CREATE ROLE založí samostatné přihlášení bez administrátorských práv.
Příkaz \password interaktivně nastaví jeho heslo, CREATE DATABASE vytvoří novou
cvičnou DB s touto rolí jako vlastníkem a \q konzoli opustí. Databáze i role
mají shodně jméno akademie, ale jsou to dvě různé věci. Pokud už existují,
neopakujte CREATE a nemažte je; vyberte vlastní nový název nebo ověřte původní.

## Nastavení přístupu v terminálu

PowerShell (pro právě otevřený terminál):
    $env:PGHOST = "127.0.0.1"
    $env:PGPORT = "5432"
    $env:PGDATABASE = "akademie"
    $env:PGUSER = "akademie"
macOS/Linux:
    export PGHOST=127.0.0.1
    export PGPORT=5432
    export PGDATABASE=akademie
    export PGUSER=akademie
Jde o libpq proměnné: klient, nikoli server, z nich určí připojení. Změňte port
či jména podle vlastní instalace. Neobsahují heslo. Příkazy spouštějte ze stejného
terminálu, editor nemusí změny převzít do již běžícího procesu.

Přepínač --heslo se zeptá přes getpass bez echa. Heslo není argument příkazu,
zdrojový kód, webový vstup ani Git soubor. Bez --heslo knihovna použije vlastní
libpq nastavení, například soukromý PGPASSFILE. Soubor hesel se nevkládá do
repozitáře; na macOS/Linux musí mít práva 0600. Vzdálený server vyžaduje síťové
povolení, vlastní účet a TLS podle správce, obvykle PGSSLMODE=verify-full a
PGSSLROOTCERT. Místní postup zde server nezpřístupňuje do internetu.

## Skutečný běh uloženého řešení

Dokončete reseni.py, uložte celou pracovní složku s helpery, v jejím terminálu:
    python spust_postgres.py --help
    python spust_postgres.py
    python spust_postgres.py --pripojit --heslo init
    python spust_postgres.py --pripojit --heslo pridat "Karty O'Neil" 2
    python spust_postgres.py --pripojit --heslo prehled --minimum 1
Help pouze vypíše volby, bez parametrů běží označená simulace. --pripojit je
výslovný požadavek použít server. Init vytvoří tabulku akademie_pomucky, nic
nemaže. Pridat vloží pomůcku a vypíše id; prehled načte řádky s počtem kusů
alespoň rovným minimu. Každé spuštění znovu otevře stejnou DB. Duplicitní název
odmítne UNIQUE, neplatný počet aplikace. --heslo je samostatný přepínač, nikdy
za něj nepište skutečné heslo. Ukončení procesu uzavře jeho spojení/pool.

Ve32 spouštěč používá studentovy pridej_davku a prehled_z_poolu. Pool má min1/
max3 spojení, čekání na převzetí3 s, připojení5 s a úvodní open(wait=True)8 s.
Pool uzavře vlastník po poslední operaci. Funkce spojení pouze vrací do poolu.
Pool není async, nevytváří tabulku a sám nezajišťuje atomickou dávku.

Při chybě skutečného běhu dostanete návratový kód2 a obecnou diagnostiku bez
podrobností přístupu. Ověřte službu/host/port, roli/databázi/heslo a zda proběhl
init; při duplicitě použijte jiný název. V simulaci je chyba vypsaná přímo.
Při opravách používejte své fiktivní záznamy a nový terminál pro nové nastavení.

Ve32 navíc python pokus_davky.py --pripojit --heslo ověří skutečnou dávku:
přidá dva fiktivní řádky s novými názvy, druhá dávka obsahuje konflikt UNIQUE.
Ta se musí vrátit celá a pool musí zůstat použitelný. Dva úspěšné řádky v cvičné
DB zůstanou. Bez --pripojit se i tento pokus omezuje na označenou simulaci.
