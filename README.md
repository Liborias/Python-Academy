# Dílna Pythonu

Česká výuková aplikace pro Python. Každá učebnice je samostatný podkurz, studovat lze v libovolném pořadí, nic se nezamyká. Kód píšete ve VS Code, VSCodium, PyCharm nebo přímo v aplikaci, aplikace ho spouští a kontroluje.

**Stav (v0.37):** úvodní koncept přípravy (15 průvodců), Základy (40 lekcí), Soubory a web (22), Pygame 1 (18), Turtle/OOP (16 ze 40). Další podkurzy jsou plánované, viz `PLAN.md` a `STATUS.md`.

## Aktualizace z GitHubu

Projekt je uložen přímo v kořeni repozitáře `Liborias/Python-Academy`.
Po prvním `git clone` přejděte do jeho složky a použijte rychlý start níže.
Pro další aktualizace na čisté větvi main použijte `git pull --ff-only origin main`.
Balíčky a virtuální prostředí se připravují na každém počítači zvlášť.
Podrobný návod včetně vlastních korektur: [Místní projekt a Git](docs/lokalni-projekt-git.md).

## Rychlý start

1. Nainstalujte Python 3.12 nebo novější (ideálně 3.14) a jeden editor podle vlastní volby. Návod: `docs/instalace.md`; stručné příkazy: `POKYNY-SPUSTENI.md`.
2. V terminálu ve složce projektu:
   ```
   python tools/setup_env.py --courses zaklady # vytvoří .venv jen pro základní kurz (Windows: python, macOS/Linux: python3)
   python tools/install_extensions.py # doporučená rozšíření do VSCodium (volitelné)
   python tools/doctor.py             # kontrola prostředí
   python start.py                    # spustí aplikaci a otevře prohlížeč
   ```
3. Otevřete adresu, kterou `start.py` vypíše (obsahuje token). V aplikaci je stránka **Příprava prostředí**.

Aplikace běží jen na vašem počítači (`127.0.0.1`), nic se neodesílá na internet. Webová písma se načítají z Google Fonts, bez internetu se použijí systémová.

## Začínáme: prostředí, projekt a Git (koncept)
Na prvním místě katalogu je návrh úvodního podkurzu: 15 průvodců v pěti modulech.
Provede vás instalací, výběrem VS Code/VSCodium/PyCharm, vlastním projektem,
virtuálním prostředím, místním serverem, spouštěním přes token, Gitem a GitHubem. Virtuální server
je volitelný závěr. Jde o koncept s praktickými kroky a vlastním ověřením,
ne o automaticky ověřenou instalaci na vašem počítači. Návrh viz `docs/koncept-priprava.md`.

Každý podkurz včetně plánovaných má před lekcemi přípravu s volbou systému a editoru,
seznamem konkrétních balíčků a příkazy pro ověření. Rozšířená stránka Příprava prostředí
obsahuje i návody pro všechny tři editory. Tlačítko „Otevřít ve VSCodium“ v samotné lekci
má původní funkci; v jiném editoru otevřete vypsaný soubor ručně.

## Pět úkolů na procvičení
V běžných lekcích Základů (01–31 a 37–39) přepínají tlačítka **Úkol 1 až Úkol 5**
mezi původním úkolem a čtyřmi novými. Každý má vlastní zadání, rozepsaný kód,
kontrolu a pracovní soubor pro externí editor. Nových úkolů je celkem 136.
Úkol 1 zachovává původní uložený kód i návaznost na splnění lekce. Nové úkoly mají
vlastní značky úspěšného procvičení. „Začít znovu“ obnoví jen právě vybraný úkol.
Mini-projekty 32–36, závěrečný test 40 a ostatní kurzy zůstávají beze změn.

Další verze doručujeme přímo přes GitHub; ZIP není potřeba.

## Další příklady v Základech
V lekcích 01–31 a 37–39 jsou nad editorem ukázky tři tlačítka: původní ukázka
a dva nové příklady. Vybraný příklad můžete upravit a spustit. Jeho úpravy se
ukládají v tomto prohlížeči odděleně pro každý příklad; tlačítko **Obnovit příklad**
vrátí původní kód jen vybrané ukázky. Vlastní úkol níže zůstává oddělený.
Mini-projekty, závěrečný test a další podkurzy mají původní chování.

## Co obsahuje

- `start.py` spuštění, `server/` místní server (jen standardní knihovna Pythonu)
- `web/` stránka aplikace (HTML, CSS, JS moduly, chytrý editor kódu)
- `courses/` podkurzy a lekce (`courses/SCHEMA.md` popisuje formát)
- `lib/dilna_check/` knihovna pro kontrolu cvičení
- `tools/` `setup_env.py`, `doctor.py`, `install_extensions.py`, `validate_courses.py`
- `docs/` instalace, VSCodium, řešení problémů
- `tests/` testy

## Přidání lekce

Zkopírujte složku `courses/zaklady/lessons/01-prvni-program`, upravte soubory, přidejte id do `courses/<podkurz>/course.json` a spusťte `python tools/validate_courses.py`. Vzorové řešení musí projít kontrolou a výchozí šablona ne.

## Testy

```
python -I -m unittest discover -s tests
```
Testy v prohlížeči (potřebují `pip install playwright` a `playwright install chromium`): `python tests/e2e_web.py`, `e2e_lesson.py`, `e2e_editor.py`, `e2e_setup.py`, `e2e_pilot.py`.

## Bezpečnost

Aplikace spouští kód, který napíšete. Server proto poslouchá jen na `127.0.0.1`, vyžaduje náhodný token a kontroluje hlavičky `Host` a `Origin`. Adresu s tokenem nesdílejte.
