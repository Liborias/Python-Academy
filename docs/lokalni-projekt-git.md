# Python Akademie: místní složka, aktualizace a korektury přes Git

Tento návod používá repozitář `https://github.com/Liborias/Python-Academy` a hlavní větev `main`. Příklady jsou pro Windows a PowerShell; odlišné příkazy pro macOS/Linux jsou níže. Doporučená místní složka je `C:\Projekty\Python-Academy`.

## 1. Co je potřeba vyřešit jednou

Repozitář nyní obsahuje celý projekt Dílna Pythonu v0.36. Po clone nebo pull máte v jeho kořeni start.py a složky aplikace. Jednorázový import popsaný v oddílu 4 už pro tento repozitář není potřeba; tento oddíl je ponechán jako postup pro případ jiné dosud prázdné kopie.

Publikace cloudového prostředí vytvoří jeho uloženou verzi. Nevytváří automaticky commit a neodesílá aplikaci na GitHub. Ani vytvoření nového ZIPu neaktualizuje repozitář. Pro budoucí `git pull` musí být každá nová verze commitnutá a odeslaná do téhož repozitáře; na main se dostane přímo nebo sloučením pull requestu.

Pokud už mezitím na GitHubu vidíte `start.py`, `server`, `web` a `courses`, přeskočte jednorázový import v oddílu 4.

## 2. Nainstalujte nástroje

- Git z https://git-scm.com/downloads
- Python 3.14 z https://www.python.org/downloads/ (projekt byl ověřen na 3.14.8).
- Jeden editor: VS Code, VSCodium nebo PyCharm.

Po instalaci otevřete nový PowerShell a ověřte:

```powershell
git --version
py -3.14 --version
```

První příkaz vypíše verzi dostupného Gitu. Druhý vybere nainstalovanou řadu Pythonu 3.14 a vypíše její verzi. Pokud příkaz není nalezen, ověřte instalaci a otevřete terminál znovu. Tyto příkazy ještě žádný projekt nestahují.

## 3. Jednou naklonujte repozitář

V PowerShellu vytvořte rodičovskou složku, pokud ji ještě nemáte:

```powershell
New-Item -ItemType Directory -Force C:\Projekty
cd C:\Projekty
git clone https://github.com/Liborias/Python-Academy.git
cd Python-Academy
git status
git remote -v
```

- `New-Item` vytvoří složku pro vaše projekty; `-Force` dovolí použít již existující adresář.
- `cd` mění pracovní složku aktuálního terminálu.
- `git clone` vytvoří novou složku Python-Academy a stáhne soubory i historii. Uvnitř založí skrytou `.git` s propojením na GitHub. **Neklonujte do složky s rozbaleným projektem; cílová složka má být nová.**
- `git status` ukáže aktuální větev a místní změny. Po čistém clone očekávejte main a čistý pracovní strom.
- `git remote -v` ukáže vzdálený repozitář pod názvem origin. Adresa má být právě Liborias/Python-Academy.

U soukromého repozitáře se může otevřít přihlášení přes prohlížeč/správce údajů Gitu. Použijte účet s přístupem do tohoto repozitáře. Běžné heslo k GitHubu neslouží jako heslo pro Git přes HTTPS. Tokeny nevkládejte do adresy repozitáře, kódu ani chatu. Přístup pro čtení stačí na clone/pull, pro push potřebujete oprávnění zapisovat.

Příkaz clone použijete **jen jednou pro tento počítač a tuto složku**. Příště použijete pull.

## 4. Jednorázově vložte celý projekt, pokud na GitHubu ještě není

Nejprve stáhněte a rozbalte `dilna-pythonu-v0.36.zip` do jiné dočasné složky. Z jeho vnitřní složky `dilna-pythonu` zkopírujte **obsah** do právě naklonované složky `C:\Projekty\Python-Academy`. Vložte také `.gitignore` a `.vscode`; při kopírování si zobrazte skryté soubory. Stávající krátký README bude nahrazen návodem projektu.

Výsledek má vypadat takto:

```text
C:\Projekty\Python-Academy\
    .git\                  původní Git metadata z clone, ponechat
    .gitignore
    .vscode\
    start.py
    README.md
    courses\
    docs\
    lib\
    server\
    tests\
    tools\
    web\
    workspace\
```

Nevkládejte další vnořenou složku `Python-Academy\dilna-pythonu\start.py`. Kořenem projektu bude přímo Python-Academy. `.git` nemažte ani nenahrazujte. `git init` už není potřeba, protože repozitář založil clone.

V editoru zkontrolujte `.gitignore`. Archiv už ignoruje `.venv`, Python cache a pracovní řešení studentů. Na konec doplňte tyto dva řádky, pokud chybí:

```gitignore
.env
*.zip
```

Tím se nové lokální konfigurace `.env` a ZIP archivy nebudou nabízet ke commitu. Ignorování nezruší sledování souboru, který už byl dříve commitnutý. Žádná hesla ani soukromé klíče do repozitáře nekopírujte.

V terminálu ve složce Python-Academy nastavte autora commitů. **Jméno a e-mail v příkladu nahraďte svými údaji**; pro soukromí můžete použít svou noreply adresu z nastavení GitHubu:

```powershell
git config user.name "Vase jmeno"
git config user.email "vas-email@example.com"
git status
git add .
git diff --staged --stat
git diff --staged
git commit -m "Pridani projektu Dilna Pythonu v0.36"
git push origin main
```

- `git config` bez `--global` uloží autora pouze pro tento repozitář. Nejde o přihlášení k GitHubu.
- `git add .` připraví neignorované změny v aktuální složce k uložení. Proto jej pouštějte z kořene projektu a nejdřív zkontrolujte status.
- `git diff --staged --stat` ukáže souhrn připravených souborů, bez `--stat` jejich konkrétní změny. Ověřte, že mezi nimi není `.venv`, vaše rozepsaná řešení nebo soukromá konfigurace.
- `git commit` uloží místní verzi s popisnou zprávou.
- `git push origin main` odešle commit do hlavní větve na GitHubu.

Pokud se omylem připravil nežádoucí soubor, před commitem jej vyřaďte pomocí `git restore --staged cesta/k/souboru`. Tento příkaz ponechá soubor na disku a jen ho odebere z připravených změn.

Nakonec na GitHubu ověřte, že ve větvi main vidíte `start.py` a složky aplikace. Pokud pravidla repozitáře zakazují přímý push do main, zachovejte svůj místní commit, vytvořte větev `git switch -c import-v0-36`, odešlete `git push -u origin import-v0-36` a na GitHubu vytvořte pull request do main. Po jeho sloučení se vraťte `git switch main` a spusťte `git pull --ff-only origin main`.

## 5. Vytvořte místní virtuální prostředí a spusťte projekt

Stále pracujte v `C:\Projekty\Python-Academy`:

```powershell
py -3.14 tools/setup_env.py --courses zaklady
.\.venv\Scripts\python.exe -c "import sys; print(sys.executable)"
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe start.py
```

- Pomocník `setup_env.py` vytvoří místní `.venv`. Pro Základy nepřidává žádné externí pip balíčky. Pro více kurzů použijte například `--courses zaklady,soubory-web,pygame-1` nebo postup v přípravě konkrétního podkurzu.
- Druhý příkaz ověří interpreter: očekávejte cestu začínající `C:\Projekty\Python-Academy\.venv\`.
- `pip check` zkontroluje deklarované závislosti.
- `start.py` spustí místní server a otevře prohlížeč. Terminál ponechte běžet. K ukončení použijte Ctrl+C.

Aktivace prostředí není nutná, protože používáte jeho přesnou cestu. `.venv` si každý počítač vytvoří zvlášť a Git ji nepřenáší.

V editoru otevřete celou složku Python-Academy. VS Code/VSCodium: Python: Select Interpreter → `.venv\Scripts\python.exe`. PyCharm: nastavení Python Interpreter → existující prostředí se stejnou cestou. Nové další prostředí nevytvářejte, pokud tato `.venv` už funguje.

## 6. Běžné stažení nové verze bez vlastních korektur

Nejdříve zastavte aplikaci pomocí Ctrl+C. Ve složce projektu:

```powershell
cd C:\Projekty\Python-Academy
git status
```

Jestli status hlásí čistý pracovní strom, pokračujte:

```powershell
git switch main
git pull --ff-only origin main
.\.venv\Scripts\python.exe start.py
```

`git switch main` vybere hlavní větev. `git pull --ff-only origin main` stáhne její nové commity a aktualizuje místní soubory, pokud to jde bez slučovacího commitu. Výpis `Already up to date` znamená, že na GitHubu není nic novějšího. Pull neinstaluje Python, neaktualizuje balíčky a sám nespouští aplikaci.

Pokud nová verze mění závislosti nebo začínáte další podkurz, před spuštěním zopakujte příslušný `tools/setup_env.py --courses ...` a ověření pip check. Nemusíte mazat a tvořit `.venv` při každém pull.

Pokud status ukazuje rozdělané změny, nejprve je uložte do vlastní větve postupem níže. Nepoužívejte mazání změn jako prostředek k vynucení aktualizace.

## 7. Doporučená práce s korekturami

Používejte **main pro přebírání hlavní verze** a **vlastní větev pro korektury**. Začněte z čisté aktualizované main:

```powershell
git switch main
git pull --ff-only origin main
git switch -c korektury-prvni-kolo
```

`switch -c` založí novou větev z aktuálního stavu a přepne do ní. V této větvi upravujte texty nebo kód. Před commitem soubory uložte v editoru a změny vyzkoušejte spuštěním aplikace.

Pokud už jste začali upravovat soubory přímo na main, s necommitnutými úpravami můžete nejprve vytvořit novou větev `git switch -c korektury-prvni-kolo`. Necommitnuté soubory zůstanou ve vaší pracovní složce a další commit už vznikne v nové větvi. Neprovádějte předtím pull.

Po dokončení malé srozumitelné dávky korektur:

```powershell
git status
git diff
git add .
git diff --staged
git commit -m "Korektury vykladu a navodu"
git push -u origin korektury-prvni-kolo
```

- `git diff` ukáže zatím nepřipravené rozdíly. `git diff --staged` ověří, co opravdu uložíte.
- Commit je místní bod v historii. Push větev navíc uloží na GitHub.
- `-u` nastaví vztah této místní větve k její vzdálené větvi; příště na ní stačí `git push`.

Na GitHubu vytvořte pull request z `korektury-prvni-kolo` do `main`. Je to návrh na přijetí změn; po kontrole ho sloučíte. Potom místně:

```powershell
git switch main
git pull --ff-only origin main
```

Tím stáhnete hlavní verzi již s přijatými korekturami. Pro další kolo založte novou větev s novým názvem, například `korektury-druhe-kolo`. Větev se stejným názvem nevytvářejte příkazem `-c` znovu.

## 8. Nová hlavní verze během rozepsaných korektur

Nejprve na korekturní větvi uložte svůj aktuální stav přes add a commit. Ověřte čistý status. Potom:

```powershell
git switch main
git pull --ff-only origin main
git switch korektury-prvni-kolo
git merge main
```

První dva příkazy stáhnou hlavní verzi. Návrat na vaši větev a `merge main` přidají nové hlavní změny k vašim korekturám. Pokud se upravovaly různé řádky, Git je většinou spojí sám. Po sloučení aplikaci znovu vyzkoušejte a větev odešlete pomocí `git push`.

Pokud obě strany změnily stejnou část, Git oznámí konflikt. Spusťte `git status`, otevřete označené soubory, vyberte výsledné znění a odstraňte konfliktní značky. Po kontrole připravte vyřešené soubory přes `git add` a dokončete slučování `git commit`.

Jestli si s rozpracovaným konfliktem nejste jistí, použijte `git merge --abort`. Protože jste před slučováním měli vlastní korektury commitnuté a čistou pracovní kopii, vrátíte se k nim před pokusem o merge. Force push nebo `reset --hard` pro tento postup nejsou potřeba.

## 9. macOS a Linux: odlišné příkazy

Git příkazy fungují stejně. Pro rodičovskou složku a první clone můžete použít:

```bash
mkdir -p ~/Projekty
cd ~/Projekty
git clone https://github.com/Liborias/Python-Academy.git
cd Python-Academy
```

Po importu aplikace nebo stažení již naplněného repozitáře:

```bash
python3 tools/setup_env.py --courses zaklady
./.venv/bin/python -c "import sys; print(sys.executable)"
./.venv/bin/python -m pip check
./.venv/bin/python start.py
```

`mkdir -p` dovolí použít existující rodičovskou složku. `~` značí váš domovský adresář. Ověřte `python3 --version` před tvorbou prostředí; doporučujeme 3.14. Místo windowsové cesty k interpreteru používejte `.venv/bin/python`. Ostatní postupy pro main, pull a korekturní větve se nemění.

## Rychlá denní připomínka

1. Zastavit běžící aplikaci, uložit soubory v editoru, zkontrolovat git status.
2. Vlastní korektury mít uložené ve své větvi.
3. Na main provést git pull --ff-only origin main.
4. Pro korektury založit novou větev nebo začlenit main do existující korekturní větve.
5. Spustit projekt Pythonem z místní .venv a ověřit změny.

Cloudové prostředí, GitHub a místní disk jsou tři různá místa. Změna se přenese přes Git až po commitu a push; z GitHubu na váš disk až po pull.
