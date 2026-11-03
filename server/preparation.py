"""Návody přípravy kurzů; balíčky sdílíme s instalačním pomocníkem."""
from tools.setup_env import PACKAGES, OPTIONAL_PACKAGES

PROFILES = {
    'priprava': {
        'focus': 'Začněte instalací Pythonu a výběrem editoru. Git, GitHub a server přijdou až v dalších modulech.',
        'verify': 'import sys; print(sys.executable); print(sys.version)',
        'system': 'Stačí Python a terminál. Git nainstalujete až pro modul Verzování. GitHub účet ani server nejsou potřeba pro první lekce.',
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
        'focus': 'pandas pro tabulky, matplotlib pro grafy, openpyxl pro Excel a ipykernel pro notebooky a buňky # %%.',
        'verify': 'import pandas, matplotlib, openpyxl, ipykernel; print(pandas.__version__)',
        'system': 'V notebooku vyberte jádro ze stejné .venv jako v terminálu. VS Code/VSCodium: rozšíření Jupyter; v PyCharm záleží dostupnost notebooků na verzi a licenci. Záložní postup je obyčejný soubor .py v terminálu. Kurz je zatím plánovaný.',
    },
    'tkinter-api': {
        'focus': 'Tkinter je systémová součást, requests slouží pro HTTP API. PyInstaller je volitelný až pro balení aplikace.',
        'verify': 'import tkinter, requests; print(tkinter.TkVersion); print(requests.__version__)',
        'system': 'Tkinter ověřte na grafické ploše pomocí Pythonu z .venv s volbou -m tkinter. Na Debianu/Ubuntu potřebujete odpovídající python3-tk; na Homebrew python-tk@3.14. Pro lokální e-mailový test nebude potřeba osobní heslo ke schránce. Konkrétní API se doplní s lekcemi; kurz je plánovaný.',
    },
    'pygame-2': {
        'focus': 'Stejné pygame-ce jako v Pygame 1; znalost tříd se hodí z Turtle a OOP.',
        'verify': 'import pygame; print(pygame.version.ver)',
        'system': 'Potřebujete místní grafickou plochu, klávesnici a případně zvuk. Běžný vzdálený server bez plochy herní okno nezobrazí. Kurz je zatím plánovaný.',
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
