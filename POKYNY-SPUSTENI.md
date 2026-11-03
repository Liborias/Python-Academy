# Dílna Pythonu: ověření Pythonu, instalace a spuštění

Všechny příkazy se zadávají v terminálu **ve složce projektu** (složka `dilna-pythonu` po rozbalení ZIPu).
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
Vytvoří složku `.venv` (virtuální prostředí) a nainstaluje balíčky pro všechny podkurzy
(`requests`, `beautifulsoup4`, `pygame-ce`, `pandas`, `matplotlib`, `openpyxl`, `ipykernel`, `pyinstaller`, `qrcode[pil]`, `pyttsx3`).
Vyžaduje internet.

Jen vybrané podkurzy:
```
python tools/setup_env.py --courses soubory-web,pygame-1
```
Co by se instalovalo, bez instalace:
```
python tools/setup_env.py --dry-run
```
Základní podkurz **Základy** žádné balíčky nepotřebuje.

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

V katalogu začněte konceptem „Začínáme: prostředí, projekt a Git“. GitHub a virtuální
server jsou až další témata; pro běžné procvičování nejsou potřeba.
