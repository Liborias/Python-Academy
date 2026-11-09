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
Varianty jsou v Základech, lekce 01–31 a 37–39, a v prvních devatenácti lekcích
Datové analýzy. Nevytvářejí se automaticky pro navazující projektové kroky.

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

## Odkrývání řešení (od v0.49, všechny kurzy od v0.57)
Pro všechny kurzy vrací lesson API příznak `has_solution`, pokud existuje neprázdné
solution.py. Totéž platí pro další úkoly. Web nabízí zavřený panel „Zobrazit možné
řešení“; při otevření načte `GET /api/solution?course=<kurz>&lesson=<id>&task=task-1`.
Vynechané task nebo task-1 čte solution.py z kořene lekce, task-2 až task-5 ze svého
podadresáře. Vrací course, lesson, kanonické task a code. Neexistující/nesprávná
volba či chybějící řešení vrací 404. Endpoint používá stejné kontroly Host/Origin jako
čtení lekce a neprovádí kód ani zápisy do workspace.

Panel používá existující otestované vzory; při úpravě řešení ponechte shodu se
zadáním a ověřte jej kontrolou daného úkolu. Zobrazení nic nevkládá do editoru,
neprovádí kontrolu a nemění značky splnění. Přepnutí úkolu panel zavře, vymaže
předchozí zobrazení a ignoruje opožděnou odpověď jiného úkolu. Jednotlivá načtená
řešení se drží jen v paměti aktuální stránky; obnovení stránky je znovu skryje.
Všech 210 praktických lekcí a 268 doplňkových úkolů má řešení. Průvodce bez
programového zadání ani plánovaný kurz panel nezobrazuje. Zpřístupnění dalšího
kurzu nevyžaduje seznam povolených kurzů v kódu: rozhoduje existence jeho vzoru.

## Kontroly pandas (od v0.59)
Lekce pandas používají volitelný lib/dilna_check/pandas_tools.py. Základní import
dilna_check tím nezískává závislost na pandas. Check_cases porovnává skutečné
Series/DataFrame přes pandas.testing včetně typu, pořadí, popisků a názvu;
aritmetika má toleranci 1e-12, kontrola zachování vstupu je přesná. U prázdného
výsledku bez popisků se nevyžaduje konkrétní typ prázdného indexu řádků
ani sloupců odvozený konstruktorem; dtype hodnot a jména se kontrolují dál.
Výstupní časové indexy se porovnávají podle skutečných hodnot, jednotky a názvu,
nikoli nepovinného metadata freq: správný ručně vytvořený index může mít freq=None.
Přesná kontrola zachování vstupu dál zahrnuje i freq a typ prázdných indexů. Readonly_files hlídá,
že načtené CSV nezmizí ani se nezmění. Případy mají zahrnovat prázdné vstupy,
NaN, jiné názvy/pořadí a čísla, která odhalí předčasné zaokrouhlení.

Doplňkový úkol dědí pouze vlastní files/, nikoli files/ kořene lekce.
Potřebné CSV proto vložte i k příslušnému tasks/task-N/files/. Ověřte nejen
volání funkcí kontrolou, ale také skutečný samostatný běh ukázky řešení.

Lekce 6–10 ověřují také tvar Series/DataFrame/skalár, prázdné a opakované
výběry, číselné popisky proti pozicím, hranice filtrů a masku s přeházeným
indexem. Při požadavku na stabilitu řazení zahrňte delší vstup se shodami;
krátký může dát stejné pořadí i s nestabilním algoritmem. Úpravy tabulek mají
zachovat původní vstup a přiřazení Series má respektovat popisky. Testy
nevyžadují konkrétní zápis, přijímají alternativní správné postupy.

Lekce 11–15 rozlišují NaN/NA/NaT od nuly, prázdného textu a neplatného
existujícího zápisu. Přehled počtů výslovně vrací int64 i bez sloupců;
datumové převody mají určený formát, errors="coerce" a jednotku datetime64[us].
Kontroly zahrnují přestupný rok, nemožný čas, obě hranice období, pravidlo
prvního/posledního výskytu duplicit, četnosti chybějících hodnot a doslovnou
koncovou příponu. Čištění má zachovat neupravované hodnoty i zdrojové vstupy.
Textové příklady ověřujte také s tabulátorem, novým řádkem, diakritikou a NaN.

Dlouhý inline code v odstavci či seznamu prose se může zalomit pomocí
overflow-wrap:anywhere (lesson.css). Samostatné pre.code zachovává původní
řádky a vlastní posouvání; mobilní zkouška ověřuje šířku stránky i toto chování.

Lekce 16–19 ověřují min_count, osu souhrnu, velikost skupiny proti count,
dropna=False pro klíče, tvar a názvy agregací i rozdíl průměru a mediánu.
Pro medián použijte nesymetrická data s alespoň třemi známými hodnotami;
u dvou se průměr a medián mohou shodovat. Bool výsledky mohou být bool nebo
NumPy bool_; číslo 1 se za booleovský výsledek nepřijímá a bool se nepřijímá
za číselný počet. Dtype a jména Series/DataFrame se dál kontrolují.

Projekt pandas 20 je jedna úloha se dvěma funkcemi a bez examples.json/tasks.json.
Má vlastní files/prodeje.csv a README. Checker počítá očekávané přehledy
nezávislým cyklem a kontroluje i poškozené souhrny, přesné počty a toleranci
částek. Samotné kontrolní součty nezaručují správné jednotlivé skupiny.

Lekce 21–25 ověřují zarovnání podle popisků, obě osy concat, opakované záznamy
a počet řádků i při prázdném průniku sloupců. Merge rozlišuje left/inner/outer,
různé názvy klíče, dvojici klíčů, suffixes a categorical indikátor původu.
Validate má odhalit i nepoužitý duplicitní pravý klíč; kontroluje se konkrétní
MergeError a zachování obou vstupů při odmítnutí. Neexistující protějšek
se nesmí určovat podle NaN v ceně známého produktu.

Časové úkoly používají datetime64[us] bez NaT a časového pásma, stabilitu
shod ověřuje i 40 řádků. Přesný úsek zahrnuje obě hranice; celý den zahrnuje
poslední mikrosekundu, ale ne další půlnoc. Mřížka reindex nemá doplňovat
předchozí hodnotu ani agregovat. Resample rozlišuje min_count=1, size/count/mean,
prázdné dny, samé NaN a skutečnou nulu; měsíce používají MS, nikoli 30D či ms.
Test_pandas_joins zahrnuje i správné alternativy, samostatné běhy všech řešení,
pět úryvků výkladu a propojení ceníku s časovým souhrnem. Každá lekce 21–25
má dvě doplňkové ukázky a čtyři doplňkové úkoly; projekt 20 zůstává jeden celek.

## Grafy a náhledy PNG (od v0.64)
Lekce 26–30 jsou kind=console a mají preview_images=true v lesson.json.
API lesson vrací tento bool; API run určí režim z hlavní lekce i u task-2 až
5. Příznak v těle run se nepoužívá. Ostatní běhy neimportují Matplotlib.
Grafické běhy mají MPLBACKEND=Agg a zapisovatelnou cache v workspace/_run/_matplotlib.
Použité skripty vytvářejí skutečný Figure a ukládají PNG bez volání plt.show.

Runner před smazáním celé dočasné složky včetně podsložek načte PNG do paměti.
Poll je vrací po dokončení jako images:[{name,data}] s base64 PNG a image_notice.
Platí stávající token/Host/Origin ochrana; do odpovědi nejdou místní absolutní
cesty ani libovolné soubory. Symlinky se nepřebírají. Maximum 6 PNG, každý
2 MB a 8 milionů pixelů, celkem 4 MB. Kontroluje se hlavička a rozměry;
server k tomu nepřidává závislost na Pillow/Matplotlib. Při vynechání náhledu
vrátí vysvětlení. Toto omezuje náhled, nikoli samostatný export v editoru.

Runner-client tvoří img s pevným data:image/png typem a textové popisky/odkazy
pomocí DOM. Galerie se při novém běhu či změně úkolu/příkladu vyprázdní, stará
opožděná odpověď díky generaci nemůže nahradit nový graf. PNG lze stáhnout;
po reloadu nejsou obrázky uložené v localStorage, znovu je vytvoří běh kódu.
Bílý podklad náhledu neodstraňuje průhlednost staženého PNG. Zveřejnění řešení
zůstává samostatné čtení a nemění rozepsanou práci ani postup.

Volitelný matplotlib_tools.py se importuje jen v grafických kontrolách.
Kontroluje Figure/Axes a skutečné čáry, sloupce, body a histogramy podle dat,
popisků, značek předepsaných úkolem, nulových základen a měřítek. Barva/písmo
nejsou předepsané. Kontroly zachovávají původní tabulky/seznamy; úkoly pro
úpravu existující Axes a export mají zvlášť ověřenou identitu a původní obsah.
Exporty se otevírají přes Pillow: formát, cesta/Path, rozměry, DPI, skutečná
čára, alfa kanál i tight rámeček. Cizí aktuální pyplot Figure odhaluje záměnu
fig.savefig a plt.savefig. Testy přijímají správné alternativy včetně ručního
výpočtu četností/hustoty a odlišného vzhledu, neporovnávají snímky pixel po pixelu.
Lekce 26–30 mají po třech ukázkách a pěti úkolech, každý s možným řešením.

## CSV/XLSX a opakovatelný postup (od v0.65)
Lekce 31–35 mají download_files=true v hlavním lesson.json. API lesson vrací bool,
run jej stejně jako preview_images určí z hlavní lekce i pro doplňkové úkoly,
nikoli z POST těla. Po dokončení poll vrací files:[{name,mime,data}] s base64
pouze pro UTF-8 CSV (také BOM) a XLSX se základní ZIP strukturou sešitu.
Do nabídky patří přiložené vstupy i vytvořené výstupy, včetně podsložek;
helpery .py, poznámky a jiné typy souborů se nezpřístupňují. Maximum 6 souborů,
2 MB každý a 4 MB celkem; symlinky se nepřebírají. Současný projektový běh
může mít files i images. Tyto dva seznamy mají vlastní limity a zůstává
původní token/Host/Origin ochrana. Server nepotřebuje pandas/openpyxl.

Odkazy vznikají přes DOM s pevným MIME podle přípony a jménem jako text.
Galerie souborů se vyčistí při změně úkolu/příkladu či novém běhu, nepřežije
reload. Kód a postup zůstávají; nové odkazy vytvoří spuštění. Opožděný starý
poll nepřepíše aktuální soubory. V editoru výstupy zůstávají v pracovní složce.

Volitelný pandas_files.py kontroluje skutečné soubory nezávisle na studentově
exportu: CSV čte csv.reader a porovnává hlavičky, uvozování, čárku v číslech,
UTF-8/BOM a hodnoty; XLSX otevírá openpyxl a kontroluje listy, hlavičky,
číselné hodnoty a skutečné textové typy kódů. Případy zahrnují jiný název
listu, poznámku před hlavičkou, opačné pořadí sloupců, názvy listů mimo
abecední pořadí, nuly, NA jako text, nový řádek/středník, přesná desetinná
čísla a prázdné tabulky. Zdrojové soubory a vstupy se nesmějí měnit.

Cisteni.py ve files každého úkolu 34 má přesné funkce řešení 34/1 a 34/2;
Kavarna.py ve files 35 funkce projektu 20. Test hlídá AST shodu i vlastní
samostatný běh se správnými soubory. Projekt 35 má tři navazující funkce,
žádné tasks.json/examples.json, jeden vzor a pět kvízových otázek.
Měsíční výběr kontroluje nezávislý cyklus včetně přestupného dne a konce
roku, také skutečně opakované položky. Report se otevírá jako CSV/XLSX/PNG;
Figure.savefig se při skutečném uložení sleduje kvůli ověření dat grafu,
barva/písmo předepsané nejsou. Celkový test validátoru má pro rozšířený katalog
limit 420 s; jednotlivé studentské běhy a CHECK_TIMEOUT zůstávají stejné.

## Závěrečná Analytická dílna (od v0.66)
Lekce 36–42 tvoří sedm navazujících kroků bez tasks.json/examples.json, každý
s jedním řešením a třemi otázkami. Files/predchozi.py má přesné funkce řešení
všech předchozích kroků, shodu hlídá AST test. Data jsou vlastní smyšlené teploty,
ne reprezentativní vzorek. Kod je text s nulami/NA, řádek jedno pozorování.
Čištění vrací cista a odmitnuta s původním textem a prioritou důvodů; radek je
pořadí záznamu od 1, nikoli fyzická CSV linka. Nuly a záporné konečné hodnoty
zůstávají, inf/NaN se odmítnou. Neznámý kód se zvlášť oddělí při left merge,
katalog se validuje many_to_one i pro nepoužité duplicity. Skupiny mají kod/nazev.

Výstupy: stanice.csv, prehled.xlsx (Stanice/Dny/Nespárovaná/Odmítnutá),
teploty.png a zprava.md. Ověřují se skutečné buňky a artists, záporná data
se nesmějí skrýt. XLSX prázdný text chápe jako prázdnou buňku; audit DataFrame
uchová přesný text. Celkový průměr je za jednotlivá spárovaná měření, nikoli
prostý průměr skupin. Zpráva vymezí cvičný zdroj a příčinné závěry.

Osm veřejných unittestů v test_dilna.py lze spustit s předanou funkcí nebo
z pracovního reseni.py; v předaném projektu testují místní predchozi.py.
Notebook 4.5 má unikátní id, čisté outputs/execution_count a dané zdroje pěti
buněk. Kontrola ověřuje i serializaci JSON a metadata jádra. Skutečné ipykernel
ověření restartuje jádro a provede všechny buňky; běžný skript zůstává
rovnocennou možností. Při měnících se snapshotech helperů je třeba restart
jádra (samotné reset proměnných nemaže cache importovaných modulů).

Krok 42 vytvoří úplný adresář z podkladu projekt, přiloží skutečné vstupy,
notebook a výstupy. Kontrola adresář přenese, odstraní PYTHONPATH Akademie,
spustí jeho CLI i veřejné testy a znovu ověří data. Jiné soubory se nemažou.
README obsahuje vlastní .venv, požadavky, spuštění a volitelné kroky Gitu;
žádný git/publish příkaz se při běhu lekce automaticky neprovádí.

Metadata download_formats=[".md",".ipynb"] povolují navíc pouze tyto formáty
z pevného seznamu v serveru. Jiné přípony se ignorují i při chybném metadatu,
POST tento výběr nezapíná. Výchozí CSV/XLSX režim dál nabízí max 6 souborů;
projektový režim až 12, každý 2 MB/celkem 4 MB. Markdown se dekóduje jako
UTF-8, notebook jako JSON s nbformat 4 a buňkami. Původní token/Host/Origin,
DOM textové názvy a ochrana před starým pollem zůstávají. Výsledkem finálního
předání je kompletní pracovní složka v editoru, nikoli distribuční ZIP.

## Odolné ukládání postupu (od v0.58)
Web/js/store.js zachovává klíč dilna-python-v1 a dosavadní strukturu done,
tasks, checks a theme. Done a tasks evidují kladné příznaky 1/true, checks
navíc zachovává 0/false; neplatné typy a dílčí záznamy se ignorují. Dictionary
mají nulový prototyp. Neznámá pole kořene zůstávají zachovaná a samotné čtení
původní uložený text nepřepisuje. Rozepsané kódy mají své původní samostatné klíče.

Každá změna nejprve načte aktuální uložený stav a potom aplikuje vlastní operaci,
takže nevychází ze starého snímku jiné karty. Událost storage načte nejnovější
obsah, nikoli případně opožděné event.newValue. Nepodařený zápis ponechá operace
v paměti; po načtení nového stavu se znovu aplikují a při úspěšném zápisu uklidí.
Úmyslné removeItem/clear se bez neuložených vlastních operací projeví jako prázdný
stav, staré značky se při další akci nevracejí. Toto není přenos mezi různými
adresami/profily ani záloha mezi počítači.

Store při změně vysílá dilna-store-change. App.js aktualizuje vzhled tlačítka
a upozornění na nedostupné ukládání, nepřekresluje při tom editor. Upozornění
storage-warning má role=status a po úspěšném zápisu se skryje. Při trvajícím
odmítnutí jsou nové změny jen v paměti současné stránky. E2e_progress.py ověřuje
dvě skutečné karty, pozdní oznámení, validní část staršího záznamu, nedostupné
úložiště, kvótu/obnovení, zrušení splnění, vymazání, checklisty, úkoly a kurzor.

RenderPreparation zobrazuje selhání čtecího API jen uvnitř přípravného panelu
a nabízí data-prep-retry. Chyba nepropadne do globálního rendereru, který by
přepsal celý seznam lekcí. Opakování mění jen tento panel. E2e_preparation.py
ověřuje HTTP 503, zachovaný seznam 40 lekcí a úspěšný nový pokus.

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

### Vlastní testy a dokončený projekt (v0.56)
Tk_run má akci `{"action":"focus","kind":"text","name":"telo"}`. Vybere
jediný viditelný cíl podle kind (výchozí entry) a volitelného name a nastaví
fokus; neexistující/nejasný cíl je TclError. Následná key může použít například
`<Control-s>`. Vlastní vazba widgetu s návratem break zastaví cestu k oknu.
Náhrada stále neimplementuje třídní vazby skutečného Text: kontrola 27 proto
ověřuje také přítomnost vlastních vazeb na něm. Skutečné chování před třídou
ověřuje tkinter_finish_real_smoke.py v reálném Tk.

Lekce 25 je konzolová. TestDilna má alespoň pět vlastních testů, žádné skip ani
expectedFailure. Kontrola sadu načte znovu pro každou z osmi dočasných změn
veřejných funkcí modelu/pracovníka; musí zachytit chybu, jinak nestačí. Běžný
unittest přehled včetně OK je na stderr; rozhoduje návratový kód a výsledek.
Testy používají dočasné soubory a řízenou náhradu přenosu. Skutečnou síť ani
vykreslení tím neprohlašovat za ověřené.

Lekce 26 je konzolový plán argumentů, ne automatická instalace/stavba.
Prikaz_sestaveni vrací seznam, interpreter ponechá jako jeden argument a
vrací absolutní vstup/výstupy. Volby onedir/console a případné --add-data
vycházejí z ověřené verze PyInstalleru 6.22.3. Kontroly neimportují ani
nespouštějí PyInstaller, v requires_packages kurzu není. Ruční sestavit.py
spustí seznam přes subprocess.run(check=True) bez shellu.

Lekce 27 je GUI. Cesty zdrojů se odvozují od __file__, výchozí cesta dialogů
od zadaného domova; nic se při výpočtu nezapisuje. Vadný/chybějící zdroj
nenahrazuje formulář. Ctrl+S/O/Enter mají vlastní vazbu i na Entry/Text a
vracejí break. Enter s Control pouze ověřuje náhled, síť spouští tlačítko.
Busy chrání také klávesové callbacky a Načíst ukázku. Data jsou vedle modulu,
ve frozen balíčku uvnitř _internal; uživatelské soubory se tam neukládají.

Lekce 28 je konzolová závěrečná zkouška jednoho skutečného místního předání.
Souhrn čte data a obálku ze zachyceného záznamu, nikoli původního konceptu.
Jiný stav než prijato nebo počet odlišný od jedné je RuntimeError, bez retry.
Nejistý stav se odmítá i tehdy, když už záchyt zprávu má. Finální okno je ve
files/aplikace.py, spolu s testy, README, SCENARE a požadavky. Sestavit.py po
úspěšné stavbě přidává do výsledku README a scénáře; souborový zápis konceptu
a potřeba kontroly po nejistém výsledku zůstávají stejné jako v 24.

Test_tkinter_finish hlídá 39 přesných kopií: ve files 25–28 osm starších
řešení (koncept 21, zpravy 17, prilohy 19, priprava 22, prenos 23, odesilani 18,
nastaveni 20, dilna 24) a cvicna_posta ze shared, ve 28 navíc aplikace ze 27,
baleni ze 26 a test_projekt z 25. Při opravě rozhraní aktualizovat návaznosti.
Kvíz 28 má deset otázek, ostatní tři. E2e kontroluje i vnořenou složku data.

PyInstaller 6.22.3 byl skutečně sestaven a spuštěn na Linuxu s Pythonem 3.14.8
a Tk 9.0, ze zdrojové cesty s mezerou a jiného cwd. Zobrazená ukázka pocházela
z přibaleného data, skutečné SMTP skončilo jednou zprávou v místním záchytu.
Automatický běh source GUI navíc ověřuje klávesy v Text, chyby souborů, odezvu,
nezměněný snímek i nejistý výsledek. Volbu cest řídí test, vzhled nativního
dialogu neověřuje. Windows/macOS a jejich binární balení vyžadují vlastní
zkoušku. Stav hotového obsahu 28/28 je dál draft pro připomínky studentů.


## Pygame 2, první modul (od v0.68)

Course pygame-2 má první modul 1–5, draft a plán 30 lekcí (level 4, úvod 3).
Každá lekce je console s preview_images=true: v prvním modulu jde o deterministické
modely a obrázkové náhledy, nikoli smyčku nativního okna. Example.py a dvě další
konzolové varianty kreslí skutečné Surface do nahled.png 640×360. Režim PNG se
sdílí s grafy; UI používá obecné názvy obrázek, nikoli pouze graf. Server a limity
se nemění, nové závislosti nejsou potřeba (pouze stávající pygame-ce).

Každá lekce má čtyři další tasks s vlastním zadáním, šablonou, kontrolou a řešením.
Files obsahuje zaklad.py, nahled.py a od třetí lekce pohyb.py s přesnou třídou
PohyblivaLod z řešení 2/1; shodu hlídá AST test. Soubory se kopírují vedle reseni.py,
check.py přidává pracovní adresář do sys.path. Import modelu nevytváří okno.
Volitelný pygame2_intro.py používá skutečné Sprite/Surface/Vector2/Group a vlastní
vstupní objekty; funkční správnost ověřuje na více případech, ne konkrétním AST.
Zahrnuje desetinný pohyb, dt=0, záporné směry, prázdné/sdílené skupiny, identitu,
pixely a nezměněné zdroje, dotyk hran/kruhů, kill všech členství, opakované události,
pauzu, jednorázový časovač a tvorbu nového světa bez poškození staré skupiny.

Navazující projekty zůstávají souvislé celky; případné budoucí příklady nativních
her musí mít kind=gui a odpovídající headless kontrolu. Neprovádět GUI smyčku při
importu přes c.load. První blok se ověřuje bez SDL okna, nativní editory/OS se tím
netestují. Global counts: 215 hlavních + 288 dalších řešení = 503.
