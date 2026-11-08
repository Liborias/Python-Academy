## Sešit je soubor, list je jedna tabulka

CSV má jednu textovou tabulku. Sešit XLSX může obsahovat více listů s různým účelem a rozložením. Nejdřív zjistíme názvy a hlavičky. První list může být poznámka, nikoli správný datový zdroj. V této lekci pracujeme s přiloženým smyšleným sešitem dilna.xlsx; zdroj nepřepisujeme.

## Příprava a soubory

Pro čtení a zápis XLSX používáme openpyxl společně s pandas. Pomocník `python tools/setup_env.py --courses pandas` už obě knihovny zahrnuje do projektové .venv. Vyberte ji ve VS Code, VSCodium nebo PyCharm. Ověřte `python -c "import pandas, openpyxl; print(pandas.__version__); print(openpyxl.__version__)"`. Testováno s Pythonem 3.14.8, pandas 3.1.1 a openpyxl 3.1.5; Microsoft Excel není pro spuštění nutný.

V aplikaci se soubor přiloží k běhu. V editoru se zkopíruje vedle pracovního reseni.py přes tlačítko Otevřít ve VSCodium; v jiném editoru otevřete stejnou složku ručně. Relativní cesta hledá soubor v pracovní složce procesu, nikoli automaticky tam, kde právě prohlížíte návod. Po spuštění jsou v aplikaci odkazy ke stažení CSV/XLSX včetně přiložených vstupů; soubor můžete otevřít v tabulkovém programu a porovnat s výpisem.

## Názvy, hlavička a typy

```python
import pandas as pd
with pd.ExcelFile("dilna.xlsx", engine="openpyxl") as sesit:
    print("Listy:", sesit.sheet_names)
    cenik = pd.read_excel(sesit, sheet_name="Ceník", keep_default_na=False,
                         dtype={"kod": "str", "nazev": "str", "cena": "float64"})
print(cenik)
```

ExcelFile otevře sešit a sheet_names vrátí názvy v jeho pořadí. With jej po dokončení bloku zavře i při chybě. Read_excel přečte zadaný sheet_name, engine vybere knihovnu openpyxl. První řádek je výchozí hlavička, datové řádky dostanou RangeIndex od nuly. Dtype určí typ jednotlivých sloupců. Lze také volat přímo read_excel s cestou a engine, když potřebujeme jen jeden list.

Kód 001 je identifikátor, ne počet. Ve zdroji je opravdu uložen jako text a jako str jej ponecháme. Číslo 1 pouze zobrazené formátem 000 je stále číslo; čtení jako str z něj neobnoví ztracenou informaci o počtu nul. Takovou opravu musíme řídit známým pravidlem zdroje, nemůžeme si ji domyslet. Keep_default_na=False navíc zabrání běžnému převodu textu NA na chybějící hodnotu. Zde je NA skutečný kód či název, datové buňky nejsou prázdné.

## Vybrané sloupce a úvodní poznámka

`usecols=["kod", "nazev"]` vybírá potřebné sloupce podle hlaviček. Samotné usecols neurčuje jejich konečné pořadí, proto výslednou tabulku ještě vybereme jako `data[["kod", "nazev"]]`. V jiném sešitu mohou být mezi dalšími údaji nebo obráceně.

`skiprows=1` přeskočí první řádek a teprve potom použije zbývající první řádek jako hlavičku. V listu S poznámkou je tak první textová poznámka vynechaná a druhý řádek kod/cena správná hlavička. Není to pravidlo pro každý sešit; odpovídá konkrétnímu zdroji.

## Dva listy nemusí mít stejné schéma

Ceník má cenu float64, Prodeje kusy int64. Každý načteme se svým dtype a vložíme do slovníku cenik/prodeje. Tady je zatím nespojujeme. Dříve naučené merge lze použít až po ověření klíčů, když je to cílem otázky. Openpyxl nevypočítává excelové vzorce; naše cvičné sešity obsahují skutečné hodnoty, nikoli vzorce závislé na přepočtu.

## Váš úkol

Načtěte zadaný list XLSX se sloupci kod, nazev a cena v tomto pořadí. Kódy a názvy vraťte jako str, cenu float64; RangeIndex od nuly. Kódy jsou v sešitu skutečný text včetně úvodních nul, název NA je doslovný text. Hodnoty nechybějí, list může mít jen hlavičky. Zdroj neměňte.

Dokončete `nacti_cenik(cesta, list)`.

Další procvičování zjistí listy, vybere sloupce, přeskočí poznámku a načte dvě různá schémata. Kontrola zkouší také jiné pořadí dat, jiný název listu a list s pouhými hlavičkami. U každého úkolu lze zobrazit možné řešení; jiný správný postup je v pořádku.
