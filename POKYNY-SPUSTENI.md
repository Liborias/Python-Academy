# Dílna Pythonu: ověření Pythonu, instalace a spuštění

Všechny příkazy se zadávají v terminálu **ve složce projektu** (`Python-Academy` po git clone).
Na Windows se píše `python` (případně `py`), na macOS a Linuxu `python3`. Dále je psáno `python`.

## 1. Ověření verze Pythonu

```
python --version
```
Potřebujete **Python 3.12 nebo novější** (ideálně 3.14). Pokud příkaz neexistuje nebo vypíše nižší verzi, nainstalujte nový Python z https://www.python.org/downloads/ (Windows: při instalaci zaškrtněte „Add python.exe to PATH“) a terminál otevřete znovu.

Alternativy při potížích:
- Windows: `py --version` nebo `py -3 --version`
- macOS / Linux: `python3 --version`

Podrobnosti: `docs/instalace.md`.

## 2. Instalace potřebných komponent

```
python tools/setup_env.py --courses zaklady
```
Vytvoří nebo použije složku `.venv` (virtuální prostředí). Základy další balíčky
nepotřebují. První vytvoření prostředí a instalace závislostí mohou potřebovat internet.

Jen vybrané podkurzy:
```
python tools/setup_env.py --courses soubory-web,pygame-1
```
Co by se instalovalo, bez instalace:
```
python tools/setup_env.py --dry-run
```
Základní podkurz **Základy** žádné balíčky nepotřebuje.

Pro Databáze a projekty (prvních 25 z 32 lekcí):
```
python tools/setup_env.py --courses databaze
python -c "import sys, sqlite3; print(sys.executable); print(sqlite3.sqlite_version)"
```
První příkaz připraví projektovou .venv bez dalších povinných balíčků,
druhý ověří vybraný interpreter a SQLite. Ve VS Code/VSCodium/PyCharm
zvolte stejný Python. Vyžadujeme Python 3.12+, ověřeno 3.14.8/SQLite 3.53.1.
Server, účet ani síť nejsou potřeba. Pro okna 12–14 a 19 potřebujete Tk a grafickou plochu. V lekcích jsou
vysvětlené SQL příkazy, parametry, vlastnictví spojení a commit/rollback.
Ukázky používají :memory: či TemporaryDirectory. Pro vlastní trvalou evidenci
uložte pracovní složku a spusťte reseni.py v editoru s vlastní cestou k souboru;
běžný webový běh je dočasný. Samostatné lekce 1–9 mají tři ukázky,
pět úkolů s možnými řešeními a NAVOD.md; projekt 10 je jeden celek.
Po uložení projektu spustí python reseni.py paměťovou ukázku,
python spust_klub.py --help popíše skutečnou konzoli. Ta používá nový
klub.sqlite3 vedle skriptu, --db CESTA před příkazem zvolí jiný soubor.
Kategorie/pomucka/pujcit/vratit/prehled/vypujcky jsou vysvětlené v lekci 10.
Starý sklad z 1–5 se nemigruje, vazby se zapínají před transakcí. Volitelné QR/řeč/PostgreSQL
patří až k dalším plánovaným tématům a pro tento blok se neinstalují.

Evidence kroužků 11–15 je jeden projekt s možnými řešeními. Pro okna:
```
python -m tkinter
```
Příkaz otevře zkušební okno, zavřete ho křížkem. Windows: Python s Tcl/Tk;
Linux: python3-tk pro správný Python; macOS: oficiální Python s Tk.
Tkinter se neinstaluje přes pip. Vyberte stejnou .venv v editoru i terminálu.
V uložené složce lekcí 12–14 po dokončení reseni.py:
```
python spust_krouzky.py --help
python spust_krouzky.py
```
Help popíše volby, druhý příkaz otevře vlastní prázdnou evidenci s trvalým
krouzky.sqlite3 vedle spouštěče. --db CESTA zvolí jiný soubor, rodič už musí
existovat. Běžný reseni.py je paměťová ukázka. V lekci 15 reseni.py spouští
šest vašich izolovaných testů, spust_krouzky.py otevře hotové GUI z 14.
Okno se nezobrazuje uvnitř webové stránky, běží na počítači se serverem Pythonu.

BMI tracker 16–20 přidává výpočet, datum/SQLite, období/souhrny a vlastní okno.
Každý krok má řešení, výpočetní lekce tři ukázky. Bez nových pip balíčků.
V uloženém dokončeném projektu 19 a 20:
```
python spust_bmi.py --help
python spust_bmi.py
```
Help nic nevytváří, okno otevře vlastní prázdný bmi.sqlite3 vedle spouštěče.
Pro stejná měření mezi složkami použijte absolutní --db CESTA před příkazem;
schéma 17–20 je stejné. V 20 navíc:
```
python spust_bmi.py export mereni.csv --od 2026-04-01 --do 2026-04-30
python spust_bmi.py zaloha kopie.sqlite3
python overeni.py
```
CSV je UTF-8 se středníkem a desetinnou tečkou, záloha celá DB přes backup API.
Rodič cíle musí existovat, cíl nesmí přepsat zdrojovou DB. Existující cíl se
nahradí jen při úspěchu. Overeni.py má tři vlastní izolované testy, nečte vaše
data. Export/záloha/help/testy nepotřebují Tkinter ani grafickou plochu.
BMI je orientační ukazatel s mezemi interpretace popsanými v lekci 16.

Místní účty 21–25 používají stejnou .venv a standardní knihovnu. Profil scrypt
n=131072/r=8/p=1 potřebuje přibližně 128 MiB; podpora závisí na Pythonu.
Po dokončení uložené 23 nebo 25:
```
python spust_ucty.py --help
python spust_ucty.py registrace Zofie
python spust_ucty.py prihlaseni Zofie
```
Heslo zadáte až přes getpass, ne do příkazu či reseni.py. Registrace dvakrát,
přihlášení jednou. Menu 1 výpis, 2 nová poznámka, 3 odhlásit. Vlastní
ucty.sqlite3 je vedle spouštěče, --db CESTA před příkazem naváže na jinou
složku se stejným schématem 22/23/25. Webová ukázka je dočasná.
V 25 přibude export/import Zofie soubor.txt, také s ověřením hesla. Přenáší
jen poznámky, není to šifrování ani záloha účtů. Import přidává, původní nemaže.
Řeč 24 je volitelná: python precti.py "Ukázka." je náhled, --mluv zvolí
systémový hlas (Windows System.Speech, macOS say, Linux espeak-ng/espeak cs).
Bez nových pip balíčků; skutečný hlas a reproduktor ověřte místně.

Pro Pygame 2 (dostupné všechny lekce 1–30):
```
python tools/setup_env.py --courses pygame-2
```
Instaluje stejné pygame-ce jako Pygame 1, nikoli původní balíček pygame.
Prvních pět lekcí má obrázkové náhledy z Surface bez okna a zvuku. PNG lze
prohlédnout/stáhnout v aplikaci; v editoru zůstává v pracovní složce.
Vyberte stejnou .venv ve VS Code, VSCodium nebo PyCharm. Meteority 6–10 otevírají
živé okno na počítači, kde běží Python; pro hraní je potřeba místní grafická
plocha. Okno se nepřenáší ze vzdáleného serveru do prohlížeče. Aktivujte je
kliknutím a pohybujte lodí šipkami. V lekci 10 P přepíná pauzu, R restartuje
a Esc ukončí hru. Běžné zavření uloží poslední `meteority.png` do pracovní složky
a aplikace jej nabídne ke stažení; Stop tento snímek nezaručuje. Zvuk není potřeba.
Chyť robota 11–15 používá stejné prostředí a místní okno, cíle chytáte levým
tlačítkem myši. V lekci 15 Mezerník spustí lov nebo vrátí výsledek do nabídky,
P pozastaví/pokračuje, R začne nový lov a Esc ukončí program. Běžné zavření
uloží `roboti.png`. Žádné další balíčky se neinstalují.
Součásti větší hry 16–20 tvoří samostatné pokusy bez okna a povinného zvuku,
s PNG `soucasti.png`. Po uložení do pracovní složky je v lekci 16 volitelný
`python prehraj_ton.py --play` (krátký vlastní tón, limit zařízení 5 s).
V Úkolu 5 lekce 20 lze po uložení reseni.py spustit `python ziva_dilna.py`:
myš spustí dílnu, P pauza, M nabídka, Esc/křížek konec. Potřebuje místní
grafickou plochu, zvuk nepoužívá. Použijte stejný Python z .venv.
Hon na dronech 21–25 otevírá místní okno 720×540. Šipky/WASD pohybují hráčem;
v lekci 25 Mezerník spustí let nebo vrátí výsledek do nabídky, P přepíná pauzu,
R začne nový let a Esc zavře program. Nasbírejte alespoň šest dat a přežijte
tři desetisekundové vlny. Štít přístavu má 2,5 s a dobíjí se pouze mimo něj.
V tréninku 23 je N další vlna, v hotové misi se střídají automaticky.
Běžné zavření uloží `droni.png`; Stop soubor nezaručuje. Nové závislosti
ani zvuk nejsou potřeba, okno se ze vzdáleného Pythonu do prohlížeče nepřenáší.
Závěr 26–29 má konzolové scénáře, unittest, JSON výsledky a příkazy k předání.
Kurýrská směna 30 je živá varianta s profilem a tabulkou pěti výsledků.
Pro trvalé data/vysledky.json uložte pracovní složku a spusťte v ní reseni.py;
běžný webový běh používá dočasné soubory. python over_projekt.py provede
přiložené testy modelu; vlastní testy doplňte do testy. Volitelný PyInstaller 6.22.3
nainstalujte jen pro stavbu ve stejné .venv; python sestavit.py spustí skutečné
sestavení onedir. Celou distribuční složku ponechte pohromadě. Ověřen Linux,
Windows/macOS vyžadují vlastní sestavení a zkoušku. Podrobnosti v lekci 29 a NAVOD.md.
Ověřeno Python 3.14.8/pygame-ce 2.5.8.

Pro Datovou analýzu:
```
python tools/setup_env.py --courses pandas
```
Nainstaluje pandas řady 3, matplotlib, openpyxl a ipykernel do stejné projektové
.venv. Prvních 25 lekcí potřebuje pouze pandas, lekce 26–30 také Matplotlib.
Modul 31–35 používá i openpyxl pro Excel; měsíční projekt propojí tabulky a graf.
Závěr 36–42 má samostatnou Analytickou dílnu, testy a volitelný notebook.
Všech 42 lekcí je připravených. Projekt nabízí také MD/IPYNB ke stažení.
Soubory .py běží v aplikaci i terminálu bez grafické plochy. V aplikaci vzniknou
náhledy PNG s možností stažení; v editoru obrázky najdete v pracovní složce procesu. Souborové lekce nabízejí
také stažení CSV/XLSX včetně zdrojů; v editoru výstupy zůstávají na disku.
Notebooky a buňky # %% jsou volitelné. Po změně projektových helperů
restartujte jádro a spusťte buňky od začátku, ne pouze poslední buňku.
Balíčky používá Python z .venv; zvolte jej také v editoru. Po instalaci aplikaci
znovu spusťte. Ověřeno s Pythonem 3.14.8, pandas 3.1.1, Matplotlib 3.11.2 a openpyxl 3.1.5.

Bez --courses pomocník připraví běžné balíčky všech kurzů; --extras navíc
volitelné PyInstaller, qrcode a pyttsx3. Instalace těchto součástí není nutná
pro úvod Datové analýzy.

Volitelně rozšíření pro VSCodium:
```
python tools/install_extensions.py
```

## 3. Kontrola prostředí

```
python tools/doctor.py
```
Vypíše, co je v pořádku a co chybí.

## 4. Spuštění serveru a aplikace

```
python start.py
```
Spustí místní server na `127.0.0.1` a otevře prohlížeč. Pokud se prohlížeč neotevře, zkopírujte do něj adresu, kterou `start.py` vypíše, včetně části `?t=...` (token). Adresu s tokenem nikomu nedávejte.

Užitečné volby:
```
python start.py --port 8800        # jiný port (výchozí 8765)
python start.py --no-browser       # neotevírat prohlížeč
```
Server zastavíte v terminálu klávesami **Ctrl+C**. Při dalším spuštění se vypíše nová adresa s novým tokenem.

## 5. Kontrola lekcí a testy (volitelné)

```
python tools/validate_courses.py
python -I -m unittest discover -s tests
```
Pygame lekce se při kontrole spouští bez okna, pro vlastní hraní potřebují nainstalovaný `pygame-ce` (krok 2).

## Když něco nejde

- „python není rozpoznán“: Python není v PATH, použijte `py` nebo ho přeinstalujte se zaškrtnutým PATH.
- Port je obsazen: spusťte s jiným `--port`.
- Další rady: `docs/reseni-problemu.md`.

## Příprava konkrétního kurzu a volba editoru (v0.35)
Na začátku každého podkurzu vyberte systém a VS Code, VSCodium nebo PyCharm.
Návod ukáže správnou cestu k interpreteru, balíčky a jejich ověření. Příkazy pro
aktivaci lze vynechat, když používáte přímo `.venv\Scripts\python.exe` na Windows
nebo `./.venv/bin/python` na macOS/Linux. V PowerShellu přidejte na začátek `./`
nebo `.\` pro cestu v aktuálním adresáři.

`--courses` vybírá podkurzy, `--dry-run` ukáže plán bez instalace. `--extras` je
volba pro pozdější volitelné balíčky (PyInstaller, QR kódy, řeč). Výchozí instalace
je neinstaluje. Systémový Tkinter se přes pip neinstaluje.

V kurzu Okenní aplikace, API a e-maily je od lekce 13 potřeba requests a od
lekce 18 také aiosmtpd pro místní SMTP záchyt. Připraví je
`python tools/setup_env.py --courses tkinter-api`. Pro doplnění do již existující
.venv lze použít její Python s `-m pip install "aiosmtpd>=1.4.6,<2"`.
E-mailová cvičení nepotřebují osobní schránku, zprávy zůstávají na 127.0.0.1.

V katalogu začněte konceptem „Začínáme: prostředí, projekt a Git“. GitHub a virtuální
server jsou až další témata; pro běžné procvičování nejsou potřeba.
