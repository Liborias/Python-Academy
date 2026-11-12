# Nástroje a předání půjčovny

Python 3.12+, ověřeno 3.14.8/SQLite 3.53.1. Jádro používá standardní knihovnu.
VS Code/VSCodium/PyCharm a terminál musí mít stejnou .venv. Návazné helpery
z předchozích lekcí ponechte vedle reseni.py. Import nic nespouští.

26: Luhn na zkušebních inventárních číslicích, nikoli potvrzení skutečného
předmětu. Vstup je text ASCII číslic a úvodní nuly se zachovávají. Luhn
nedokáže odhalit všechny chyby ani potvrdit identitu či oprávnění.

27: QR je volitelný. Pro skutečný PNG do stejné .venv:
    python -m pip install "qrcode[pil]>=8.2,<9"
    python -c "import qrcode, PIL; print('QR připraveno')"
Případně python tools/setup_env.py --courses databaze --extras v kořeni Akademie.
Bez knihovny příklad vypíše postup a nic nezapíše. PNG vytváříme lokálně,
QR obsah neotevíráme ani neposíláme do sítě. Obsah není tajný nebo šifrovaný.

28: python reseni.py spustí šest vašich izolovaných unittest. Každý případ má
vlastní TemporaryDirectory a model; addCleanup zavře spojení před mazáním
složky. Testy nepoužívají vlastní pujcovna.sqlite3. OK znamená úspěch, jinak
FAILED, návratový kód 0/1. Testy musí odhalit také záměrně porouchaný model.

29 a 30: po dokončení a uložení pracovní složky:
    python spust_pujcovnu.py --help
    python overeni.py
    python spust_pujcovnu.py pridat "Míč" 2
    python spust_pujcovnu.py prehled
    python spust_pujcovnu.py pujcit 18 "Žofie"
    python spust_pujcovnu.py vypujcky
    python spust_pujcovnu.py vratit 1
    python spust_pujcovnu.py zaloha kopie.sqlite3

Číslo 18 je ukázkový kód pro id1, číslo1 ukázkové id první výpůjčky. Převezměte
skutečné kódy/id ze svého výstupu. Výchozí vlastní pujcovna.sqlite3 je vedle
spouštěče i při jiném cwd. --db CESTA před příkazem volí jinou DB; relativní
cesta je vůči aktuálnímu adresáři, rodič musí existovat. Pro pokračování mezi
uloženými kroky použijte absolutní cestu ke stejné DB. Model přebírá relační
schéma projektu10, jiné staré soubory se nemigrují. Nový projekt začněte novým
pujcovna.sqlite3. Vlastní data a .venv do repozitáře běžně nepatří.

30 přidává:
    python spust_pujcovnu.py export stitky.csv
    python spust_pujcovnu.py qr 1 stitek.png
    python overeni.py


Význam příkazů:
- --help pouze vypíše volby, bez vytvoření DB.
- overeni.py vytvoří dočasné modely, porovná výsledky a oznámí OK/FAILED.
- pridat "Míč" 2 uloží pomůcku se dvěma dostupnými kusy a vypíše její id/kód.
- prehled vypíše uložené pomůcky; ve30 jsou to karty včetně aktivních výpůjček.
- pujcit 18 "Žofie" ověří kód, odečte jeden kus a uloží výpůjčku jako celek.
- vypujcky vypíše jen aktivní půjčení. vratit 1 vrátí výpůjčku id1 nejvýše jednou.
- zaloha kopie.sqlite3 vytvoří samostatný stav celé DB přes SQLite backup API.
- export stitky.csv ve30 zapíše karty inventáře, ne historii půjčujících.
- qr 1 stitek.png ve30 zapíše PNG s kódem existující pomůcky id1.
Každé spuštění znovu otevře stejnou vlastní DB. Návratový kód0 znamená úspěch,
kód2 chybu vstupu, souboru či SQLite. Detaily chyby jsou v terminálu.

CSV je UTF-8 se středníkem, obsahuje jen karty inventáře, ne seznam členů.
QR kóduje text PY-AKADEMIE:PUJ:<inventární kód>. Vyžaduje volitelnou knihovnu,
ostatní příkazy fungují bez ní. Overeni.py v30 spustí osm izolovaných testů
nad vaším MojePujcovna. V29 ověřuje šest testů modelu.

Záloha používá SQLite backup API, ne prosté kopírování otevřeného souboru.
CSV/PNG/záloha nahradí zvolený cíl až po úspěchu; zdrojová DB nesmí být cílem.
Pro zálohu/export/QR musí rodič cíle existovat. Chyba CLI vrací2. Model vlastní
spojení i transakce, nedávejte do con jinou rozepsanou práci. Dostupné kusy
jsou právě volné kusy, celkem = dostupné + aktivně vypůjčené.

Předání: zavřete běžící vlastní aplikaci, spusťte testy, předejte pracovní
složku se všemi helpery a NAVOD.md, na novém místě vyberte stejný Python.
Cizí .venv nekopírujte, připravte ji znovu. Data ponechte zvlášť, pracujte
s kopií a ověřte ji novým procesem. Není nutné vytvářet ZIP. Ukázky Spustit
používají dočasnou kopii: v27 vzniká PNG, v30 CSV, vlastní DB nemění.
Běžný python reseni.py v30 vytvoří stitky.csv v aktuálním adresáři.
