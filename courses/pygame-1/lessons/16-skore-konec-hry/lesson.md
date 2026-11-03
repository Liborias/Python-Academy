## Stav hry

Hra má obvykle několik **stavů**: běží hra, je pauza, je konec hry. Stav se uloží do proměnné a smyčka se podle něj chová:

```python
stav = "hra"                         # na začátku se hraje

if stav == "hra":
    ...                              # pohyb, kolize, kreslení hry
else:                                # stav == "konec"
    ...                              # obrazovka „Konec hry“
```

Stav se mění při nějaké události: dojdou životy, nasbírá se dost bodů, hráč stiskne klávesu.

```python
if skore >= 5:
    stav = "konec"
```

## Události podle stavu

Stejná klávesa může dělat různé věci podle stavu. Podmínka na stav patří do `if` u události:

```python
if udalost.type == pygame.KEYDOWN and udalost.key == pygame.K_SPACE and stav == "hra":
    skore += 1
```

Po konci hry mezerník nic nedělá, protože `stav == "hra"` už neplatí.

## Skóre a text

Skóre je obyčejná proměnná: `skore = 0`, přičtení `skore += 1`. Pro zobrazení se text **vyrábí znovu** v každém snímku z f-řetězce: `font.render(f"Skóre: {skore}", True, (255, 255, 255))`.

## Restart

Restart znamená vrátit všechny proměnné na počáteční hodnoty (zde `skore = 0` a `stav = "hra"`). U velké hry se k tomu hodí funkce, ale zatím stačí tyto řádky v obsluze klávesy `R`.

## Váš úkol

Podle poznámek v kostře naprogramujte hru „klikátko“: mezerníkem sbíráte body do pěti, pak je konec a klávesou **R** hrajete znovu.

Okno **400 × 300**, titulek **Konec hry**, dva fonty: `pygame.font.Font(None, 32)` a `pygame.font.Font(None, 64)`. Stav hry držte v proměnné `stav` s hodnotami `"hra"` a `"konec"`.

- **Stav `"hra"`:** pozadí `(0, 0, 30)`, vlevo nahoře bílý text `Skóre: N` (písmo 32, levý horní roh v bodě `(10, 10)`). Každý stisk mezerníku zvýší skóre o 1. Při skóre 5 se stav změní na `"konec"`. Klávesa **R** v průběhu hry nic nedělá.
- **Stav `"konec"`:** pozadí `(60, 0, 0)`, žlutý `(255, 220, 0)` text `Konec hry` (písmo 64, střed v bodě `(200, 110)`), bílý text `Skóre: 5` (písmo 32, střed `(200, 170)`) a bílý text `Stiskni R` (písmo 32, střed `(200, 220)`). Mezerník už nic nedělá. Klávesa **R** vynuluje skóre a vrátí stav `"hra"`.