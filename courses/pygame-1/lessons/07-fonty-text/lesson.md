## Text je také obrázek

Pygame nekreslí text přímo. Text nejdřív **vyrobí jako obrázek** a ten pak vykreslí jako každý jiný:

```python
font = pygame.font.Font(None, 48)                      # 1. písmo (None = výchozí), velikost 48
text = font.render("Skóre: 0", True, (255, 255, 255))  # 2. vyrobí obrázek s textem
screen.blit(text, (10, 10))                            # 3. vykreslí ho
```

- `Font(None, velikost)` načte výchozí písmo pygame (umí i češtinu). Vlastní soubor písma `.ttf` lze zadat místo `None`.
- `font.render(text, vyhlazení, barva)`: `True` zapne vyhlazené hrany (vypadá lépe).
- Písmo vytvořte **jednou před smyčkou**. Vytvoření písma je pomalé.

## Umístění textu

Obrázek textu má `get_rect()` jako každý jiný, takže jde umístit podle středu nebo rohu:

```python
rect = text.get_rect(center=(200, 50))     # nadpis uprostřed nahoře
screen.blit(text, rect)
```

## Měnící se text (skóre)

Text je obrázek vyrobený pro konkrétní řetězec. Když se skóre změní, text se musí **vyrobit znovu**. Dělá se to ve smyčce těsně před vykreslením:

```python
skore = 5
text = font.render(f"Skóre: {skore}", True, (255, 255, 255))
```

f-řetězec dosadí číslo do textu.

## Váš úkol

V okně **400 × 200** s pozadím `(0, 0, 40)` zobrazte:

1. nadpis **Sběratel hvězd** žlutou barvou `(255, 220, 0)`, písmo velikosti 48, **vystředěný** vodorovně se středem v bodě `(200, 50)`,
2. text **Skóre: 0** bílou barvou, písmo velikosti 32, jehož levý dolní roh je v bodě `(10, 190)`.

Použijte proměnnou `skore = 0` a text sestavte f-řetězcem.