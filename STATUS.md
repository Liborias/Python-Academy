# STATUS – Dílna Pythonu

Plán: PLAN.md. Nový rozhovor začněte slovem „pokračuj“, přečtu tento soubor.

## Rozhodnutí
- Stažitelná složka, spouští se `python start.py` (potvrzeno implicitně, uživatel řekl „pokračuj“).
- Základ Python 3.14, testováno i 3.15; SQLite jako hlavní databáze; pygame-ce.

## Kroky
| Krok | Stav |
|---|---|
| F1 Kostra, start.py, catalog.json, schémata | HOTOVO |
| F2 Server: /api/run (vstup, limit, stop), token, Host, Origin, 17 testů | HOTOVO (/api/check přijde v F3) |
| F3 dilna_check, /api/check, doctor.py, 11 testů | HOTOVO |
| F4 Web: vzhled, router, katalog, e2e test | HOTOVO |
| F5 Stránka lekce (Markdown, ukázka, vstup, kvíz, kontrola, VSCodium) | HOTOVO |
| F6 Editor pro Python (zvýraznění, odsazování, závorky, našeptávač, zarovnání, nápověda) | HOTOVO |
| F7 VSCodium: .vscode, docs, kontrolní seznam, setup_env, install_extensions | HOTOVO |
| F8 Pilotní podkurz Základy (5 lekcí), validate_courses.py, bezpečnostní testy | HOTOVO |
| F9 ZIP (tools/make_zip.py), README, doručení v0.1 | HOTOVO |

## Otevřené / neověřeno
- Rozšíření ve VSCodium (Python, debugpy, Jupyter, BasedPyright, Ruff) – ověří uživatel dle F7.
- API, gTTS, PyInstaller na 3.14/3.15 – při psaní lekcí.
- Testováno zde na Pythonu 3.13.

## Poznámky z F4
- Web: ES moduly (api, store, router, util, catalog, app), CSS tokens/layout/components.
- /api/course?id= vrací courses/<id>/course.json (nebo prázdné moduly).
- Test v prohlížeči: `python tests/e2e_web.py [--shots DIR]` (Playwright), ověřuje katalog, filtr, motiv, mobil 380 px.
- Webová písma se načítají z Google Fonts; offline se použijí systémová (záloha je v tokens.css).

## Poznámky z F5
- Server: /api/lesson, /api/workspace (GET), /api/workspace/save a /open (POST), server/content.py.
- Web: lesson.js, markdown.js, runner-client.js, quiz.js, css/lesson.css, js/editor/editor.js (zatím textarea, rozhraní createEditor(el,text,{readOnly,onChange}) -> {get,set,onRun} zůstane i pro F6).
- Test: `python tests/e2e_lesson.py [--shots DIR]` (fixtures v tests/fixtures/demo).
- Neověřeno: skutečné spuštění VSCodium příkazem `codium` a URI vscodium://file/… (jen záložní ruční postup otestován).
- Drobnost k F8: chybová hláška obsahuje cestu k dočasnému souboru main.py, zvážit úpravu na „main.py“.

## Poznámky z F6
- web/js/editor/: highlight.js, smart.js, autocomplete.js, format.js, help.js, editor.js; css/editor.css.
- Test: `python tests/e2e_editor.py [--shots DIR]` (24 kontrol psaní kláves). Všechny e2e testy: e2e_web, e2e_lesson, e2e_editor.
- Zarovnání kódu neopravuje odsazení bloků (v Pythonu má význam), jen tabulátory, mezery na koncích a prázdné řádky.
- Neověřeno: Firefox a Safari (testováno jen Chromium), dotyková klávesnice na mobilu.

## Poznámky z F7
- .vscode/ (extensions, settings, tasks, launch), pyrightconfig.json, tools/setup_env.py, tools/install_extensions.py, docs/{instalace,vscodium,reseni-problemu}.md, stránka #/priprava s kontrolním seznamem.
- start.py spouští cvičení Pythonem z .venv, pokud existuje (jinak Python, kterým běží server).
- ZJIŠTĚNO (web, hlášení VSCodium #2752): rozšíření ms-python.python 2026.4.0 z Open VSX nemá složku python-env-tools/bin (pet), takže nenajde interpretery; oprava se nechystá. Proto tasks.json a launch.json míří přímo na .venv a nezávisí na detekci.
- NEOVĚŘENO uživatelem: instalace všech rozšíření ve VSCodium, ladění F5, Jupyter, URI vscodium://file. Slouží kontrolní seznam na #/priprava.
- Neověřeno: příkazy winget a brew, Flatpak varianta VSCodium (v docs uvedeno opatrně).

## Poznámky z F8
- Pilot: courses/zaklady (5 lekcí: print, proměnné, input, podmínky, for), course.json, katalog status draft.
- tools/validate_courses.py: soubory, kvíz, komentáře v ukázce, zakázaná témata, běh ukázky (volitelně example.stdin), vzorové řešení MUSÍ projít, šablona NESMÍ projít.
- Testy: `python -I -m unittest discover -s tests` (52 testů) + e2e: web, lesson, editor, setup, pilot.
- Traceback už neukazuje cestu k dočasné složce.
- Pravidlo pro autoring lekcí: zkopírovat strukturu z courses/zaklady/lessons/01-prvni-program, po každých 5 lekcích spustit validátor.
- Zbývá do podkurzu Základy 35 lekcí (viz PLAN.md, oddíl 3A).

## Základ hotový (v0.1)
- Doručeno: dilna-pythonu-v0.1.zip (114 souborů, 103 kB). Po rozbalení čistě: 52 testů OK, validátor OK, start.py běží.
- DALŠÍ: dopsat podkurz Základy (35 lekcí zbývá), potom B, G1, C, F, D, G2, E (pořadí v PLAN.md). Autoring po 5 lekcích na krok (~15–20 k tokenů), vždy validate_courses.py.
- Z1–Z3 (závěrečný test napříč podkurzy, dokumentace pro autory, volitelně Pyodide) až po podkurzech.

## v0.2 (24. 10. 2026): f-řetězce v editoru
- Zvýraznění: {} (růžové), proměnné (tyrkysové), volání, atributy, čísla, řetězce, vnitřní závorky, formát (:>3, !r), {{ }} jako text. Nový fstring.js, lexicon.js, context.js.
- Našeptávač: uvnitř {…} nabízí proměnné/funkce z kódu (od 1 znaku, nebo hned po {), metody po tečce; v textu řetězce a ve formátu mlčí. V běžném kódu jsou proměnné z přiřazení, for, def a as před obecnými slovy.
- { v textu f-řetězce se vždy spáruje na {}.
- Opraveno: stav našeptávače byl asynchronní vůči rychlému psaní, nyní synchronní přes událost dilna-caret.

## v0.3 (24. 10. 2026): Základy, lekce 6–10 (10 ze 40 hotovo)
- Nové lekce: 06-cyklus-while, 07-seznamy, 08-operace-se-seznamy, 09-seznamy-a-cykly, 10-retezce. course.json: moduly m01 První kroky (1–3), m02 Rozhodování a opakování (4–6), m03 Seznamy a texty (7–10).
- Každá lekce má negativní test: špatná řešení (sort() místo sorted(), dělení // místo /, replace(" ", "_") apod.) kontrola odmítne s nápovědou.
- e2e_pilot.py přepsán: vstupy do ukázek bere z example.stdin; vždy ukončí běžící programy.
- Zbývá 30 lekcí Základů. Další kroky: 11–15 funkce (def, parametry, return, rozsah platnosti), 16–20 slovníky a n-tice, 21–25 chyby a try/except + moduly (random, math), 26–30 ladění ve VSCodium, 31–35 mini-projekty (hádej planetu, šibenice se zvířaty, Caesarova šifra...), 36–40 závěrečné opakování a test.

## v0.4 (24. 10. 2026): Základy, lekce 11–15 (15 ze 40 hotovo)
- Nový modul m04 Funkce: 11-funkce, 12-parametry-a-return, 13-vychozi-hodnoty, 14-rozsah-platnosti, 15-funkce-a-seznamy (docstring, n-tice, nemodifikace předaného seznamu).
- Kontroly volají studentovy funkce přes dilna_check (load + returns, kwargs, kontrola mutace seznamu); negativní zkoušky 13 špatných řešení odmítnuty.
- Zbývá 25 lekcí Základů: 16–20 slovníky a n-tice, 21–25 chyby (try/except) a moduly (random, math, datetime), 26–30 ladění ve VSCodium + čitelný kód, 31–35 mini-projekty, 36–40 opakování a závěrečný test.

## v0.5 (24. 10. 2026): nezávislá revize lekcí 1–15 a opravy (16 lekcí z 40)
Revizi provedl samostatný agent bez znalosti mých závěrů (23 nálezů). Opraveno:
- Chybějící vysvětlení: % a // (lekce 9, 12), True/False (4), + u textů (3), násobení textu (1), += (5), pojem metoda (7), None (8).
- Kontroly: lekce 11 ověřuje volání funkce a print uvnitř ní; 7 a 8 hlídají výsledek vypsaný natvrdo; 7 nevyžaduje append; 14 povoluje while a vyžaduje použití konstanty DPH; 2 vyžaduje proměnné v f-řetězci; 6, 9, 10 nový dilna_check.output_has_line (Součet: 8 nepustí Součet: 80).
- Kvízy: možnosti se v aplikaci míchají (správná odpověď nebyla v 28 z 30 otázek na stejném místě).
- Lekce 15 rozdělena: 15 Funkce se seznamy, 16 Více hodnot a docstring (n-tice, //, %). Nyní 16 lekcí; course.json m04 má 6 lekcí.
- Čeština a terminologie (funkce vs příkaz), přejmenována funkce odsazeni→cara, smazány nepoužité example.stdin.
- Pravidlo pro další lekce: pojem nesmí být použit dřív, než je vysvětlen (zkontrolovat), kontrola musí odmítnout natvrdo vypsaný výsledek, kvízové distraktory věrohodné, po každých 5 lekcích nezávislá revize jiným agentem (cca 110 k tokenů, dělat jen po větších blocích).
- Zbývá 24 lekcí Základů: 17–21 slovníky a n-tice, 22–26 chyby a moduly, 27–31 ladění a čitelný kód, 32–36 mini-projekty, 37–40 opakování a závěrečný test.

## v0.6 (25. 10. 2026): lekce 17–21, slovníky a n-tice (21 lekcí z 40)
- Nový modul m05 „Slovníky a n-tice“: 17 Slovníky, 18 Slovníky: get, in a cykly, 19 Počítání pomocí slovníku (split, lower, max s key), 20 N-tice a množiny (set, sorted, & a |), 21 Seznam slovníků (lambda jen jako nepovinná zmínka).
- validate_courses: 21 lekcí, 0 chyb. Negativní testy: hard-coded řešení, chybějící lower(), `>=` místo `>`, špatný klíč, nevrácená hodnota: všechna odmítnuta.
- Revizi nezávislým agentem tento blok zatím nemá (plán: po lekcích 27–31).
- Zbývá 19 lekcí Základů: 22–26 chyby (try/except) a moduly (random, math, datetime), 27–31 ladění ve VSCodium a čitelný kód, 32–36 mini-projekty, 37–40 opakování a závěrečný test.

## v0.7 (25. 10. 2026): lekce 22–26, chyby a moduly (26 lekcí z 40)
- Nový modul m06 „Chyby a moduly“: 22 Chyby a try/except, 23 Více výjimek, else, finally a raise, 24 Moduly a math, 25 Náhoda a random, 26 Datum a čas (datetime).
- dilna_check: nové metody `call`, `returns_close` (tolerance u desetinných čísel) a `raises` (očekává výjimku). Přidán test (53 testů).
- Lekce 25 kontroluje náhodné funkce statisticky (200 volání, rozsah, rozmanitost) a seed; řešení prošlo 25× za sebou.
- Doplněno vysvětlení umocnění `**` do lekce 9 (používalo se od lekce 13 bez vysvětlení).
- Validace: 26 lekcí, 0 chyb. Negativní testy (špatná řešení, holé except, hard-coded, chybějící raise, špatný formát data, seed ignorován) všechna odmítnuta.
- Zbývá 14 lekcí: 27–31 ladění ve VSCodium a čitelný kód, 32–36 mini-projekty, 37–40 opakování a závěrečný test. Po lekcích 27–31 plánuji nezávislou revizi lekcí 16–31.

## v0.8 (25. 10. 2026): lekce 27–31, ladění a čitelný kód (31 lekcí z 40)
- Nový modul m07 „Ladění a čitelný kód“: 27 Čtení chybových hlášek (oprava 4 chyb), 28 Hledání chyb: print a assert (student píše vlastní testy; kontrola počítá `assert`), 29 Ladicí program ve VSCodium (F5, breakpointy, F10/F11, Watch, záložní `breakpoint()` a pdb), 30 Čitelný kód (jména, konstanty, žádná magická čísla; kontrola AST), 31 Styl PEP 8 a Ruff (docstringy, snake_case, délka řádku, dva prázdné řádky).
- Lekce 29 se dělá mimo prohlížeč ve VSCodium; kontrola v aplikaci ověřuje jen opravy. Postup ladění ve VSCodium NENÍ ověřen na skutečném VSCodium (viz seznam neověřeného).
- Validace: 31 lekcí, 0 chyb. Negativní testy: 16 špatných řešení odmítnuto (včetně magických čísel, jednopísmenných parametrů, chybějících docstringů, porušení stylu).
- Zbývá 9 lekcí: 32–36 mini-projekty, 37–40 opakování a závěrečný test. Poté nezávislá revize lekcí 16–40.

## v0.9 (25. 10. 2026): lekce 32–36, mini-projekty (36 lekcí z 40)
- Nový modul m08 „Mini-projekty“: 32 Hádej planetu (slovník slovníků, `if __name__ == "__main__"`, náhoda), 33 Šibenice se zvířaty (množina, logika odděleně od hry), 34 Caesarova šifra (index, %, isupper, lámání šifry), 35 Seznam úkolů (seznam slovníků, split s maxsplit, enumerate, příkazy), 36 Kámen, nůžky, papír (pravidla jako slovník, n-tice skóre).
- dilna_check: `call` nově umí `stdin` a ukládá výstup do `last_output`; projekty se kontrolují voláním funkcí s připraveným vstupem (včetně textu vypsaného hrou).
- Validace: 36 lekcí, 0 chyb. 15 záměrně špatných řešení odmítnuto. Náhodné kontroly (32, 33, 36) prošly 15× za sebou. 53 testů + e2e pilot OK.
- Poučení: `if __name__ == "__main__"` se v dřívějších lekcích nevysvětlovalo, doplněno v lekci 32. `enumerate` a zkrácený if doplněny v lekci 35. Pozor příště: vzorová data (např. palindromy) ověřovat během validace.
- Zbývají 4 lekce: 37–39 opakování, 40 závěrečný test. Poté nezávislá revize lekcí 16–40 a změna stavu „draft“ na „ready“ po zpětné vazbě.

## v0.10 (25. 10. 2026): lekce 37–40, opakování a závěrečný test (Základy: 40 lekcí z 40, text hotový)
- Modul m09 „Opakování a závěrečný test“: 37 Opakování: podmínky, cykly a texty (fizzbuzz, prvočísla, cifry), 38 Opakování: slovníky a výjimky, 39 Opakování: oprava a úklid kódu (4 chybné funkce + docstringy), 40 Závěrečný test (rozbor textu `analyzuj_text`, `popis_analyzy`, `hlavni` + kvíz o 10 otázkách z celého kurzu).
- V adresáři lekcí se našly starší, nezapsané lekce 37-opakovani-zaklady, 38-opakovani-data, 39-opakovani-chyby-moduly (a 40-zaverecny-test) z 05:08, o kterých STATUS nic neříkal. Starší 37–39 jsem přesunul mimo projekt (scratchpad `old-lekce`), lekci 40 přepsala nová verze. Příčina neznámá, k ověření.
- Validace: 40 lekcí, 0 chyb. 13 špatných řešení odmítnuto. 53 testů + e2e pilot OK.
- Zbývá: nezávislá revize lekcí 16–40 (hlavní riziko: nikdo nečetl), poté status „draft“ -> „ready“ po zpětné vazbě. Pak další podkurzy: soubory-web, pygame-1, turtle-oop, pandas, tkinter-api, pygame-2, databaze.

## v0.11 (26. 10. 2026): nezávislá revize lekcí 16–40, opravy
- Revize proběhla ve třech várkách, vždy jeden agent (16–24, 25–32, 33–40; po ~100–130 tis. tokenů). Třetí pokus selhal na limitu relace a byl zopakován samostatně. Agenti nic neupravovali, opravy jsem dělal sám a ověřil špatnými řešeními.
- Nálezy: 11 + 12 + 10. Převažují slabé kontroly (špatná řešení procházela: náhoda v lekci 25, `assert` počítaný kdekoliv, výsledek kola v lekci 36 vůbec netestován, `rozlam` v lekci 34, `try` kontrolovaný jen kdekoliv v souboru, chybějící krajní případy). Dále: lekce 27–29 nespouštěly kód, takže chyby nebyly vidět (doplněna volání `print` do výchozího kódu), tvrzení o Ruffu zpřesněno, `pass`/`enumerate` ve vzorových řešeních nahrazeno tím, co kurz učil.
- Poučení: požadované konstrukce (try, raise, seed, volání funkce) vždy kontrolovat uvnitř konkrétní funkce; u náhody požadovat pokrytí celého rozsahu; u her ověřit výsledek kola s dosazeným tahem počítače (`ns["funkce"] = lambda: ...`).
- Validace: 40 lekcí, 0 chyb. 12 nových záměrně špatných řešení odmítnuto. Náhodné kontroly (25, 33, 36) 20× za sebou OK. 53 testů + e2e pilot OK.
- Podkurz Základy: text i kontroly revidovány (lekce 1–15 v v0.5, 16–40 ve v0.11), stále chybí zpětná vazba skutečného studenta a ověření ve VSCodium. Stav v catalog.json ponechán „draft“.
- Další krok: podkurz Soubory a web scraping (22 lekcí), po várkách po 5 lekcích.

## v0.12 (26. 10. 2026): infrastruktura souborů lekce a podkurz Soubory a web scraping, lekce 1–5 (z 22)
- **Nová funkce aplikace: složka `files/` v lekci.** Soubory z `courses/<kurz>/lessons/<lekce>/files/` (i v podsložkách) se kopírují vedle kódu studenta při spuštění (`/api/run` dostává `course` a `lesson`), při kontrole (`run_check`) i do pracovní složky pro VSCodium (`save_workspace`, bez přepsání už upravených). Kód: `server/lessonfiles.py`, úpravy `runner.py`, `checker.py`, `content.py`, `app.py`, `web/js/runner-client.js`, `web/js/lesson.js`, `tools/validate_courses.py`. Test: `tests/test_lessonfiles.py` (6 testů) a fixtura `tests/fixtures/demo/lessons/03-soubor`. Zdokumentováno v `courses/SCHEMA.md`.
- **dilna_check:** nová metoda `utf8()` (každé textové `open`, `read_text`, `write_text` má `encoding`). Dříve přidáno: `call` (stdin, `last_output`), `returns_close`, `raises`.
- **Soubory a web scraping, modul m01 „Čtení a zápis souborů“ (lekce 1–5):** 01 Čtení textového souboru (open, with, UTF-8, read), 02 Čtení po řádcích (strip, prázdné řádky, slovník z řádků), 03 Zápis do souboru (w, a, write, print file=), 04 Složky a modul pathlib (Path, glob, iterdir, mkdir, read_text/write_text), 05 Chyby při práci se soubory (FileNotFoundError, OSError, přeskakování špatných řádků).
- Validace: 45 lekcí celkem, 0 chyb. 16 záměrně špatných řešení nových lekcí odmítnuto (jeden případ, řazení bez `sorted`, odhalil nespolehlivost testu pořadí na disku, proto kontrola `sorted` přes AST). 59 testů + e2e pilot a web OK.
- Stav v catalog.json: soubory-web „draft“ (5 z 22 lekcí).
- Chybí pro dokončení podkurzu (17 lekcí): viz HANDOVER.md, oddíl „Plán zbývajících lekcí soubory-web“.

## v0.13 (26. 10. 2026): soubory-web lekce 6–10 (10 z 22)
- 06 Projekt: Deník (soubor jako jediné místo dat, split s maxsplit, tuple zápisy), modul m02 „CSV a JSON“: 07 CSV čtení (`csv.reader`, `newline=""`, `next`, `delimiter`), 08 CSV slovníky (`DictReader`, `DictWriter`), 09 JSON (`load/dump/loads/dumps`, `ensure_ascii`, `indent`, překlad typů), 10 Zpracování tabulky (`sorted` s `key` a `lambda`, součty podle skupiny, řez `[:n]`).
- Validace: 50 lekcí, 0 chyb. 22 záměrně špatných řešení: 21 odmítnuto, 1 prošlo oprávněně (`int` místo `float` na celočíselném sloupci). 59 testů + e2e OK.
- Zbývá 12 lekcí: 11 Kontakty v JSON (projekt), 12–22 web scraping (viz HANDOVER.md, oddíl 7, vč. otevřeného rozhodnutí o lokálním serveru pro `requests`).

## v0.14 (27. 10. 2026): soubory-web lekce 11–15 (15 z 22)
- 11 Projekt: Kontakty v JSON (m02 hotový), nový modul m03 „Web scraping“: 12 HTML a hledání v textu (`find`, `count`, řezy: motivace pro parser), 13 BeautifulSoup první kroky (`find`, `get_text`, atributy, `class_`), 14 `find_all` a tabulky, 15 CSS selektory (`select`, `select_one`, třídy jako seznam). Vstupní HTML je v `files/` lekce, funkce dostávají HTML jako text, vše offline.
- Validace: 55 lekcí, 0 chyb. 24 záměrně špatných řešení: 22 odmítnuto, 2 prošla oprávněně (ekvivalentní řešení). 59 testů + e2e OK.
- Poučení: `get_text(strip=True)` slepuje kusy textu bez mezery (`"x"+"y"`), v testech se na to nespoléhat. Při generování kontrol z Python řetězců pozor na escapování uvozovek (`\"` v `'''` se ztratí).
- Zbývá 7 lekcí: 16–20 requests proti lokálnímu serveru (nutné rozhodnout, jak student importuje pomocný server), 21 opakování, 22 závěrečný test. Generátory lekcí ve scratchpadu nejsou součástí projektu.

## v0.15 (27. 10. 2026): soubory-web lekce 16–20 (20 z 22), místní server pro `requests`
- **Rozhodnutí:** lekce o webu běží offline proti malému serveru na `127.0.0.1`. Pomocný modul `dilna_web.py` (`spust()` vrací adresu) leží jako `files/dilna_web.py` v lekcích; originál je `courses/soubory-web/shared/dilna_web.py`. Server umí chybové kódy, pomalé a nestabilní odpovědi, přesměrování a vrací hlavičky klienta. Test `tests/test_dilna_web.py` hlídá shodu kopií a funkčnost.
- 16 `requests.get` (stavový kód, text, hlavičky, json), 17 Když se stahování nepovede (`raise_for_status`, `timeout`, `RequestException`, opakování s pauzou), 18 Projekt: ceník knih do CSV (tři funkce: získání, uložení, stažení), 19 Stahování souborů a obrázků (`wb`, `urljoin`, `mkdir(exist_ok=True)`), 20 Slušné chování robotů (`robots.txt`, User-Agent, pauzy, autorské právo, GDPR).
- Validátor (`tools/validate_courses.py`) teď spouští `example.py` jako `main.py` bez `-I`, tedy jako skutečný runner (jinak by nenašel `dilna_web`).
- Validace: 60 lekcí, 0 chyb. 26 záměrně špatných řešení: 24 odmítnuto, 2 prošla oprávněně (ekvivalentní: dodatečný `except Exception` v lekci 18, vynechané ošetření 404 u `robots.txt` v lekci 20, protože text chybové stránky nemá žádná pravidla). Kontrola pauz v lekci 17 doplněna po zjištění, že špatné řešení bez pauzy prošlo. 62 testů OK.
- Zbývá: 21 Opakování, 22 Závěrečný test. Pak nezávislá revize lekcí 6–22 (po jednom agentovi), další podkurzy.

## v0.16 (27. 10. 2026): soubory-web dokončen (22 z 22)
- 21 Opakování: CSV po třídách, nejlepší žák, převod do JSON, odkazy z HTML (vše offline, `body.csv` v `files/`). 22 Závěrečný test: sběrač cen (`nejlevnejsi`, `prumerna_cena`, `sber_cen` s kontrolou `robots.txt`, `User-Agent`, `timeout`, `raise_for_status`, uložení do JSON; zakázaná cesta `/soukrome/knihy.html` se nesmí stáhnout).
- Validace: 62 lekcí, 0 chyb. 14 záměrně špatných řešení: 13 odmítnuto, 1 prošlo oprávněně (User-Agent jen u druhého dotazu).
- Podkurz zůstává ve stavu „draft“: nikdo ho nečetl a nebyl ověřen ve VSCodium. Zbývá nezávislá revize lekcí 6–22 (po jednom agentovi), pak další podkurzy (pygame-1, turtle-oop, pandas, tkinter-api, pygame-2, databaze).

## v0.17 (27. 10. 2026): revize soubory-web, várka 1 (lekce 06–14)
- Revizi udělal jeden agent (~105 tis. tokenů, nic neupravoval); první pokus selhal na limitu relace a byl zopakován. 14 nálezů, všechny opraveny a ověřeny.
- Slabé kontroly: `hledej` (06) a `najdi` (11) nehlídaly, že se nehledá v datu, telefonu a e-mailu; `uloz_zaky` (08) nevynucoval `newline=""`; lekce 13 netestovala bílé znaky u `prvni_odkaz` a `prvni_odstavec`.
- Skryté požadavky doplněny do zadání: `try/except` (06, 09, 11), `find` a texty bez mezer (13), prázdný `href` se počítá (14); věta „všude find_all“ v lekci 14 zpřesněna.
- Chyby v textu: uvozovky `newline=""` v hlášce kontroly 07, escape `\u010d` v kvízu 09, nadpis o řezu seznamu v 10, matoucí vysvětlení `class_` v kvízu 13; přidána poznámka o kódování `cp1250` u CSV z Excelu (07).
- Validace: 62 lekcí, 0 chyb, 3 nová špatná řešení odmítnuta.
- Zbývá revize lekcí 15–22 (jedna várka, jeden agent); lekce 1–5 byly revidovány dříve? Ověřit podle STATUS (v0.12 je neuvádí jako revidované), pokud ne, zařadit do další várky.

## v0.18 (27. 10. 2026): revize soubory-web, várka 2 (lekce 15–22)
- Jeden agent (~128 tis. tokenů), 18 nálezů, všechny opraveny.
- Chyby: ukázka lekce 17 volala neexistující `data.json` (a pořadí `except` Timeout/ConnectionError, na Windows by se vypsala jiná hláška); zbytečně přísné kontroly (lekce 15 vyžadovala přesně `select_one`, 17 `for` a `raise_for_status`, 18 `select`, 21 jen `json.dump`) nahrazeny chováním; skryté požadavky doplněny do textu (klíče knih v lekci 22).
- Slabé kontroly: `timeout` v 17 se ignoroval (nově test s `timeout=0.1` a AST jméno parametru); `ceny` a `body` mohly být `float` (15, 21); `stahni_knihy` mohla ukládat natvrdo `knihy.csv` (18); v 22 se nekontrolovala hodnota `User-Agent`, pořadí dotazů ani že se zakázaná stránka nepožaduje: kontrola nyní zaznamenává skutečné volání `requests.get` (monkeypatch v check.py).
- Text: v lekci 20 doporučení dát do User-Agent vlastní e-mail (odporovalo bodu o osobních údajích) změněno na kontakt na učitele; vysvětleno API a scraping; test chybějícího `robots.txt` teď používá `/bez/` místo triku s `/_status/404`; opraveno „otvírá“, zavádějící `why` v kvízech 18 a 21, odstraněna nevysvětlená `PurePosixPath` z lekce 19 a doplněn `raise_for_status` do jejího příkladu.
- Platforma: kontroly 16, 17, 20 čtou očekávané texty z `files/` jako bajty (odolné proti CRLF na Windows).
- Validace: 62 lekcí, 0 chyb; 10 záměrných mutací dopadlo podle očekávání (7 odmítnuto, 3 oprávněně prošla). Všechny testy OK.
- Zbývá: revize lekcí 01–05 (jedna várka), poté zpětná vazba skutečného studenta a ověření ve VSCodium; další podkurzy.

## v0.19 (28. 10. 2026): revize soubory-web, várka 3 (lekce 01–05), kurz soubory-web zrevidován celý
- Jeden agent (~92 tis. tokenů), 13 nálezů, všechny opraveny. Žádná z kontrol 01–05 nepropouštěla špatná řešení kromě lekce 04.
- Lekce 04: kontrola `najdi_txt` nehlídala složku s příponou (`files/poznamky/stare.txt/`, nově přidána), proto mutace bez `is_file()` procházela; lekce teď složky zmiňuje, `iterdir()` je vysvětlen a ukázka používá `is_file()`.
- Lekce 05: lekce tvrdila, že student `FileNotFoundError` už viděl (v Základech není); vysvětlena hierarchie výjimek a rozdíl Windows (`PermissionError`) / Linux (`IsADirectoryError`) při otevření složky; zadání požaduje `try`/`except OSError`; doplněn test `nacti_cisla_bezpecne("slozka")`.
- Lekce 03: kontrola čte bajty a převádí CRLF (Windows); zadání říká, že každý řádek včetně posledního končí `\n`. Kvízy 02 a 03: zpětná lomítka se zobrazovala zdvojeně (`\\n`), opraveno.
- Lekce 01, 02: drobná zpřesnění textu.
- Validace: 62 lekcí, 0 chyb. Všechny testy OK.
- Podkurz soubory-web (22 lekcí) je celý nezávisle zrevidován. Stav v katalogu zůstává „draft“: chybí zpětná vazba skutečného studenta a ověření ve VSCodium a na Windows.
- Další krok: další podkurz (pygame-1, turtle-oop, pandas, tkinter-api, pygame-2, databaze), viz HANDOVER oddíl 8.

## v0.20 (30. 10. 2026): podkurz pygame-1, lekce 01–05 (5 z 18) a pygame bez okna v kontrolách
- **Nová funkce kontrol:** `c.pygame_run(...)` (`lib/dilna_check/pgrun.py`): program studenta běží v podprocesu s SDL `dummy`, po zadaném počtu snímků se zastaví, kontrola zná barvy pixelů, počty barev, volání `pygame.draw`, texty, načtené obrázky, zvuky, tisk a skončil-li program sám. Podstrčí události (klávesy, myš, zavření okna), držené klávesy a polohu myši, hodiny jsou rychlé a deterministické. Test: `tests/test_pgrun.py` (4 testy). Validátor spouští okenní `example.py` s pygame bez okna (pět snímků) a hlásí chybu, když spadne nebo nic nenakreslí.
- **pygame-1 m01 „Okno, smyčka a kreslení“:** 01 První okno (`init`, `set_mode`, `fill`, `flip`), 02 Herní smyčka a události (`QUIT`, `KEYDOWN`, `Clock.tick`), 03 Barvy a souřadnice (RGB, osa y dolů, `fill` s obdélníkem, vlajka), 04 Kreslení tvarů (`draw.rect/circle/polygon/line`, pořadí), 05 Obrázky (`image.load`, `convert_alpha`, `blit`, `get_rect`). Obrázky rakety a hvězdy jsou vlastní, generované.
- Validace: 67 lekcí, 0 chyb. 20 záměrně špatných řešení nových lekcí odmítnuto; po prvním kole se zesílily dvě slabé kontroly: posunuté slunce (přidány body na okraji a pod kruhem) a `convert()` místo `convert_alpha()` (pozadí lekce 05 je tmavě modré, ne černé, jinak se rozdíl nepozná).
- Poznámka: pygame-ce je v testovacím prostředí nainstalováno (2.5.8, Python 3.13), na počítači studenta ho nainstaluje `tools/setup_env.py --courses pygame-1`. Skutečné okno ve VSCodium jsem neověřoval.
- Zbývá: lekce 06–18 (viz HANDOVER oddíl 8), pak revize jedním agentem.

## v0.21 (30. 10. 2026): pygame-1, lekce 06–10 (10 z 18)
- m02 „Rect, text, zvuk a první projekt“: 06 Rect (atributy, `get_rect(topleft=...)`, `move`), 07 Fonty a text (`Font`, `render`, f-řetězec, vystředění), 08 Zvuky a hudba (`mixer.Sound`, `music.load/play(-1)/set_volume`; vlastní WAV generované modulem `wave`), 09 Projekt Pohlednice z kosmu (seznam poloh, `for`, scéna); m03 „Pohyb a vstupy“ začíná lekcí 10 Pohyb a FPS (`rect.x += rychlost`, návrat zleva, `dt`).
- `pygame_run`: `colors` umí i část okna `(r, g, b, x, y, š, v)` a `r.color_count(barva, snímek, region)` (kontrola vystředění textu). Záznam `mixer.music` zapisuje i pojmenované argumenty (`loops=-1`).
- Validace: 72 lekcí, 0 chyb. 25 záměrně špatných řešení: 23 odmítnuto, 1 prošlo oprávněně, 2 slabé kontroly zesíleny (posunutá hvězda v 09: přidány špičky hvězd; chybějící `screen.fill` v 10: bod, kudy raketa proletěla). Všechny testy OK.
- Zbývá: lekce 11–18 (klávesy, myš, hranice, kolize, více objektů, skóre a konec hry, Sběratel hvězd 1 a 2), pak revize.

## v0.22 (31. 10. 2026): pygame-1, lekce 11–15 (15 z 18)
- m03 „Pohyb a vstupy“: 11 Klávesnice (`KEYDOWN` proti `get_pressed`, samostatná `if` pro šikmý pohyb), 12 Myš (`get_pos`, `MOUSEBUTTONDOWN`, `button`, seznam otisků), 13 Hranice a odrazy (míč, `vx = -vx`, okraje podle poloměru), 14 Kolize (`colliderect`, `collidepoint`; kostra s hotovým pohybem), 15 Více objektů (seznam `Rect`, dva cykly, `random.randint`, návrat nahoře).
- Kontroly simulují vstupy (`held`, `mouse`, `events`) a čtou barvy pixelů v zadaných snímcích; u pohybu se bere tolerance jednoho kroku, aby prošlo pořadí „pohyb, kresba“ i „kresba, pohyb“. Lekce 15 se kontroluje bez náhody: před prvním návratem hvězdy podle pozic, po návratu přes počet žlutých pixelů v pásu.
- Validace: 77 lekcí, 0 chyb. 23 záměrně špatných řešení všechna odmítnuta (po prvním kole zesíleny tři kontroly: poloměr otisku v 12, pátá hvězda v 15, `elif` se testuje u celého řetězu v 11). Vzorová řešení 13, 14 a 15 prošla 12× za sebou.
- Poučení: při skriptu volajícím `run_check` používat absolutní cesty (relativní daly falešných 0 z 12).
- Zbývá: 16 Skóre a konec hry, 17 a 18 Sběratel hvězd (projekt), pak revize jedním agentem.

## v0.23 (31. 10. 2026): pygame-1 dokončen (18 z 18)
- 16 Skóre a konec hry (stav hry `"hra"`/`"konec"`, skóre, obrazovka konce, restart klávesou R), m04 „Projekt: Sběratel hvězd“: 17 (jádro: raketa se šipkami a hlídáním okrajů, čtyři padající hvězdy, kolize, skóre) a 18 (životy, zvuk `cinknuti.wav`, hudba `hudba.wav` při hlasitosti 0.3, konec hry, restart). Exercise lekce 18 je hotová hra z lekce 17, kterou student rozšiřuje.
- Kontroly hry jsou deterministické do prvního návratu hvězdy nahoře (náhodné x): časová osa 17 a 18 (hvězda 0 mine raketu ve snímku ~167, hvězda 2 se chytí ~183, hvězda 1 mine ~194, hvězda 3 mine ~247, konec ~247, restart R ve snímku 262). Texty se ověřují podle snímku (`r.texts[].frame`), zvuky podle snímku přehrání.
- Validace: 80 lekcí, 0 chyb. 22 záměrně špatných řešení; první kolo propustilo čtyři (hvězdy se nevracejí, jiné začátky hvězd, restart bez resetu hvězd, pohyb i po konci hry). Doplněno: počet žlutých bodů v horním pásu, pozice hvězd 1 a 3 v daných snímcích, pozice hvězdy 0 po restartu a AST kontrola, že `colliderect` leží v `if` na `stav`. Všech 22 nyní odmítnuto, vzorová řešení 16–18 prošla 10× za sebou.
- Podkurz pygame-1 (18 lekcí) zůstává „draft“: nezrevidován nezávislým agentem, bez zpětné vazby studenta, okno a zvuk ve VSCodium neověřeny.
- Další krok: nezávislá revize pygame-1 (jeden agent, dvě várky: 01–09 a 10–18), pak další podkurzy (turtle-oop, pandas, tkinter-api, pygame-2, databaze).

## v0.24 (31. 10. 2026): revize pygame-1, lekce 01–09 (jeden nezávislý agent, ~130 mutací)
- Opraveny věcné chyby v textu: L04 (okno si pamatuje předchozí snímek), L05 (průhlednost ztrácí `.convert()`, ne chybějící `convert_alpha`; „z disku“), L08 (`init()` chybu zvuku tiše přeskočí, `pygame.error` přijde až u `Sound`/`music.load`; tip `try`/`except`), L09 (nesrozumitelná věta, „v tomto pořadí“).
- Zpřísněné kontroly: L01 (`wait`, `quit`), L03 (hodnoty a použití konstant), L04 (hrany zdi, trávy, střechy), L05 a L06 (hrot a boky rakety, hrany hvězdy, `convert_alpha` u obou obrázků), L07 (velikost písma a poloha podle počtu bodů v pásu), L09 (cyklus přímo přes `HVEZDY`, okraje planety, hrot rakety, velikost nadpisu).
- Uvolněno: L06 přijme výpis středu i jako `200 150` (regulár `200\D+150`), L09 přijme `HVEZDY: list = [...]`.
- Neřešeno (vědomě): L02 `event.get(pygame.QUIT)` s filtrem (omezení pgrun, filtr se ignoruje); přesun `get_rect` z L05 do L06 (didaktický návrh, ponecháno); L08 a L09 mají jen 2 otázky v kvízu.
- Další krok: revize lekcí 10–18 (jeden agent), pak další podkurzy.

## v0.25 (1. 11. 2026): revize pygame-1, lekce 10–18 (jeden agent, 25 nálezů), opraveny lekce 10–15
- Text: L10 (`Rect` ořezává desetinná čísla, při `dt` držet polohu v proměnné `x`; cvičení je po snímcích; pořadí posun/kreslení), L13 (souřadnice kruhu a „neopustí okno“ přeformulováno: míč smí o pár bodů přesáhnout), L14 (hvězda je vpravo od rakety, kostra říká, že se řádek `screen.fill` nahrazuje).
- Kontroly: L10 přesné zalomení (`rect.right = 0`, vynucené načtení obrázku), L11 pozadí, pohyb v obou osách, jiná klávesa nevrací do středu, mezerník vrací x i y, L12 poloměr otisku (bod +11), L13 velikost okna, pozadí, poloměr 15, L14 návrat pozadí po odjezdu od hvězdy a `collidepoint(pygame.mouse.get_pos())`, L15 `randint(0, 368)` v AST, `bottom = 0` při návratu hvězdy, počítání cyklů nahrazeno hledáním cyklu přes seznam.
- Ověřeno mutacemi (nepropustí) a variantami (propustí); L15 stabilní 6×.
- Zbývá z revize: lekce 16–18 (texty a barvy, `mixer.music` vs `Sound`, reset rakety a R, `if zivoty > 0`, pozice textů, náhodné x v 17), L15 výklad prozrazuje skoro celé řešení, kvízy mají správnou odpověď většinou na pozici 1–2.

## v0.26 (1. 11. 2026): revize pygame-1 dokončena, opraveny lekce 16–18
- L16: do lesson.md přesné zadání (fonty, pozice, barvy, texty obou stavů); kontrola už nevyžaduje proměnnou `stav` (jen chování), nově hlídá barvu, velikost a místo textů (počty bodů v pásech).
- L17: `randint(0, 368)` kontrolováno v AST, hvězda se vrací až při `top > 500` (bod (46, 496) ve snímku 160), skóre bílé, písmo 32, vlevo nahoře.
- L18: text i kvíz rozlišují `mixer.music` (hudba) a `mixer.Sound` (efekt); kontrola zvuku filtruje jen `cinknuti.wav`; klávesa R uprostřed hry nic nedělá (snímek 192); polohy, barvy a velikosti textů hry i obrazovky konce; obrazovka konce se nemění; `if zivoty > 0` místo `stav` je také platné.
- Ověřeno 14 chybnými řešeními (písmo, poloha, barva, `top > 450`, `randint(0, 50)`, R kdykoli) a variantou; správná řešení 16–18 prošla 5× za sebou.
- Neřešeno (vědomě): výklad L15 prozrazuje skoro celé řešení, kvízy mají správnou odpověď většinou na pozici 1–2, kontrola resetu rakety při restartu v L18 (raketa se v testu nepohybuje).
- Pygame-1 zůstává „draft“ (bez zpětné vazby studentů, okno a zvuk ve VSCodium neověřeny).
- Další krok: další podkurz (turtle-oop, 40 lekcí) podle PLAN.md, nebo oprava zbylých drobností.

## v0.27 (1. 11. 2026): začátek podkurzu turtle-oop (4 z 40 lekcí) a kontrola želvy bez okna
- Nový nástroj `c.turtle_run()` (`lib/dilna_check/turtlerun.py`, `TurtleResult`): místo skutečného `turtle` se podstrčí náhrada, která zaznamená úsečky, barvy, tloušťky, výplně, tečky, texty a volání funkcí a spočítá stejnou geometrii (kruh = mnohoúhelník podle vzorce z CPythonu). 5 testů v `tests/test_turtlerun.py`. Validátor teď spouští želví `example.py` bez okna. `uses_call` přijímá alternativy (`"forward|fd"`).
- Lekce m01 „Kreslení želvou“: 01 První čára (L na ležato), 02 Čtverec a cyklus for (jeden `forward` v cyklu, modrá, tloušťka 3), 03 Mnohoúhelníky a funkce (`mnohouhelnik(t, strany, delka)`, trojúhelník a šestiúhelník, geometrie ověřena středy stran), 04 Barvy, tloušťka a pozadí (jméno, `#00ff00`, `colormode(255)`).
- Validace: 84 lekcí, 0 chyb. 33 mutací a variant: první kolo odmítlo správná řešení s `fd`/`lt` a `pencolor` místo `color` (opraveno přes alternativy). Všechny chybné varianty odmítnuty, správné (`fd`, `_`, `//`, hex velkými písmeny, `"orange"`) propuštěny.
- Podkurz turtle-oop je „draft“, nezrevidovaný. Pravý turtle ani tkinter v testovacím prostředí nejsou ověřeny (bez displeje), kontroly stojí na náhradě modulu.
- Další krok: lekce 05–08 (vyplněné tvary, kruhy a oblouky, souřadnice a tuple, projekt spirograf).

## v0.28 (1. 11. 2026): tři drobnosti po revizi pygame-1
- L15: výklad už neukazuje řešení cvičení (příklad s kapkami deště a jinými čísly, vysvětleno záporné `y`).
- Kvízy pygame-1 (lekce 01, 02, 09, 11, 12, 13, 15): správné odpovědi rozmístěny na různé pozice (dřív většinou druhá).
- L18: kontrola ověřuje, že se po restartu vrátí raketa na (200, 450) (v testu se raketa před koncem hry posune doleva klávesami ve snímcích 210–220). Bez řádku `raketa_rect.center = (200, 450)` kontrola selže, vzorové řešení prošlo 5× za sebou.
- Validátor: 84 lekcí, 0 chyb.

## v0.29 (1. 11. 2026): turtle-oop, modul m01 „Kreslení želvou“ hotov (8 z 40 lekcí)
- 05 Vyplněné tvary (domeček: žlutá zeď a červená střecha, hnědá čára; plochy výplní a rohy se kontrolují přes `fills`), 06 Kruhy a oblouky (sněhulák ze tří kruhů poloměrů 60/40/25, dvě tečky, úsměv `circle(10, 180)`; kruhy se ověřují body na obvodu), 07 Souřadnice, `goto` a dvojice (cik-cak z `body`, rozbalení `for x, y in body`, slicing `body[1:]`), 08 Projekt Spirograf (36 kruhů po 10°, barvy `barvy[i % 6]`, rozměr obrazce ≈ 320 × 320 se středem v (0, 0)).
- Validace 88 lekcí, 0 chyb. 30 mutací (špatná barva, poloměr, úhel, tloušťka, chybějící `end_fill`, posun, chybějící poslední tečka, špatný slicing, `i % 5`, chybějící `hideturtle`): všechny odmítnuty. Varianty (`steps=`, `circle(r, 360)`, `goto((x, y))`, posunutý začátek barev, `fd`) prošly. Barva nastavená až po kruhu správně selhala (první kruh by byl černý).
- Pozor při psaní dalších lekcí: kontrola nesmí vyžadovat `print(t.pos())`, protože náhrada vrací běžnou dvojici, pravý turtle vrací `Vec2D` s jiným výpisem.
- Další krok: m02 turtle-oop (opakování typů a řetězců, seznamy, slicing, `set`, rozbalování), případně nejdřív nezávislá revize lekcí 01–08.

## v0.30 (2. 11. 2026): revize turtle-oop lekce 01–08 (jeden agent, 15 nálezů)
- Náhrada želvy (`turtlerun.py`): přidán `t.screen`, úsečky nulové délky se nezapisují, `clear`/`reset` mažou nakreslené, `pos()` vrací `Vec2D` (`+`, `-`, `*`, `abs`, výpis `(x,y)`), `speed` se mapuje jako v pravém turtle (jména, 0 pro hodnoty mimo 0.5 až 10.5), `pencolor(255, 165, 0)` bez `colormode(255)` vyhodí `TurtleGraphicsError` jako pravá želva, základní barvy se vrací jménem (hex `#ffff00` a `yellow` jsou totéž), zkrácený hex `#rgb` se rozšíří. Test rozšířen (6 testů).
- Kontroly: všechny lekce 02–08 vyžadují `turtle.done()`; 03 nepočítá místa volání funkce; 04 sčítá navazující úsečky a přijme `"green"` i `"#00ff00"`; 07 srovnává tečky jako množinu (první bod smí mít tečku dvakrát); 08 ověřuje, že každý z 36 kruhů je pootočený o 10° (středy kruhů), rychlost 0 a `done()`.
- Texty: zatáčejte doleva (02, 03, 05), varování, aby se soubor nejmenoval `turtle.py`, a „jako v pygame“ pryč (01), přesnější popis oblouku a kvíz o `dot` vs. `circle` (06), `for x, y in body` bez omezení (07).
- Ověřeno: `left(20)`, `left(30)`, `left(90)`, `speed(5)`, chybějící `done()` už lekci 08 neprojdou; `speed("fastest")`, `speed(11)`, `Screen().bgcolor`, `t.screen.exitonclick()`, `#0f0`, dvě `forward(100)` místo jedné čáry, volání funkce ve smyčce prošly. Validátor: 88 lekcí, 0 chyb.
- Další krok: m02 turtle-oop (opakování typů a řetězců, seznamy, slicing, `set`, rozbalování).

## v0.31 (2. 11. 2026): turtle-oop, modul m02 „Zpět k základům“, lekce 09–12 (12 z 40)
- 09 Čísla, typy a převody (`rozloz_cas` přes `divmod` a `:02d`, `na_cislo` s čárkou a `None`, `je_cele`), 10 Řetězce: indexy a řezy (`prvni_a_posledni`, `obrat`, `kazde_druhe`, `bez_okraju`, `je_palindrom`), 11 Řetězce: metody (`pocet_slov`, `nejdelsi_slovo` s prvním při shodě, `titulek`, `zamen_samohlasky`), 12 Seznamy: metody a kopie (`bez_duplicit`, `serad_podle_delky`, `posun`, `odeber_vsechny`; kontrola ověřuje, že se vstupní seznam nezmění).
- Validace 92 lekcí, 0 chyb. 33 mutací: první kolo propustilo palindrom s mezerami (`"ab a"`), doplněno do kontroly lekce 10; ostatní chybné varianty (bez nulového doplnění, 24h zalomení, bez čárky, `isinstance`, `split(" ")`, poslední ze shod, `title` místo vnitřních mezer, místní řazení, žádný modulo, mutace vstupu) odmítnuty; správné varianty (`x % 1 == 0`, `filter`, `dict.fromkeys`, `title()`) prošly.
- Nezrevidováno nezávislým agentem.
- Další krok: lekce 13–16 (řezy seznamů a kopie, dvojice a rozbalování, množiny, projekt analýza textu).

## v0.32 (3. 11. 2026): turtle-oop, modul m02 hotov, lekce 13–16 (16 z 40)
- 13 Řezy seznamů a kopie (`poslednich` s pastí `s[-0:]`, `obrat_seznam`, `rozdel_na_poloviny` jako tuple, `kopie_matice` hluboká kopie; kontrola ověřuje, že se vstup nemění), 14 Dvojice, rozbalování a zip (`min_max` jako tuple, `prvni_a_zbytek` s `*`, `ocisluj` přes `enumerate(start=1)`, `sloz_dvojice`), 15 Množiny (`unikatni_pocet`, `spolecne`, `jen_v_prvnim`, `vsechna_pismena`, `ma_duplicity`; množiny se vracejí jako seřazený seznam, kontrola má i textové vstupy, aby nepropustila neseřazený výsledek), 16 Projekt Analýza textu (`analyza(text)` vrací slovník: slov, unikatnich, nejdelsi, nejcastejsi, prumerna_delka; počítání přes slovník a `min` s klíčem).
- Validace 96 lekcí, 0 chyb. 32 mutací: všechny chybné odmítnuty (`s[-0:]`, obrácení na místě, horní polovina, mělká kopie, tuple vs. list, špatný prázdný vstup, `start=0`, indexování místo `zip`, `^` místo `-`, bez `lower`, interpunkce, slova prázdná po očištění, nejčastější při shodě, zaokrouhlení, floor průměr). Jediné první kolo: neseřazený `list(set(a) & set(b))` prošel kvůli malým číslům, doplněny textové vstupy. Správné varianty (`deepcopy`, `list(r)`, ruční `zip`, `*` vs. řez) prošly.
- Nezrevidováno nezávislým agentem (lekce 09–16).
- Další krok: nezávislá revize lekcí 09–16, pak m03 OOP (třída, konstruktor, atributy, metody).

## v0.33 (3. 11. 2026): revize turtle-oop lekce 09–16 (jeden agent, ~130 variant, 11 nálezů)
- Opraveno: L16 text učil `strip` bez pomlčky, ale zadání ji vynechává (teď `.strip(".,!?;:\"()-")` a výčet interpunkce, přidán `lower()` a vysvětlení součtu a `lambda`); L11 `"banán".count("a")` bylo 1, ne 2 (nyní `count("n")`); L11 kontrola má případ s diakritikou (`žluťoučký`); L09 kontrola typu `float` pro `" 7 "`, `"2"`, `"0,25"` a poznámka o `nan`/`inf`; L13 nápověda `return levá, pravá` a kvíz o řezech seznamu místo duplicity `s[::-1]`; L12 vysvětlená `lambda` a dvojice klíče, „abecedně“ → „podle řazení Pythonu“; L10 nápověda `lower`/`replace`, přesnější věta o řezech mimo rozsah; L14 „zkuste“ rozbalování s hvězdičkou.
- Správná alternativní řešení (např. `x % 1 == 0`, `dict.fromkeys`, `deepcopy`, `max(key=len)`) kontroly propustily, chybné mutace odmítly (130 zkoušek).
- Validátor 96 lekcí, 0 chyb. Generátory v scratchpadu už neodpovídají souborům (ručně opraveno): nepřegenerovávat, pracovat s hotovými soubory.
- Další krok: m03 OOP (třída, konstruktor, atributy, metody).


## v0.34 (3. 11. 2026): více přepínatelných příkladů v Základech
- Na výslovné přání uživatele je pokračování podle PLAN.md pozastaveno. Nezačínat m03 OOP bez nového zadání.
- Základy: v lekcích 01–31 a 37–39 přibylo 68 dalších konzolových příkladů (dva v každé z 34 lekcí). Každý má název, popis, námět ke změně a komentovaný kód, uložený v `examples.json`. Zůstává i původní `example.py`, celkem tři ukázky na lekci.
- Nad editorem ukázky jsou přepínací tlačítka se stavem aria-pressed. Varianty lze upravovat a spouštět, rozepsaný kód se ukládá odděleně do localStorage. Obnovit příklad vrátí pouze vybranou variantu. Vlastní úkol, jeho kontrola, kvíz a postup jsou oddělené.
- Mini-projekty 32–36, závěrečný test 40 i všechny ostatní podkurzy zůstaly obsahově beze změn (ověřeno porovnáním s archivem v0.33). Nejsou přidané žádné další navazující lekce.
- API `/api/lesson` vrací nové pole `examples`; stávající `example` zůstává. Formát popisuje `courses/SCHEMA.md`. Validátor kontroluje metadata, jedinečnost id, komentáře a spouští všechny varianty; interaktivní mají vzorový `stdin` pouze pro validaci.
- Ověřeno na Linuxu, Python 3.14.8: validátor všech 96 lekcí (včetně 68 dalších příkladů), 0 chyb a 0 upozornění. Unit testy: 77 testů, OK, žádné přeskočené; včetně 4 nových testů příkladů a odhalení chybných metadat i chyb při běhu. Sada na Pythonu 3.14 vydává ResourceWarning o neuzavřených rourách v dosavadních runner testech; testy prošly, životní cyklus runneru se v tomto kroku neměnil.
- Chromium/Playwright: `tests/e2e_examples.py` prošel se studentským kódem na Pythonu 3.14.8. Ověřeno přepínání, zachování úprav při přepnutí i obnovení stránky, původní ukázka, funkční běh upraveného příkladu, vstup přes input(), zastavení při přepnutí, obnova příkladu, nezměněný rozepsaný úkol a mobilní šířka 380 px. Ovladač Playwright běžel v platformním Pythonu 3.12.
- Ověřeno i skutečné `start.py --no-browser`, katalog, načtení variant přes API a spuštění kódu na Pythonu 3.14.8. Windows, macOS a skutečné VSCodium v tomto kroku neověřeny.
- Cloud: Python 3.14.8 nainstalován do `/workspace/.python`, venv `/workspace/.venvs/python-academy-3.14.8`. Přístup ke GitHubu ověřen `git ls-remote origin HEAD`. Dřívější selhání sítě bylo způsobeno socketovým omezením sandboxu; s rozšířeným oprávněním funguje. Uloženy nové install_script a start_skill do pracovního návrhu; agent nic nepublikoval.
- Další krok: zpětná vazba uživatele k novým příkladům; původní plán zůstává pozastavený.

## v0.35 (3. 11. 2026): příprava všech podkurzů a úvodní koncept
- Nové zadání uživatele: sjednotit přípravu prostředí a uspořádat návrhy do úvodního podkurzu. Původní obsahový plán (např. další lekce OOP) zůstává pozastavený.
- Na první místo katalogu přidán podkurz `priprava` „Začínáme: prostředí, projekt a Git“, výslovně označený `concept` / Koncept. 14 průvodců v 5 modulech: orientace a nástroje; vlastní projekt a podkurzy; místní server; Git/GitHub/obnova; volitelný virtuální server a nasazení.
- Každý průvodce má cíl, praktické kroky a vlastní kontrolní seznam. Nový typ `kind: guide` nevytváří falešná automatická cvičení pro lokální instalaci. Checklist a ruční splnění jsou oddělené. Jde o koncept k dalšímu dopracování, nikoli dokončený prakticky ověřený kurz pro všechny OS a editory. Návrh i hranice rozsahu: `docs/koncept-priprava.md`.
- Před lekcemi všech 9 podkurzů, včetně plánovaných, je rozbalitelná příprava s nezávislou volbou Windows/PowerShell, macOS, Linux a VS Code, VSCodium, PyCharm. Zahrnuje balíčky, systémové součásti, interpreter, ověřovací příkazy a spuštění. Volby se pamatují; vlastní potvrzení připravenosti je oddělené podle podkurzu, OS a editoru. Nic se nezamyká.
- Nový `/api/preparation` a `server/preparation.py`, balíčky ze stejného zdroje jako `tools/setup_env.py`. Přidáno `--extras`: PyInstaller, qrcode[pil] a pyttsx3 se instalují jen na výslovnou volbu. SQLite a Tkinter nejsou pip balíčky. Nový profil má i samotný úvodní podkurz, bez pip závislostí.
- Společná stránka přípravy rozšířena o výběr podkurzu a samostatné návody VS Code/PyCharm vedle VSCodium. Aktualizovány instalační a spouštěcí pokyny. Tlačítko „Otevřít ve VSCodium“ v lekci nadále míří pouze na VSCodium; pro ostatní editory je výslovně popsané ruční otevření vypsané cesty.
- GitHub, klonování a VPS jsou návody, nikoli provedené vnější akce. Nevytvořili jsme repozitář ani server. VPS část používá malý vlastní projekt a statický web přes SSH tunel; veřejné nasazení je plán konkrétních dalších kroků, ne vystavení Dílny se spouštěním studentského kódu na internet.
- Ověřeno na Pythonu 3.14.8/Linux: 81 unittest testů OK (0 přeskočených). Validátor: 110 lekcí, 0 chyb a upozornění — původních 96 s běhovými kontrolami včetně 68 příkladů, plus strukturální validace 14 koncepčních průvodců.
- Chromium/Playwright: nový test `e2e_preparation.py` prošel (první karta, všech 9 profilů, 3 × 3 systém/editor, uložení voleb, oddělené potvrzení, checklist průvodce, dokumenty a mobilní šířka). Prošly také dosavadní `e2e_setup.py` a `e2e_web.py`. Chybějící favicon způsobující 404 v regresním testu doplněn vlastní malou SVG ikonou.
- Praktické linuxové kroky ověřeny na dočasném projektu: vytvoření .venv, spuštění main.py, pip check, místní Git init/add/commit/větev/merge a statický http.server s HTTP požadavkem. Windows/macOS, skutečná menu editorů, GitHub přihlášení/push, SSH a VPS nejsou ověřeny skutečným provedením. Tyto části mají zůstat označené k vlastnímu ověření.
- Dosavadní lekce, mini-projekty a 68 přepínatelných příkladů nebyly přepsány. Připraven archiv v0.35. Agent nic nepublikoval a neměnil cloudový instalační návrh; existující Python 3.14.8 zůstává.
- Další krok: připomínky ke konceptu a případné zvolení jedné části k podrobnému dopracování. Bez nového zadání nepokračovat původním plánem.

## v0.36 (3. 11. 2026): srozumitelné příkazy a spuštění přes token
- Uživatel schválil doplnění vysvětlení a návrh nové lekce po místním serveru. Všech 14 původních průvodců přípravy má nyní oddíl „Co příkazy dělají a co se děje“: význam argumentů, pracovní složka, procesy, změny a očekávané výsledky. Příkazy jsou vysvětlené v kontextu konkrétní lekce.
- Za místní server vložena nová devátá lekce `09-server-a-token`, celkem 15 průvodců. Dosavadní id lekcí se zachovala, aby fungovaly odkazy i uložené checklisty; zobrazované číslo určuje pořadí v course.json (Git začíná číslem 10).
- Lekce vysvětluje odlišné role .venv, serveru a tokenu a poskytuje hotové soubory main.py, token_server.py a token_client.py v jejím files/. Student je zkopíruje do vlastní složky token-demo, vytvoří .venv, ověří přímý běh a pak spustí server a klienta ve dvou terminálech.
- Ukázka používá jen standardní knihovnu. Server generuje nový token při startu, ověřuje hlavičku, Host a Origin, poslouchá pouze na loopbacku a spouští výhradně main.py pomocí sys.executable. Klient nemůže předat kód, cestu ani shellový příkaz. Program je neinteraktivní s timeoutem 5 sekund. Token se nevkládá do URL, zdrojů ani souboru. Ukázka je pro místní vlastní důvěryhodný program, nikoli sandbox nebo veřejný server.
- Python klient je první názorný krok; v lekci se vysvětluje i analogie tlačítka v prohlížeči. V této dodávce nevzniklo nové webové tlačítko nebo veřejné nasazení.
- Ověřeno na Pythonu 3.14.8/Linux: 87 unit testů OK, bez přeskočení, včetně 6 testů tokenové ukázky. Ověřeno odmítnutí chybějícího/chybného/starého tokenu, cizího Host/Origin, GET, cizí cesty a těla s kódem; při odmítnutí se program nespouští. Ověřen i výstup pevného programu a stejná cesta interpreteru.
- Navíc proběhl skutečný start token_server.py a token_client.py v samostatných procesech v .venv: správný token vrací pozdrav, chybný HTTP 401. Validátor 111 lekcí bez chyb a upozornění (96 původních běhově, 15 průvodců strukturálně), e2e_preparation.py OK. Windows/macOS a grafické editory se tímto strojovým ověřením nepotvrzují.
- Aktualizovány README a koncept. Archiv v0.36. Dosavadní výukové kurzy a jejich mini-projekty nezměněny; nic nebylo publikováno. Další rozvoj podle konkrétní zpětné vazby uživatele, původní plán nadále pozastaven.

## Přesun v0.36 do Git repozitáře (3. 11. 2026)
- Na výslovnou žádost uživatele vložen obsah archivu v0.36 do existujícího checkoutu Liborias/Python-Academy. Hlavní historie prvního commitu zachována; aplikace leží přímo vedle README a .git.
- Přidán návod `docs/lokalni-projekt-git.md` pro clone, místní .venv, aktualizace a oddělené korekturní větve. README odkazuje na návod. Ignorovány i lokální .env soubory a ZIP archivy.
- Pro další vývoj používat `/workspace/Python-Academy`, nikoli původní adresář rozbaleného archivu. Publikace cloudového prostředí sama neodesílá Git commity.
- Tento krok nepřidává nové lekce ani nepokračuje původním plánem; převádí hotový projekt na doručování přes Git.
- Ověření v cílovém checkoutu před odesláním: 87 unit testů OK, validátor 111 lekcí bez chyb a upozornění, e2e_preparation.py OK na dostupném Chromium. Použit Python 3.14.8.

## v0.37 (3. 11. 2026): pět přepínatelných úkolů v Základech
- Uživatel požádal verzovat další práci přímo do GitHubu a nevytvářet další ZIPy. V tomto kroku vzniká Git commit pro main; distribuční ZIP se nevytváří.
- Ve stejných 34 lekcích, které mají další příklady (Základy 01–31 a 37–39), přidáno 136 nových úkolů. Tlačítka Úkol 1 až Úkol 5 přepínají zadání, vlastní kód a kontrolu. Původní exercise.py/check.py/solution.py zůstaly beze změn jako Úkol 1.
- Každý nový úkol má exercise.md, exercise.py, solution.py a check.py v tasks/task-2 až tasks/task-5, metadata v tasks.json. Zadání procvičují pouze znalosti dané nebo předchozích lekcí; funkce mají testy různých vstupů a krajních případů, náhodnost testuje rozsah a variabilitu. Kontroly připouštějí správné alternativy, například řešení seznamu bez append.
- U původního úkolu zachován localStorage klíč i workspace soubor, další jsou oddělené podle id úkolu. Úspěchy procvičení mají vlastní značky ✓; splnění lekce se dál váže na původní úkol nebo ruční potvrzení. Reset obnovuje pouze vybraný úkol. Výsledky kontrol se nepřenášejí mezi úkoly.
- API check/run/workspace nově volí task; neplatné identifikátory a cesty se odmítají. Ve veřejném API jsou jen zadání a šablony, nikoli kontroly a řešení. Zachována původní HTTP 400 pro neplatné workspace identifikátory.
- Opraveno přepínání běžících programů: pozdní odpovědi starého běhu se ignorují a případný proces dokončeného startovacího požadavku se zastaví. Přepnutí úkolu ukončí jeho běh a vyčistí výstup. Pozdní check nebo načtení souboru nepřepisuje jiný úkol ani mezitím upravený kód.
- Ověřeno na Pythonu 3.14.8/Linux: validátor 111 lekcí bez chyb a upozornění, včetně běhu všech 136 nových vzorových řešení a odmítnutí všech šablon. Celá unittest sada má 91 scénářů; po nalezení a opravě odlišného HTTP statusu byla znovu úspěšně provedena dotčená skupina 44 API/server/workspace/tools testů. Ostatních 47 scénářů prošlo v celkovém běhu. Specifické kontroly pro lekce 7 a 29 znovu ověřeny po upřesnění testů.
- Chromium e2e_tasks.py OK: pět voleb, přepínání zadání, zachování draftů i po reloadu, kontrola správné varianty, vlastní ✓ bez ovlivnění splnění lekce, reset, vlastní pracovní soubor, opožděná kontrola, zastavení běhu, mobil a nezměněné projekty. e2e_examples.py OK jako regrese původních přepínatelných příkladů. Testy nemohou potvrdit skutečné chování externího VSCodium na počítači uživatele.
- Mini-projekty 32–36, závěrečný test 40 a všechny ostatní podkurzy zůstaly obsahově beze změn. Původní plán dalších kurzů nepokračuje. Další dodávky přes GitHub, bez automatického vytváření ZIPů.

## v0.38 (3. 11. 2026): favicony, obsahové názvy a úvod do OOP
- Uživatel výslovně obnovil pokračování kurzu Turtle, OOP a hra Snake. V této dávce dokončen nový modul m03, lekce 17–20: třída a instance; __init__ a self; metody měnící stav; vlastní seznam každého objektu. Turtle/OOP má nyní 20 ze 40 plánovaných lekcí. Hra Snake se teprve bude stavět na těchto základech, v této dávce nevznikla.
- Každá nová lekce má srozumitelný výklad dění v programu, konzolovou ukázku s komentáři, samostatný úkol, šablonu, vzorové řešení, kontrolu a tři kvízové otázky. Ukázky jsou zvířata, knihy, teploměry a playlisty; úkoly hráči, obdélníky, počítadla a batohy. Pojmy se zavádějí v pořadí od class/pass přes self a konstruktor k metodám a sdílení měnitelných hodnot.
- Kontroly OOP ověřují skutečné instance, různé argumenty, více objektů současně, opakované změny stavu, negativní i nulové přírůstky, reset, vlastní seznamy, duplicity a nezávislost vrácených kopií. Chybné studentské atributy a metody mají vracet srozumitelné výsledky, nikoli shodit kontrolní proces.
- Přidán test_oop_intro.py: 28 chybných variant odmítnuto, 7 správných alternativ přijato. Akceptuje například jiná lokální jména, hromadné přiřazení, explicitní return None a různé způsoby kopie seznamu. Původní příklady a úkoly jiných lekcí nepřepisovány.
- U 34 lekcí s přepínatelnými ukázkami dostala první ukázka obsahový název v example_title (např. Planeta Merkur, Cena s DPH, Slovník známek). Ve webu nahradil obecné tlačítko „Původní ukázka“. API vrací example_title, fallback je název lekce. Interní id original a klíče rozepsaného kódu zůstaly stejné.
- SVG favicon již existovala; doplněna ICO varianta 16/32/48/64 px a verze odkazů kvůli cache prohlížeče. Nová ikonka nevyžaduje žádný balíček při běhu aplikace.
- Ověřeno na Pythonu 3.14.8/Linux: všech 95 unittest testů OK (bez přeskočených); validátor všech 115 lekcí bez chyb a upozornění (včetně dřívějších 136 procvičovacích úkolů). Nový e2e_oop_intro.py v Chromium ověřil čtyři skutečné výstupy ukázek, odeslání čtyř řešení, kontrolu, uložení splnění a přehled 20 lekcí. e2e_examples.py prošel s novým názvem první ukázky, zachováním draftů a HTTP načtením SVG/ICO.
- Skutečné Windows/macOS, grafická okna, editory a kreslení želvou nebyly tímto krokem nově ověřeny; nové lekce 17–20 jsou konzolové a nepotřebují grafické prostředí.
- Další blok: zapouzdření a pravidla změn stavu, dědění a super(); orientačně 4 lekce a 12–18 tisíc tokenů podle šířky kontrol. Další podkurzy se bez zadání nerozšiřují. Dodávka přímo přes GitHub, bez ZIPu.

## v0.39 (3. 11. 2026): další OOP lekce a oddělený koncept nového kurzu
- Pokračování původní rozpracované tvorby: do Turtle/OOP doplněny lekce 21–24 v modulu m04: zapouzdření a pravidla stavu, property, dědění/přepisování, super. Každá má výklad, konzolovou ukázku, úkol, šablonu, řešení, kontrolu a tři kvízové otázky. Kurz má nyní 24/40 lekcí, Snake zatím nevznikl.
- Kontroly ověřují také zachování stavu po odmítnuté operaci, obě hranice property, neplatnou konstrukci, pouze čtenou property, nezávislé instance, skutečné dědění a spolupráci základní a odvozené třídy. U super se změní základní popis a sleduje základní inicializátor, aby neprošlo pouhé opisování výsledku.
- Test_oop_rules.py odmítl 34 chybných variant a přijal 8 správných alternativ (včetně jiného vnitřního atributu, odmítajícího setteru read-only property, vlastního správného konstruktoru a alternativního zápisu super).
- Během práce uživatel požádal o zajímavý OOP plán a upřesnil, že má jít o samostatný kurz, nikoli součást Turtle a her. V odpovědi na otázku výslovně zvolil: dosavadní OOP lekce zatím ponechat a nový kurz pouze navrhnout. Proto se stávající obsah nepřesouvá; návrh hry ve stávajícím kurzu byl zrušen ještě před commitem.
- Nový samostatný koncept `oop` má kartu v hlavním katalogu hned za Základy a panel s plánem. Navrženo 20 lekcí v 5 modulech: první objekty, pravidla a property, spolupráce/dědění, čitelnost a testy, praktický projekt. Celková obtížnost 3/4, vstupní kroky od 2/4. Vyžaduje základy Pythonu, nikoli Turtle, hry nebo grafiku.
- Nosné téma: Chytré expediční centrum — objednávky, zásoby, storna a různé způsoby doručení. Zábavnost stojí na praktických scénářích a hledání chyb, ne na herním prostředí. Jde pouze o návrh v courses/oop/plan.md. V novém kurzu nejsou lekce, řešení ani implementovaný projekt; nerealizovat ho bez dalšího zadání.
- Inspirace praktickým vývojem: veřejný cosmicpython/code ke knize Architecture Patterns with Python, ověřeno 2726 hvězdiček k 3. 11. 2026. Hvězdičky vyjadřují komunitní zájem, ne recenze studentů. Zdrojový projekt ani jeho pokročilá architektura, Docker nebo staré instalační pokyny se do kurzu nekopírují. Odkaz a omezení zdroje jsou v návrhu.
- API course přidává learning_plan.md ze souboru plan.md; v katalogu se nový koncept zobrazuje jako plán 20 lekcí, bez falešného průběhu 0/0. Připraven základní profil prostředí oop (jen standardní Python). Katalog nyní obsahuje 10 podkurzů.
- Všech 101 unittest testů prošlo bez přeskočených. Validátor ověřil 119 skutečných lekcí bez chyb a upozornění; koncept oop nemá žádné realizované lekce a do tohoto počtu se nepřičítá. Chromium e2e_oop_rules.py ověřil čtyři ukázky, řešení a uložené splnění; e2e_course_plan.py samostatný návrhový panel/obtížnost/zdroj/mobil a zachování původního kurzu. Prošly i e2e_preparation.py (10 profilů) a e2e_web.py.
- Další dávka původního Turtle/OOP: speciální metody, rovnost, MRO a dataclass, orientačně 4 lekce. Nový samostatný OOP zůstává pouze plánem. Dodávky přes GitHub/main, bez ZIPů.


## v0.40 (3. 11. 2026): speciální metody, rovnost, MRO a dataclass
- Na pokračování uživatele dokončen modul m05 původního Turtle/OOP, lekce 25–28. Kurz má nyní 28 ze 40 plánovaných lekcí. Každá nová lekce má výklad, komentovanou konzolovou ukázku, úkol, šablonu, řešení, kontrolu a tři kvízové otázky.
- Lekce 25: str, repr a len na vlastní třídě, návrat místo výpisu, !r a kopie vstupního seznamu. Kontrola tras ověřuje prázdné vstupy, diakritiku/uvozovky, aktuální stav a čtení bez změn seznamu.
- Lekce 26: identita is proti hodnotové rovnosti ==, __eq__, isinstance, NotImplemented a možnost porovnání druhou stranou. Kontrola bodů zkouší obě souřadnice, změnu stavu, odvozený typ, nepodporované typy i !=. Hashování se zde neimplementuje.
- Lekce 27: MRO, diamantové dědění a spolupráce super pro stejnou instanci. Kontrola pěti tříd ověřuje obě pořadí základů, nové výsledné seznamy a po změně základní metody její skutečné využití právě jednou. Vícenásobné dědění je vysvětlené jako nástroj pro čtení kódu, ne povinnost pro každou hru.
- Lekce 28: standardní dataclasses, anotace bez automatické runtime validace, vygenerované metody a field(default_factory=list). Kontrola záznamů hráčů ověřuje vlastní seznamy, explicitní argumenty, pořadí/duplicity/prázdné události a vliv polí na rovnost. Factory nekopíruje výslovně předaný seznam; výklad tento rozdíl vysvětluje.
- Nový test_oop_tools.py: 35 chybných variant odmítnuto a 8 správných alternativ přijato. Pokrývá sdílení seznamu, konstantní nebo zastaralé výstupy, nesprávný návrat, porovnání jen jedné souřadnice, chybné typové odmítnutí, nefunkční super, opakované volání základu a chybnou dataclass/factory.
- Validátor na Pythonu 3.14.8/Linux: 123 lekcí, 0 chyb a upozornění, včetně dřívějších 136 procvičovacích úkolů. Nové ukázky běží, čtyři řešení projdou a čtyři šablony neprojdou.
- Celá unittest sada: 105 testů OK, bez přeskočených (Python 3.14.8/Linux). Po úspěšném výsledku se při ukončení procesu objevují ResourceWarning o neuzavřených rourách; běhové moduly serveru se touto obsahovou dávkou neměnily.
- Chromium/Playwright: e2e_oop_tools.py prošel se čtyřmi skutečnými výstupy ukázek, odesláním řešení a kvízy; reload zachoval rozepsaný kód i splnění nových lekcí a dříve splněnou lekci 24. Prošly také e2e_oop_rules.py a e2e_course_plan.py. Dosavadní testy přehledu nyní tolerují přidávání dalších lekcí.
- Nový samostatný kurz oop zůstává pouze původním konceptem; žádná výuková implementace do něj nepřibyla a žádné stávající lekce se nepřesouvají. ID starých lekcí, úkolů a klíče uloženého postupu zůstaly zachované. Nové lekce nevyžadují pip balíčky; skutečné Windows/macOS a editory tímto během nově ověřeny nebyly.
- Další dávka: začátek projektu Snake, orientačně lekce 29–32 (model/mřížka, zobrazení, časovač/pohyb, ovládání), poté 33–36 a závěrečný kvíz/API 37–40. Pokračovat po menších dávkách. Dodávka přes GitHub/main, bez ZIPů.
