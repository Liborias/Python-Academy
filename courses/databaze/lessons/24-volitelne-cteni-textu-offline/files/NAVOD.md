# Místní účty a soubory: příprava a spuštění

Python 3.12+, ověřeno Python 3.14.8/SQLite 3.53.1. Hashlib, secrets, hmac,
SQLite, zlib a Base64 jsou standardní knihovna. Žádné pip balíčky, účet,
server či internet nepotřebujete. Ve VS Code/VSCodium/PyCharm i terminálu
zvolte stejnou .venv. Scrypt vyžaduje podporu v daném sestavení Pythonu.

Profil scrypt má n=131072, r=8, p=1, dklen=32, sůl 16 náhodných bajtů.
Pracovní paměť je přibližně 128 MiB; maxmem=256 MiB je povolená horní mez,
ne objem uloženého otisku. Výpočet je záměrně dražší než obyčejný hash.
Na slabším počítači může trvat déle. Neměňte parametry uložených záznamů.

Příklad používá pouze fiktivní fráze. Vlastní heslo nepatří do reseni.py,
příkazových argumentů ani poznámek. Ve skutečné konzoli ho čte getpass,
který při psaní nezobrazuje znaky. V Akademii Spustit pracuje s pamětí či
TemporaryDirectory a ukázkami, nikoli s vaší trvalou evidencí.

Po dokončení a uložení pracovní složky 23 nebo 25:
    python spust_ucty.py --help
    python spust_ucty.py registrace Zofie
    python spust_ucty.py prihlaseni Zofie

Help nevytvoří DB ani nepožádá o heslo. Registrace si heslo vyžádá dvakrát,
přihlášení jednou. Menu: 1 vypíše vlastní poznámky, 2 přidá jednu, 3 odhlásí.
Na skutečný skrytý vstup použijte místní terminál; webová ukázka není getpass
terminál. Výchozí ucty.sqlite3 je vedle spouštěče i při jiném cwd. --db CESTA
před příkazem zvolí jiný soubor, rodič už musí existovat. Pro pokračování
s účty z předchozí uložené lekce použijte absolutní cestu ke stejné DB.
Schéma 22/23/25 je stejné. Nepoužívejte DB předchozích projektů.

Účty jsou místní cvičení, nemění přihlašování webové Akademie. Sezení chrání
přístup v tomto programu; samotný soubor chrání oprávnění operačního systému.
Poznámky jsou běžný text, ne šifrovaná data. Nové spuštění začíná odhlášené.

Lekce 24 je volitelná, základní běh je náhled bez zvuku:
    python precti.py "Ukázková poznámka."
    python precti.py "Ukázková poznámka." --mluv

Skutečný zvuk potřebuje systémový program a hlas. Windows: powershell.exe
s dostupným System.Speech a hlasem; macOS: say s instalovaným hlasem;
Linux: espeak-ng nebo espeak s českým hlasem cs (např. balíček espeak-ng
správce distribuce). Text jde přes stdin, nikoli přes shell. Náhled nic
neinstaluje a nevolá hlas. Stav nedostupne znamená chybějící program,
chybu hlasu nebo překročení 15 s. Reproduktor a výslovnost ověřte místně.
Do hlasu neposílejte hesla. Tato lekce nevyžaduje knihovnu pyttsx3 ani síť.

Závěr 25 přidává ověřený přenos vlastních poznámek:
    python spust_ucty.py export Zofie moje-poznamky.txt
    python spust_ucty.py import Zofie moje-poznamky.txt

Obě operace vyžádají heslo. Export přenáší jen poznámky, ne účet ani ověřovací
záznam. UTF-8 -> zlib -> Base64 s verzí z1:. To není šifrování ani záloha DB.
Cíl se při úspěchu nahradí, nesmí být zdrojovou DB. Import validuje celý obsah
před jednou transakcí. Přidává poznámky, původní nemaže; opakováním vzniknou
kopie. Limity: 65536 bajtů rozbaleného UTF-8 a 100000 znaků balíčku. Zkrácený,
poškozený nebo rozšířený zlib proud je chyba. Chyba CLI vrací kód 2, přerušení
Ctrl+C kód 130. Po zavření sezení nic nepřihlašuje samo.
