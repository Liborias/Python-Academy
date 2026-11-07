## Jeden nákup, několik odpovědností

Začínáme závěrečný projekt. Objednávka zná zboží a jeho cenu, sklad dostupné kusy, balík svou hmotnost a doprava podmínky přepravy. Konzole bude přijímat příkazy. Jedna třída nemusí dělat všechno.

```text
NakupniObjednavka obsahuje Objednavka a její Polozka
RezervacniSklad přiřadí rezervované kusy číslu objednávky
ExpedicniCentrum propojí objednávku, Expedice a štítek s adresou
Konzole převede vstup a zavolá veřejné metody
```

Tento krok vytvoří NakupniObjednavka. Původní Objednavka z lekce 4 přijímá hotové položky. Pro projekt navíc potřebujeme skladové kódy, ověřené počty a možnost uzavřít úpravy. Starší rozhraní neměníme: nová třída si původní objednávku uloží jako spolupracující objekt a využije její pridej a celkem. Potřebné objednavka.py a polozka.py jsou přiložené, nic se neinstaluje.

## Řádky nákupu a požadavek na sklad

Konstruktor NakupniObjednavka(cislo) přijímá neprázdný text obsahující i něco jiného než mezery. Původní text uchová. Property cislo a uzavrena jsou pouze pro čtení. Nová objednávka je otevřená, tedy uzavrena je False.

pridej(kod, nazev, cena, pocet=1) přidá nový řádek přes Polozka a původní Objednavka.pridej. Kód a název musejí být neprázdné texty, cena nezáporný int a počet kladný int; bool se nepřijímá. Při chybě se nezmění cena ani požadavek. Vstupy neořezáváme. Kódy a čísla objednávek rozlišují velikost písmen.

Metoda vrací počet řádků objednávky, nikoli součet kusů. Dva řádky téhož zboží jsou dva řádky, ale požadavek skladu sečte jejich množství pod jeden kód:

```python
self._pozadavek[kod] = self._pozadavek.get(kod, 0) + pocet
```

get(kod, 0) přečte dosavadní počet, nebo nulu, pokud kód ještě není uložený. Přičteme nové kusy a uložíme součet. Názvy a ceny řádků poskytuje v závěrečné konzoli připravený ceník; skladové kódy určují, které zásoby rezervujeme.

## Kopie chrání plán rezervace

celkem() vrátí součet z původní objednávky. pozadavek() vrátí nový slovník kódů a počtů. Úprava vráceného slovníku nesmí přepsat objednávku. Vnitřní položky ven nevydáváme, takže se přes veřejné rozhraní nedají po uzavření měnit jejich počty.

uzavri() dovolí uzavřít jen otevřenou neprázdnou objednávku. Nastaví uzavrena na True a vrátí None. Další přidání, druhé uzavření i uzavření prázdné objednávky vyvolají ValueError beze změny. Uzavření zde znamená konec úprav řádků; stav rezervace a storno přidá další lekce. Po stornu se tato objednávka znovu neotevírá.

## Váš úkol

Doplňte pridej, celkem, pozadavek a uzavri podle uvedeného rozhraní. Používejte veřejné metody vnitřní Objednavka, ne její interní výpočet. Metody nic nevypisují a každá instance má vlastní data. Podtržítka vyjadřují dohodu používat veřejné rozhraní, nikoli technickou ochranu před úmyslným přepisováním vnitřností.

Ukázka vytvoří tři knihy a jeden obal za 780 Kč. Změna kopie požadavku ani odmítnuté přidání po uzavření původní počty neovlivní. Vytvořte druhou objednávku a vysvětlete, které objekty patří které z nich.
