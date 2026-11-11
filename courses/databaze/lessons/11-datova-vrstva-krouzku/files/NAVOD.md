# Evidence kroužků: prostředí a spuštění

Potřebujete Python 3.12+ (ověřeno 3.14.8), sqlite3 a pro okno také Tkinter.
SQLite, unittest a Tkinter jsou součásti Pythonu, neinstalujte balíček tkinter
přes pip. Ve VS Code/VSCodium/PyCharm a terminálu zvolte stejnou .venv.

1. python --version ověří verzi vybraného Pythonu.
2. python -c "import sys, sqlite3, tkinter; print(sys.executable); print(sqlite3.sqlite_version); print(tkinter.TkVersion)"
   ověří interpretr a dostupnost modulů; ještě neověří grafickou plochu.
3. python -m tkinter otevře skutečné zkušební okno. Zavřete ho křížkem.
   Ve Windows opravte instalaci Pythonu a zapněte Tcl/Tk; na Debianu/Ubuntu
   nainstalujte python3-tk pro odpovídající systémový Python. Na macOS použijte
   oficiální instalátor Pythonu s Tk. Potom znovu vyberte správnou .venv.

Lekce 11 je konzolový model. V 12–14 python reseni.py otevře pracovní ukázku
v paměti se dvěma kroužky. Po zavření se její data zahodí. Kontrola v Akademii
umí ověřit chování bez okna, vzhled posuďte na své místní grafické ploše.

Uložte pracovní složku a ponechte pomocné .py soubory vedle reseni.py.
V 12–14 dokončete reseni.py a pak spusťte:
    python spust_krouzky.py --help
    python spust_krouzky.py

Help vysvětlí volby a nevytvoří databázi ani okno. Druhý příkaz otevře prázdnou
vlastní evidenci se souborem krouzky.sqlite3 vedle spouštěče. Po zavření a novém
spuštění záznamy zůstanou. Volba --db CESTA zvolí jiný soubor, rodičovská složka
musí existovat. Nepoužívejte starý klub.sqlite3: tento projekt má jiné schéma.
Běžný běh v prohlížeči používá dočasnou kopii, není vaší trvalou databází.
Každá uložená lekce má vlastní složku. Chcete-li v dalším kroku pokračovat se
stejnými záznamy, zadejte --db s absolutní cestou k předchozímu krouzky.sqlite3.
Schéma zůstává v 11–15 stejné, nové otevření staré záznamy nepřidává ani nemaže.

V lekci 15 python reseni.py spustí vaši sadu šesti testů nad oddělenými
TemporaryDirectory. Po dokončení přehled oznámí OK; návratový kód je 0 při
úspěchu, 1 při selhání. Vaše vlastní krouzky.sqlite3 se netestuje ani nemaže.
Spouštěč spust_krouzky.py v této závěrečné lekci používá dokončený model i GUI z lekce 14,
reseni.py je nyní soubor s vlastními testy. Pro změny vzhledu upravujte pohled.py
či navazující GUI helper, pro změny datové vrstvy příslušný model.

Každý kroužek má kladnou kapacitu a jedinečný neprázdný název. Přihlášku
určuje kroužek + přesné jméno; dvě stejnojmenné osoby ve stejném kroužku tato
cvičná aplikace nerozliší. Nejprve odhlaste členy, potom lze kroužek smazat.
Není to síťový systém pro více současných správců. Číslo řádku okna není id DB.
