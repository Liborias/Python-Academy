## Kameny vznikají podle času, ne podle počtu snímků

Loď už reaguje na šipky. Přidáme proud meteoritů s různou velikostí, vodorovnou polohou a rychlostí. Predchozi.py obsahuje přesného hráče a čtení vstupu z lekce 6. Nyní doplníte třídy Meteorit a ProudMeteoritu; společná smyčka a kreslení je zapojí do stejného okna.

## Vlastní generátor náhody

```python
import random
rng = random.Random(7)
polomer = rng.randint(12, 26)
x = rng.randint(20 + polomer, 620 - polomer)
rychlost = rng.randint(90, 160)
print('Poloměr, x, rychlost:', polomer, x, rychlost)
```

Random(7) vytvoří samostatný generátor se semenem 7. Stejná posloupnost volání dostane stejná čísla, což se hodí při opakovaném tréninku a hledání chyby. Randint zahrnuje obě krajní hodnoty. Nejde o bezpečnostní náhodu ani důvod měnit globální random.seed. U hráče později můžeme zvolit jiné semeno nebo None pro jiný začátek.

Meze x závisejí na poloměru: celý kámen musí vodorovně patřit do plochy. Na výšku začne těsně nad ní — spodní hrana meteoritu se rovná horní hraně hracího Rect. Herní plochou je obdélník (20, 70, 600, 390), nikoli celé okno s informačním pruhem.

## Meteorit jako Sprite

**Meteorit(stred, polomer, rychlost)** inicializuje Sprite a má radius=polomer, image z obraz_meteoritu(polomer), vlastní rect, vlastní Vector2 pozice a číselnou rychlost dolů v px/s. Poloměr je kladné celé číslo, střed může být desetinný, rychlost nezáporná. `update(dt)` přičte rychlost × dt jen do y a odvodí rect.center přes round. X se nemění, malé pohyby se neztrácejí a původní vektor zůstává stejný.

## Časový zásobník

Proud místo vytváření „každý čtyřicátý snímek“ sčítá uplynulé sekundy. Interval je standardně 0,65 s. Pokud krok přeskočí několik intervalů, while vytvoří všechny potřebné objekty a zbytek času zůstane uložený pro další krok. Jediné if by umělo vytvořit jen jeden. V běžné smyčce je dt malé, ale model umí vysvětlit i větší krok.

## Váš úkol: ProudMeteoritu

Konstruktor **ProudMeteoritu(rng, interval=0.65)** uloží předaný generátor a interval. Nekladný interval odmítne ValueError, jinak by časová smyčka neměla správný konec. Vlastní objekty je prázdná Group, cas=0.0 a minulo=0. Žádná část nesmí být sdílená mezi dvěma proudy.

**vytvor(hranice)** provede tři randint volání v tomto pořadí: poloměr 12–26, x od left+r do right−r, rychlost 90–160. Použijte předaný rng, který toto rozhraní poskytuje. Nový Meteorit má střed (x, top−r), patří do objekty a vrátíte právě tento objekt. Hranice jsou Rect o šířce alespoň 52, jejich poloha nemusí být od nuly.

**update(dt, hranice)** nejprve aktualizuje existující objekty. Ty, které už mají rect.top >= hranice.bottom, odstraní pomocí kill a každému přičte jeden do minulo. Pak přičte dt do cas a za každý celý interval jej odečte a zavolá vytvor. Nově vytvořené kameny se v témž kroku ještě nepohnou. Zbytek cas zachovejte; hranice neměňte. Dt je nezáporné a konečné. Jednou odstraněný kámen se v dalším kroku znovu nepočítá.

Minulo zatím znamená počet kamenů, které plochu celé opustily spodem. Kolize s hráčem ještě neřešíme. Na obrázku tak mohou projít lodí; další lekce přidá životy. Zkuste pozorovat různé velikosti a rychlosti, potom okno zavřete a prohlédněte uložený snímek.
