# Formát podkurzů a lekcí

## courses/catalog.json
Seznam podkurzů (id, title, level 1–4, lessons, doporuceno, status: planned|draft|ready, summary).

## courses/<id>/course.json
```json
{
  "id": "zaklady",
  "title": "Základy Pythonu",
  "requires_packages": [],
  "modules": [
    {"id": "m01", "title": "Začínáme", "lessons": ["01-prvni-program", "02-chyby"]}
  ]
}
```
Pořadí lekcí = od jednoduchých ke složitým. `requires_packages` = pip balíčky pro celý podkurz (např. `["pandas", "matplotlib"]`).

## courses/<id>/lessons/NN-nazev/
| Soubor | Povinný | Účel |
|---|---|---|
| `lesson.json` | ano | `{"title": "...", "minutes": 10, "kind": "console|gui|notebook", "tags": []}` |
| `lesson.md` | ano | výklad (Markdown: nadpisy, odstavce, seznamy, `code`, bloky ```python, `> poznámka`) |
| `example.py` | ano | ukázka s komentáři vysvětlujícími kód; musí běžet bez chyby |
| `exercise.py` | ano | šablona pro studenta (kopíruje se do `workspace/<podkurz>/<lekce>/reseni.py`); nesmí projít kontrolou |
| `check.py` | ano | kontrola přes `dilna_check` (viz lib/dilna_check); GUI používá odpovídající běh bez okna a případně AST/funkce |
| `solution.py` | ano | vzorové řešení; musí projít kontrolou |
| `files/` | ne | pomocné soubory lekce (texty, CSV, HTML…). Kopírují se do složky, kde běží kód studenta (spuštění, kontrola i pracovní složka ve VSCodium). Student je otevírá relativní cestou, např. `open("data.txt")` |
| `quiz.json` | ne | `[{"q": "...", "options": ["..."], "answer": 0, "why": "..."}]` |

## Pravidla
- Žádné autorské postavy a značky (žádný Harry Potter apod.), grafika her je kreslená kódem.
- Soubory se čtou a zapisují s `encoding="utf-8"`.
- Lekce o sítí mají mock data v `courses/<id>/data/` a běží offline.
- Hesla a klíče nikdy v kódu, jen v proměnných prostředí.

## Přepínatelné příklady (od v0.34)
Volitelný `examples.json` je seznam dalších **konzolových** ukázek:
```json
[
  {
    "id": "varianta-1",
    "title": "Název tlačítka",
    "description": "Co sledovat nebo změnit.",
    "code": "# Vysvětlení.\n# Další vysvětlení.\nprint(2 + 3)\n",
    "stdin": ""
  }
]
```
`id` musí být jedinečné v lekci (rezervováno `original`), podle stejných pravidel jako id lekce.
`stdin` je volitelný vstup **pro validátor**; student vstup zadává při běhu sám.
Validátor spustí každou variantu, vyžaduje úspěšné dokončení a nejméně dva komentáře.
Původní `example.py` se zachovává jako první ukázka. Tlačítka se zobrazí pouze u lekcí
s dalšími příklady. Jejich editor je upravitelný a každá varianta má vlastní
rozepsaný kód v localStorage. Přepnutí neovlivňuje úkol, jeho kontrolu ani postup studenta.
V aktuální verzi jsou varianty pouze v Základech, lekce 01–31 a 37–39;
mini-projekty 32–36, závěrečný test 40 a ostatní podkurzy jsou beze změny.

## Koncept úvodního podkurzu (od v0.35)
Katalog může obsahovat `status: "concept"` (štítek Koncept). `priprava` je první
podkurz se 14 navrženými lekcemi, ne automatická kontrola nastavení počítače.

Průvodce má `lesson.json` s `kind: "guide"` a `lesson.md`. Nemá `exercise.py`,
`solution.py` ani `check.py`. Jeho povinné oddíly jsou `## Cíl`,
`## Praktický krok` a `## Vlastní ověření` s alespoň jedním `- [ ]` bodem.
Validátor kontroluje strukturu; neprovádí instalace, Git push, přihlášení ani
nasazení z textu. UI checklisty ukládá pro každou lekci zvlášť a splnění je ruční.
Dosavadní konzolové/GUI lekce dále podléhají všem původním běhovým kontrolám.

## Příprava každého kurzu
`server/preparation.py` popisuje účel balíčků, systémové požadavky a ověření.
Seznam balíčků přebírá z `tools/setup_env.py`: `PACKAGES` a `OPTIONAL_PACKAGES`.
Volitelné součásti instaluje jen explicitní `--extras`. Nový podkurz musí mít
profil i záznam balíčků; test kontroluje shodu s celým katalogem.

`GET /api/preparation?course=<id>` vrací profil nebo 404. Web jej vykreslí před
seznamem lekcí, včetně plánovaných kurzů, a na společné stránce přípravy.
Podporované volby: Windows/PowerShell, macOS, Debian/Ubuntu a VS Code,
VSCodium, PyCharm. Systém a editor se pamatují, potvrzení se ukládá odděleně pro
kombinaci kurzu/systému/editoru. Profily i potvrzení nemění průchodnost lekcí.

### Soubory tokenové ukázky (v0.36)
Úvodní podkurz má 15 průvodců. Nová devátá lekce `09-server-a-token` obsahuje
ve `files/` tři samostatné výukové soubory. Průvodce je nespouští automaticky;
student je zkopíruje podle návodu do vlastní složky a spustí je v terminálu.
Jejich skutečný běh a odmítání neplatných požadavků ověřuje `tests/test_token_lesson.py`.
Zobrazované pořadí pochází z course.json, id dřívějších lekcí se kvůli vložení neměnila.

## Přepínatelné úkoly (v0.37)
Původní exercise.py, check.py a solution.py zůstávají v kořeni lekce jako Úkol 1.
Volitelný `tasks.json` obsahuje čtyři položky `{"id":"task-2","title":"Pozdrav a součet"}`
až po task-5. Jejich obsah leží v `tasks/<id>/exercise.md`, `exercise.py`,
`check.py` a `solution.py`. Zadání musí uvádět vstupy, očekávané výstupy nebo
návratové hodnoty a doménu platných vstupů. Checker má ověřovat více případů a
mezní hodnoty, aniž by odmítal správné alternativní řešení.

API lesson vrací pole tasks s id, title, md, exercise a has_solution; kód kontroly
a řešení do tohoto seznamu nevkládá. Has_solution je také na úrovni původního úkolu.
API check/run/workspace/open/save přijímá volitelné pole task. GET workspace má
stejnojmenný parametr. Vynechání nebo task-1 používá původní chování.
Ostatní id mimo task-2 až task-5 se odmítají; vybraná kontrola musí existovat.
Pracovní soubor původního úkolu se nemění, další jsou v
`workspace/<kurz>/<lekce>/tasks/<task-id>/reseni.py`.

Web zachovává původní localStorage klíč kódu pro Úkol 1. Nové úkoly mají vlastní
klíče, vlastní značky úspěšného procvičení a oddělené výsledky kontrol. Úspěch
nového úkolu automaticky neoznačuje původní úkol za splněný. Pozdní odpověď nesmí
přepsat právě vybraný úkol ani hodnotit mezitím upravený kód. Přepnutí zastaví
běžící program a vyčistí jeho výstup.

Validátor provede vzorové řešení i výchozí šablonu každého dalšího úkolu. Řešení
musí projít, šablona nesmí; chyba samotného kontrolního procesu není řádné
odmítnutí šablony. Rozsah aktuálně odpovídá 34 lekcím s examples.json.

## Obsahový název první ukázky (v0.38)
Volitelné pole `example_title` v lesson.json pojmenuje původní example.py.
API jej vrací pod stejným názvem; bez pole použije název lekce. Přepínač zobrazuje
obsahový název, interní id původního příkladu však zůstává `original`, aby se
zachoval rozepsaný kód v prohlížeči. Toto pole nepřidává novou variantu ani
nemění počty příkladů/úkolů.

## Plán samostatného kurzu bez výukových lekcí (v0.39)
Katalogový záznam může mít `status: concept`, `lessons: 0` a `planned_lessons`
s počtem navržených lekcí. Karta pak ukazuje plán, nikoli průběh 0/0 nebo hotové
lekce. Course.json má prázdné modules a objekt learning_plan (title, level,
summary, placement, difficulty_reason, duration). Text plánu je ve fixním souboru
plan.md vedle course.json; API course jej přidá jako learning_plan.md.

Web zobrazí samostatný rozbalitelný panel plánu. Nespouští kód a neoznačuje nic
za splněné. OOP má vlastní id oop a profil přípravy; všech 20 programových lekcí
je hotových. Panel dál nabízí úplný přehled kurzu. Dosavadní lekce v turtle-oop se nemigrují a jejich id
ani uložený postup se nemění.

## Delší interaktivní běh
Volitelné `run_timeout` v lesson.json je celé číslo 1–600, počet sekund pro spuštění
ukázky i úkolu v prohlížeči. Chybějící či neplatná hodnota zachová výchozích
20 sekund pro konzoli a 600 pro GUI. Kontrola řešení si ponechává vlastní limit.
Závěrečné expediční centrum má 600 sekund pro ruční zadávání příkazů; Stop funguje dál.

## Odkrývání řešení v Základech (od v0.49)
Pro kurz zaklady vrací lesson API příznak `has_solution`, pokud existuje neprázdné
solution.py. Totéž platí pro další úkoly. Web nabízí zavřený panel „Zobrazit možné
řešení“; při otevření načte `GET /api/solution?course=zaklady&lesson=<id>&task=task-1`.
Vynechané task nebo task-1 čte solution.py z kořene lekce, task-2 až task-5 ze svého
podadresáře. Vrací course, lesson, kanonické task a code. Neexistující/nesprávná
volba nebo jiný kurz vrací 404. Endpoint používá stejné kontroly Host/Origin jako
čtení lekce a neprovádí kód ani zápisy do workspace.

Panel používá existující otestované vzory; při úpravě řešení ponechte shodu se
zadáním a ověřte jej kontrolou daného úkolu. Zobrazení nic nevkládá do editoru,
neprovádí kontrolu a nemění značky splnění. Přepnutí úkolu panel zavře, vymaže
předchozí zobrazení a ignoruje opožděnou odpověď jiného úkolu. Jednotlivá načtená
řešení se drží jen v paměti aktuální stránky; obnovení stránky je znovu skryje.

## Úvodní Tkinter bez okna (od v0.50)
`r = c.tk_run(actions=[{"action": "fill", "value": "  Ema  "},
{"action": "click", "text": "Pozdravit"}])` spustí studentský program v podprocesu
s malou náhradou modulů tkinter/ttk. Podporuje Tk, Label, Button, Entry, Frame,
Checkbutton/Radiobutton, StringVar/IntVar, základní nastavení okna, configure/config, pack/grid a přístup
k textu. Od v0.52 také Listbox, Text, Scrollbar, řádky mřížky a řízené odpovědi
filedialog. Nejde o úplné Tk ani vykreslování; nepodporované funkce skončí chybou.
Před přidáním dalšího widgetu nebo událostí je nutné náhradu rozšířit a ověřit
proti skutečnému Tkinteru. Míchání pack/grid v jednom rodiči je chyba.

Mainloop zachytí počáteční stav a postupně provede zadané akce. Fill vyžaduje
právě jedno viditelné Entry; click právě jeden viditelný Button, Checkbutton nebo
Radiobutton s daným textem. Volby mění svou propojenou proměnnou před callbackem.
Akce `{"action": "key", "sequence": "<Return>"}` odešle událost widgetu, který
dostal focus_set. Bind předává objekt s widget/keysym, podporuje nahrazení vazby,
add="+" a návrat break. Z rozsahu Tk vazeb podporujeme jen vlastní vazbu widgetu
a hlavního okna pro tuto událost, nikoli třídní vazby a úplnou logiku klávesnice.
`r.widgets("label", index=0)` vrátí počáteční popisky, index=1 stav po první akci,
index=-1 poslední stav. Záznam má id/kind/parent, text, visible, manager/layout
a pořadí umístění, columns/rows, state, focused a bindings; okno navíc title/geometry/minsize,
tlačítko has_command, vstup value a přepínače selected/variable_kind.
Výsledek obsahuje také mainloops, error, timed_out, crashed, out/err.
`c.tk_no_error(r)` vypíše případnou chybu včetně studentského řádku. Běh má časový
limit, limit kroků studentského kódu a počtu widgetů.

Kontroly mají ověřovat stavy před kliknutím i po více opakováních, nové hodnoty
vstupu a zachování původního widgetu. Samotná přítomnost callbacku nestačí.
Validátor Tkinter ukázku skutečně provede přes tuto náhradu a vyžaduje viditelné
okno s hlavní smyčkou. Vzhled a skutečnou odezvu prvních dvanácti lekcí ověřuje
`python tests/tkinter_real_smoke.py` na grafické ploše se skutečným Tk;
volba `--shots DIR` uloží snímky, pokud je dostupný Pillow.

Pro oddělený výpočet lze použít `c.tk_run(run_name="student", calls=[
{"name": "preved_vzdalenost", "args": [1.25, "km-m"]}])`. Program dostane jiné
__name__ než __main__, takže může přeskočit blok s otevřením okna. R.calls
obsahuje pro každé volání value a error (stejný formát chyby včetně řádku).
Argumenty a návratové hodnoty jsou omezené na JSON data; výjimka jednoho volání
se zaznamená a další pokračují. Tato cesta stále používá náhradu Tk, proto
kontrola 8 navíc vyžaduje, aby import a výpočet nevytvořily žádné widgety.

### Seznamy, delší text a soubory (v0.52)
Listbox má insert/delete/get se zahrnutým posledním indexem, size,
curselection, selection_set/clear a see. Snapshot obsahuje items, selection a yview.
Akce `{"action":"select","index":2}` vybere jediný řádek a vyšle
<<ListboxSelect>>; index=null výběr vymaže. Programové selection_set samo
událost nevyvolává, stejně jako ve skutečném Tk. Ověřujte i stejné názvy na
různých indexech a návaznost dalších operací na změněný model.

Text podporuje insert/delete/get s indexy řádek.sloupec, end a end-1c.
Get do end zahrne automatický koncový nový řádek; snapshot value jej vynechává.
Akce `{"action":"fill_text","value":"A\nB\n"}` změní právě jeden Text;
disabled odmítá úpravy stejně jako reálný widget. Posun je logický podle řádků
a height, bez měření písma či zalamování. Yview hlásí výřez přes yscrollcommand;
Scrollbar má set/get a snapshot range. Akce scroll s fraction nebo number/what
použije command posuvníku; kind=text či listbox může posunout přímo obsah.
Při ověřování posuvu neporovnávejte přesné podíly s pixelovým vykreslením Tk.

`c.tk_run(actions, dialogs=[{"kind":"open","path":"..."},
{"kind":"save","path":""}])` vrací z askopenfilename/asksaveasfilename
připravené cesty v pořadí volání, prázdná znamená zrušení. Jiný typ dialogu nebo
chybějící odpověď je chyba. R.dialogs zaznamená kind/path. Soubory se čtou a
zapisují skutečně, proto kontroly vytvářejí vlastní cvičná data vedle studentova
dočasného souboru. Testujte i neexistující cestu, chybný JSON/kódování, neplatný
pozdější záznam, prázdná data a následnou opravu. Nativní vzhled dialogu není
součástí náhrady. I test skutečného Tk řídí volbu cesty testovacími odpověďmi;
ověřuje skutečné widgety, zachování stavu a souborové operace.

### Události, pracovníci a HTTP (v0.53)
Tk_run podporuje after(ms, callback, *args) a after_cancel. Callbacky vykonává
v hlavním vlákně podle skutečného času, práci threading/Queue ponechává skutečnému
Pythonu. Akce `{"action":"wait","ms":50}` zpracuje naplánované události po danou
dobu. Varianta `{"action":"wait","until":{"kind":"button","text":"Načíst kurz",
"state":"normal"},"timeout":2}` čeká na stav widgetu s omezením času. Nejde
o plný event loop Tk; nepodporované události stále vyžadují rozšíření.

Přístupy k widgetům a Tk proměnným z jiného vlákna kontrola odmítne, i když
student výjimku zachytí. Nezachycené výjimky pracovníka se také hlásí. Tento kurz
předává přes frontu jen běžná data a Tk obsluhuje výhradně z hlavního vlákna.
R.callbacks obsahuje origin (click/after) a ms trvání callbacku. Pomalý požadavek
ani join nemají být v hlavní smyčce. Pro důkaz odezvy ověřujte stav v průběhu
načítání, další ovládání a obnovení po chybě; samotný import threading nestačí.
Entry ve stavu disabled/readonly ignoruje úpravy, stejně jako v reálném widgetu.

Volitelné `http=[{"json":data,"delay_ms":350},{"status":503,"json":{}},
{"error":"Timeout"}]` v tk_run dodá řízené odpovědi místo GET přes
requests.sessions.Session.request. Obslouží také Session.get; vrací skutečný
requests.Response s chováním json/raise_for_status. Body může obsahovat chybný
JSON. R.http zaznamená url, params, timeout a main_thread. Odpovědi jsou jen pro
testování spolupráce GUI; skutečné HTTP, timeout a cvičné endpointy zvlášť ověřuje
test_tkinter_api.py. Zpoždění je skutečné, síťový timeout nenapodobujeme automaticky.

Lekce 13/14 jsou kind=console a validátor spouští jejich příklady skutečně.
Lekce 15/16 používají Tk a ověřuje je navíc `python tests/tkinter_api_real_smoke.py`
na grafické ploše. Tento test používá skutečné místní HTTP, měří odezvu hlavní
smyčky a provede neúspěch i nový pokus. Nepotřebuje veřejnou službu ani účet.
`shared/cvicne_api.py` má přesné kopie ve files všech čtyř lekcí. Kontext spouští
server jen na 127.0.0.1 a volném portu; přidá pro tuto dobu loopback do obou
variant NO_PROXY se zachováním ostatních položek a potom vrátí původní hodnoty.
`kurzy.py` v 15/16 je kopie solution.py lekce 14; shodu hlídá test. Při změně
rozhraní aktualizujte návaznosti. Žádné cvičné kurzy nevydávejte za dnešní tržní data.

### E-mail a místní SMTP (v0.54)
Lekce 17/18 jsou konzolové; validátor skutečně vytvoří zprávu a v 18 ji předá
místnímu SMTP. Lekce 19/20 mají GUI. `test_tkinter_mail.py` ověřuje UTF-8,
hlavičky proti SMTP obálce, přesné bajty přílohy, chyby před změnou zprávy,
konfiguraci i skutečné odmítnutí a ztracené potvrzení. Neprovádí externí odesílání.

`shared/cvicna_posta.py` a jeho přesné kopie ve files 18/20 používají aiosmtpd
na 127.0.0.1 a volném portu. Ověřeno s aiosmtpd 1.4.6/Pythonem 3.14.8;
rozsah instalace je `aiosmtpd>=1.4.6,<2`. Pomocný `_Controller._trigger_server`
doplňuje skutečný port před úvodním spojením při port=0. Používá neveřejný bod
knihovny: při upgradu ověřte start, přenos i ukončení skutečného serveru.
Záchyt zprávy nepřeposílá, uchovává je jen v paměti a přístup k seznamu chrání
zámkem. Režim pomalu uloží zprávu před opožděným potvrzením; timeout klienta
proto není důkazem, že ji server nepřevzal. Žádné automatické opakování přenosu.

Zpravy.py ve files 18–20 je přesná kopie řešení 17 a odesilani.py ve files 20
kopie řešení 18. Shodu těchto čtyř a dvou kopií záchytu hlídá test. Úpravy
rozhraní musí aktualizovat návazné lekce. Náhled zprávy je dekódovaný text;
nenahrazuje serializovaný MIME přenos a nevypisuje binární přílohu jako text.

`c.tk_run(..., extra_env={"DILNA_SMTP_TIMEOUT":"0.05"})` předá řetězcové
proměnné pouze studentskému podprocesu, rodičovské prostředí nemění. Slouží
k ověřování konfigurace a skutečných místních SMTP scénářů, nikoli k náhradě
SMTP falešnými výsledky. Nemění seznam povolených proměnných v běžném běhu
aplikace. Zkoušku vlastních DILNA_SMTP_* provádějte přímo v terminálu/editoru
a po změně prostředí program znovu spusťte, jak vysvětluje lekce 20.

`python tests/tkinter_mail_real_smoke.py` vyžaduje grafickou plochu. Ve
skutečném Tk ověřuje výběr/výměnu přílohy, zrušení a chybu bez ztráty předchozí
zprávy a odezvu při skutečném SMTP, odmítnutí i timeoutu s již uloženou zprávou.
Odpovědi výběru souboru řídí test; vzhled nativního dialogu tím ověřen není.
Veřejná SMTP služba, přihlášení a doručení do skutečné schránky sem nepatří.

### Korespondenční dílna a více polí (v0.55)
Akce `fill` a `fill_text` přijímají volitelné `name`, například
`{"action":"fill","name":"prijemce","value":"jan@example.test"}` nebo
`{"action":"fill_text","name":"telo","value":"A\nB\n"}`. Filtruje vnitřní
jméno z konstruktoru widgetu (`name="prijemce"`), nikoli proměnnou Pythonu.
Snapshot obsahuje name. Bez jména zůstává původní požadavek jediného viditelného
widgetu daného druhu. Chybějící nebo nejednoznačný cíl vyvolá TclError;
disabled/readonly se nadále neupravuje. Stejný filtr podporuje select/scroll.

Lekce 21 zachovává surové texty neúplného konceptu. Lekce 22 sestaví novou
EmailMessage a chyby předá přes ChybaPole s pole. Lekce 23 předává hotový snímek
včetně bytes přílohy pracovníkovi: formulář během přenosu zůstává editovatelný,
ale předávaný objekt už aplikace nemění. Nejde o neměnný datový typ EmailMessage.
Po nejistém výsledku další přenos vyžaduje ruční kontrolu záchytu, bez deduplikace.
Tuto podmínku nesmí obejít ani načtení dalšího konceptu v lekci 24.

Koncept JSON v 24 má verze=1 (skutečný int, nikoli bool) a koncept se čtyřmi
textovými poli. Dovoluje neúplné údaje a neexistující absolutní cestu přílohy;
relativní cestu odmítá. Příloha ani SMTP nastavení a výsledky přenosu se do souboru
nekopírují. Uložení připraví celý obsah před zápisem, zavře dočasný soubor ve
stejné složce a použije os.replace s úklidem ve finally. Ověření modelu a chyba
před nahrazením zachovají původní cíl. Nejde o záruku obnovy po výpadku napájení.
Načtení ověří celý model před první změnou formuláře; při chybě/zrušení ponechá
pole, přílohu i náhled. Platný prázdný model je přípustný a pole vyprázdní.

Test_tkinter_correspondence hlídá 18 přesných pomocných kopií: ve files 22–24
koncept.py ze solution 21, zpravy.py ze 17 a prilohy.py z 19; v 23/24 navíc
priprava.py z 22, odesilani.py z 18, nastaveni.py z 20, cvicna_posta.py ze shared;
ve 24 také prenos.py z 23. Při změně zdrojového řešení aktualizovat návaznosti.
Skutečné Tk/SMTP v tests/tkinter_correspondence_real_smoke.py ověřuje všechna
čtyři okna, zachování při souborové chybě i skutečně přijaté hlavičky, tělo
a bytes přílohy při změně formuláře a souboru během čekání. Odpovědi výběru
souboru jsou řízené testem; vzhled nativního dialogu se netestuje. Chromium
e2e_tkinter_correspondence.py ověřuje kontroly, workspace, reload a mobil,
včetně zachování rozepsané starší SMTP lekce a jejího splnění.
