## Jak hra rozhodne, že došlo k zásahu

Obrázek a pravidlo kolize nejsou totéž. Průhledný roh kruhového meteoritu pořád patří do jeho obdélníku rect. Nejprve se naučíme přesně říct, jaké pravidlo právě používáme. Díky tomu nás nepřekvapí, že různé metody mohou pro stejné obrázky dát jiný výsledek.

## Obdélníkový průnik

```python
import pygame
a = pygame.Rect(0, 0, 20, 20)
b = pygame.Rect(20, 0, 20, 20)
print(a.colliderect(b))
b.x = 19
print(a.colliderect(b))
```

Nejprve False, pak True. Dotyk pravé a levé hrany bez společné plochy nestačí. Změna x na 19 vytvoří průnik široký jeden pixel. V ukázkách to uvidíte na dvou lodích s rect; šedý okraj přidal pomocný náhled, nezvětšuje kolizní obdélník.

## Sprite proti skupině

`pygame.sprite.spritecollide(hrac, skupina, False)` vrátí seznam skutečných kolidujících spritů. False říká, že je pouze hledáme; True by na zasažených zavolalo kill a odstranilo je ze všech skupin. Hrác nemusí být členem této skupiny. Počet výsledků může být nula, jeden i více, seznam proto není totéž jako jeden objekt.

Pro pouhou otázku „najdi nějaký zásah“ existuje spritecollideany: výstup je Sprite nebo None. Pro dvě skupiny použijeme groupcollide, který vrací slovník objekt → seznam jeho zásahů a má dva samostatné přepínače odstraňování. Tady nepředepisujeme pořadí vrstev, důležité jsou správné identity a dvojice.

## Váš úkol

`zasahy(hrac, nepratele)` vrátí seznam skutečných členů skupiny nepratele, jejichž rect má plošný průnik s rect hráče. Pouhý dotyk hran se nepočítá. Pořadí seznamu není předepsané. Nic neodstraňujte, neměňte polohy ani členství. `pygame.sprite.spritecollide(hrac, nepratele, False)` provede právě tuto kontrolu; False říká, že zásah nemá zavolat kill.

## Co změní další varianty

U seber_bonusy sečtete jejich hodnota a odstraníte pouze zasažené. Záporná hodnota může být podle pravidel hry penalizace, není automaticky chyba. U dvojice_zasahu nic neodstraňujeme, protože nejprve chceme prohlédnout celou mapu dvojic.

V posledním úkolu předáme do spritecollide callback `pygame.sprite.collide_circle`. Callback je funkce, kterou knihovna zavolá pro dvojici objektů. Zde mají všechny objekty výslovný radius a platí vzdálenost středů **≤ součet poloměrů**, takže přesný dotyk kruhů zásah je. To je jiné pravidlo než plošný průnik Rect. Poloměr nemusí být odvozený z obrázku; barevná kresba sama ho neurčuje.

Přesné masky neprůhledných pixelů přijdou později. Pro rychlé jednoduché hry může být vhodnější obdélník nebo kruh. Zvolte a vysvětlete pravidlo, podle kterého má hra skutečně fungovat. Samotná detekce také neřeší nezranitelnost: trvající kolize se může hlásit v každém kroku.
