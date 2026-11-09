## Proč uložit přesnější polohu než jeden pixel

Rect používá celé pixely. Loď rychlostí 1 pixel za sekundu se za setinu sekundy posune jen o 0,01. Kdybychom každý drobný krok hned převáděli na celé číslo a ukládali jen do rect, mohla by stát navždy. Uchováme proto pozici jako Vector2 a rect z ní jen odvodíme pro kreslení a obdélníkové kolize.

Přiložený ZakladSprite už připravuje image 32 × 24 a rect podle středu. Nemá vlastní pohyb. Vaše třída jej zdědí přes `super().__init__(stred)` a doplní nové atributy a metodu update. Dědění použijeme pro společné rozhraní Sprite, nikoli jako důvod vytvořit hluboký strom téměř stejných tříd.

## Vektor a jednotky

```python
import pygame
pozice = pygame.Vector2(100, 80)
rychlost = pygame.Vector2(80, -20)
dt = 0.25
pozice += rychlost * dt
print(tuple(pozice))
print((round(pozice.x), round(pozice.y)))
```

Oba výpisy odpovídají poloze (120, 75). Rychlost je v pixelech za sekundu, dt v sekundách, součin je posun v pixelech. Záporné y znamená pohyb nahoru. Vector2 umí sčítání a násobení číslem po složkách; číslo 0,25 se zapíše v Pythonu s tečkou jako 0.25.

Ve skutečné smyčce získáme dt přes `clock.tick(60) / 1000`: tick vrací milisekundy a současně omezuje frekvenci. Teď předáváme čas ručně, takže jde snadno porovnat jeden krok sekundy se čtyřmi kroky po čtvrt sekundě. Při konstantní rychlosti dostaneme stejnou pozici s běžnou tolerancí float.

## Image a rect se pohybují přes stejný střed

`self.pozice = pygame.Vector2(stred)` vytvoří vlastní vektor, i když už byl vstup Vector2. Totéž platí pro rychlost. Prosté přiřazení by mohlo sdílet měnitelný vstup s volajícím. Po aktualizaci nastavíme rect.center na dvojici zaokrouhlených složek. `round` u přesné poloviny vybírá nejbližší sudé celé číslo; vlastní float pozici přitom nezaokrouhlujeme.

Ukázka malých kroků přičte stokrát 0,01 a výsledný rect se opravdu posune o pixel. Číselný výpis float může ukázat drobnou odchylku za poslední desetinnou číslicí. To není důvod ukládat po každém kroku zaokrouhlenou polohu. Pro porovnání reálných výpočtů používáme toleranci.

## Váš úkol

Doplňte `PohyblivaLod(stred, rychlost)` odvozenou od přiloženého `ZakladSprite`. Vlastní Vector2 `pozice` a `rychlost` kopírují obě předané dvojice/vektory. `update(dt)` přičte rychlost × dt k desetinné pozici a nastaví rect.center na `(round(pozice.x), round(pozice.y))`. dt je nezáporný počet sekund, rychlosti mohou být záporné i nulové. Vstupní vektory ani jiné instance neměňte, nezaokrouhlujte pozici samotnou.

## Další procvičení

RizenaLod nejprve normalizuje nenulový směr, jinak by diagonální vstup byl rychlejší. OmezenaLod ořízne desetinný střed podle rozměrů celé lodě. ZrychlujiciLod nejprve změní rychlost, potom polohu; je to kroková aproximace, u níž počet kroků může výsledek změnit. CilovaLod doletí k cíli a nepřeletí jej. Každé tlačítko popisuje vlastní pravidlo před použitím nových metod.

Náhled zobrazuje poslední stav po všech krocích. Skutečný pohyb v čase uvidíme v herní smyčce dalšího modulu. Přepínání příkladů a úkolů zachová oddělené rozpracované kódy, možné řešení slouží k porovnání.
