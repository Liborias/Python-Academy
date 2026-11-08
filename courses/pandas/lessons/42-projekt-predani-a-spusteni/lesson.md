## Předání znamená možnost zopakovat výpočet

Hotový obrázek bez vstupů a postupu nestačí. Vytvoříme samostatný adresář s vlastními daty, ověřenými funkcemi, skriptem, notebookem, návodem, seznamem závislostí a testy. Musí fungovat po přenesení do jiné složky, bez importů Akademie. Publikace na GitHubu není součást automatického spuštění lekce.

## Co už máte připravené

Predchozi.py obsahuje přesné funkce lekcí 36–41. V podsložce projekt je podklad se zdrojovým analyza.py, stejnými funkcemi, bunky.py, test_dilna.py, README, datovým slovníkem, requirements.txt a .gitignore. Tento podklad nekopíruje vaše tajné nastavení ani .venv; obsahuje pouze cvičný projekt. Vstupní soubory ale musí být skutečné cesty předané vaší funkci, ne natvrdo vzor z jiného běhu.

## Váš úkol

Dokončete `spust_dilnu(mereni_cesta, mista_cesta, slozka)`. Obě vstupní cesty existují, jsou různé a neleží v cílové složce ani v podkladu projekt. Slozka je jiná cesta než podklad; může existovat s dalšími soubory. Zachovejte zdroje i tyto další soubory. Nový běh může přepsat pojmenované součásti sestavení a výsledky.

1. Načtěte oba CSV jako UTF-8 text se středníkem a bez výchozího NA. Pomocí over_schema ověřte měření a katalog; chybné schéma odmítněte ValueError.
2. Proveďte vycisti_mereni a spoj_a_shrn. Duplicitní katalog musí pořád vyvolat MergeError. Ověřujte před vytvořením výsledného projektu, abyste nesestavovali výsledek z neplatné struktury.
3. Přeneste podklad projekt do cílové složky. `shutil.copytree(..., dirs_exist_ok=True)` kopíruje i podsložky a dovolí existující adresář. Nemažte nejprve celý cíl.
4. Přes shutil.copy2 zkopírujte skutečné vstupy do cíle jako mereni.csv a mista.csv. Kopie zůstanou shodné bajty, originály se nemění.
5. Vytvořte analyticka_dilna.ipynb pomocí vytvor_notebook a JSON zápisu z minulé lekce. Podadresář vysledky dostane čtyři skutečné výstupy z vytvor_vystupy.
6. Vraťte slovník projekt (Path cílové složky), vystupy (slovník csv/excel/graf/zprava), prijato/odmitnuto/nesparovano (celočíselné počty z cisteni a prehled).

```python
from pathlib import Path
projekt = Path("hotovy_projekt")
print("Cílová složka:", projekt)
print("Výsledky patří do:", projekt / "vysledky")
print("V terminálu se nejprve přepněte do cílové složky projektu.")
```

Operátor / u Path sestaví další část cesty; sám nic nezapisuje. Po spuštění vašeho kódu se v editoru vytvoří hotovy_projekt. V aplikaci jsou tabulky, zpráva, dokumentace a notebook ke stažení a PNG jako náhled. Pro celý zdrojový adresář použijte pracovní složku editoru: obsahuje i Python moduly a testy. Odkazy po reloadu obnovíte spuštěním kódu; stažené soubory a výstupy z editoru zůstávají na disku.

## Zkouška mimo původní složku

Přepněte se do hotovy_projekt, zvolte vlastní .venv a nainstalujte požadavky příkazem python -m pip install -r requirements.txt. Pak spusťte python analyza.py. Skript znovu načte místní mereni.csv/mista.csv a vytvoří vysledky. Parametry --mereni, --mista a --vystup dovolují zvolit jiné cesty; --help je popíše. Argparse v přiloženém skriptu zpracuje tyto volby, takže nemusíte upravovat zdroj kvůli každému souboru.

Příkaz python -m unittest -v test_dilna spustí osm testů nad funkcí over_prehled z místního predchozi.py. Notebook je další možnost, ne podmínka: po volitelné instalaci ipykernel vyberte stejné jádro, restartujte jej a spusťte všechny buňky. README obsahuje příkazy pro Windows i macOS/Linux a ověřené verze knihoven.

## Git a vlastní korektury

Chcete-li projekt samostatně verzovat, zkopírujte jeho adresář mimo zdrojový repozitář Akademie. README nabízí git init, výběr souborů do git add a první commit; teprve poté lze připojit vlastní prázdný GitHub repozitář a push. Do commitu nepatří .venv ani citlivá vlastní data. Lekce žádný repozitář nevytváří ani nic neodesílá automaticky.

## Závěrečná kontrola

U dodaných dat má celek 11 vstupních záznamů, 7 přijatých, 4 odmítnuté, 1 nespárovaný a 6 spárovaných. Celkový průměr spárovaných měření je 28/6, zobrazený jako 4,67 °C. Excel obsahuje i audit odmítnutí, graf nezakrývá -2 °C a zpráva vymezuje omezení zdroje. Automatický test přenese vytvořenou složku jinam, spustí analyza.py i veřejné testy a ověří výstupy nad více daty.

Tím je všech 42 lekcí Datové analýzy připravených k průchodu a korekturám. Zkuste změnit vlastní vstup, ponechat původní soubor a vysvětlit každou změnu výsledku. To je praktický výstup celého kurzu: opakovatelná analýza, nikoli jen jednou uložený obrázek.
