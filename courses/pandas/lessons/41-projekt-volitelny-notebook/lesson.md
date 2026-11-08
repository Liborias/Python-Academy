## Notebook je jiný způsob spuštění stejné analýzy

Notebook kombinuje text a buňky kódu. Výhodou je průběžný výklad a viditelné mezivýsledky, rizikem skrytý stav: buňka může používat proměnnou vytvořenou dávno předtím. Proto musí jít vše spustit od začátku v novém jádře. Samotný uložený obrázek v notebooku není důkaz, že kód pořád funguje.

Notebook je zde volitelný. Přiložený bez_notebooku.py používá stejné buňky a funkce jako notebook; funguje i běžný .py bez interaktivního editoru. V prohlížeči spouštíme tuto skriptovou variantu, nikoli interaktivní Jupyter server. Výstupy jsou stejné CSV/XLSX/PNG/MD.

## Příprava jádra

Pomocník kurzu už instaluje ipykernel. VS Code/VSCodium potřebuje také rozšíření Jupyter a zvolené jádro ze stejné .venv. V PyCharm dostupnost notebooků závisí na verzi a licenci. Metadata mohou zobrazovat jméno Python 3 (projektová .venv), ale to samo interpreter nevytvoří ani nezvolí. První buňka vypíše sys.executable; ten porovnejte s Pythonem vašeho projektu.

## Co je soubor IPYNB

IPYNB je JSON dokument, nikoli zip ani obrázek. Formát 4.5 má seznam cells a metadata. Textová buňka má cell_type markdown; kódová code, source, prázdné outputs a execution_count None, dokud se nespustí. Každá buňka má jedinečné id. Kernelspec v metadatech popisuje jazyk a jméno jádra. Tyto položky nevykonávají kód, dokud buňky nespustíte.

```python
from bunky import BUNKY, UVOD
print("Počet kódových buněk:", len(BUNKY))
print(UVOD)
for cislo, source in enumerate(BUNKY, 1):
    print("Buňka", cislo, "má", len(source.splitlines()), "řádků.")
```

Bunky.py je přiložený modul s hotovými zdroji pěti buněk a úvodem. Enumerate čísluje od 1. Splitlines(keepends=True) může zdroj rozdělit na seznam řádků se zachovanými konci; JSON notebook dovoluje pro source i jediný str. Každá buňka má svůj krok: importy/interpreter, načtení a schéma, čištění/spojení, výstupy/zpráva a veřejné testy. Tento obsah neměňte ani nepřeskládávejte.

## Váš úkol

Dokončete `vytvor_notebook()`. Vraťte slovník pro notebook 4.5: nejprve jednu Markdown buňku s UVOD, potom pět kódových podle BUNKY, v tomto pořadí. Přidejte neprázdná jedinečná id (písmena, čísla, podtržítko nebo pomlčka, nejvýše 64 znaků), metadata, prázdné outputs a execution_count=None. Metadata kernelspec mají neprázdné name a display_name, language python; language_info má name python. Hodnoty pořadí neodvozujte od předchozího běhu.

Ukázkové volání použije json.dumps(..., ensure_ascii=False, indent=2) a write_text s UTF-8 pro skutečný analyticka_dilna.ipynb, který lze stáhnout. Ensure_ascii=False ponechá český text čitelný, indent jen formátuje JSON. Pak spustí obyčejnou skriptovou variantu. Odkrytí řešení váš kód nepřepisuje.

V editoru otevřete stažený nebo vytvořený notebook v pracovní složce se zdroji a helpery. Restartujte jádro a spusťte všechny buňky od první. Nevytvářejte výsledek spuštěním jen poslední buňky. Automatická kontrola ověří strukturu i provedení buněk od čistého prostoru. Při potížích v editoru nejprve porovnejte sys.executable s Pythonem projektu a ověřte, že má nainstalované potřebné knihovny.
