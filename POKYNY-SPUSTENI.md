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

Pro Datovou analýzu:
```
python tools/setup_env.py --courses pandas
```
Nainstaluje pandas řady 3, matplotlib, openpyxl a ipykernel do stejné projektové
.venv. Prvních pět lekcí potřebuje pouze pandas a běží jako běžné .py soubory
v aplikaci nebo terminálu. Notebooky a buňky # %% jsou volitelné.
Balíčky používá Python z .venv; zvolte jej také v editoru. Po instalaci aplikaci
znovu spusťte. Ověřený úvod používá Python 3.14.8 a pandas 3.1.1.

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
