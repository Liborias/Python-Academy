# Předávací dokument: Dílna Pythonu

> **Aktuální v0.40:** Na uživatelovo „pokračuj“ dokončen m05 původního Turtle/OOP, lekce 25–28: speciální metody, identita/rovnost, MRO a dataclass. Kurz má 28/40 lekcí. Nový samostatný `oop` nadále pouze koncept — nepřesouvat do něj dosavadní obsah a neimplementovat ho bez nového zadání. Další blok původního kurzu je Snake (orientačně 29–36), pak kvíz/API (37–40); pracovat po dávkách přibližně čtyř lekcí. Nové kontroly zkouší 35 chybných a 8 správných alternativ, v prohlížeči ověřeny ukázky, řešení i zachování kódu a postupu. Úplné výsledky jsou v posledním STATUS.md. Pracovat v `/workspace/Python-Academy`, dodávat přes GitHub/main, bez ZIPů.

> **Aktuální v0.39:** Původní Turtle/OOP pokračuje lekcemi 21–24 (pravidla stavu, property, dědění, super), celkem 24/40. Nově je v katalogu **samostatný koncept OOP** s id `oop`, plán 20 lekcí a obtížnost 3/4, nezávislý na Turtle a hrách. Praktické téma je Chytré expediční centrum, text v courses/oop/plan.md, panel zatím bez výukové implementace. Uživatel výslovně upřesnil: stávající OOP lekce ponechat a nový kurz pouze navrhnout. Nepřesouvat dosavadní obsah a nový koncept zatím neimplementovat. Pracovat v `/workspace/Python-Academy`, změny doručovat přes GitHub/main, bez ZIPů. Ověřeno: 101 testů OK, validátor 119 lekcí bez chyb a 4 prohlížečové testy OK. Viz poslední STATUS.md.


> **Aktuální v0.38:** Uživatel obnovil pokračování Turtle/OOP/Snake. Nový modul m03 má lekce 17–20 (instance, konstruktor, metody/stav, vlastní seznamy), celkem 20/40 lekcí kurzu. Další dávka: zapouzdření a dědění/super(); Snake zatím nevznikl. Obsahové názvy prvních ukázek jsou v example_title místo tlačítka „Původní ukázka“, id original zůstává. Doplněna ICO favicona vedle SVG a verze odkazů. Ověřeno: 95 testů OK, validátor 115 lekcí bez chyb, prohlížečové testy OOP a ukázek OK. Viz poslední STATUS.md. Pracovat v `/workspace/Python-Academy`, změny doručovat přes GitHub/main, nevytvářet ZIPy. Historický zákaz pokračování tohoto kurzu níže je překonán nynějším zadáním; jiné kurzy zůstávají mimo rozsah.


> **Aktuální v0.37:** Uživatel chce odteď verzovat přímo v GitHubu a nevyžaduje další ZIPy. Ve 34 běžných lekcích Základů doplněny čtyři nové úkoly (136 celkem), přepínání Úkol 1–5 s vlastními zadáními, kontrolami, drafty a pracovními soubory. Původní úkoly i jejich uložená data zůstaly zachované. Značky procvičení jsou samostatné. Viz poslední STATUS.md, courses/SCHEMA.md a nový modul web/js/tasks.js. Používejte `/workspace/Python-Academy`. Nové změny určené uživateli commitovat a pushnout do main podle jeho autorizace. Původní obsahový plán je pozastaven; neprovádět historické pokyny k ZIPům níže bez nové žádosti.


> **Git repozitář:** Projekt v0.36 je nyní vložen přímo do kořene `Liborias/Python-Academy`. V cloudu používejte existující checkout `/workspace/Python-Academy`; starší cesty do rozbalených ZIPů níže jsou historické. Změny určené pro místní `git pull` je potřeba commitnout a odeslat do tohoto repozitáře; publikace cloudového prostředí je jiný krok. Uživatel nyní výslovně autorizoval první nahrání aplikace na GitHub. Návod pro lokální kopii a korektury je v `docs/lokalni-projekt-git.md`.


> **Aktuální v0.36:** Na schválení uživatele doplněna vysvětlení příkazů ve všech původních průvodcích přípravy a nová devátá lekce `09-server-a-token`. Úvodní koncept má nyní 15 průvodců. Tři spustitelné soubory v jejím files/ ukazují pevný main.py, server v .venv a ověření tokenu klienta. V lekci jsou přesné postupy pro dva terminály, očekávaný výstup a chybové stavy. Nejde o veřejný server ani automatické nasazení. Původní id dalších lekcí zachována. 87 testů OK, validátor 111 lekcí bez chyb, prohlížečový test přípravy OK. Viz poslední STATUS.md. Nic nepublikováno, původní plán dalších kurzů nepokračuje.


> **Aktuální předání v0.35 (3. 11. 2026):** Na žádost uživatele je v katalogu první koncept „Začínáme: prostředí, projekt a Git“ (`priprava`, 14 průvodců s `kind: guide`, 5 modulů). Není to hotový automaticky kontrolovaný kurz instalace. Každý podkurz má před lekcemi přípravu pro Windows/macOS/Linux a volbu VS Code/VSCodium/PyCharm. Společné návody rozšířeny, volitelné pip balíčky jsou pod `--extras`. Viz poslední STATUS.md a `docs/koncept-priprava.md`. 81 unit testů OK, validátor 110 lekcí bez chyb (96 původních běhově, 14 koncepčních strukturálně), 3 prohlížečové testy OK. Původní plán OOP nepokračoval; čeká se na připomínky ke konceptu. Nic nebylo publikováno. Historické pokyny a omezení pouze na VSCodium níže neplatí proti tomuto novému zadání; aktuální jsou tři editory.


> **Aktuální předání v0.34 (3. 11. 2026):** Uživatel pozastavil pokračování podle plánu a požádal o více přepínatelných příkladů pouze v základním kurzu. Hotovo: 68 nových příkladů v lekcích 01–31 a 37–39; tlačítka nad upravitelným editorem ukázky, oddělené rozepsané varianty, obnova původního kódu. Mini-projekty a navazující kurzy nezměněny. Přečtěte poslední záznam STATUS.md a aktualizované courses/SCHEMA.md. Validátor: 96 lekcí, 0 chyb; 77 unit testů OK; e2e přepínání OK, studentský kód na Pythonu 3.14.8. Neprovádět historické pokyny „další krok“ níže bez nového zadání. Nový kořen rozbaleného projektu v cloudu je `/workspace/dilna-pythonu-v0.33/dilna-pythonu`; původní absolutní cesty v tomto dokumentu jsou historické.


Určeno pro dalšího agenta (nový chat). Stav k **26. 10. 2026, verze v0.14**. Piš česky. Nejdřív přečti tento soubor, pak `STATUS.md` (historie a poučení) a `PLAN.md` (celkový plán).

## 1. Zadání od uživatele (v kostce)
Česká výuková aplikace na procvičování Pythonu postavená z 7 učebnic (zip `bdd6c544-U_ebnice_python.zip`, převedené do markdownu ve scratchpadu původního chatu, `py-md/b1.md` až `b7.md`: b1 Datová analýza, b2 Pygame, b3 soubory a web scraping, b4 Tkinter/API/e-maily, b5 začátečník, b6 středně pokročilé, b7 Tkinter a databáze). Požadavky:
- Projekt je stažitelná složka s odděleným html/css/js/py (ne jeden soubor), spouští se `python start.py`.
- Každá učebnice je samostatný podkurz, bez povinného pořadí. Lekce od jednoduchých ke složitým.
- Kód se píše ve **VSCodium** (ne PyCharm). Pro rozšíření, která tam nefungují, jsou alternativy (BasedPyright místo Pylance, Ruff, debugpy).
- Žádné hry s Harry Potterem ani jinými cizími postavami, grafika her jen kódem.
- **Kroky plánovat tak, aby stačil volný limit tokenů (uživatel má free plán).** Po každém kroku napsat, co je hotovo a co bude dál. Uživatel píše „pokračuj“. **Nespouštět více agentů najednou** (revize vždy jedním agentem po druhém, ~100–130 tis. tokenů každý). Uživatel jednou ztratil várku, protože došel limit relace: dělat menší várky a po každé uložit stav.

## 2. Co existuje
Kořen projektu: `/home/claude/dilna-pythonu/` (v novém chatu ho obnov z přiloženého zipu `dilna-pythonu-v0.12.zip`: `unzip`, pak `cd dilna-pythonu`). Pokud zip nepřiložen, najdeš `STATUS.md` a `PLAN.md` také v Projektu (`claude/STATUS-dilna-pythonu.md`, `claude/PLAN-dilna-pythonu.md`, `claude/HANDOVER-dilna-pythonu.md`).

| Podkurz | Stav |
|---|---|
| `zaklady` (Základy Pythonu) | 40 lekcí hotovo a nezávisle zrevidováno (1–15 ve v0.5, 16–40 ve v0.11). Status „draft“, čeká na zpětnou vazbu skutečného studenta |
| `soubory-web` | **22 z 22 lekcí HOTOVO** (m01: 01–06, m02: 07–11, m03: 12–22), kurz celý nezávisle zrevidován (v0.17–v0.19), zbývá zpětná vazba studenta a ověření ve VSCodium/Windows |
| `pygame-1` | **18 z 18 lekcí HOTOVO** (m01: 01–05 okno, smyčka, barvy, tvary, obrázky; m02: 06 Rect, 07 Fonty, 08 Zvuky, 09 Projekt Pohlednice; m03: 10–16 pohyb, klávesy, myš, odrazy, kolize, více objektů, skóre a konec hry; m04: 17–18 Sběratel hvězd). Nezávisle zrevidováno a opraveno (v0.24–v0.26), čeká na zpětnou vazbu a ověření okna a zvuku ve VSCodium. Plán viz oddíl 8 |
| `turtle-oop` | **rozpracováno, 16 z 40 lekcí** (m01 „Kreslení želvou“ hotov: 01 první čára, 02 čtverec a cyklus, 03 mnohoúhelníky a funkce, 04 barvy a tloušťka, 05 vyplněné tvary, 06 kruhy a oblouky, 07 souřadnice, `goto` a dvojice, 08 projekt spirograf). m02 „Zpět k základům“ hotov (09 čísla a typy, 10 řetězce: indexy a řezy, 11 řetězce: metody, 12 seznamy: metody a kopie, 13 řezy seznamů a kopie, 14 dvojice, rozbalování, `enumerate`, `zip`, 15 množiny `set`, 16 projekt analýza textu; kind `console`, kontrola přes `c.returns`). Plán dál: m03 OOP (třída, konstruktor, atributy, metody), čtyři pilíře, dědění, `super()`, dunder metody, MRO, `@property`, `@dataclass`, Snake a kvíz s API (viz `PLAN.md`, C). Lekce `kind: gui`, kontrola přes `turtle_run`. Zrevidováno agentem (lekce 01–16, v0.30 a v0.33) |
| `pandas`, `tkinter-api`, `pygame-2`, `databaze` | prázdné složky, plán v `PLAN.md` a `courses/catalog.json` (status „planned“) |

Další dokumenty: `README.md`, `docs/instalace.md`, `docs/vscodium.md`, `docs/reseni-problemu.md`, `courses/SCHEMA.md` (formát lekce).

## 3. Architektura (stručně)
- `start.py` spustí lokální `http.server` na 127.0.0.1 (jen stdlib), token v `?t=`, kontrola Host a Origin. Student kód běží v podprocesech s timeoutem, limitem výstupu a očištěným prostředím.
- `server/`: `app.py` (API), `runner.py` (spouštění), `checker.py` (kontrola lekce v podprocesu), `content.py` (katalog, pracovní složka), `security.py`, `lessonfiles.py` (kopírování `files/` lekce).
- `lib/dilna_check/__init__.py`: knihovna pro `check.py` lekcí (viz oddíl 5).
- `web/`: ES moduly (router, katalog, lekce, vlastní chytrý editor s našeptávačem a zvýrazněním f-řetězců, kvíz, nastavení).
- `tools/`: `validate_courses.py` (povinná kontrola), `setup_env.py` (venv a balíčky podle podkurzu), `install_extensions.py`, `doctor.py`, `make_zip.py`.
- `tests/`: 62 unittest testů (`python3 -m unittest discover -s tests -q`) a Playwright e2e skripty (`e2e_pilot.py`, `e2e_web.py` atd., spouštět jednotlivě, `timeout 300 python3 tests/e2e_pilot.py`).

## 4. Formát lekce
`courses/<kurz>/lessons/NN-nazev/`: `lesson.json` (`title`, `minutes`, `kind`), `lesson.md`, `example.py` (min. 2 vysvětlující komentáře, musí běžet bez chyby, volitelně `example.stdin`), `exercise.py` (výchozí kód, **nesmí projít kontrolou**), `check.py`, `solution.py` (**musí projít**), `quiz.json` (`q`, `options`, `answer` = index, `why`; možnosti se při zobrazení míchají), volitelně **`files/`** (pomocné soubory, kopírují se vedle kódu při spuštění, kontrole i do pracovní složky; podsložky povolené). Lekce se přidá do `courses/<kurz>/course.json` (moduly). Po každé dávce: `python3 tools/validate_courses.py` (kontroluje soubory, kvíz, komentáře, běh příkladu, že vzorové řešení projde a výchozí kód neprojde).

Kontrola se spouští **v samostatném podprocesu**: `server.checker.run_check(lesson_dir, kód, lib_dir, workdir)`. Student kód je `reseni.py` v dočasné složce (cwd), do které se zkopíruje `files/`. Proměnné prostředí: `DILNA_STUDENT`, `DILNA_RESULT`, `DILNA_DATA`.

## 5. Knihovna dilna_check (co umí)
`c = check()`; `c.load()` (spustí kód studenta s `__name__ = "student"`, takže blok `__main__` se neprovede, vrací jmenný prostor); `c.returns(ns, "f", (args), očekávané)`; `c.returns_close(...)` (desetinná čísla s tolerancí); `c.raises(ns, "f", (args), ValueError)`; `c.call(ns, "f", (args), kwargs, stdin="...")` vrací `(ok, hodnota)` a vypsaný text je v `c.last_output`; `c.run(stdin=...)` pustí soubor jako program; `c.no_error`, `c.output_contains`, `c.output_has_line` (řádek KONČÍ textem); `c.uses(ast.For, hint)`, `c.uses_call("name")`, `c.function("f")` (AST funkce), `c.calls_in(node, "name")`, `c.imports("math")`, `c.utf8()` (každé textové `open`/`read_text`/`write_text` má `encoding`), `c.add(name, ok, msg)`, `c.done()` (nutné na konci).

**Želva bez okna (od v0.27):** `r = c.turtle_run(keys=["Up"], clicks=[(x, y)], ticks=3)` spustí program s náhradou modulu `turtle` (`lib/dilna_check/turtlerun.py`), která si pamatuje kreslení a nic nezobrazuje (kruh je mnohoúhelník jako v pravé želvě). `TurtleResult`: `segments` (`[x1, y1, x2, y2, barva, tloušťka, želva, zdroj]`, zdroj `move`/`goto`/`circle`), `fills`, `dots`, `texts`, `stamps`, `calls`, `turtles` (konečný stav každé želvy), `bgcolor`, `title`, `handlers`, `mainloop`, `ended`, `error`, `out`; metody `called(jméno)`, `length(barva)`, `colors()`, `widths()`, `covers(bod, tol, barva)`, `bbox()`, `corners()` (rohy mezi navazujícími úsečkami; uzavřený n-úhelník jich má n−1, protože za poslední stranou nic nenavazuje), `fill_area(barva)`. Barvy jsou jména malými písmeny nebo `#rrggbb`; RGB trojice se po `colormode` převedou na `#rrggbb`. `c.turtle_no_error(r)`. Klávesy a časovač se spustí při `done()`/`mainloop()`. `c.uses_call("forward|fd", ...)` přijímá alternativy přes `|`. Validátor spouští `example.py` s `import turtle` přes turtlerun. Test: `tests/test_turtlerun.py`. Náhrada od v0.30: barvy se vrací jménem, pokud jde o základní barvu (`#ffff00` → `yellow`), RGB mimo rozsah `colormode` vyhodí `TurtleGraphicsError`, `pos()` vrací `Vec2D`, `t.screen`, `clear`/`reset` mažou, úsečky nulové délky se nezapisují, `speed` se mapuje jako v pravém turtle. Pozor: skutečný turtle potřebuje tkinter (na Linuxu `python3-tk`).

**Pygame bez okna (od v0.20):** `r = c.pygame_run(frames=5, pixels=[(x, y)], colors=[(r, g, b)], events={snímek: [{"type": "KEYDOWN", "key": "K_LEFT"}, {"type": "QUIT"}, {"type": "MOUSEBUTTONDOWN", "pos": [x, y], "button": 1}]}, held={od_snímku: ["K_LEFT"]}, mouse={od_snímku: [x, y]})` spustí program studenta v podprocesu (`lib/dilna_check/pgrun.py`, SDL `dummy`, žádné okno ani zvuk). Program se zastaví po `frames` snímcích (volání `display.flip`/`update`). Hodiny jsou zrychlené (`Clock.tick` vrací 16 ms, zapisuje požadované FPS do `r.fps`). Výsledek `PgResult`: `r.frames`, `r.ended` (program skončil sám), `r.error`, `r.timed_out`, `r.size`, `r.caption`, `r.pixel((x, y), snímek=-1)`, `r.color_count((r, g, b), snímek, region=(x, y, š, v))` (v `pygame_run` pak `colors=[(r, g, b, x, y, š, v)]`), `r.drew("circle")` (volání `pygame.draw`), `r.rendered("text")`, `r.images` (načtené soubory), `r.sounds`, `r.music`, `r.out` (stdout). `c.pg_no_error(r)` zapíše kontrolu „program běží bez chyby“ s užitečnou hláškou. Snímky se číslují od 0; událost ve snímku k dostane program při (k+1). průchodu smyčkou. Barvy kontrolovat na pixelech uvnitř tvarů, ne na hranách. Pozadí lekcí s průhlednými obrázky nesmí být černé, jinak se `convert()` nepozná od `convert_alpha()`. `PYGAME_HIDE_SUPPORT_PROMPT` se nastavuje jen v kontrole; v aplikaci se banner pygame ve výstupu zobrazí.

## 6. Poučení z revizí (dodržuj při psaní nových lekcí)
1. **Pojem nesmí být použit dřív, než je vysvětlen** (i ve vzorovém řešení). Před psaním grepni `lesson.md` předchozích lekcí. Ve skutečnosti se opakovaně přehlédlo: `%`, `//`, `**`, `if __name__`, `enumerate`, `str()`, `is None`, `key=`, `pass`, `isalpha` a podobně.
2. **Kontroly musí odmítnout výsledek zapsaný natvrdo** (více vstupů, krajní případy: prázdný vstup, jedna položka, velká/malá písmena, diakritika). Požadované konstrukce (`try`, `raise`, `seed`, `sorted`) kontrolovat **uvnitř konkrétní funkce** přes AST, ne kdekoliv v souboru.
3. Kontroly nesmí odmítnout správné alternativní řešení (např. nevyžadovat `append`, když jde použít `+`).
4. Náhodné funkce kontrolovat statisticky (pokrytí celého rozsahu, více volání), vzorové řešení ověřit 20× za sebou. U her dosadit tah počítače: `ns["nahodny_tah"] = lambda: "nůžky"`.
5. Pořadí souborů z disku (`glob`, `iterdir`) není zaručené: výsledek testovat s `sorted` a kontrolovat jeho použití přes AST.
6. Každou dávku **zkus špatnými řešeními** (skript volající `run_check` s upravenými vzorovými řešeními) a výchozí kód nesmí projít.
7. Po větším bloku (cca 15–20 lekcí) nezávislá revize jedním agentem (prompt viz minulé revize: dát mu seznam předchozích lekcí, co už je vysvětleno, a pokyn nic needitovat, ověřovat spuštěním).
8. Ve vzorových datech ověřovat fakta spuštěním (chybně označený palindrom, špatný počet samohlásek se chytil až při validaci).
9. Nepoužívej `pkill -f` s vzorem, který se vyskytuje v samotném příkazu (zabije shell). Používej absolutní cesty ve skriptech.
10. Nikdy nespoléhej na to, že kroky ve VSCodium (F5, Ruff, `codium`) fungují: nejsou ověřeny na skutečném VSCodium, formuluj je jako návod a vždy nabídni záložní postup.

## 7. Plán zbývajících lekcí podkurzu `soubory-web` (06–22)
Dávky po 5 lekcích (~20 tis. tokenů). Balíčky `requests` a `beautifulsoup4` jsou v `tools/setup_env.py` pro tento kurz; v testovacím prostředí jsou nainstalované (bs4 4.15, requests 2.34), na studentově počítači je nainstaluje `setup_env.py` do `.venv`.
- **m01:** HOTOVO (01–06, včetně mini-projektu Deník).
- **m02 CSV a JSON:** HOTOVO 07 CSV čtení, 08 DictReader/DictWriter, 09 JSON, 10 Zpracování tabulky (`sorted` s `key` a `lambda` už vysvětleno). 11 Kontakty v JSON je také hotová.
- **m03 Web scraping (offline):** HOTOVO 12–15 (parser nad textem) a 16 `requests` (GET, status_code, text, json), 17 chyby sítě (`raise_for_status`, timeout, opakování), 18 Projekt: ceník knih do CSV, 19 Stahování souborů a obrázků (`wb`, `urljoin`), 20 Etika a `robots.txt` (`RobotFileParser`, User-Agent, pauzy). 21 Opakování (CSV, JSON, HTML offline) a 22 Závěrečný test (sběrač cen: robots.txt, stažení s ošetřením chyb, zpracování, JSON). Podkurz je kompletní.
- **Rozhodnuto (lekce 16–20, offline):** pomocný modul `dilna_web.py` (originál `courses/soubory-web/shared/dilna_web.py`) se do každé lekce, která ho potřebuje, kopíruje jako `files/dilna_web.py` (+ stránky v `files/web/`). Díky mechanismu `files/` je u studenta vedle kódu v aplikaci, v kontrole i ve složce pro VSCodium, aniž by se měnilo `PYTHONPATH`. `spust()` vrací `http://127.0.0.1:<port>`; server umí `/_status/<kód>`, `/_pomalu/<s>`, `/_nestabilni/<jméno>` (2× 500, pak 200), `/_presmerovani`, `/_hlavicky` (JSON s hlavičkami klienta). Při úpravě originálu je nutné přegenerovat kopie (`tests/test_dilna_web.py` hlídá shodu). `check.py` si server spouští sám (`sys.path.insert(0, os.getcwd())`) a předává adresu studentovým funkcím. Dotazy na `time.sleep` se v kontrole zaznamenávají (v hlavním vlákně), server dál čeká doopravdy.
- Obrázky v lekci 19 (`files/web/img/*.png`) jsou drobné 8×8 PNG generované skriptem (binární soubory v `files/` fungují).
- Do `courses/soubory-web/data/` zatím nic nepatří (pomocné soubory jsou u lekcí v `files/`).

## 8. Další podkurzy (po dokončení soubory-web)
Pořadí podle plánu: pygame-1 (okno, kreslení, vstupy, 18; **hotovo, čeká revize;** po revizi pokračovat dalším podkurzem. Obrázky `raketa.png` a `hvezda.png` generuje skript (vlastní kresba, žádné cizí postavy), jsou v `lessons/05-obrazky/files/`; další lekce si je zkopírují do vlastní `files/`), turtle-oop (40), pandas (42, Pandas 3.0 Copy-on-Write), tkinter-api (28), pygame-2 (30), databaze (32, SQLite, parametrizované dotazy). Počty a témata viz `PLAN.md`. Ekosystém: Python 3.14 jako základ, `pygame-ce` místo `pygame`, psycopg 3, Gmail jen s heslem aplikace. U GUI lekcí je `kind: "gui"` (kontrola jen přes AST a funkce).

## 9. Neověřeno a otevřené body
- Instalace rozšíření ve VSCodium, F5 ladění, Jupyter, příkaz `codium`, URI `vscodium://file/...`, Flatpak, winget/brew příkazy.
- Chování na Windows a macOS (testováno jen na Linuxu, Python 3.13), Firefox, Safari, dotykové klávesnice, offline záložní písma.
- Lekce **nečetl žádný skutečný student**. Uživatel se o úrovni a tónu zatím nevyjádřil.
- Dříve se v adresáři `courses/zaklady/lessons/` objevily nezapsané starší lekce `37-opakovani-zaklady`, `38-opakovani-data`, `39-opakovani-chyby-moduly` (a stará verze `40-zaverecny-test`) neznámého původu. Byly přesunuty mimo projekt do scratchpadu původního chatu (`old-lekce/`), lekci 40 přepsala nová verze. V tomto předání nejsou. Pokud je chceš, zeptej se uživatele.
- Zbývá dodělat pro Základy: zpětná vazba, případně změna stavu `draft` na `ready` v `courses/catalog.json`.

## 10. Jak začít v novém chatu
1. Rozbal zip, `cd dilna-pythonu`, ověř: `python3 tools/validate_courses.py` (očekávání: 80 lekcí, 0 chyb) a `python3 -m unittest discover -s tests -q` (62 testů OK).
2. Přečti `STATUS.md` (posledních ~60 řádků) a oddíl 7 výše.
3. Napiš uživateli první větu, co budeš dělat, a pusť se do lekcí 16–20 (requests proti lokálnímu serveru, chyby sítě, projekt scraping, stahování souborů). Skripty na generování lekcí byly jednorázové ve scratchpadu a nejsou součástí projektu: piš lekce přímo do složek, nebo si vytvoř vlastní generátor.
4. Po dávce: validate, špatná řešení, testy, `STATUS.md` dopsat a zrcadlit do Projektu (`Projects` → `project_write` do `claude/STATUS-dilna-pythonu.md`), `python3 tools/make_zip.py /home/claude/dist/dilna-pythonu-v0.N.zip` a poslat uživateli. Číslo verze zvyš v `README.md` a `tools/make_zip.py`.
5. Odpověď končí: co je hotovo, co bude další krok.

**Trvalé pravidlo:** soubor `POKYNY-SPUSTENI.md` (ověření Pythonu, instalace, spuštění) je v kořeni projektu a patří do každého ZIPu (make_zip ho zahrne automaticky). Při změně příkazů nebo voleb ho aktualizovat.
