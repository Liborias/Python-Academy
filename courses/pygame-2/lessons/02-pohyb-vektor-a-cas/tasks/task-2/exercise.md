### Stejná rychlost i diagonálně

`RizenaLod(stred, rychlost)` dědí ZakladSprite, kopíruje pozici do Vector2 a uloží nezápornou číselnou rychlost. `update(smer, dt)` posune loď o **rychlost × dt ve směru jednotkového vektoru smer**. Nulový směr znamená stát. Vstupní směr může být Vector2; neměňte jej. `length_squared()` zjistí nulový vektor bez odmocniny; nenulový `normalize()` vrátí nový vektor délky 1. Bez normalizace by diagonála byla rychlejší. Rect zaokrouhlujte stejně jako v Úkolu 1.
