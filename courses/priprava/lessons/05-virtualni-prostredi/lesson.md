## Cíl
Oddělit balíčky vlastního projektu od ostatních projektů. `.venv` je adresář s interpreterem a balíčky; není to virtuální počítač ani vzdálený server.

## Praktický krok
Ve složce vlastního projektu z minulé lekce:
```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -c "import sys; print(sys.executable)"
.\.venv\Scripts\python.exe -m pip --version
```
Na macOS/Linux místo toho:
```bash
python3 -m venv .venv
./.venv/bin/python -c "import sys; print(sys.executable)"
./.venv/bin/python -m pip --version
```
Aktivace je pohodlí, ne nutnost: PowerShell `.\.venv\Scripts\Activate.ps1`, macOS/Linux `source .venv/bin/activate`. Pokud ji systém blokuje, použijte přímo Python z `.venv`; není třeba oslabovat systémovou politiku. Po aktivaci znamená `python` interpreter prostředí, ukončíte ji `deactivate`.

Základní projekt žádný balíček nepotřebuje. Pro samostatný cvičný pokus lze Pythonem z `.venv` spustit `-m pip install requests`, ověřit `-c "import requests; print(requests.__version__)"` a zapsat závislosti pomocí `-m pip freeze > requirements.txt`. Poslední příkaz používejte v čistém prostředí tohoto malého projektu a nepřepisujte cizí soubor bez kontroly. Obnova probíhá přes `-m pip install -r requirements.txt`, kontrola přes `-m pip check`.

Do Gitu patří `requirements.txt`, nikoli `.venv`. Tu lze znovu vytvořit; nenahrazuje zálohu kódu a nepřenáší se mezi Windows a Linuxem.

## Co příkazy dělají a co se děje
V příkazu `python3 -m venv .venv` (Windows `py -3.14 -m venv .venv`) volba `-m` spouští pojmenovaný modul standardní knihovny. Modul `venv` vytvoří adresář `.venv`, do něj místní interpreter a základní nástroje. Neinstaluje server ani nekopíruje váš kód. Cesta `./.venv/bin/python` nebo `.\.venv\Scripts\python.exe` pak vybere tento interpreter přímo, bez závislosti na aktivaci.

`-m pip --version` vypíše verzi pip a jeho umístění. `-m pip install requests` stáhne requests a jeho závislosti do zvoleného prostředí; potřebuje síť. `-c "import requests; print(requests.__version__)"` prověří, že tento Python knihovnu skutečně načte. `-m pip freeze` vypíše nainstalované balíčky s verzemi. Znak `>` je operátor shellu, který tento výpis uloží do `requirements.txt` a existující soubor přepíše. Přepínač `-r requirements.txt` při instalaci říká pipu, odkud seznam přečíst. `-m pip check` kontroluje soulad deklarovaných závislostí; netestuje funkčnost vašeho programu.

Aktivace upraví výběr příkazu `python` jen v aktuálním terminálu. `deactivate` vrátí předchozí nastavení, adresář `.venv` přitom nemaže. Nový terminál potřebuje novou aktivaci nebo úplnou cestu k interpreteru.

## Vlastní ověření
- [ ] Interpreter i pip ukazují do stejné `.venv`.
- [ ] Spustím svůj `main.py` Pythonem z prostředí.
- [ ] Rozlišuji virtuální prostředí a virtuální server.
