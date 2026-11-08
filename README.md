# Dílna Pythonu

Česká výuková aplikace pro Python. Každá učebnice je samostatný podkurz, studovat lze v libovolném pořadí, nic se nezamyká. Kód píšete ve VS Code, VSCodium, PyCharm nebo přímo v aplikaci, aplikace ho spouští a kontroluje.

**Stav (v0.57):** úvodní koncept přípravy (15 průvodců), Základy (40 lekcí), samostatné OOP (20 ze 20), Soubory a web (22), Pygame 1 (18), Turtle/OOP (40 ze 40) a Okenní aplikace, API a e-maily (28 z 28). Dokončené kurzy čekají na připomínky studentů. Další podkurzy jsou plánované, viz `PLAN.md` a `STATUS.md`.

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

## Okenní aplikace, API a e-maily — všech 28 lekcí připravených
Kurz začíná oknem Tkinteru, popisky, tlačítky a formulářem se jménem.
Navazuje rámečky Frame a změnou rozměrů, ovládáním přes Enter, propojenými
proměnnými a přepínači. První projekt převádí kilometry a metry: výpočet funguje
samostatně, formulář přijímá desetinnou čárku i tečku a dovolí opravit chybný vstup.
Třetí blok přidává Listbox s bezpečným výběrem, víceřádkový Text s posuvníkem
a souborové dialogy pro JSON v UTF-8. Úkolníček umí přidat, dokončit a odstranit
konkrétní úkol i mezi stejnými názvy. Uložený model lze znovu načíst; zrušení
dialogu nebo neplatná data zachovají současné úkoly, výběr i podrobnosti.
Čtvrtý blok učí HTTP GET, parametry, JSON, timeout a ověření dat. Místní cvičné
API nabízí předvídatelné chyby bez závislosti na internetu. Pracovní vlákno,
fronta a after umožní načítat bez zamrzání okna; widgety zůstávají v hlavním vlákně.
Převodník měn ukazuje zdroj a datum smyšleného kurzu a dovolí zvolit API nebo
JSON soubor. Změna volby vyžádá nový kurz, neúspěch neponechá starý výsledek.
Pátý blok učí EmailMessage, český náhled, SMTP obálku, přílohy a konfiguraci
z prostředí. Zprávy míří výhradně do místního záchytu bez osobní schránky.
Ukázka rozlišuje přijetí, odmítnutí i ztrátu potvrzení po převzetí; po timeoutu
neopakuje odesílání automaticky. Zrušení či chyba přílohy zachová předchozí zprávu.
Šestý blok propojuje Korespondenční dílnu: samostatný koncept, formulář,
ověření konkrétních polí a předání hotového snímku do místního SMTP.
Během přenosu lze dál psát bez změny předávané zprávy. Koncept se ukládá
do JSON i neúplný; načtení při chybě zachová rozepsaná pole, přílohu i náhled.
Zápis přes dočasný soubor chrání před poškozením původního cíle při chybě
před nahrazením. Příloha se ukládá jako cesta, její obsah se do konceptu nekopíruje.
Závěrečný blok přidává vlastní unittest testy s řízenými chybami, přípravu
argumentů pro volitelné balení, cesty ke zdrojům nezávislé na pracovní složce
a Ctrl+S/Ctrl+O/Ctrl+Enter. Hotový projekt obsahuje README, praktické scénáře,
testy i závěrečnou zkoušku jednoho skutečného místního předání. PyInstaller
6.22.3 byl ověřen s Pythonem 3.14.8 na Linuxu včetně spuštění s přibaleným Tk
a daty; Windows/macOS vyžadují vlastní sestavení a ověření.
Každá lekce vysvětluje nové příkazy před použitím a obsahuje ukázku, úkol,
automatickou kontrolu chování a kvíz. Příprava kurzu pomůže ověřit Tkinter
ve zvoleném editoru; prvních dvanáct lekcí nepotřebuje další pip balíčky,
od lekce 13 je potřeba requests a od SMTP lekce 18 aiosmtpd (ověřeno 1.4.6 na
Pythonu 3.14.8). Instalaci zajistí příprava podkurzu. Pomocné soubory z files
jsou součástí lekcí; starý modul smtpd v Pythonu 3.14 není.
Okno se otevře na počítači, kde běží Python, vedle prohlížeče s učebnicí.

Celá osnova 28 lekcí je v rozbalitelném panelu kurzu a v
[plánu kurzu](courses/tkinter-api/plan.md). Obsah je dokončený a čeká na
vyzkoušení a připomínky studentů; stav zůstává draft. Náročnost celku je 3/4,
první okna jsou vhodná po Základech Pythonu. Balení je volitelné a k běžnému
studiu ani automatickým kontrolám není PyInstaller potřeba.

## Samostatný OOP kurz — všech dvacet lekcí připravených
V katalogu je vedle Základů samostatná karta **Objektově orientované programování v praxi**.
Kurz má osnovu 20 lekcí s náročností **3/4**, bez závislosti na Turtle a hrách.
Nosný praktický projekt „Chytré expediční centrum“ propojí objednávky, zásoby a způsoby doručení.
První blok učí objekt zásilky, konstruktor a self, metody položky a objednávku
s vlastním seznamem položek. Druhý přidává zapouzdření, výjimky před změnou stavu,
property pouze pro čtení a sklad s rezervací celého požadavku, nebo žádné jeho části.
Třetí učí dědění na balíku, polymorfismus osobního odběru a kurýra, rozšíření
přes super() a expedici, která bezpečně mění dopravu. Nová doprava může spolupracovat
přes stejnou metodu cena bez úpravy Expedice.
Čtvrtý blok přidává __str__/__repr__, identitu a hodnotovou rovnost adres,
dataclass štítku s vlastními poznámkami a vlastní unittest testy dopravy.
Kontrola testů ověří i jejich schopnost odhalit úmyslně vložené chyby.
Závěrečné lekce 17–20 propojí nákup, rezervace podle čísla objednávky, bezpečné
storno, dopravu a konzolový ovladač. Přijatý nákup se uzavře a opakované storno
nevrací kusy podruhé. Odmítnutá doprava nezablokuje zboží.
Každá lekce má komentovanou ukázku, úkol s automatickou kontrolou a tři kvízové otázky.
Příprava prostředí je před lekcemi, stačí standardní Python.

Panel zobrazuje dostupné lekce i zbývající plán v [courses/oop/plan.md](courses/oop/plan.md).
Obsah všech 20 lekcí je dokončený; status draft zůstává pro zpětnou vazbu a revizi.
Hotovou aplikaci spusťte v ukázce lekce 20 (na běh máte deset minut): například `nova A 2 1 1200`,
`doprava A kolo`, `prehled A`, `storno A` a `konec`. Běží v paměti s cvičnými
údaji, po novém spuštění začíná znovu. V pracovní složce jsou také README
a čtyři testy projektu: `python -m unittest -v test_centrum`.

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

## Pomoc s řešením ve všech kurzech
Pod úkolem je rozbalovací ovladač **Zobrazit možné řešení**. Ukáže jednu ověřenou
variantu k právě vybranému zadání s připomenutím, že správných postupů může být více.
Pomoc je dostupná pro všech 168 hlavních zadání napříč šesti hotovými kurzy
i 136 dalších úkolů v Základech, celkem 304 řešení včetně projektů a závěrečných
programů. Kód má zvýrazněnou syntaxi a dá se běžně označit a zkopírovat.
Průvodce přípravou bez programovacího úkolu tento panel nemá.

Při přepnutí Úkolu 1–5 se panel zavře a nabídne řešení nového zadání. Rozepsaný kód
zůstává v editoru a postup se ukládá stejným způsobem jako dosud. Řešení se načítá
teprve po rozbalení; po obnovení stránky je opět skryté.

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
