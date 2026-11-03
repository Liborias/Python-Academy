## Obrázek na obrazovku

Hry se skládají z obrázků (**spritů**). Postup je vždy stejný:

```python
raketa = pygame.image.load("raketa.png").convert_alpha()    # 1. načtení (jednou, PŘED smyčkou)
...
screen.blit(raketa, (100, 80))                              # 2. vykreslení (v každém průchodu smyčkou)
```

- `pygame.image.load("soubor.png")` načte obrázek ze souboru. Dělá se **jednou před smyčkou**, protože čtení souboru je pomalé.
- `.convert_alpha()` obrázek přizpůsobí obrazovce, zrychlí kreslení a zachová **průhledná** místa (PNG je může mít). Obyčejné `.convert()` by průhlednost zahodilo. Voláme ho až po `set_mode`.
- `screen.blit(obrazek, (x, y))` ho vykreslí tak, že jeho **levý horní roh** je v bodě `(x, y)`. (Slovo *blit* zkracuje „block transfer“, přenos bloku bodů.)

Soubor s obrázkem musí ležet ve složce programu. U této lekce jsou obrázky už připravené.

## Rozměr a poloha: Rect

Z obrázku získáte jeho obdélník: `rect = raketa.get_rect()`. Má šířku a výšku obrázku a **polohu**, kterou lze nastavit různými způsoby:

```python
rect = raketa.get_rect(center=(200, 150))      # střed obrázku v bodě (200, 150)
rect.topleft = (10, 10)                        # nebo levý horní roh
print(rect.width, rect.height)                 # 64 64
screen.blit(raketa, rect)                      # blit umí vzít přímo Rect
```

Rect umí i `rect.center`, `rect.top`, `rect.bottom`, `rect.left`, `rect.right`. Využijeme je při pohybu a kolizích.

## Průhlednost

Hvězda `hvezda.png` je čtverec 32 × 32, ale hvězda nevyplňuje rohy. Díky `convert_alpha()` jsou rohy průhledné a vidíte pozadí. Kdybyste obrázek přizpůsobili obyčejným `.convert()`, průhlednost by se ztratila a rohy by zčernaly.

## Váš úkol

Na tmavě modrém pozadí `(20, 20, 60)` v okně **400 × 300** vykreslete **raketu** se středem v bodě `(200, 150)` a **hvězdu** s levým horním rohem v bodě `(50, 50)`. Oba obrázky načtěte jednou před smyčkou.