"""Návody přípravy kurzů; balíčky sdílíme s instalačním pomocníkem."""
from tools.setup_env import PACKAGES, OPTIONAL_PACKAGES

PROFILES = {
    'priprava': {
        'focus': 'Začněte instalací Pythonu a výběrem editoru. Git, GitHub a server přijdou až v dalších modulech.',
        'verify': 'import sys; print(sys.executable); print(sys.version)',
        'system': 'Stačí Python a terminál. Git nainstalujete až pro modul Verzování. GitHub účet ani server nejsou potřeba pro první lekce.',
    },
    'oop': {
        'focus': 'Samostatný OOP kurz má všech 20 lekcí připravených. Konzolové příklady a expediční projekt používají standardní knihovnu Pythonu.',
        'verify': 'import sys; print(sys.executable); print(sys.version)',
        'system': 'Nepotřebujete Turtle, Pygame, grafické prostředí, Docker ani účet u externí služby. Nejprve zvládněte základní funkce a datové struktury. Kurz vede od prvních objektů přes dědění, kompozici a testy až po expediční centrum.',
    },
    'zaklady': {
        'focus': 'Čistý Python: proměnné, cykly a funkce. Žádné další pip balíčky nejsou potřeba.',
        'verify': 'import sys; print(sys.executable); print(2 + 3)',
        'system': 'Stačí Python a prohlížeč. Očekávaný výsledek posledního řádku ověření je 5.',
    },
    'soubory-web': {
        'focus': 'requests stahuje data, beautifulsoup4 zpracovává HTML (v kódu import bs4). Výukové weby běží místně.',
        'verify': 'import requests, bs4; print(requests.__version__); print(bs4.__version__)',
        'system': 'Internet potřebujete pro instalaci balíčků. Dosavadní scrapingové lekce používají místní cvičný web a nepotřebují účty ani API klíče.',
    },
    'pygame-1': {
        'focus': 'Instalujte pygame-ce. V kódu se píše import pygame; neinstalujte současně původní balíček pygame.',
        'verify': 'import pygame; print(pygame.version.ver)',
        'system': 'Pro hraní a tvorbu oken potřebujete místní grafickou plochu a pro zvuk funkční zvukový výstup. Samotný import okno ani zvuk neověří.',
    },
    'turtle-oop': {
        'focus': 'turtle je součástí Pythonu a používá systémový Tkinter. requests je připraven pro pozdější práci s API.',
        'verify': 'import turtle, tkinter, requests; print(tkinter.TkVersion); print(requests.__version__)',
        'system': 'Na Debianu/Ubuntu doinstalujte python3-tk pro používaný systémový Python; u Homebrew Pythonu 3.14 balíček python-tk@3.14. Tkinter neinstalujte přes pip. Pro ověření okna spusťte Pythonem z .venv příkaz -m tkinter. Vyžaduje grafickou plochu.',
    },
    'pandas': {
        'focus': 'pandas řady 3 pro tabulky, matplotlib pro grafy, openpyxl pro Excel a ipykernel pro notebooky a buňky # %%. Prvních 25 lekcí potřebuje jen pandas, grafy v lekcích 26–30 také Matplotlib. Modul 31–35 přidává Excel přes openpyxl, měsíční projekt tabulky a graf. Ipykernel je volitelný.',
        'verify': 'import pandas, matplotlib, openpyxl, ipykernel; print(pandas.__version__)',
        'system': 'V notebooku vyberte jádro ze stejné .venv jako v terminálu a ověřte sys.executable. Při změně lekce/helperů restartujte jádro a spusťte všechny buňky od začátku. VS Code/VSCodium: rozšíření Jupyter; v PyCharm záleží dostupnost notebooků na verzi a licenci. Obyčejný soubor .py s buňkami # %% lze vždy spustit také celý v terminálu a v prohlížeči. Všech 42 lekcí je připravených: od Series a čištění dat po souhrny, groupby, statistiku a projekt kavárny, následně spojování tabulek, časové souhrny, grafy, CSV/Excel, měsíční přehled kavárny a Analytická dílna s auditem, testy a předáním. Grafy používají Figure a export PNG bez okna; aplikace zobrazí náhled a odkaz ke stažení. V editoru se soubor uloží do pracovní složky procesu. U souborových lekcí lze stáhnout CSV/XLSX včetně vstupů; závěr navíc nabízí dokumentaci MD a notebook IPYNB. Pracovní editor má přiložené soubory vedle reseni.py. Samostatné lekce mají tři ukázky a pět úkolů s možným řešením; projekty 20/35 i kroky 36–42 tvoří souvislé celky se vzorem. Ověřeno na Pythonu 3.14.8 s pandas 3.1.1, NumPy 2.5.4, matplotlib 3.11.2, openpyxl 3.1.5 a ipykernel 7.4.0. Používáme vlastní cvičná data, první blok nevyžaduje internet ani grafickou plochu.',
    },
    'tkinter-api': {
        'focus': 'Úvodních dvanáct lekcí používá standardní Tkinter a ttk. Od lekce 13 je potřeba requests pro místní HTTP API, od lekce 18 aiosmtpd pro místní SMTP záchyt. EmailMessage, smtplib a přílohy jsou standardní knihovna. PyInstaller zůstává volitelný pro závěrečné balení.',
        'verify': 'import tkinter, requests, aiosmtpd; print(tkinter.TkVersion); print(requests.__version__); print(aiosmtpd.__version__)',
        'system': 'Tkinter ověřte na grafické ploše pomocí Pythonu z .venv s volbou -m tkinter. Na Debianu/Ubuntu potřebujete odpovídající python3-tk; na Homebrew python-tk@3.14. E-mailové lekce používají místní záchyt bez osobní schránky a bez hesla. Všech 28 lekcí je připravených, včetně API, Korespondenční dílny, vlastních testů, cest k datům a předání. Balení zůstává volitelné; PyInstaller 6.22.3 byl ověřen s Pythonem 3.14.8 na Linuxu, jiný cílový systém je nutné sestavit a vyzkoušet zvlášť. Okno se otevře na počítači s Pythonem, nikoli uvnitř webové stránky; v prostředí bez grafické plochy ho nelze zobrazit. Cvičné API z files/cvicne_api.py se spouští automaticky jen na 127.0.0.1, vyžaduje povolení místních spojení a nezávisí na internetu. Záchyt z files/cvicna_posta.py potřebuje aiosmtpd (ověřeno 1.4.6 na Pythonu 3.14.8), naslouchá jen na 127.0.0.1 a zprávy neodesílá dál. Modul smtpd v Pythonu 3.14 již není. Konfiguraci DILNA_SMTP_* zkoušejte při přímém spuštění v terminálu či editoru.',
    },
    'pygame-2': {
        'focus': 'Stejné pygame-ce jako v Pygame 1, v kódu import pygame. Hodí se základní třídy ze samostatného OOP nebo Turtle. První modul používá Sprite, Surface, Vector2, Group a události bez otevírání okna.',
        'verify': 'import pygame; print(pygame.version.ver)',
        'system': 'Všech 30 lekcí je připravených. Úvod 1–5 a Součásti větší hry 16–20 používají PNG pokusy bez okna. Meteority, Chyť robota a Hon na dronech jsou živé místní hry; okno se ze vzdáleného Pythonu nepřenáší do prohlížeče. Hon na dronech: šipky/WASD, závěr Mezerník/P/R/Esc; N jen v tréninku 23. Běžné zavření uloží PNG, Stop to nezaručí. Závěr 26–29 přidává konzolové scénáře, vlastní unittest, JSON výsledky a přípravu složky; samostatná témata mají tři ukázky a pět úkolů s řešeními. Kurýrská směna 30 propojí profil a tabulku výsledků s místní hrou. Pro trvalé data/vysledky.json uložte pracovní složku a spusťte ji v editoru; běžný webový běh je dočasný. Stejná .venv pro VS Code/VSCodium/PyCharm, Python 3.14.8/pygame-ce 2.5.8. Nové povinné knihovny ani audio nejsou potřeba. PyInstaller 6.22.3 je volitelný pro vlastní sestavení; nejprve testy a místní hraní. Tón 16 a živá dílna 20 zůstávají volitelné.',
    },
    'databaze': {
        'focus': 'SQLite, hashlib.scrypt, secrets, hmac, zlib a Base64 jsou standardní knihovna. Základ 30 lekcí nepotřebuje pip balíčky ani server, PNG v 27 a 30 má volitelný qrcode[pil]>=8.2,<9. Scrypt profil n=131072/r=8/p=1 používá přibližně 128 MiB pracovní paměti; Python musí mít podporu scrypt.',
        'verify': 'import sys, sqlite3, hashlib; print(sys.executable); print(sqlite3.sqlite_version); print("scrypt dostupné:", hasattr(hashlib,"scrypt"))',
        'system': 'Prvních 30 z 32 lekcí je připravených: SQLite a klubovní evidence, Tkinter kroužky, BMI tracker a místní účty/soubory 21–25. Nově scrypt/sůl/ověření hesla, registrace, vlastní poznámky podle přihlášeného id, volitelná offline řeč a přenos přes zlib/Base64. Všechna zadání mají možná řešení, samostatné výpočty/scrypt/kodek více ukázek. Python 3.12+, ověřeno 3.14.8/SQLite 3.53.1/Tk 9.0. Ve VS Code/VSCodium/PyCharm i terminálu stejná .venv. Základ bez pip balíčků či internetu; pouze QR vyžaduje volitelný qrcode[pil]>=8.2,<9. Okna 12–14/19 vyžadují systémový Tk a grafickou plochu, ověřte python -m tkinter. Místní účty 21–25 jsou konzolové, nemění přihlašování Akademie. Uložený spust_ucty.py má vlastní ucty.sqlite3 vedle sebe; --db CESTA před příkazem naváže na předchozí složku, rodič už musí existovat. Registrace/přihlášení čtou heslo přes getpass, nikoli argument nebo zdrojový kód. Schéma 22/23/25 je stejné. Výchozí řeč 24 je náhled bez zvuku, skutečnou volbu dává precti.py --mluv. Windows potřebuje dostupný System.Speech/hlas, macOS say/hlas, Linux espeak-ng či espeak s hlasem cs. Chybějící hlas ostatní lekce neblokuje. Zlib/Base64 není šifrování, export přenáší jen vlastní poznámky. Ukázky jsou dočasné, pro trvalou práci uložte složku; příkazy a význam jsou v lekcích/NAVOD.md. Blok 26–30 propojuje Luhn, volitelný QR, vlastní unittest a půjčovnu s CSV, SQLite backup a předáním. Pro PNG do stejné .venv spusťte python -m pip install "qrcode[pil]>=8.2,<9" nebo v kořeni Akademie python tools/setup_env.py --courses databaze --extras. Bez knihovny se vypíše návod, ostatní části fungují. Uložený spust_pujcovnu.py v 29/30 používá vlastní pujcovna.sqlite3 vedle sebe; --db CESTA před příkazem naváže na dřívější složku. Python overeni.py spustí šest/osm izolovaných testů. Předání kopíruje zdroje s NAVOD.md, .venv se vytváří znovu, data zvlášť. PostgreSQL 31–32 zatím není potřeba.',
    },
}


def course_preparation(cid):
    profile = PROFILES.get(cid)
    if profile is None:
        return None
    return {'course': cid, **profile, 'packages': PACKAGES[cid],
            'optional_packages': OPTIONAL_PACKAGES.get(cid, [])}
