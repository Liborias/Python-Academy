# Dílna Pythonu: plán projektu

Stav: plán schválený k zahájení. Verze plánu z 23. 10. 2026.
Navazuje na hotovou aplikaci Dílna JavaScriptu (jádro: design, chytrý editor, kvízy, výzvy s automatickou kontrolou, testy v prohlížeči).

---

## 1. Co obsahují učebnice

V archivu je sedm učebnic (celkem asi 600 videolekcí). Každá se stane samostatným podkurzem.

| Podkurz (zdroj) | Lekcí v učebnici | Obsah |
|---|---|---|
| Základy (Python – začátečník) | 88 | print, input, proměnné, typy, podmínky, seznamy, cykly, funkce, slovníky, scope, ladění |
| Soubory a web scraping | 30 | open/with, zápis, try/except, BeautifulSoup, requests, stahování souborů |
| Středně pokročilé | 89 | OOP (4 pilíře, dunder, MRO), Turtle graphics, hra Snake, kvíz s API, „zpět k základům“ (typy, string, list, tuple, set) |
| Tkinter, API a e-maily | 52 | okna a widgety, převodník měn, úkolníček, REST API, odesílání e-mailů |
| Tkinter a databáze | 84 | SQL, PostgreSQL + psycopg2, venv, git, projekty (BMI, registrace, text na řeč, komprese, validace čísla, QR) |
| Datová analýza (Pandas) | 93 | Anaconda + JupyterLab, Series, DataFrame, čištění, filtrování, loc/iloc, graf, text, groupby, CSV a Excel |
| Pygame | 121 | okno, kreslení, obrázky, fonty, zvuk, vstupy, tři hry s Harry Potterem, OOP ve hrách |

---

## 2. Co je dnes jinak (ověřeno ke dni 23. 10. 2026)

### Python a ekosystém
- **Python 3.15.0 vyšel 9. 10. 2026.** Přináší mimo jiné UTF-8 jako výchozí kódování, lazy importy, `frozendict`, rychlejší JIT. Python 3.10 právě skončil podporu.
- **Základ kurzu: Python 3.14.** Má nejširší podporu knihoven. Kurz musí fungovat na 3.12 až 3.15. Python 3.15 se bude testovat jako druhá linie.
- **Upozornění pro macOS 27:** IDLE a tkinter aplikace se mohou při otevření dialogu zaseknout (oznámení k vydání 3.15). Patří do lekce o Tkinteru.
- **Virtuální prostředí jsou povinná.** Moderní Linux a Homebrew blokují `pip install` do systémového Pythonu (PEP 668). V učebnici je venv až v kurzu o databázích, v novém kurzu musí být hned na začátku.
- **Nástroj uv** (open source) je dnes běžná rychlá náhrada za pip a venv. Kurz bude učit standardní `python -m venv` a `pip`, uv bude uvedený jako volitelné zrychlení.
- Novinky, které stojí za zmínku jako bonusy: `match`, lepší chybové hlášky, `pathlib`, `dataclass`, typové anotace, REPL s barvami.

### Prostředí: PyCharm nahrazuje VSCodium
- VSCodium používá registr **Open VSX**. Microsoft rozšíření jsou licencí vázaná na produkty Microsoftu, takže řada z nich ve VSCodium chybí nebo nefunguje ([dokumentace VSCodium](https://github.com/VSCodium/vscodium/blob/master/docs/extensions.md), [diskuse](https://github.com/VSCodium/vscodium/discussions/2286)).
- **Pylance (jazykový server od Microsoftu) ve VSCodium nelze použít.** Náhrady: **BasedPyright** (nabízí kontrolu typů, našeptávání, přechod na definici), případně **Jedi** (nastavení v rozšíření Python, viz [diskuse VSCodium](https://github.com/VSCodium/vscodium/issues/1724)).
- Na Open VSX se podle výsledků vyhledávání nachází: [Python](https://open-vsx.org/extension/ms-python/python), [Python Debugger](https://www.open-vsx.org/extension/ms-python/debugpy), [Jupyter](https://open-vsx.org/extension/ms-toolsai/jupyter), [Ruff](https://open-vsx.org/extension/charliermarsh/ruff), [BasedPyright](https://open-vsx.org/extension/detachhead/basedpyright), [Pyright](https://open-vsx.org/extension/ms-pyright/pyright).
- **Neověřeno prakticky:** jestli se všechna tato rozšíření v dnešním VSCodium nainstalují a spolupracují. Krok F7 proto obsahuje kontrolní seznam a záložní řešení (viz níže). Do té doby tuto část považujeme za pracovní předpoklad.
- **Záložní řešení bez rozšíření:** spouštění souboru přes `tasks.json` a klávesu F6 funguje i bez rozšíření Python. Ladění přes `debugpy` a `launch.json`. Ruční instalace `.vsix` (podle dokumentace VSCodium).
- **Debugger:** učebnice popisuje ladění ve Visual Studio Code. Lekce se přepíše pro VSCodium (rozšíření Python Debugger, `launch.json`).

### Knihovny a služby, které se změnily
| Téma | Učebnice | Dnes | Co s tím |
|---|---|---|---|
| Pygame | `pip install pygame` | Původní pygame má poslední vydání z 9/2024 a pro Python 3.14 nemá wheel, instalace padá ([diskuse](https://discuss.python.org/t/trouble-installing-pygame-on-python-3-14/106397)). | Používáme **pygame-ce** (komunitní fork, `import pygame` zůstává stejný). Verze 2.5.8 z 8/2026 má wheely pro Python 3.10 až 3.15 ([PyPI](https://pypi.org/project/pygame-ce/)). |
| Pandas | Pandas 2 | **Pandas 3.0 (21. 1. 2026)**: Copy-on-Write (řetězené přiřazení `df[...]["b"] = 0` už nic nezmění, `SettingWithCopyWarning` zmizel), výchozí textový typ `str` místo `object`, datum s jednotkami (us, s) místo nanosekund, minimum Python 3.11 ([co je nového](https://pandas.pydata.org/docs/whatsnew/v3.0.0.html)). | Přepsat lekce o view/copy, o přiřazení hodnot a o typech sloupců. Vždy `df.loc[maska, "sloupec"] = hodnota`. |
| Anaconda | Anaconda Navigator + JupyterLab | Zbytečně těžké. | `venv` + `pip install pandas matplotlib openpyxl`. Notebooky přes rozšíření Jupyter ve VSCodium, záložně JupyterLab nebo Google Colab. |
| psycopg2 | psycopg2 + PostgreSQL | Vývojáři doporučují pro nové projekty **psycopg 3**, psycopg2 se jen udržuje ([FreeBSD](https://reviews.freebsd.org/D48493)). | Hlavní větev s **SQLite** (součást Pythonu, žádná instalace). PostgreSQL + psycopg 3 + pool jako volitelný blok. |
| E-maily přes Gmail | přihlášení běžným heslem | Běžné heslo Google od 5/2025 nepřijímá. Je nutné dvoufázové ověření a **heslo aplikace**, nebo OAuth. Limit 500 zpráv denně ([Nylas](https://developer.nylas.com/docs/cookbook/email/gmail-smtp-settings/)). | Výuka přes lokální testovací SMTP server (nic se neodešle, nic se neriskuje). Gmail jako volitelná lekce, heslo jen v proměnné prostředí. |
| Web scraping | Senam.cz, cizí PDF | Cizí weby se mění a scraping může porušovat podmínky. | Cvičné weby určené pro scraping, místní HTML ukázky pro offline testy, lekce o `robots.txt` a etice. |
| Veřejná API | měny, ISS, „urážky“ | Dostupnost se mění a „urážky“ nejsou vhodné pro výuku. | Každé API ověřit při psaní lekce. Ke každému **mock server** s uloženými odpověďmi, aby lekce fungovala offline a testy byly stabilní. Téma „urážky“ nahradí „rada dne“. |
| Text na řeč | gTTS (online služba Google) | Spolehlivost neověřena. | Hlavní varianta offline (`pyttsx3`), gTTS volitelně. Ověřit při psaní lekce. |
| Hesla | hashování | Zásadní je správný postup. | `hashlib.scrypt` se solí, žádné MD5 ani SHA bez soli. |
| Pythonový výstup do souborů | `open("x.txt")` | Od Pythonu 3.15 je UTF-8 výchozí, dříve záleželo na systému (Windows). | Učíme vždy `encoding="utf-8"`. |

---

## 3. Podkurzy, pořadí od jednoduchých ke složitým

V aplikaci jsou podkurzy **nezávislé**. Student si vybere kterýkoli z nich. Obtížnost a „doporučené předpoklady“ jsou jen informace, nic se nezamyká. Uvnitř každého podkurzu jsou lekce seřazeny od jednoduchých ke složitým (sloučené a přeřazené oproti učebnici tam, kde to dává smysl).

| # | Podkurz | Obtížnost | Lekcí | Doporučené předpoklady |
|---|---|---|---|---|
| A | Základy Pythonu | ★☆☆☆☆ | 40 | žádné |
| B | Soubory a web scraping | ★★☆☆☆ | 22 | A (funkce, seznamy) |
| G1 | Pygame 1: okno, kreslení, vstupy | ★★☆☆☆ | 18 | A |
| C | Turtle, OOP a hra Snake | ★★★☆☆ | 40 | A |
| F | Datová analýza v Pandas | ★★★☆☆ | 42 | A (slovníky, seznamy) |
| D | Okenní aplikace (Tkinter), API a e-maily | ★★★☆☆ | 28 | A, B |
| G2 | Pygame 2: hry s třídami | ★★★★☆ | 30 | A, C (OOP), G1 |
| E | Databáze a projekty | ★★★★☆ | 32 | A, D |

Pygame z učebnice se dělí na dva podkurzy (G1 a G2), protože první polovina je jednoduchá a druhá vyžaduje OOP. V seznamu v aplikaci je vedle sebe, ale je to jedna učebnice. Celkem asi **252 lekcí** (učebnice mají asi 600 videí, hodně z nich jsou krátká opakování a „procvičování“, která se spojí).

### A. Základy Pythonu (40 lekcí)
Moduly: Začínáme (Python, VSCodium, venv, první program, chyby) · Proměnné a vstup · Čísla a výpočty · Podmínky a logika · Seznamy · Cykly · Moduly a náhoda · Funkce a rozsah platnosti · Slovníky · Ladění v VSCodium · Projekty.
Nová témata projektů místo Harryho Pottera a podobných: interaktivní příběh „Expedice na Mars“, hádej planetu, šibenice se zvířaty, vyšší nebo nižší (města a obyvatelé), aukce, Caesarova šifra, kalkulačka plateb.

### B. Soubory a web scraping (22 lekcí)
Moduly: Čtení a zápis souborů (`with`, `pathlib`, UTF-8) · Chyby (`try`, `except`) · CSV a JSON (nově) · Scraping základy (`requests`, `BeautifulSoup`, selektory) · Ukládání a stahování souborů · Etika a pravidla (`robots.txt`).
Projekty: hromadné dopisy s proměnlivým oslovením, sběrač citátů, sledování cen ve cvičném e-shopu, stahování obrázků z cvičné stránky.

### G1. Pygame 1: základy (18 lekcí)
Okno a smyčka · barvy a tvary · obrázky · fonty · zvuky a hudba · klávesy a myš · FPS a pohyb.
Mini-hra **Sběratel hvězd**: raketa sbírá hvězdy, skóre, zvuk (náhrada za „dýně“).

### C. Turtle, OOP a hra Snake (40 lekcí)
Stav po v0.42: 36 lekcí, moduly m01–m07 jsou hotové. Snake má osm kroků (29–36): model, zobrazení, časovač, šipky, potrava/růst, kolize s tělem, skóre/stav partie a hotová hra s restartem. Průchozí okraje zůstávají pravidlem varianty. Číslo generace zneplatní staré časovače i při restartu během update; drží se jedna zatáčka na krok. Ve files/ jsou předchozí vzorová řešení, jejich shodu hlídají test_snake_start.py a test_snake_finish.py.
Další dávka 37–40: kvíz s API a offline daty, uzavření původního kurzu 40 lekcemi. Připravit malý datový model otázky/partie, lokální předvídatelná data pro úkoly a testy a srozumitelnou obsluhu selhání vzdáleného API. Nespoléhat na dostupnost internetu během automatické kontroly. Nové pojmy musí být vysvětleny před použitím.
Konkrétní další dávka se provede na uživatelovo pokračování; ostatní podkurzy se nerozšiřují automaticky.

Pořadí od nejjednoduššího: Turtle (kreslení, tuple, spirograf) · Opakování typů a řetězců („zpět k základům“) · seznamy a slicing, `set`, rozbalování · Úvod do OOP (class, konstruktor, atributy, metody) · Čtyři pilíře, dědění, `super()`, dunder metody, MRO, `@property`, `@dataclass` (novinka) · Projekty: **Snake**, kvíz s API (Open Trivia DB, s mockem).

### F. Datová analýza v Pandas (42 lekcí)
Moduly: Prostředí (venv, Jupyter ve VSCodium, záložně Colab) · Series · DataFrame · načítání dat · čištění · filtrování · `loc` a `iloc` · změny hodnot (**s Pandas 3.0**) · vizualizace (matplotlib) · práce s textem · `groupby` · CSV a Excel.
Lekce jsou ve formátu `# %%` (buňky), takže jdou spustit v Jupyteru i jako obyčejný skript.
Datové sady: vlastní malé vymyšlené sady (kavárna, planety, filmy, ceny) generované skriptem. Žádný Bond. Odkazy na otevřená data jako doplněk.

### D. Okenní aplikace, API a e-maily (28 lekcí)
Tkinter základy (okno, Label, Button, Entry, `pack`, `grid`, `place`, `ttk`) · Převodník měn · Úkolníček (Listbox, Scrollbar, ukládání do JSON) · API (REST, stavové kódy, chyby, `requests`) · Převodník měn 2.0 · E-maily přes lokální testovací server, Gmail volitelně · Balení do spustitelného souboru (PyInstaller, ověřit podporu Pythonu 3.14/3.15).

### E. Databáze a projekty (32 lekcí)
SQL základy (SQLite) · CRUD z Pythonu · **parametrizované dotazy a SQL injection** · venv a git (Git je ve VSCodium zabudovaný) · Tkinter a databáze (evidence kroužků místo učitelů) · BMI tracker · registrace a přihlášení (scrypt) · text na řeč (offline) · komprese souborů (`zlib`, `base64`) · kontrolní číslice (Luhn na zkušebních číslech) · generátor QR kódů · volitelně PostgreSQL + psycopg 3 + connection pool.

### G2. Pygame 2: hry s třídami (30 lekcí)
Tři hry místo Harryho Pottera (všechny nové, všechna grafika kreslená kódem):
1. **Meteority**: uhýbání před padajícími meteority, životy, skóre, štít jako bonus (náhrada za „Goblet of Fire“).
2. **Chyť robota**: klikání na pohybující se cíle, počítání skóre a životů (náhrada za „Útok mozkomora“).
3. **Hon na dronech**: třídy `Hra`, `Hrac`, `Dron`, kola, bezpečná zóna, pauza, restart (náhrada za „Bitva s mozkomory“).
OOP lekce (class, metody, dědění, přepisování metod) jsou v učebnici na příkladu aut. Zůstanou s novým tématem (zvířata v zoo).
Zabalení hry pro kamaráda (PyInstaller, zmínka o pygbag pro web).

---

## 4. Architektura projektu

Projekt není jeden soubor. Je to složka, kterou student rozbalí a spustí příkazem `python start.py`.

```
dilna-pythonu/
├── README.md                 návod pro studenta
├── PLAN.md                   tento plán
├── STATUS.md                 co je hotové a co je další krok (pro pokračování)
├── start.py                  spustí místní server a otevře prohlížeč (jen standardní knihovna)
├── server/                   místní server (stdlib: http.server, subprocess, threading)
│   ├── app.py                směrování, statické soubory, API
│   ├── runner.py             spuštění kódu: časový limit, stdin, výstup po částech
│   ├── checker.py            spuštění kontrol lekce
│   ├── security.py           token, kontrola Origin a Host
│   └── workspace.py          práce se složkou studenta
├── web/                      to, co vidí prohlížeč
│   ├── index.html
│   ├── css/                  tokens.css, layout.css, lesson.css, editor.css, components.css
│   └── js/
│       ├── app.js, router.js, store.js (postup)
│       ├── catalog.js, lesson.js, markdown.js, quiz.js, exam.js
│       ├── runner-client.js
│       └── editor/           highlight.js, smart.js, autocomplete.js, format.js, help.js
├── courses/
│   ├── catalog.json          seznam podkurzů, obtížnost, předpoklady
│   └── <podkurz>/
│       ├── course.json       moduly a pořadí lekcí
│       ├── data/             CSV, HTML ukázky, mock odpovědi API
│       └── lessons/NN-nazev/
│           ├── lesson.md     výklad
│           ├── example.py    ukázka s komentáři
│           ├── exercise.py   zadání (šablona řešení)
│           ├── check.py      kontrola (používá dilna_check)
│           ├── solution.py   vzorové řešení
│           └── quiz.json
├── workspace/                řešení studenta (jeho kopie exercise.py), otevírá se ve VSCodium
├── lib/dilna_check/          pomocná knihovna pro kontroly (výstup, vstup, AST, funkce)
├── tools/                    validate_courses.py, doctor.py, make_assets.py, make_datasets.py, mock_api.py
├── tests/                    testy serveru, kontrol a obsahu
├── docs/                     instalace VSCodium, řešení problémů, přehled změn
└── .vscode/                  extensions.json, settings.json, tasks.json, launch.json
```

### Jak se spouští kód
1. **Student píše ve VSCodium** do `workspace/<podkurz>/<lekce>/reseni.py`. V aplikaci je tlačítko „Otevřít ve VSCodium“ (odkaz `vscodium://file/…`, záložně příkaz `codium`).
2. **Aplikace spouští a kontroluje** přes místní server: tlačítko „Spustit“ (včetně `input()` přes okno vstupu) a „Zkontrolovat“.
3. **Okno Tkinter nebo Pygame** se při spuštění otevře na počítači studenta. Takové lekce se kontrolují strukturou kódu (AST) a funkcemi, ne okny.
4. **Volitelně později:** režim bez serveru přes Pyodide (jen čistý Python, bez oken).

### Bezpečnost místního serveru
Server spouští kód, a proto: poslouchá jen na `127.0.0.1`, vyžaduje náhodný token, kontroluje hlavičky `Origin` a `Host` (ochrana proti cizím webům), omezuje čas a velikost výstupu, běží ve složce `workspace`. Testy tohoto jsou povinné (krok F8).

### Co se přebírá z Dílny JavaScriptu
Design a světlý i tmavý režim, rozložení s postranním seznamem lekcí, kvízy, závěrečný test, ukládání postupu, chytrý editor (odsazování, závorky, našeptávač, zarovnání, nápověda v okně). Rozdíl: odsazování 4 mezery (PEP 8), po `:` se odsazuje, nabídky pro Python.

---

## 5. Kroky a rozpočet tokenů

Každý krok je navržený tak, aby se vešel do **zhruba 25 000 tokenů** (psaní, spuštění a oprava). Čísla jsou odhad z předchozího projektu, kde šest lekcí zabralo asi 15 až 20 tisíc tokenů. Pokud je váš limit nižší, krok se rozdělí na polovinu (pravidlo níže).

### Pravidla pro každý krok
1. Na začátku si přečtu `PLAN.md` a `STATUS.md`. Nic nepředpokládám z paměti.
2. Dělám **jen jeden krok**. Když vidím, že limit nestačí, zastavím se v bezpečném bodě (hotové soubory + aktualizovaný `STATUS.md`), ne uprostřed souboru.
3. Lekce píšu po pěti. Po napsání spustím `tools/validate_courses.py`: spustí každý příklad, ověří, že vzorové řešení projde kontrolou a že výchozí šablona neprojde.
4. Na konci kroku **vždy napíšu**: co jsem udělal (soubory, výsledek kontrol), co je další krok a odhad jeho tokenů.
5. `STATUS.md` obsahuje tabulku kroků, hotové lekce a otevřené otázky. Nový rozhovor začíná slovem „pokračuj“.
6. Co nemůžu ověřit v tomto prostředí (VSCodium, macOS, Windows, živá API), označím jako **neověřeno** a přidám to do kontrolního seznamu pro vás.

### Základ (jednou pro všechny podkurzy)
| Krok | Co vznikne | Odhad |
|---|---|---|
| F1 | Kostra složek, `start.py` (hledá Python, vytvoří venv, spustí server), `catalog.json`, `STATUS.md`, schémata `course.json` a `lesson` | 12 k |
| F2 | Místní server: statické soubory, `/api/run` se vstupem `input()` a výstupem po částech, časový limit, token a kontrola Origin; testy serveru | 22 k |
| F3 | Knihovna `dilna_check` (kontrola výstupu, simulovaný vstup, volání funkcí studenta, AST kontroly, pygame bez okna), `/api/check`, `tools/doctor.py` (zkontroluje Python, venv, Tk, pygame-ce, pandas, `codium`) | 20 k |
| F4 | Web: `index.html`, CSS (tokeny, světlý a tmavý režim), router, **katalog podkurzů** s obtížností a postupem | 20 k |
| F5 | Web: stránka lekce (vlastní jednoduchý Markdown, příklad se spuštěním, okno vstupu, kvíz, výzva s kontrolou, otevření ve VSCodium) | 22 k |
| F6 | Editor pro Python: zvýraznění, odsazování 4 mezery a po `:`, závorky, našeptávač (klíčová slova, vestavěné funkce, úryvky), zarovnání, nápověda v okně | 22 k |
| F7 | Prostředí: `.vscode/` (doporučená rozšíření z Open VSX, nastavení, úlohy `tasks.json`, `launch.json`), `docs/instalace` pro Windows, macOS a Linux, stránka „Příprava prostředí“ v aplikaci, kontrolní seznam rozšíření a záložní řešení | 18 k |
| F8 | Pilotní podkurz (3 lekce), `validate_courses.py`, e2e testy v prohlížeči, bezpečnostní testy serveru | 20 k |
| F9 | Zabalení do ZIP, README, doručení | 8 k |

Základ celkem asi 165 000 tokenů.

### Podkurzy
Každý podkurz má stejný rytmus: **O** (osnova a `course.json`), **L1 až Ln** (po 4 až 5 lekcích), **T** (závěrečný test podkurzu a kontrola celku).

| Podkurz | Lekcí | O | Kroky L | T | Odhad celkem |
|---|---|---|---|---|---|
| A Základy | 40 | 8 k | 8 | 10 k | 180 k |
| B Soubory a web | 22 | 6 k | 5 | 8 k | 115 k |
| G1 Pygame 1 | 18 | 6 k | 4 | 8 k | 95 k |
| C Turtle, OOP, Snake | 40 | 8 k | 8 | 10 k | 180 k |
| F Pandas | 42 | 8 k | 9 | 10 k | 195 k |
| D Tkinter, API, e-maily | 28 | 7 k | 6 | 9 k | 130 k |
| G2 Pygame 2 | 30 | 8 k | 6 | 10 k | 130 k |
| E Databáze a projekty | 32 | 8 k | 7 | 10 k | 150 k |

Podkurzy celkem asi 1 175 000 tokenů, s základem **zhruba 1,3 milionu**. Je to velký projekt. Proto jde dělat po částech:
- **Minimální použitelná verze:** základ + podkurz A = asi 350 000 tokenů (cca 17 kroků).
- **Zkrácená varianta:** 4 lekce na krok a o třetinu méně lekcí v každém podkurzu, celkem asi 0,9 milionu.
- Pořadí podkurzů po základu volí student zadání. Doporučené pořadí: A, pak B, G1, C, F, D, G2, E.

### Závěr
| Krok | Co vznikne | Odhad |
|---|---|---|
| Z1 | Společná stránka „Závěrečný test“ přes podkurzy, doladění vzhledu, přístupnost | 15 k |
| Z2 | Dokumentace pro učitele (jak přidat lekci a podkurz), přehled změn proti učebnicím | 10 k |
| Z3 | Volitelně: režim bez serveru (Pyodide) a statický náhled lekcí jako artifact | 20 k |

---

## 6. Co je třeba potvrdit nebo ověřit

1. **Kde poběží aplikace:** Navržená je jako stažitelná složka se spuštěním přes `python start.py`, protože jen tak se dají spouštět okna Tkinter a Pygame. V prostředí artifact v Claude se Python spustit nedá. Můžu ale přidat statický náhled lekcí.
2. **Python 3.14 jako základ** (3.15 jako druhá linie). Souhlasíte?
3. **SQLite jako hlavní databáze** místo PostgreSQL. Souhlasíte?
4. **Ověřit na vaší straně:** instalace rozšíření (Python, Python Debugger, Jupyter, BasedPyright, Ruff) ve vašem VSCodium. V kroku F7 dostanete kontrolní seznam s tím, co zkusit a co dělat, když něco nejde. Já to tady vyzkoušet nemůžu.
5. **Dostupnost API, gTTS a PyInstaller na Pythonu 3.14/3.15** ověřím při psaní příslušných lekcí. Lekce budou mít záložní řešení bez internetu.

---

## 7. Zdroje

- [Python 3.15.0 final](https://blog.python.org/2026/10/python-3150-final-is-here/) a [oznámení rc3](https://www.warp2search.net/story/python-3150rc3-release-candidate-announced-stable-release-set-for-october-9-2026/)
- [pandas 3.0 – co je nového](https://pandas.pydata.org/docs/whatsnew/v3.0.0.html)
- [pygame na Pythonu 3.14](https://discuss.python.org/t/trouble-installing-pygame-on-python-3-14/106397), [pygame-ce na PyPI](https://pypi.org/project/pygame-ce/)
- [VSCodium: rozšíření](https://github.com/VSCodium/vscodium/blob/master/docs/extensions.md), [Microsoft rozšíření ve VSCodium](https://github.com/VSCodium/vscodium/discussions/2286), [Pylance a Jedi](https://github.com/VSCodium/vscodium/issues/1724)
- Open VSX: [Python](https://open-vsx.org/extension/ms-python/python), [Python Debugger](https://www.open-vsx.org/extension/ms-python/debugpy), [Jupyter](https://open-vsx.org/extension/ms-toolsai/jupyter), [Ruff](https://open-vsx.org/extension/charliermarsh/ruff), [BasedPyright](https://open-vsx.org/extension/detachhead/basedpyright)
- [Gmail SMTP](https://developer.nylas.com/docs/cookbook/email/gmail-smtp-settings/)
- [psycopg 3 vs psycopg2](https://reviews.freebsd.org/D48493)

## Samostatný podkurz OOP — návrh z v0.39

Uživatel si přál samostatný OOP kurz bez Turtle a her. Návrh 20 lekcí je v
`courses/oop/plan.md`, projekt Chytré expediční centrum, celková obtížnost 3/4.
V katalogu je pouze koncept s planned_lessons=20 a bez hotových lekcí. Zatím
neimplementovat výukový obsah ani projekt. Na výslovné upřesnění uživatele
zůstávají dosavadní OOP lekce v původním kombinovaném kurzu; nic nepřesouvat.
Návrh nepřidává nové realizované lekce do původního plánu 40 lekcí Turtle/OOP.
