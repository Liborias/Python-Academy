## Program se ptá

Funkce `input()` zastaví program, zobrazí otázku a počká, až uživatel napíše odpověď a stiskne Enter. Odpověď vrátí jako **text**.

```python
jmeno = input("Jak se jmenuješ? ")
print("Ahoj", jmeno)
```

## Převod na číslo

I když uživatel napíše `15`, `input()` vrátí text `"15"`. Počítat s ním nejde, dokud ho nepřevedete:

- `int("15")` převede na celé číslo
- `float("3.5")` převede na desetinné číslo

```python
vek = int(input("Kolik je ti let? "))
```

Pozor na `+`: mezi dvěma **čísly** je sečte, mezi dvěma **texty** je spojí. Proto `"5" + "5"` je `"55"`, ale `5 + 5` je `10`.

> Napíše-li uživatel místo čísla slovo, `int()` skončí chybou `ValueError`. Ošetření chyb se naučíte později.

## Váš úkol

Zeptejte se na věk (celé číslo) a vypište například `Za rok ti bude 16.`, když uživatel zadá 15.
