## Co budeme z dat zjišťovat

Datová analýza začíná otázkou. Které místo mělo nejvyšší teplotu? Kolik návštěvníků přišlo a jak se dny lišily? Budeme používat malé vlastní vymyšlené sady. Není potřeba stahovat skutečná osobní data ani přistupovat k internetu.

V tomto bloku se naučíme Series, výpočty, výběr, DataFrame a CSV. Kurz má připravenou osnovu 42 lekcí a první témata navazují na seznamy, slovníky a funkce ze Základů. Před každým modulem rozlišíme, co už máme a co teprve přidáme.

## Stejný Python pro knihovny i kód

Příprava nahoře nabízí Windows/macOS/Linux a VS Code/VSCodium/PyCharm. Ve složce projektu lze Pythonem z vybraného prostředí použít `python tools/setup_env.py --courses pandas`. Pomocník připraví .venv a balíčky pandas, matplotlib, openpyxl a ipykernel. První blok používá jen pandas; další součásti jsou pro grafy, Excel a notebookové buňky.

Ověření v aktivované .venv: `python -c "import sys, pandas as pd; print(sys.version); print(pd.__version__)"`. Python spustí krátký kód za -c, sys.version ukáže interpreter a pd.__version__ knihovnu. V této verzi kurzu ověřujeme Python 3.14.8 s pandas 3.1.1. Potřebujete řadu pandas 3, instalace používá rozsah pandas>=3,<4.

Soubory obsahují značky `# %%`. Pro Python jsou to komentáře; editor s podporou Jupyter je může rozdělit na buňky. V prohlížeči se spouští celý .py soubor. V editoru zvolte stejné jádro ze své .venv, případně soubor prostě spusťte jako běžný skript. Nezávisíme na funkci notebooků konkrétní edice editoru.

## Series je seznam hodnot s popisky

`import pandas as pd` načte knihovnu pod krátkým názvem pd. `pd.Series(hodnoty, index=mista, name=nazev, dtype="float64")` vytvoří jednorozměrná data. Hodnoty pocházejí ze seznamu, index jsou popisky jednotlivých záznamů, name název celé Series a dtype určuje typ hodnot. Float64 dovolí desetinná čísla a stejný typ i pro prázdný výsledek. Hodnoty a index musí mít stejnou délku.

V našich prvních příkladech je index jedinečný a textový. Může to být Brno, Praha a Zlin, později i číselný kód. Pořadí se při konstrukci zachová. Index není automaticky pořadové číslo a name není další prvek dat. Výpis ukazuje vlevo popisky, vpravo hodnoty a pod nimi název a datový typ. Zobrazení se může mezi verzemi mírně lišit v mezerách; podstatná jsou data.

Series lze vytvořit také ze slovníku: klíče se stanou indexem a hodnoty daty. Pořadí vložení slovníku zůstává zachované. Vstupní seznam nebo slovník se při konstrukci nemění.

## Název, seznam a délka

V doplňkových úkolech použijeme `serie.rename("novy")` pro nový název celé Series, `serie.tolist()` pro běžný seznam hodnot a `len(serie)` pro počet prvků. Rename bez inplace vrací nový výsledek, původní Series nepojmenovává znovu. ToList zahodí popisky, ale zachová pořadí hodnot.

U číselné float64 Series se z chybějícího údaje None stane NaN. Znamená chybějící hodnotu, ne nulu. Len počítá všechna místa včetně tohoto záznamu. Metoda count naopak počítá jen hodnoty, které nechybějí. Podrobné čištění přijde v dalším modulu.

## Váš úkol

Dokončete `vytvor_mereni(hodnoty, mista, nazev)`. Dostanete seznam čísel nebo None, stejně dlouhý seznam jedinečných textových popisků a textový název. Vraťte Series přesně v předaném pořadí s předaným name a dtype="float64". Prázdné seznamy jsou platné. Vstupy neměňte.

Vyzkoušejte vlastní místa, zápornou teplotu, nulu a None. Pod úkolem lze zobrazit možné řešení. Další čtyři zadání mají vlastní kód i řešení, takže se mezi nimi můžete přepínat bez přepsání rozepsané práce.
