## Graf a zpráva musí odpovídat stejným datům

Máme už čisté/odmítnuté záznamy a přehledy. Teď vytvoříme předatelné soubory a krátkou zprávu. Použijeme funkce předchozích kroků z predchozi.py. Žádný úspěšný export sám o sobě nezaručuje správný obsah; proto kontrolujeme skutečné buňky i hodnoty vykreslené v grafu.

```python
import pandas as pd
from predchozi import vycisti_mereni, spoj_a_shrn
raw = pd.read_csv("mereni.csv", sep=";", encoding="utf-8", dtype="str", keep_default_na=False)
mista = pd.read_csv("mista.csv", sep=";", encoding="utf-8", dtype="str", keep_default_na=False)
cisteni = vycisti_mereni(raw)
prehled = spoj_a_shrn(cisteni["cista"], mista)
print("Spárovaná měření:", len(prehled["spojena"]))
print("Celkový průměr:", prehled["spojena"]["teplota"].mean())
```

Mean počítá průměr jednotlivých spárovaných měření. Průměr tří skupinových průměrů by stanicím dal stejnou váhu, přestože mají 3/2/1 pozorování. U vzoru dostaneme 28/6, tedy po zobrazení na dvě desetinná místa 4,67 °C. Původní hodnoty ani mezivýsledky přitom nezaokrouhlujeme.

## Nejprve čitelná zpráva

`napis_zpravu(cisteni, prehled)` vrátí Markdown str. Uveďte nadpis Analytická dílna a řádky Přijaté záznamy, Odmítnuté záznamy, Spárovaná měření, Nespárovaná měření a Celkový průměr. Za dvojtečkou budou skutečné počty, průměr zobrazený na dvě desetinná místa s čárkou a °C. U žádného spárovaného měření napište neurčen, nikoli 0 °C. Ve vzoru jsou počty 7/4/6/1.

Formát `f"{hodnota:.2f}"` zaokrouhlí pouze zobrazený text; replace(".", ",") upraví desetinný oddělovač zprávy. Výsledek zůstává původní float v tabulkách. Do zprávy přidejte, že nejde o průměr průměrů a že Cvičná data neprokazují příčinu rozdílů ani dlouhodobé počasí. Zpráva tak odliší výsledek od jeho interpretace a omezení.

## Čtyři skutečné výstupy

`vytvor_vystupy(cisteni, prehled, slozka)` vytvoří složku i rodiče přes Path.mkdir(parents=True, exist_ok=True). Vrátí slovník csv/excel/graf/zprava s Path:

- Stanice.csv (název stanice.csv): UTF-8 bez BOM, středník, desetinná čárka, souhrn podle_mist bez indexu.
- Prehled.xlsx (prehled.xlsx): listy Stanice, Dny, Nespárovaná a Odmítnutá v tomto pořadí; poslední list obsahuje původní text a důvody z cisteni, žádné řádkové indexy.
- Teploty.png (teploty.png): Figure 6 × 4 palce, 120 DPI, jedna Axes, svislé sloupce prumer podle kod. Titulek Průměrné teploty podle stanic, popisky Stanice (kód) a Teplota (°C).
- Zprava.md (zprava.md): UTF-8 text z napis_zpravu.

Jedním ExcelWriter ve with zapíšete všechny čtyři tabulky, na konci se soubor uloží a zavře. XLSX může prázdný text zobrazit jako prázdnou buňku; původní audit v DataFrame pořád obsahuje přesný text. Write_text uloží zprávu s výslovným UTF-8. Nový běh může přepsat tyto čtyři názvy, jiné soubory ani předané tabulky nemažte.

Sloupce grafu začínají na nule a musejí být vidět i záporné průměry. Nepřebírejte set_ylim(bottom=0) z grafu nezáporných počtů; zde by skryl stanici s -2 °C. Barva a písmo nejsou předepsané. Prázdný přehled má platný prázdný graf i tabulky a zprávu bez vymyšleného průměru.

## Váš úkol

Doplňte obě funkce. Spuštění ukáže PNG a nabídne CSV/XLSX i zprávu MD ke stažení. Po reloadu odkazy vzniknou znovu spuštěním zachovaného kódu. V editoru soubory zůstanou v pracovní složce. Výsledky prohlédněte: 11 vstupů musí rozdělit 4 odmítnuté + 1 nespárovaný + 6 použitých, jejich součet je důležitá kontrola toku dat, ale konkrétní skupiny ověřujte také.
