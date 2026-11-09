## Letka není seznam zkopírovaných lodí

Group uchovává členství spritů. Jeden objekt může současně patřit do skupiny všeho ke kreslení a do skupiny nepřátel pro kolize. Přidání do další Group nevytvoří další loď. Sdílíme stejný objekt, proto je jeho posun vidět přes všechny skupiny.

Pohyb.py obsahuje ověřenou PohyblivaLod z minulé lekce, ZakladSprite společný vzhled. Nyní řešíme správu více objektů; nemusíte znovu psát celý pohyb. V pracovní složce je můžete později nahradit vlastním správným řešením stejného rozhraní.

## Update a draw mají odlišnou práci

```python
import pygame
from pohyb import PohyblivaLod
lod = PohyblivaLod((100, 80), (80, 0))
skupina = pygame.sprite.Group(lod)
skupina.update(0.5)
plocha = pygame.Surface((200, 120))
plocha.fill((10, 20, 30))
skupina.draw(plocha)
print(lod.rect.center, len(skupina))
```

Po půlsekundě je střed (140, 80), člen je stále jeden. `update(0.5)` předá argument každému členovi a zavolá jeho update. Sama Group neví, co pohyb znamená. `draw(plocha)` jen vykreslí image každého člena na jeho rect; neposouvá jej a nesmaže dřívější obrázky. Ve smyčce se proto pozadí obvykle vyplní před novým kreslením.

Pro důležité pořadí vrstev později zvolíme vhodnou skupinu, například LayeredUpdates. Tady se neopíráme o obecnou záruku pořadí kreslení Group. Číselný přehled středů seřadíme výslovně, test kreslení používá nepřekrývající se objekty.

## Remove, kill a existence objektu

`skupina.remove(lod)` ukončí členství jen v jedné skupině. `lod.kill()` ukončí všechna členství. Ani kill nemusí zničit Python objekt: proměnná lod na něj stále může odkazovat. Prázdná Group je platná, update a draw na ní nemají co provádět.

Při odstraňování můžeme projít `skupina.sprites()`, což je samostatný seznam aktuálních členů. Tím je zřejmé, že pracujeme se seznamem původního průchodu. Kontrola úplného opuštění herní plochy může použít `not rect.colliderect(hranice)`: rect pouze přiložený k vnější hraně už nemá průnik.

## Váš úkol

`posun_skupinu(skupina, dt)` zavolá update(dt) právě jednou na každém členu (např. přes `skupina.update(dt)`). Vraťte **seřazený seznam dvojic rect.center**. Zachovejte členství a dt předejte beze změny. Všechny členy mají metodu update(dt), skupina může být prázdná. Sorted dovolí porovnat přehled bez závislosti na pořadí kreslení.

Další úkoly procvičí kreslení do kopie pozadí, vyřazení ze všech skupin, filtrování typu včetně potomků a sjednocení dvou skupin. U posledních dvou vznikne nové členství stejných objektů, ne jejich kopie. Dva objekty na stejné pozici jsou stále dva různé objekty a nesmějí se ztratit jen kvůli shodným souřadnicím.

V ukázce sdílené lodi se po aktualizaci jedné skupiny změna projeví i ve druhé. Pokud byste ve stejné herní smyčce aktualizovali obě skupiny, společný objekt by dostal update dvakrát. To už je otázka návrhu smyčky, nikoli chyba Group.
