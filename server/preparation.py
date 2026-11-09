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
        'system': 'Prvních 20 z 30 lekcí je připravených. Úvod 1–5 a Součásti větší hry 16–20 mají obrázkové pokusy bez okna, tři ukázky a pět úkolů s řešeními na lekci. Meteority 6–10 a Chyť robota 11–15 tvoří souvislé živé hry: šipky nebo myš, v závěru P/R/Escape, u robotů i Mezerník. Živá okna vyžadují místní grafickou plochu na počítači s Pythonem a nepřenášejí se do prohlížeče. Běžné zavření zachová meteority.png či roboti.png; Stop uložení nezaručuje. Laboratoř 16–20 ukládá soucasti.png, vysvětluje cache, animaci, masky, kameru a režimy. Běžné pokusy neotvírají zvukové zařízení. V lekci 16 lze volitelně spustit vlastní tón přes python prehraj_ton.py --play; tento pokus má limit pěti sekund. Úkol 20/5 přidává místní živou dílnu přes python ziva_dilna.py po uložení reseni.py, bez zvuku. Použijte stejnou .venv ve VS Code, VSCodium nebo PyCharm. Ověřeno Python 3.14.8/pygame-ce 2.5.8, žádné nové knihovny ani síťová data. Následuje Hon na dronech 21–25.',
    },
    'databaze': {
        'focus': 'SQLite je v modulu sqlite3 standardní knihovny. Základní databázový kurz nepotřebuje PostgreSQL ani databázový server.',
        'verify': 'import sqlite3; con = sqlite3.connect(\":memory:\"); print(con.execute(\"SELECT 2 + 3\").fetchone()[0]); con.close()',
        'system': 'Ověření vytvoří jen dočasnou databázi v paměti a vypíše 5. Tkinter bude potřeba pro okenní projekty. QR a převod textu na řeč jsou volitelné pozdější projekty; pyttsx3 navíc závisí na hlasovém systému OS. Kurz je plánovaný.',
    },
}


def course_preparation(cid):
    profile = PROFILES.get(cid)
    if profile is None:
        return None
    return {'course': cid, **profile, 'packages': PACKAGES[cid],
            'optional_packages': OPTIONAL_PACKAGES.get(cid, [])}
