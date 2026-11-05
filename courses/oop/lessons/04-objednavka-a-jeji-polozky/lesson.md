## Objednávka je složená z položek

Jedna objednávka může obsahovat knihu, obal i další výrobek. Každá položka už umí počítat svou cenu. Objednávka proto bude tyto objekty uchovávat a jejich výsledky sčítat. Tomuto uspořádání říkáme **skládání objektů**: objednávka má položky a spolupracuje s nimi.

Soubor polozka.py obsahuje vzorové řešení předchozí lekce. `from polozka import Polozka` načte třídu z vedlejšího souboru. Hlavní blok tohoto modulu se při importu nespustí, takže nevzniknou další ukázkové položky ani výpisy. V aplikaci i pracovní složce editoru dostanete pomocný soubor připravený; vaše rozepsané řešení předchozího úkolu zůstává samostatné.

## Dva názvy nemusí znamenat dva objekty

```python
kniha = Polozka("Průvodce Pythonem", 250)
dalsi_odkaz = kniha
dalsi_odkaz.pridej()
print(kniha.pocet)                 # 2
print(dalsi_odkaz is kniha)        # True
```

Přiřazení dalsi_odkaz = kniha nevytváří další položku. Obě proměnné odkazují na tentýž objekt. Operátor is se ptá právě na tuto identitu. Nová položka naopak vznikne dalším voláním Polozka(...).

Seznam uchovává také odkazy. Když přidáme knihu do objednávky a později přes stejný objekt přidáme kus, součet objednávky se má přizpůsobit. Nechceme si při přidání uložit jen staré číslo nebo vytvořit neviditelnou kopii položky.

## Každá objednávka potřebuje svůj seznam

```python
def __init__(self, cislo):
    self.cislo = cislo
    self.polozky = []
```

Prázdný seznam vzniká při každém vytvoření objednávky znovu. Kdyby byl jediný seznam společný na třídě nebo mimo konstruktor, přidání do jedné objednávky by mohlo změnit i druhou. Stejná jména atributů na různých instancích mají označovat jejich vlastní kolekce.

Metoda pridej uloží předanou položku na konec a vrátí nový počet **řádků objednávky**. To není totéž co počet kusů uvnitř jednotlivých položek. Dvě položky po třech kusech jsou stále dva řádky.

## Každý objekt má svou odpovědnost

Celkem projde položky a od každé zavolá její metodu celkem. Objednávka tak nemusí opisovat vnitřní výpočet položky. Při budoucí změně jejího způsobu počítání se využije nový výsledek.

Začneme součtem nula a v běžném cyklu k němu přidáváme vrácené ceny. Prázdná objednávka stojí nula. Samotné čtení nesmí měnit řádky ani množství položek a musí fungovat po každé pozdější změně.

## Kopie přehledu je kopie seznamu

```python
kopie = list(self.polozky)
```

Nový seznam obsahuje odkazy na **stejné položky**. Vymazání nebo přidání řádku v tomto přehledu tedy nezmění členství původní objednávky. Pokud ale upravíme samotnou položku z přehledu, pracujeme dál se stejným objektem a změna se projeví i v objednávce.

Jde o mělkou kopii, nikoli automatické kopírování celého grafu objektů. V této lekci je to záměr: chceme samostatný seznam pro přehled a společné aktuální položky. Zapouzdření a další ochranu stavu přidáme v dalším bloku.

## Váš úkol

Doplňte `Objednavka(cislo)` a její metody:

1. Konstruktor uloží cislo a vytvoří vlastní seznam polozky.
2. Pridej(polozka) přidá přesně předaný objekt a vrátí počet řádků. Pořadí i opakované přidání téže položky zachovejte; v této jednoduché verzi každý vstup znamená další řádek.
3. Celkem vrátí součet výsledků celkem všech právě uložených položek. Čte jejich aktuální stav a nic nemění.
4. Prehled vrátí nový seznam se stejnými objekty ve stejném pořadí.

Ukázka nejprve spočítá knihu za 250 a dva obaly po 30, tedy 310 Kč. Po přidání knihy vrátí 560 Kč. Potom odebere řádek z kopie přehledu: původní objednávka má stále dva řádky a druhá objednávka zůstává prázdná.

První blok kurzu tím zakončuje malá použitelná objednávka. V dalších lekcích se zaměříme na pravidla stavu, sklad a odmítání chybných operací.
