## Složíme celou scénu

Spojíte vše, co umíte: pozadí, tvary, obrázky, polohu přes `Rect` a text. Výsledkem bude „pohlednice z kosmu“. Zatím nic nehýbe, to přijde v další lekci.

## Seznam poloh

Stejný obrázek se vykresluje víckrát, ale polohy nebudete psát za sebou. Uložte je do **seznamu** a projděte cyklem `for`:

```python
HVEZDY = [(50, 60), (120, 100), (300, 70)]
for pozice in HVEZDY:
    screen.blit(hvezda, pozice)
```

Přidání další hvězdy je pak jedna položka v seznamu.

## Váš úkol

Okno **400 × 300**, titulek **Pohlednice**, pozadí `(10, 10, 40)`. Nakreslete:

1. pět **hvězd** `hvezda.png` v levých horních rozích: `HVEZDY = [(50, 60), (120, 100), (300, 70), (350, 150), (80, 200)]` (seznam, který projdete cyklem `for`),
2. **planetu**: červený kruh `(200, 60, 60)` se středem `(330, 230)` a poloměrem 40,
3. **raketu** `raketa.png` se středem v bodě `(200, 180)`,
4. **nadpis** **Pozdrav z kosmu** bílou barvou, písmo velikosti 40, vystředěný se středem v bodě `(200, 25)`.

Obrázky načtěte jednou před smyčkou. Celou scénu kreslete znovu v každém průchodu smyčkou.