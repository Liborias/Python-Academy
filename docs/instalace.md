## Co budete potřebovat

Python 3.12 nebo novější, doporučená řada 3.14 (ověřeno v této verzi na 3.14.8), prohlížeč a jeden editor: **VS Code, VSCodium nebo PyCharm**. Editor Python nenahrazuje. Git a účet GitHub potřebujete až pro verzování; virtuální server je volitelný.

V katalogu je na prvním místě koncept **Začínáme: prostředí, projekt a Git**. Na začátku každého podkurzu je vlastní příprava: zvolte systém a editor a použijte příkazy pro jeho konkrétní balíčky. Výběr se pamatuje v tomto prohlížeči, ale nic automaticky neinstaluje.

## Windows

1. Stáhněte [Python](https://www.python.org/downloads/windows/). U klasického instalátoru povolte launcher a Add python.exe to PATH. V novém PowerShellu ověřte `py -3.14 --version`.
2. Vybraný editor stáhněte z [VS Code](https://code.visualstudio.com/), [VSCodium](https://vscodium.com/) nebo [PyCharm](https://www.jetbrains.com/pycharm/). Podrobnosti jsou v odpovídající záložce Přípravy.
3. Otevřete složku `dilna-pythonu` a její terminál. Pro začátek stačí:
```powershell
py -3.14 tools/setup_env.py --courses zaklady
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe start.py
```
Aktivace není nutná. Volitelně `.\.venv\Scripts\Activate.ps1`; pokud je blokovaná, dále používejte přímou cestu, není potřeba měnit systémovou politiku.

## macOS

1. Použijte [instalátor Pythonu](https://www.python.org/downloads/macos/) nebo Homebrew `brew install python@3.14`. Ověřte `python3 --version`.
2. Nainstalujte jeden editor z jeho oficiálního webu a otevřete složku projektu.
3. V terminálu ve složce `dilna-pythonu`:
```bash
python3 tools/setup_env.py --courses zaklady
./.venv/bin/python -m pip check
./.venv/bin/python start.py
```
Volitelná aktivace: `source .venv/bin/activate`. Pro Tkinter u Homebrew Pythonu 3.14 doinstalujte `brew install python-tk@3.14`.

## Linux (Debian / Ubuntu)

1. Doinstalujte systémový Python: `sudo apt update` a `sudo apt install python3 python3-venv python3-pip`. Ověřte `python3 --version`. Verze závisí na distribuci, příkaz negarantuje řadu 3.14. Potřebujete alespoň 3.12; systémový Python nepřepisujte ručně.
2. Nainstalujte jeden editor z oficiálního zdroje. Izolované distribuce editorů, například Flatpak, mohou vyžadovat zvláštní přístup k systémovému Pythonu.
3. Použijte stejné příkazy pro instalaci a spuštění jako u macOS. Balíčky pip instalujte do `.venv`, nikoli systémově pomocí sudo pip.
4. Pro Turtle/Tkinter doinstalujte `python3-tk` odpovídající použitému systémovému interpreteru. Ověřte na grafické ploše `./.venv/bin/python -m tkinter`. Tkinter se neinstaluje pomocí pip.

## Balíčky pro vybraný kurz

`tools/setup_env.py --courses zaklady` vytvoří nebo použije společnou `.venv` tohoto výukového projektu bez dalších balíčků. `--courses soubory-web,pygame-1` doplní jen závislosti těchto kurzů. `--dry-run` vypíše plán a nic nezmění.

Bez `--courses` pomocník připraví běžné balíčky všech kurzů: requests, beautifulsoup4, pygame-ce, pandas řady 3, matplotlib, openpyxl, ipykernel a aiosmtpd pro místní e-mailový záchyt. Pro začátečníka to není nutné. Příznak `--extras` přidá volitelné součásti zvoleného kurzu: PyInstaller pro balení v tkinter-api, qrcode a pyttsx3 pro pozdější projekty databaze. Jejich funkce a systémové závislosti se ověřují až v příslušném projektu.

Pro Datovou analýzu použijte `python tools/setup_env.py --courses pandas`.
Všech 42 lekcí je připravených: prvních 25 používá pandas, grafy v lekcích
26–30 také Matplotlib a modul 31–35 openpyxl pro Excel. Měsíční projekt 35
používá všechny tři knihovny; závěrečná Analytická dílna 36–42 je propojí
s testy a předáním. Ipykernel zůstává pro volitelný notebook v lekci 41. Instalace vybírá `pandas>=3,<4`. Grafy používají Figure a soubory PNG,
nejde o samostatná okna; v aplikaci uvidíte náhled a odkaz ke stažení.
Z editoru se PNG uloží do pracovní složky běžícího procesu. Souborové lekce
nabízejí i stažení CSV/XLSX; přiložené vstupy se do pracovního editoru kopírují
vedle reseni.py. Závěrečný projekt nabízí také MD/IPYNB ke stažení.
Při přechodu mezi kroky s jinou verzí helperů restartujte notebookové jádro;
vyberte .venv a ověřte sys.executable. Notebook ani zobrazené jméno jádra
nenahrazují instalaci závislostí. Ověření Excelu: `python -c "import openpyxl; print(openpyxl.__version__)"`.
Ověření v projektové .venv: `python -c "import sys, pandas as pd; print(sys.version); print(pd.__version__)"`.
Ověřeno: Python 3.14.8, pandas 3.1.1, NumPy 2.5.4 a Matplotlib 3.11.2 a openpyxl 3.1.5 na Linuxu.
Matplotlib ověří `python -c "import matplotlib; print(matplotlib.__version__)"`.
Editor musí mít zvolené stejné prostředí. Všechny úvodní .py soubory běží také
v terminálu; podpora buněk `# %%` a notebooků závisí na editoru a rozšířeních.

> Instalujte **pygame-ce**, v kódu používejte `import pygame`. Nekombinujte jej ve stejném prostředí s původním balíčkem pygame.

Pro každý vlastní projekt mimo Dílnu vytvořte jeho vlastní `.venv`. Výběr interpreteru v editoru, terminálu a případně notebookovém jádru musí mířit do stejného prostředí.

## Spuštění a ověření

Otevřete adresu, kterou `start.py` vypíše. Terminál nechte běžet, zastavení je Ctrl+C. Obsazený port změňte například pomocí `start.py --port 8766`. Server má běžet jen na vašem počítači. Pro první kurz nepotřebujete nic nasazovat na internet.

Návody pro Windows/macOS a grafická menu editorů ověřte na svém počítači; automatické testy aplikace jejich funkčnost nepotvrzují. Volby a zaškrtávací seznamy v průvodci představují vaše vlastní potvrzení.
