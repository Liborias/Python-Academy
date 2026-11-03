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
| `check.py` | ano | kontrola přes `dilna_check` (viz lib/dilna_check); `kind: gui` se kontroluje jen přes AST/funkce |
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

API lesson vrací pole tasks s id, title, md a exercise; kontroly a řešení nezveřejňuje.
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
