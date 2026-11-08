## Výsledek výpočtu patří do sloupce

Vypočítáme tržbu za položku: cena krát kusy. `tabulka["cena"] * tabulka["kusy"]` vytvoří Series zarovnanou podle řádkových popisků. Přiřazení `vysledek["trzba"] = ...` vloží nový sloupec na konec tabulky. Existuje-li název, přiřazení sloupec nahradí; v prvním úkolu zaručujeme, že trzba ještě neexistuje.

V každém dnešním úkolu vracíme upravený výsledek a původní tabulku zachováváme. Proto začneme `vysledek = tabulka.copy()`. Pouhé `vysledek = tabulka` by dalo druhé jméno témuž objektu a následná změna by změnila i vstup. Copy výslovně vytvoří samostatnou tabulku pro další práci. Pracujeme se sloupci čísel a textů, nikoli s vnořenými měnitelnými Python objekty.

## Jedna buňka a jedna cílená operace

```python
vysledek = tabulka.copy()
vysledek.loc["caj", "cena"] = 48.5
```

Loc zde není jen pro čtení. Levá strana určuje průsečík popisku řádku a názvu sloupce, pravá novou hodnotu. V úkolu oba popisky existují, takže nevytváříme nový řádek ani sloupec. Hodnota musí odpovídat datovému typu: do float64 lze dát desetinné číslo, do textového sloupce text. Pandas 3 obecně nepovoluje libovolně vkládat neslučitelné typy. Dnešní úkoly nevyžadují převody typů.

Pro více řádků použijeme masku z lekce 8:

```python
vysledek = tabulka.copy()
maska = vysledek["cena"] >= 45
vysledek.loc[maska, "cena"] = vysledek.loc[maska, "cena"] - 5
```

Nejprve jednou spočítáme, které původní ceny vyhověly. Pravá strana načte jen tyto hodnoty a odečte pět. Levá je zapíše na stejná místa. Ostatní sloupce a řádky zůstanou beze změny; NaN v podmínce >= nevyhoví. Používáme float64, takže desetinný bonus nezavádí neslučitelný typ do celočíselného sloupce.

## Co znamená Copy-on-Write v pandas 3

Odvozený objekt se vůči změnám chová odděleně. Když nejprve získáme `ceny = tabulka["cena"]` a pak upravíme ceny, původní tabulka se tím neupraví. Pandas může do okamžiku zápisu sdílet vnitřní data, ale účinek změny zůstává u objektu, do kterého zapisujeme. Není potřeba tuto optimalizaci zapínat.

Proto nepoužívejte řetězené přiřazení `tabulka["cena"][maska] = 0`. První krok vybere odvozenou Series; takový zápis není správná cesta, jak změnit buňky tabulky. Může vyvolat ChainedAssignmentError upozornění a požadovanou tabulku nezmění. Cíl vyjádřete jedním `tabulka.loc[maska, "cena"] = 0`. V našich úkolech je tímto cílem samostatný vysledek.

## Seznam se řídí pozicí, Series popiskem

Při přiřazení `vysledek[sloupec] = hodnoty`, kde hodnoty je Series, pandas zarovná řádky podle indexu této Series. Její name nezmění název cílového sloupce. V posledním úkolu má Series stejné jedinečné popisky jako tabulka v jiném pořadí. Kdybychom ji převedli na seznam, přiřadili bychom hodnoty podle pozic a mohli je prohodit mezi produkty. Zachováme proto Series.

Alternativou pro nové sloupce je `tabulka.assign(trzba=...)`, která vrací novou tabulku. Pojmenovaný argument určuje název sloupce; jeho hodnotou může být vypočtená Series. Pro název dodaný v proměnné je v úkolech nejpřímočařejší přiřazení vysledek[cil]. Výpočty s float jsou přibližné; bez výslovného zadání je nezaokrouhlujeme.

## Váš úkol

Dokončete `pridej_trzbu(tabulka)`. Tabulka má jedinečné názvy sloupců, číselné sloupce cena a kusy a nemá sloupec trzba. Vraťte novou tabulku s původními sloupci v původním pořadí a na konci s trzba = cena * kusy. Typ vypočteného sloupce odvodí pandas, NaN se zachová. Index a původní tabulku neměňte; prázdná tabulka se sloupci je platná.

Potom procvičte převod ceny, jednu buňku, podmíněný bonus a přepočet podle popisků. Vytiskněte si vstup před voláním i po něm. Možné řešení ukáže jeden postup, kontrola připouští také jiný správný výsledek podle zadání.
