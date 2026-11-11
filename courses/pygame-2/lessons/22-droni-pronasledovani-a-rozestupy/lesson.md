## Stejná otázka, dva cíle

Oranžový Dron pronásleduje hráče. Fialový HlidacBodu hlídá kotvu: v jejím dosahu sleduje hráče, mimo něj se vrací domů. Oběma položíme cil(hrac), společný pohyb nemusí větvit podle typu. To je polymorfismus.

Predchozi.py poskytuje Hrac/Dron/Svet z kroku 21, připravená sestava nahradí třetího drona vaším hlídačem. Životy se ještě neodečítají, takže lze pozorovat chování bez časového tlaku.

## Nejprve stejný snímek světa

Kdyby druhý dron počítal rozestup už z nové polohy prvního, záleželo by na pořadí skupiny. Nejprve proto zkopírujeme všechny původní pozice, vypočteme nové a až potom je zapíšeme.

```python
import pygame
levy = pygame.Vector2(100, 150)
pravy = pygame.Vector2(120, 150)
rozdil = levy - pravy
delka = rozdil.length()
odpor = rozdil / delka * (42 - delka) / 42
print('Odpuzování levého:', tuple(round(v, 3) for v in odpor))
```

X je přibližně −0,524: levý objekt míří od souseda doleva. Blízký soused přispěje více, od vzdálenosti 42 px už nepřispěje. Při shodných polohách rozdíl vynecháme a nedělíme nulou. Jde o jednoduché řízení pohybu, ne přesnou fyzikální srážku.

## Váš úkol: HlidacBodu

HlidacBodu(stred, rychlost=80, dosah=160) dědí Dron s vzhled='hlidac', inicializuje rodiče a uloží vlastní kotva=Vector2(stred), dosah. Dosah je nezáporný konečný. cil(hrac) vrátí novou kopii hráčovy pozice, je-li vzdálenost hráče **od kotvy** nejvýše dosah, jinak kopii kotvy. Kotva se během letu nemění.

## Váš úkol: posun_drony

`posun_drony(drony, hrac, dt, hranice, rozestup=42)` přijímá skupinu či seznam různých dronů, pořadí zachová. Rozestup je kladný a hranice pojmou celé obrázky. Zkopírujte původní pozice. Pro každého spočtěte cestu k jeho cil(hrac), její délku a jednotkový směr, při nule nulový Vector2.

Sečtěte odpor ostatních z původních pozic. Pro rozdíl s délkou d, kde 0 < d < rozestup, přičtěte `rozdil / d * (rozestup - d) / rozestup`. Ke směru přičtěte odpor×1,6. Nenulový výsledek normalizujte a použijte krok rychlost×dt. Je-li odpor nulový, omezte krok navíc na vzdálenost cíle, aby samostatný dron nepřelétl cíl. S nenulovým odporem tento limit nepoužijeme, aby rozestup fungoval také u cíle.

Nové přesné pozice omezte na hranice s odstupem 14 px pro celý obraz 28×28. Potom je hromadně zapište a aktualizujte rect.center přes round. Dt je konečné nezáporné, rychlosti nezáporné. Neměňte hráče, kotvy, vstupní Rect ani členství. Prázdná skupina je platná. Vyzkoušejte cíl přímo v dronovi, blízkou dvojici, shodné pozice a odlet hráče z dosahu strážce.
