## Cíl
Instalovat jen to, co potřebuji pro vybraný podkurz. Společná výuková aplikace používá jednu `.venv`; vaše jiné projekty mají svá prostředí.

## Praktický krok
Vraťte se do složky `dilna-pythonu`. Na stránce podkurzu nejprve vyberte systém a editor. Tam najdete konkrétní příkazy i ověření. Pomocník je idempotentní: existující prostředí ponechá a doplní balíčky.

- Příprava a Základy: žádné pip závislosti navíc.
- Soubory a web: requests a beautifulsoup4; import se jmenuje bs4.
- Pygame 1 a 2: pygame-ce, import pygame; potřebujete grafickou plochu.
- Turtle/OOP: systémový Tkinter pro turtle, requests pro pozdější API.
- Pandas: pandas, matplotlib, openpyxl a ipykernel. V editoru navíc podpora Jupyter podle jeho možností.
- Tkinter/API: systémový Tkinter a requests. PyInstaller je volitelný až při balení aplikace.
- Databáze: sqlite3 je součást Pythonu. QR a řeč mají volitelné balíčky, PostgreSQL není nutný pro SQLite.

Příklad instalace na Windows: `py -3.14 tools/setup_env.py --courses soubory-web`. macOS/Linux: `python3 tools/setup_env.py --courses soubory-web`. Pro více podkurzů použijte čárky: `--courses pygame-1,turtle-oop`. Příznak `--dry-run` vypíše plán bez instalace; `--extras` přidá volitelné balíčky zvoleného podkurzu.

Tkinter neinstalujte přes pip. Na Debianu/Ubuntu je to odpovídající `python3-tk`; u Homebrew Pythonu 3.14 `python-tk@3.14`. Na grafické ploše ověřte Pythonem z prostředí `-m tkinter` a zavřete zkušební okno.

## Co příkazy dělají a co se děje
Například `python3 tools/setup_env.py --courses soubory-web` spustí soubor pomocníka, nikoli samotné lekce. Argument `--courses` vybírá profil; seznam za ním určuje požadované balíčky. Pomocník vytvoří `.venv`, pokud neexistuje, a instaluje do jejího Pythonu. Existující prostředí automaticky nepřepíná na jinou řadu Pythonu, proto ověřte vypsanou verzi.

`--dry-run` vypíše cíl a balíčky bez změn. `--extras` přidá volitelné součásti příslušného profilu. Tkinter je mimo pip: například `brew install python-tk@3.14` doplní Tk pro odpovídající Homebrew Python. Příkaz s Pythonem z `.venv` a `-m tkinter` otevře malé zkušební okno. To potvrzuje, že funguje i grafické prostředí, nejen import modulu.

## Vlastní ověření
- [ ] Znám požadované i volitelné součásti svého kurzu.
- [ ] Po instalaci projde importní ověření z jeho přípravy a `-m pip check`.
- [ ] GUI ověřuji místně, ne jen na serveru bez plochy.
