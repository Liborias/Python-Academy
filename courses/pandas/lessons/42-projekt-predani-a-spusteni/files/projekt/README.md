# Analytická dílna: předaný projekt

Vlastní smyšlená měření teplot v °C. Zdrojové CSV se nemění; samostatné výstupy vzniknou ve vysledky/.
Neplatné záznamy se oddělují od nespárovaných kódů. Průměr je za známá spárovaná pozorování,
ne za rovnoměrný vzorek stanic nebo kalendářních dnů. Graf sám nedokazuje příčinu.

## Instalace

Otevřete terminál v této složce. Ověřte, že příkaz `python` používá Python 3.14, a vytvořte oddělené prostředí:

```text
python --version
python -m venv .venv
```

`--version` vypíše verzi interpreteru. `-m venv` spustí modul pro vytvoření prostředí a `.venv` je název jeho složky. Projekt tak dostane vlastní knihovny bez změny ostatních projektů.

Windows PowerShell:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

macOS/Linux:

```bash
.venv/bin/python -m pip install -r requirements.txt
```

Přímá cesta určí Python nového prostředí. `-m pip` spustí jeho správce balíčků a `-r requirements.txt` nainstaluje knihovny ze seznamu. Níže místo `python` používejte tuto cestu, pokud prostředí není aktivované. V editoru vyberte stejný interpreter.

## Spuštění a ověření

```text
python analyza.py
python -m unittest -v test_dilna
python analyza.py --mereni mereni.csv --mista mista.csv --vystup jiny_vysledek
```

První příkaz načte dodané vstupy, provede čištění a vytvoří CSV, XLSX, PNG a zprávu MD ve složce `vysledky`. Druhý spustí osm veřejných testů porovnání přehledů; `-v` zobrazí výsledek každého testu. Vedle testů prohlédněte konkrétní výstup a počty odmítnutých/nespárovaných řádků.

Třetí příkaz ukazuje volby pro vstupní soubory a jinou výstupní složku. Přehled voleb vypíše `python analyza.py --help`. Opakovaný běh přepíše pojmenované výsledky, zdrojová CSV zachová.

## Volitelný notebook

```text
python -m pip install ipykernel
```

Tento příkaz do stejného prostředí doplní jádro pro spouštění notebooků.
V editoru zvolte jádro ze stejné .venv; název v metadatech sám nezaručuje správné prostředí.
Otevřete analyticka_dilna.ipynb, restartujte jádro a spusťte všechny buňky od začátku.
Notebook a skript používají stejné ověřené funkce z predchozi.py; internet ani grafické okno nejsou nutné.

## Git a předání

Před novým repozitářem si zvolte vlastní složku mimo zdrojový repozitář Akademie. V ní spusťte:

```text
git init
git branch -M main
git add README.md requirements.txt analyza.py predchozi.py bunky.py test_dilna.py datovy_slovnik.md mereni.csv mista.csv analyticka_dilna.ipynb .gitignore
git commit -m "První opakovatelná analýza"
```

`init` vytvoří místní historii, `branch -M main` pojmenuje větev, `add` vybere vyjmenované soubory pro uložení a `commit` uloží první verzi se zprávou. `.gitignore` vynechá prostředí, mezipaměti a vytvořené výsledky. Před dalším uložením zkontrolujte změny přes `git status` a `git diff`.

Po vytvoření vlastního prázdného repozitáře na GitHubu nahraďte `URL_VASEHO_REPOZITARE` jeho adresou:

```text
git remote add origin URL_VASEHO_REPOZITARE
git push -u origin main
```

`remote add` připojí vzdálenou adresu pod jménem `origin`. `push` odešle uložené commity a `-u` nastaví sledování větve pro další práci. Tyto příkazy v lekci nic automaticky nepublikují. Do repozitáře nepatří `.venv` ani citlivá vlastní data.

Testováno na Pythonu 3.14.8/pandas 3.1.1/Matplotlib 3.11.2/openpyxl 3.1.5.
