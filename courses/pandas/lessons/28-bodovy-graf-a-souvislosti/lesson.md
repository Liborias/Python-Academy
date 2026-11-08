## Jeden bod je jedna dvojice

Bodový graf scatter ukazuje dvě veličiny z téhož pozorování: třeba dobu procvičování a body v kvízu. Obě hodnoty musí patřit stejnému řádku. Nejde o dvě nezávisle seřazené řady. Bodový graf body standardně nespojuje; pořadí řádků tedy nevytváří čáru podobnou časovému průběhu.

```python
from matplotlib.figure import Figure
fig = Figure(layout="constrained")
ax = fig.subplots()
ax.scatter([1, 2, 3, 4], [5, 9, 7, 12])
ax.set(title="Cvičná měření", xlabel="Doba učení (h)", ylabel="Body v kvízu")
fig.savefig("graf.png", dpi=120)
```

X/y jsou stejně dlouhé seznamy známých konečných čísel. V našich grafických úkolech je tento předpoklad daný; přípravu neúplných tabulek procvičíme zvlášť. Každé i-té x zůstává s i-tým y, i kdyby se x opakovalo nebo body neležely na rostoucí křivce.

## Nepřeskládat dvojice při čištění

`tabulka[["x", "y"]].dropna()` nejprve vybere obě potřebné veličiny a pak odstraní jejich neúplné řádky. Zachová zdrojový index a pořadí. Samostatné dropna nad každým sloupcem by mohlo spárovat hodnoty z různých pozorování. Dropna nad celou původní tabulkou by naopak mohlo zbytečně vyhodit řádek kvůli nepoužité poznámce. Nulu zachováme, protože je to hodnota, ne chybějící údaj.

## Bodový vzor neprokazuje příčinu

V cvičných datech mohou vyšší x doprovázet vyšší y. Z toho samotného neplyne, že zásah do x změní y. Obě veličiny může ovlivňovat další faktor, například předchozí znalosti, nebo je výběr záznamů zkreslený. Malý vzorek ani výrazný bod neopravňují ke slibu výsledku. O vysoké hodnotě nejdřív zjistíme původ, nezahodíme ji automaticky jako chybu.

V této lekci nepočítáme korelační koeficient ani netvrdíme účinek skutečného vzdělávacího postupu. Učíme se správně vykreslit dvojice a pojmenovat omezení toho, co obrázek ukazuje. Značky se také mohou překrývat: dva stejné body mohou vypadat jako jeden.

## Porovnat skupiny a měřítko

Dvě volání scatter do stejné Axes vytvoří dvě skupiny značek. Label a legenda vysvětlí skupinu A/B, marker="o" a marker="^" rozliší tvar. Skupiny nepropojujeme čarou jen podle pořadí řádků. Jejich souřadnice zůstávají ve stejných jednotkách.

Když x/y vyjadřují stejnou fyzikální jednotku, například metry na mapě, `ax.set_aspect("equal", adjustable="box")` nastaví stejnou fyzickou délku jedné jednotky na obou osách. Adjustable="box" upraví tvar kreslicí oblasti, ne data. Pomocí set_xlim a set_ylim přidáme stejné zadané meze. Samotný stejně široký a vysoký obrázek stejné měřítko nezaručuje, pokud se liší číselné rozsahy. U hodin a bodů v kvízu naopak stejná fyzická jednotka neexistuje; equal proto není univerzální pravidlo.

## Třetí veličina pomocí plochy značky

`ax.scatter(x, y, s=velikosti)` dovolí měnit velikost bodů. Parametr s označuje plochu značky v typografických bodech na druhou, nikoli poloměr. Velikost 100 proto neznamená čtyřnásobný poloměr oproti 25. V úkolu použijete předané kladné velikosti přímo; v opravdové zprávě musíte čtenáři vysvětlit, jaké veličině a jaké stupnici odpovídají. Obrázek bez takového klíče by se špatně četl.

## Váš úkol

Vraťte Figure s jednou Axes a jednou skupinou bodů scatter, bez spojovacích čar. Seznamy x/y jsou stejně dlouhé a obsahují konečná čísla; prázdné jsou platné. Zachovejte dvojice i pořadí, neměňte vstupy. Titulek Cvičná měření, popisky Doba učení (h) a Body v kvízu.

Dokončete `bodovy_graf(x, y)`.

Další úkoly procvičí úplné dvojice, dvě skupiny, stejné měřítko a velikost bodů. Kontrola ověří souřadnice, počet skupin, názvy a případné velikosti, nikoli dekorativní styl. Funkce vrací Figure, ukládání a náhled obstará zkušební volání; datový úkol vrací očištěnou tabulku.
