# Dílna Pythonu

Česká výuková aplikace pro Python. Každá učebnice je samostatný podkurz, studovat lze v libovolném pořadí, nic se nezamyká. Kód píšete ve VS Code, VSCodium, PyCharm nebo přímo v aplikaci, aplikace ho spouští a kontroluje.

**Stav (v0.45):** úvodní koncept přípravy (15 průvodců), Základy (40 lekcí), samostatné OOP (8 z 20), Soubory a web (22), Pygame 1 (18), Turtle/OOP (40 ze 40). Obsah kurzu Turtle/OOP je dokončený, včetně Snake a kvízu; čeká na připomínky studentů. Další podkurzy jsou plánované, viz `PLAN.md` a `STATUS.md`.

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

## Samostatný OOP kurz — osm připravených lekcí
V katalogu je vedle Základů samostatná karta **Objektově orientované programování v praxi**.
Kurz má osnovu 20 lekcí s náročností **3/4**, bez závislosti na Turtle a hrách.
Nosný praktický projekt „Chytré expediční centrum“ propojí objednávky, zásoby a způsoby doručení.
První blok učí objekt zásilky, konstruktor a self, metody položky a objednávku
s vlastním seznamem položek. Druhý přidává zapouzdření, výjimky před změnou stavu,
property pouze pro čtení a sklad s rezervací celého požadavku, nebo žádné jeho části.
Každá lekce má komentovanou ukázku, úkol s automatickou kontrolou a tři kvízové otázky.
Příprava prostředí je před lekcemi, stačí standardní Python.

Panel zobrazuje dostupné lekce i zbývající plán v [courses/oop/plan.md](courses/oop/plan.md).
Další blok doplní dědění, polymorfismus, super a různé způsoby dopravy. Celé expediční centrum vznikne postupně.

Dosavadní OOP lekce zůstávají na přání uživatele ve stávajícím kurzu Turtle/OOP/Snake.
Po lekcích 21–24 (zapouzdření, property, dědění a super) přibyly lekce 25–28:
speciální metody pro str/repr/len, identita a hodnotová rovnost, pořadí dědění (MRO)
a dataclass s vlastním výchozím seznamem pro každou instanci. Každá má komentovanou
ukázku, úkol s automatickou kontrolou a tři kvízové otázky.

## Projekt Snake: hotová hra v osmi krocích
Lekce 29–36 postupně přidávají model hada na mřížce, zobrazení želvou,
časovač, šipky, potravu a růst, kolize s tělem, skóre a restart.
Hra má průchozí okraje a přijme nejvýš jednu zatáčku mezi dvěma kroky.
Při zaplnění plochy vyhlásí výhru; po střetu s tělem se zastaví.

Hotovou hru spustíte v ukázce lekce 36. Šipky ovládají směr a Enter začne
novou partii i během hraní. Restart obnoví tělo, směr, skóre a potravu;
staré časovače už do nové hry nezasáhnou.

Každá lekce připraví potřebné moduly z předchozích vzorových řešení vedle kódu.
V aplikaci i pracovní složce editoru tak jde pokračovat bez přepisování minulých úkolů.
Grafická část otevírá samostatné okno Turtle na počítači s Pythonem a vyžaduje Tkinter;
vykreslování neprobíhá uvnitř webové stránky. Podrobnosti vysvětluje příprava kurzu a lekce 30.

## Závěrečný kvíz: objekty, JSON a volitelné API
Lekce 37–40 uzavírají kurz modelem otázky a skóre, převodem a kontrolou JSON,
síťovým klientem se zálohou a hotovou konzolovou aplikací. Všechny podklady
jsou v lekcích připravené; další pip balíčky nejsou potřeba.

Ukázku spusťte v lekci 40. Enter při výběru zdroje načte pět přiložených českých
otázek. Odpovídejte **a** nebo **n**, pomocí **q** skončíte s průběžným skóre.
Neplatný vstup zopakuje stejnou otázku. Režim **api** zkusí Open Trivia DB
s anglickými otázkami a při chybě použije českou zálohu s vysvětlující zprávou.
Ukázka API v lekci 39 používá předvídatelnou simulaci úspěchu i výpadku.
Kontroly otázek a klienta jsou nezávislé na dostupnosti veřejné služby.

## Názvy ukázek a favicony
V přepínači ukázek má i první příklad název podle obsahu (například „Planeta Merkur“).
Jeho id a uložené úpravy se nemění. Web používá SVG i ICO faviconu; při staré
ikoně obnovte stránku pomocí Ctrl+F5. Soubory ikon mají v odkazech verzi pro cache.

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
