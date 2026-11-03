## Cíl
Získat funkční interpreter a zjistit, který Python příkazy skutečně používají. Pro projekt doporučujeme Python 3.14; tuto verzi aplikace ověřujeme na 3.14.8. Podporované minimum návodu je 3.12.

## Praktický krok
Na Windows použijte [oficiální stažení Pythonu](https://www.python.org/downloads/windows/). U klasického instalátoru povolte launcher a přidání Pythonu do PATH. Otevřete nový PowerShell a spusťte:
```powershell
py -3.14 --version
py -3.14 -c "import sys; print(sys.executable)"
```
Na macOS použijte [instalátor pro macOS](https://www.python.org/downloads/macos/) nebo Homebrew `brew install python@3.14`. V novém terminálu ověřte:
```bash
python3 --version
python3 -c "import sys; print(sys.executable)"
```
Na Debianu/Ubuntu lze použít `sudo apt update` a `sudo apt install python3 python3-venv python3-pip`. Potom použijte stejné ověření jako na macOS. Nabízená verze závisí na distribuci: apt příkaz neslibuje instalaci 3.14. Nepřepisujte systémový Python. Pokud je starší než 3.12, zvolte podporovanou novější distribuci nebo samostatnou instalaci podle oficiální dokumentace.

Pokud příkaz neexistuje, zavřete a znovu otevřete terminál a zkontrolujte instalaci i PATH. Neřešte to instalací náhodného balíčku stejného jména přes pip.

## Co příkazy dělají a co se děje
Ve Windows `py` vybírá nainstalovaný Python a `-3.14` určí jeho řadu. Na macOS/Linux `python3` označuje interpreter nalezený v PATH. `--version` jen vypíše verzi a skončí. Volba `-c` znamená „proveď následující Python kód“; uvozovky ho drží jako jeden argument. `import sys` zpřístupní informace o běžícím interpreteru a `print(sys.executable)` vypíše jeho úplnou cestu. Očekávejte cestu k instalaci, ne název editoru.

`brew install python@3.14` požádá Homebrew o instalaci řady 3.14. Linuxové `sudo apt update` obnoví seznam dostupných balíčků; Python ještě neinstaluje. `sudo apt install ...` instaluje vyjmenované systémové balíčky s oprávněním správce, proto může chtít vaše místní heslo. `python3-venv` doplní podporu virtuálních prostředí a `python3-pip` správce balíčků. Verze závisí na repozitářích distribuce. Na úspěšnou instalaci vždy navazuje nové ověření verze.

## Vlastní ověření
- [ ] Příkaz vypíše verzi Pythonu alespoň 3.12, ideálně 3.14.
- [ ] Znám cestu k interpreteru.
- [ ] Příkaz funguje i v nově otevřeném terminálu.
