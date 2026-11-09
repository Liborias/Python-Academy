## Co se ve hře skutečně dotklo

Obdélník je rychlý test. Kruh dobře vystihne kulatou loď, ale ne otvor uprostřed obrázku. Maska si pro každý lokální pixel pamatuje jeden bit: patří do pevné části, nebo ne. Není automaticky lepší pro každou hru — stojí čas a paměť, zatímco jednoduché tvary mohou být čitelnější a herně příjemnější.

Pokusy porovnávají skutečné obrazy a binární masky v PNG. Stále stačí prostředí z lekce 16, displej ani zvuk se neotevírá. Obrázky jsou vlastní kresby; žádné soubory z internetu se nenačítají.

## Průhlednost má přesné pravidlo

U Surface s alfa kanálem `pygame.mask.from_surface(obraz, prah)` nastaví bit, pokud alfa pixelu je **větší** než práh. U RGB obrázku s nastaveným colorkey se používá barevný klíč: jeho barva je prázdná, ostatní pevné. Nespoléhejte na kombinaci obou způsobů jako na dvě nezávislé podmínky.

```python
import pygame
obraz = pygame.Surface((3, 2), pygame.SRCALPHA)
obraz.fill((80, 180, 255, 100))
print('Práh 127:', pygame.mask.from_surface(obraz, 127).count())
print('Práh 50:', pygame.mask.from_surface(obraz, 50).count())
```

Výsledek je 0 a 6 pevných pixelů. Stejný viditelný poloprůhledný obrázek má jiné kolizní pravidlo podle zvoleného prahu. Maska má rozměry obrázku, nikoli světové souřadnice.

## Dvě lokální masky ve stejném světě

Mask.overlap potřebuje posun počátku druhé masky vůči první: druhý rect minus první rect. Při opačném znaménku může test hlásit zásah na nesprávné straně. Záporný posun je běžný. Vrácený bod je lokální bod průniku, None značí žádný průnik; neposouvejte podle něj automaticky celý svět.

Na přesun stejného obrazu stačí změnit rect. Po otočení, změně snímku nebo rozměru obrazu však obnovte masku a rozměr rect. Jinak se hráč srazí s pixely, které už nejsou vidět. Prah by měl být pro daný typ kolize zvolený vědomě.

## Nejprve vyberte potřebnou přesnost

Levný test Rect může před dražší maskou mnoho kandidátů vyřadit. Nezaměňujte jej ale za konečný výsledek. Pouhý dotyk hran Rect je False, kruh v našem modelu počítá přesný dotyk a maska vyžaduje společný pevný pixel. V posledním úkolu budou všechny tři výsledky vedle sebe, ne tři různá pojmenování téhož if.

Připravený Bod slouží jen jako vstup pokusů. V úkolech 4/5 masky.py poskytuje ověřenou zasah_maskou z Úkolu 2. Skupiny zůstávají během detekce nedotčené; o odstranění nebo ubrání života rozhodne až pravidlo hry.

## Váš úkol: Sprite s vlastní maskou

Vytvořte `MaskovySprite(obraz, roh, prah=127)` jako Sprite. Má vlastní kopii image, rect s levým horním rohem na celočíselném roh a skutečnou mask z `pygame.mask.from_surface(image, prah)`. Prah je celé číslo 0..255. Alfa musí být větší než práh; u RGB obrázku s colorkey se rozhoduje podle barevného klíče. Neměňte zdrojový Surface a nesdílejte měnitelné obrázky mezi instancemi.

Maska je uložená mapa pevných pixelů. Nevzniká automaticky pokaždé, když později změníte image; tuto obnovu procvičí Úkol 3.

Další čtyři zadání přepnete tlačítky Úkol 2–5. U každého najdete vlastní možné řešení; jeho odkrytí nemění rozepsaný kód ani splnění.
