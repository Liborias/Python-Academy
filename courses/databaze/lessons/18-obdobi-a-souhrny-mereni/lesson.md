## Období má dvě volitelné meze

Základní model je beze změny v `model.py`. Nový Tracker ho rozšíří o přehled a souhrn. Parametry od/do mohou být None, tedy bez meze. Neprázdné datum musí mít přesný ISO tvar a obě meze jsou včetně. Začátek po konci je chyba, nikoli tichý prázdný výpis.

```python
# Obě hranice jsou součástí zvoleného období.
dny = ['2026-04-01', '2026-04-05', '2026-04-30']
print([den for den in dny if '2026-04-05' <= den <= '2026-04-30'])
```

Výsledek obsahuje 5. a 30. duben. Pro SQL sestavíme podmínky jen z pevných částí `den >= ?` a `den <= ?`. Uživatelská data zůstanou v seznamu parametrů; žádné datum nevkládáme do textu příkazu. To je rozdíl mezi výběrem struktury dotazu a vkládáním hodnot.

## Co přesně znamená souhrn

Průměr jednotlivých BMI není obecně stejný jako BMI z průměrné hmotnosti a průměrné výšky. U každého řádku nejprve spočítáme jeho vlastní hodnotu. Změna kg je poslední minus první měření podle data,id; vyjadřuje rozdíl záznamů, nikoli zdravotní hodnocení. U jediného záznamu je rozdíl 0.

Počet záznamů není počet dnů. Dvě měření stejného dne jsou dvě pozorování, při shodě data rozhoduje id. Prázdné období je platné: počet 0, ostatní souhrnné hodnoty None. Nula by pro chybějící průměr či rozdíl vyjadřovala jinou informaci.

## Váš úkol

Doplňte **prehled(od=None, do=None)** a **souhrn(od=None, do=None)** v odvozeném Tracker. Přehled validuje meze, případně odmítne obrácené období ValueError „Začátek období nesmí být po konci.“ Provede parametrizovaný SELECT a vrátí [(id, datum, kg, cm, BMI, poznámka)] v pořadí datum,id. BMI vypočítá pomocí dřívější funkce bez zaokrouhlení.

Souhrn používá stejný výběr a vrátí slovník s klíči pocet, prvni_den, posledni_den, prumer_bmi a zmena_kg. První/poslední den je text data z krajních řádků. Průměr lze spočítat statistics.mean nebo jiným správným aritmetickým průměrem; knihovní mean zvládá i velmi velká konečná čísla bez přetečení mezisoučtu. Rozdíl kg je poslední hmotnost minus první. Pro prázdný výběr vraťte 0 a čtyři None. Výsledek se nesmí lišit podle předchozího filtru ani měnit uložené řádky.

Procvičte celý přehled, jediný den, jen spodní/jen horní mez, prázdné období a chybná data. Při výpisu můžete použít dvě desetinná místa, uvnitř modelu zůstanou původní hodnoty.
