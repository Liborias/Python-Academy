# Dílna Pythonu

Česká výuková aplikace pro Python. Každá učebnice je samostatný podkurz, studovat lze v libovolném pořadí, nic se nezamyká. Kód píšete ve VS Code, VSCodium, PyCharm nebo přímo v aplikaci, aplikace ho spouští a kontroluje.

**Stav (v0.78):** úvodní koncept přípravy (15 průvodců), Základy (40 lekcí), samostatné OOP (20 ze 20), Soubory a web (22), Pygame 1 (18), Pygame 2 včetně tří her, vlastních testů a předání (30 ze 30), Turtle/OOP (40 ze 40), Okenní aplikace, API a e-maily (28 z 28), všech osm modulů Datové analýzy (42 ze 42) a Databáze včetně místních účtů a přenosu poznámek (25 ze 32). Dokončené kurzy čekají na připomínky studentů. Další kapitoly Databází jsou plánované, viz `PLAN.md` a `STATUS.md`.

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

## Databáze a projekty — SQLite a okenní evidence, prvních 25 lekcí

První modul 1–5 učí spojení, paměť/soubor, tabulky a pravidla hodnot,
parametrizované změny, čtení a transakce. Následují NULL/COALESCE,
doslovné hledání proti LIKE a typové afinity, souhrny/GROUP BY/HAVING,
cizí klíče a INNER/LEFT JOIN. Samostatné lekce 1–9 mají tři ukázky a pět
úkolů s vlastním zadáním, šablonou, kontrolou a možným řešením.
Projekt 10 tvoří jeden souvislý celek s řešením. V každé lekci jsou tři kvízové
otázky; první dva bloky mají **28 ukázek a 46 úkolů**, z toho 15/25 v prvním bloku.
Návazná evidence kroužků 11–15 přidává pět kroků s řešeními, první tři bloky mají **33 ukázek a 51 úkolů**.
BMI tracker 16–20 přidává sedm ukázek a pět úkolů, první čtyři bloky mají **40 ukázek a 56 úkolů**.
Místní účty/soubory 21–25 přidávají devět ukázek/pět úkolů, celkem **49 ukázek a 61 úkolů**.
Úvod 2/4, celek 4/4; panel popisuje plán 32 lekcí, dostupných pětadvacet.

Databázové části používají standardní sqlite3, bez pip balíčků, serveru a internetu.
Okna 12–14 a 19 navíc potřebují Tkinter a grafickou plochu; `python -m tkinter` ji ověří.
Python 3.12+ s výslovným autocommit; ověřeno Python 3.14.8/SQLite 3.53.1.
Příprava má postup pro VS Code/VSCodium/PyCharm ve stejné .venv.
`closing` zavírá spojení, `with con` řeší commit/rollback. Vazby se zapínají
na každém spojení před přechodem na autocommit=False. Řazení textu i chování
LIKE jsou vysvětlené bez předpokladu úplné české kolace.

**Klubovní evidence** propojí kategorie, pomůcky a historii výpůjček.
Půjčení i vrácení je transakce, stejné id výpůjčky vrátí kus jen jednou.
Nový projekt používá klub.sqlite3; starý sklad z 1–5 nemigruje a při nesprávném
schématu nechá původní data zachovaná. Konzole importuje právě vaši Evidence.
Ve stálé pracovní složce lekce 10 po dokončení modelu:

```powershell
python reseni.py
python spust_klub.py --help
python spust_klub.py prehled
```

reseni.py provede paměťovou ukázku, spust_klub.py pracuje se skutečným souborem
vedle skriptu. Podrobné příkazy pro kategorie, pomůcky, půjčení a vrácení
jsou v lekci a NAVOD.md. Použijte skutečná id z výstupu, --db CESTA před názvem
příkazu vybere jiný soubor. Běžné spuštění v prohlížeči je dočasné.
**Evidence kroužků 11–15** odděluje model od Tkinter widgetů, přidává formulář,
úpravy a mazání podle skutečných id, přihlášky s kapacitou a šest vlastních testů.
Vstupy se při chybě neztrácejí; kroužek s přihláškami nelze smazat, kapacitu
nelze snížit pod obsazenost. Každý krok má možné řešení, bez nesouvisejících variant.
Pro okna vyberte Python s Tk (Windows Tcl/Tk, Linux odpovídající python3-tk,
macOS oficiální Python); Tkinter se neinstaluje přes pip. Ověřeno Tk 9.0.
Okno běží na počítači s Pythonem, nevykresluje se uvnitř webové stránky.

V uložené složce lekcí 12–14 `python reseni.py` otevře paměťovou ukázku,
`python spust_krouzky.py` vlastní prázdnou evidenci se souborem krouzky.sqlite3
vedle skriptu. `--help` popíše volby bez vytvoření okna či souboru, `--db CESTA`
vybere jinou databázi; rodič musí existovat. V 15 reseni.py spouští izolované
testy, spouštěč používá dokončené GUI z 14. Testy nezasahují do vlastní evidence.
**BMI tracker 16–20** ukládá původní datum/kg/cm/poznámku, počítá BMI bez
předčasného zaokrouhlení a umožňuje přehled i souhrn období. BMI je orientační
ukazatel pro dospělé s vysvětlenými omezeními, ne zdravotní doporučení.
Výpočet má tři přepínatelné ukázky; všech pět kroků projektu
má vždy vlastní úkol a možné řešení. Okno přijímá čárku/tečku a zachová chybný
vstup k opravě. Ve stálé složce `python spust_bmi.py` otevře vlastní bmi.sqlite3,
--db CESTA před příkazem může navázat na databázi předchozího kroku.
V závěru `python spust_bmi.py export mereni.csv` přenese tabulku,
`python spust_bmi.py zaloha kopie.sqlite3` vytvoří celou DB přes backup API.
CSV je UTF-8 se středníkem, čísla mají tečku; cíl se nahradí až po úspěchu,
nesmí jím být zdrojová DB. `python overeni.py` spustí tři izolované testy.
Help/export/záloha/testy v 20 nepotřebují grafické importy. Navazující blok 21–25 s místními účty a soubory je hotový.

**Místní účty 21–25** učí scrypt/sůl/otisk, Unicode sjednocení jména a UNIQUE,
sezení a poznámky podle id vlastníka. Heslo se neukládá, neosekává a při skutečné
registraci/přihlášení se čte getpass. Scrypt profil N=131072/r=8/p=1 používá
přibližně 128 MiB pracovní paměti; bez nových pip knihoven. Samostatná témata
hesel a kodeku mají více ukázek, každý krok možné řešení.

V uložené složce dokončené 23/25:
```
python spust_ucty.py --help
python spust_ucty.py registrace Zofie
python spust_ucty.py prihlaseni Zofie
```
Vlastní ucty.sqlite3 je vedle spouštěče, --db CESTA před příkazem naváže na
předchozí složku. Menu vypíše/přidá poznámku/odhlásí. Nový běh je odhlášený,
chybný pokus zruší starou identitu. Nemění se přihlášení webové Akademie.
V 25 export/import po ověření hesla přenese vlastní poznámky přes zlib/Base64;
nejde o šifrování či zálohu účtů, import přidává a opakování vytvoří kopie.

Volitelná řeč 24 je výchozím náhledem bez zvuku. `python precti.py "Ukázka." --mluv`
zvolí systémový offline hlas, pokud existuje: Windows System.Speech, macOS say,
Linux espeak-ng/espeak s cs. Bez pip/API. Neposílají se hesla, text jde přes stdin
bez shellu. Chybějící hlas ostatní lekce neblokuje. Další blok je 26–30.

## Pygame 2 — herní objekty a tři vlastní hry

Nový kurz propojuje OOP s herními objekty. První modul vysvětluje Sprite a jeho
image/rect, přesný pohyb přes Vector2 a čas, Group/update/draw, kolize a stav hry
s pauzou, časovačem a restartem. Každá lekce má tři přepínatelné ukázky,
pět úkolů s vlastním zadáním/kontrolou/možným řešením a tři kvízové otázky.
Navazující projekt **Meteority, lekce 6–10**, postupně přidává pohyb lodě,
proud meteoritů, životy a ochranu po zásahu, skóre a štít, pauzu a restart.
Každý krok má jednu ukázku, vlastní úkol s možným řešením a tři kvízové otázky.

Projekt **Chyť robota, lekce 11–15**, vysvětluje souřadnice kliknutí, kruhový
výběr horního cíle, dědění a různé pohyby přes společné rozhraní, skóre,
přesnost, životy, časový limit a rychlejší vlny. Závěr propojí nabídku,
pauzu, výsledek a nový lov. Opět jedna ukázka, úkol s řešením a tři kvízové
otázky v každém kroku.

**Součásti větší hry, lekce 16–20**, mají v každé lekci tři ukázky a pět úkolů
s řešeními. Procvičíte cache obrázků/fontů, volitelný zvuk, animaci podle času,
masky, převody kamery a skládání režimů.

Projekt **Hon na dronech, lekce 21–25**, propojí hráče a svět, pronásledování
s rozestupy, postupně vznikající vlny, životy a přístav s omezeným štítem.
Závěr přidá nabídku, pauzu, výsledek a nový let přes zásobník režimů.
Každý krok má jednu ukázku, úkol s možným řešením a tři kvízové otázky.
**Ověření a předání, lekce 26–30**, přidává opakovatelné scénáře, vlastní unittest,
JSON výsledky, cesty a volitelné balení. Témata 26–29 mají tři ukázky a pět úkolů
s řešeními. Závěrečná Kurýrská směna propojí vlastní rychlost hráče s pamětí
pěti nejlepších výsledků; tvoří jeden návazný projekt s řešením.
Celkem **58 ukázek a 86 úkolů**.
Úvod má obtížnost 3/4, celek 4/4.

`python tools/setup_env.py --courses pygame-2` připraví pygame-ce do stejné
projektové .venv; v kódu používáme import pygame. Ověřeno na Pythonu 3.14.8
s pygame-ce 2.5.8. Příprava před kurzem má postup pro VS Code, VSCodium a PyCharm.
Zvolte stejný interpreter pro editor i terminál.

První modul kreslí skutečné Surface do PNG, které aplikace zobrazí a dovolí
stáhnout. V editoru se obrázek uloží do pracovní složky. Jde o poslední stav po
provedených krocích; tento úvod nepotřebuje grafickou plochu ani zvuk.

Meteority otevírají živé herní okno na počítači, kde běží Python. Při vzdáleném
serveru se okno nepřenáší do prohlížeče; pro hraní spusťte projekt místně.
Šipky pohybují lodí, od lekce 10 je **P** pauza, **R** nový let a **Esc** konec.
Okno nejprve aktivujte kliknutím. Při běžném zavření se uloží poslední snímek
`meteority.png`, který aplikace nabídne ke stažení. Tlačítko Stop v aplikaci
ukončí proces a uložení snímku nezaručuje. Zvuk ani další balíčky nejsou potřeba.

Chyť robota také otevírá místní okno; cíle chytáte levým tlačítkem myši.
V lekci 15 **Mezerník** spustí lov nebo vrátí výsledek do nabídky, **P** přepíná
pauzu, **R** začne nový lov a **Esc** ukončí program. Běžné zavření uloží
`roboti.png`. Herní čas se v pauze neodečítá a další vlna neobnovuje životy
ani skóre. Vlastní grafika všech her vzniká kódem bez cizích obrázků a síťových
dat. Panel kurzu popisuje všech 30 dostupných lekcí; obsah čeká na připomínky studentů.

Laboratoř 16–20 ukládá obrázkové pokusy do `soucasti.png`; zobrazují skutečné
pixely a zaznamenané fáze, PNG samo není animované okno. Funguje bez displeje
i bez zvukového zařízení. Podklady vytvářejí vlastní BMP/WAV přes pygame
a standardní knihovnu. V lekci 16 lze místně vyzkoušet krátký tón příkazem
`python prehraj_ton.py --play` v uložené pracovní složce; zkouška má limit
pěti sekund. Bez přepínače se nic nepřehraje. Po uložení Úkolu 5 v lekci 20
je navíc dostupná živá dílna `python ziva_dilna.py`: myš/P/M/Esc, místní
grafická plocha, bez zvuku, poslední snímek `rezimy-zive.png`.

Hon na dronech používá stejné místní prostředí a okno 720×540. Šipky nebo
WASD pohybují kurýrem; v lekci 25 **Mezerník** spustí misi nebo vrátí výsledek
do nabídky, **P** přepíná pauzu, **R** začne nový let a **Esc** ukončí program.
Cílem je nasbírat alespoň šest zelených datových bodů a přežít tři desetisekundové
vlny. Přístav chrání nejvýše 2,5 sekundy, energie se obnovuje pouze mimo něj.
Čekání v přístavu samo nestačí k výhře. V tréninku 23 lze klávesou **N**
spustit další vlnu; v hotové misi se vlny střídají automaticky. Běžné zavření
uloží `droni.png`; Stop uložení nezaručuje. Další balíčky ani zvuk nejsou potřeba.

V závěru kurzu scénáře a vlastní testy pracují se skutečným modelem bez okna.
Testy musí odlišit správnou hru od úmyslných vad. JSON úlohy vysvětlují typy,
verzi formátu, chybný soubor a nahrazení hotovým zápisem bez zničení starších dat.
Kurýrská směna 30 používá stejné ovládání jako Hon na dronech a ukáže profil
kurýra, stav zápisu a v nabídce nejlepší výsledek. Jedno dokončené kolo se zapíše
právě jednou; chyba přístupu se zobrazí bez ztráty původní tabulky.

Pro paměť mezi spuštěními uložte pracovní složku a spusťte její reseni.py
v editoru. Výsledky jsou v data/vysledky.json vedle programu. Běžné spuštění
v prohlížeči používá dočasnou kopii; jeho soubory nejsou trvalé úložiště.
Over_projekt.py provede přiložené testy modelu, NAVOD.md popisuje předání.
PyInstaller 6.22.3 je volitelný; sestavit.py se spouští vědomě po testech.
Sestavení onedir a skutečná SDL smyčka byly ověřeny na Linuxu s Pythonem 3.14.8.
Předávejte celou distribuční složku; Windows/macOS potřebují vlastní sestavení
a zkoušku. Pro běžný průchod nejsou další balíčky ani zvuk povinné.

## Datová analýza — všech 42 lekcí

Kurz začíná Series a popisky, výpočty podle indexu, výběrem loc/iloc,
prvním DataFrame a načtením místních CSV. Samostatné lekce 1–19 a 21–34 mají tři přepínatelné
ukázky a pět úkolů s vlastním zadáním, kontrolou a možným řešením. Projekty kavárny 20 a 35 i závěrečné kroky 36–42 tvoří souvislé celky,
každý s jednou ukázkou a možným řešením. Kavárenské projekty mají po pěti
kvízových otázkách, kroky Analytické dílny po třech.
Celkem je připraveno 108 ukázek a 174 úkolů. Data jsou vlastní a smyšlená,
u CSV procvičíte desetinnou čárku, hlavičku, UTF-8 a textové kódy s nulami.
Výklad vysvětluje nové operace, význam výsledku i běžné omyly.

Po aktualizaci připravte závislosti příkazem
`python tools/setup_env.py --courses pandas` a znovu spusťte aplikaci.
Pomocník použije projektovou .venv; vyberte ji také v editoru.
Instaluje pandas řady 3, matplotlib, openpyxl a ipykernel.
Prvních pět modulů používá jen pandas, šestý přidává Matplotlib, sedmý také
openpyxl pro Excel. Všech 42 lekcí běží bez internetu i grafické plochy.
Grafy se ukládají do PNG; v souborových lekcích lze stáhnout i CSV/XLSX.
Ověřeno na Pythonu 3.14.8 s pandas 3.1.1, NumPy 2.5.4, Matplotlib 3.11.2 a openpyxl 3.1.5.
Soubory .py fungují přímo v aplikaci nebo terminálu; značky # %% umožní
volitelné buňky v podporovaném editoru. Notebook není povinný.
Příprava nabízí VS Code, VSCodium i PyCharm.

Celá [osnova 42 lekcí](courses/pandas/plan.md) je dostupná také v panelu kurzu.
Úvod má náročnost 2/4 po Základech Pythonu, celek 3/4. Druhý modul přidává
Series proti DataFrame, výběr na obou osách, masky s &/| a isin, zarovnání
podle indexu, stabilní řazení, více klíčů, NaN a reset_index. Změny přes loc
a nové sloupce v samostatné kopii vysvětlují Copy-on-Write v pandas 3.
Třetí modul 11–15 učí chybějící údaje, doplňování a vynechání podle pravidla,
číselné převody a Int64, datumy s explicitním formátem, přestupné roky a NaT,
duplicity podle celého řádku i klíče a čištění textů. Neplatné texty odlišuje
od původně chybějících údajů; zdrojová data zůstávají zachovaná.
Čtvrtý modul 16–20 učí osu výpočtu, count/size, min_count, groupby včetně
chybějících klíčů, více agregací a pojmenované výsledky. Průměr porovnává
s mediánem a ukazuje, proč prostý průměr skupinových průměrů nemusí být celkový.
Projekt kavárny používá vlastní CSV, denní a produktový přehled a samostatné
ověření počtů i tržeb. Výsledky kontrolují také nezávislé součty v Python cyklu.
Pátý modul 21–25 učí reindex a concat podle os, merge podle jednoho i více
klíčů, validate, indikátor původu a překrývající se názvy. Časový index rozlišuje
přesný úsek od celého dne; resample denní a měsíční souhrny, chybějící
období i skutečnou nulu. Šestý modul 26–30 přidává Figure/Axes a popisky,
čáry a sloupce, scatter a omezení příčinných závěrů, histogramy/četnosti/hustotu
a export PNG. Každý graf lze po běhu zobrazit v aplikaci a stáhnout.
Náhledy patří aktuálnímu běhu; po reloadu je znovu vytvoříte spuštěním kódu.
V editoru PNG vznikne v pracovní složce procesu. Sedmý modul 31–35 učí
čtení listů, textové kódy s nulami, CSV v UTF-8 a ověření skutečného exportu,
XLSX s více listy a opakovatelný postup od čištění po souhrn. Měsíční projekt
kavárny propojí výběr kalendářního měsíce, CSV, tři excelové listy a graf.
V aplikaci lze stáhnout CSV/XLSX včetně přiložených zdrojů; po reloadu
odkazy znovu vytvoří běh zachovaného kódu. Osmý modul 36–42 propojí vlastní
cvičná měření teplot: datový slovník, audit čištění, nespárované kódy, souhrny,
graf a zprávu s omezením závěrů. Přidá skutečné testy a volitelný notebook,
který jde spustit od nového jádra. Poslední krok vytvoří samostatný projekt
s README, požadavky, zdroji, skriptem a testy, ověřený také v jiné složce.
Dokumenty MD a notebook IPYNB lze stáhnout přímo z těchto projektových lekcí.

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
V běžných lekcích Základů (01–31 a 37–39) a lekcích 1–19 a 21–34 Datové analýzy i lekcích 1–5, 16–20 a 26–29 Pygame 2 a v samostatných lekcích 1–9 Databází
přepínají tlačítka **Úkol 1 až Úkol 5**
mezi původním úkolem a čtyřmi novými. Každý má vlastní zadání, rozepsaný kód,
kontrolu a pracovní soubor pro externí editor. Doplňkových úkolů je celkem 360.
Úkol 1 zachovává původní uložený kód i návaznost na splnění lekce. Nové úkoly mají
vlastní značky úspěšného procvičení. „Začít znovu“ obnoví jen právě vybraný úkol.
Navazující mini-projekty a závěrečné testy tvoří vlastní celky.

## Práce s kódem v aplikaci

Editory ukázek a úkolů mají vlevo čísla řádků, která se aktualizují při psaní
a posouvají spolu s kódem. Při kopírování se přenese pouze kód.

**Ctrl+/ nebo Ctrl+Shift+7** přidá nebo odebere komentář `#` na aktuálním řádku.
Pro více řádků nejprve označte blok a použijte stejnou zkratku. Pokud jsou všechny
neprázdné řádky označeného bloku zakomentované, zkratka je odkomentuje;
jinak zakomentuje celý blok. Prázdné řádky uvnitř bloku a odsazení zůstanou zachované.
Na Macu použijte **Cmd** místo Ctrl. Druhá zkratka je praktická na české klávesnici.

Přehled zkratek otevře tlačítko **?** v pravém horním rohu pracovního editoru.
Nápověda vysvětluje také odsazování, našeptávání, spuštění a vrácení změn.

## Pomoc s řešením ve všech kurzech
Pod úkolem je rozbalovací ovladač **Zobrazit možné řešení**. Ukáže jednu ověřenou
variantu k právě vybranému zadání s připomenutím, že správných postupů může být více.
Pomoc je dostupná pro všech 265 hlavních zadání napříč devíti praktickými kurzy
i 360 dalších úkolů v Základech, Datové analýze, Pygame 2 a Databázích, celkem 625 řešení včetně projektů a závěrečných
programů. Kód má zvýrazněnou syntaxi a dá se běžně označit a zkopírovat.
Průvodce přípravou bez programovacího úkolu tento panel nemá.

Při přepnutí Úkolu 1–5 se panel zavře a nabídne řešení nového zadání. Rozepsaný kód
zůstává v editoru a postup se ukládá stejným způsobem jako dosud. Řešení se načítá
teprve po rozbalení; po obnovení stránky je opět skryté.

## Ukládání postupu a více karet

Postup a nastavení se ukládají v konkrétním profilu prohlížeče pro stejnou adresu
aplikace. Před každým zápisem se načte poslední uložený stav, aby starší otevřená
karta nepřepsala označení z jiné karty. Změna vzhledu se převezme také bez
přepsání textu nebo změny kurzoru v editoru. Platné položky staršího záznamu
zůstanou použitelné i při chybě v jiné části dat.

Když prohlížeč odmítne ukládání, zobrazí se upozornění. Změny postupu se drží
v paměti otevřené stránky a další změna postupu zkusí zápis znovu; po úspěchu upozornění
zmizí. Před zavřením si při přetrvávající chybě uložte rozepsaný kód do souboru.
Git přenáší projekt, postup mezi počítači tímto způsobem nepřenáší.
Po aktualizaci obnovte otevřené karty, aby používaly opravené ukládání.

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
Ukládání mezi kartami, poškozený záznam a dočasné odmítnutí zápisu ověřuje
`python tests/e2e_progress.py`. Přípravu včetně opakování po chybě ověřuje
`python tests/e2e_preparation.py`.

## Bezpečnost

Aplikace spouští kód, který napíšete. Server proto poslouchá jen na `127.0.0.1`, vyžaduje náhodný token a kontroluje hlavičky `Host` a `Origin`. Adresu s tokenem nesdílejte.
