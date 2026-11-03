## Režimy otevření

Funkce `open` má druhý parametr, **režim**:

| Režim | Význam |
|---|---|
| `"r"` | čtení (výchozí, když parametr neuvedete) |
| `"w"` | zápis: soubor se vytvoří, **pokud existuje, jeho obsah se smaže** |
| `"a"` | přidávání na konec souboru, nic se nemaže |

```python
with open("vysledky.txt", "w", encoding="utf-8") as soubor:
    soubor.write("první řádek\n")
    soubor.write("druhý řádek\n")
```

Metoda `write` zapisuje přesně to, co jí dáte, a **nepřidává nový řádek**. Konec řádku `\n` musíte připsat sami. Zapisovat se dá jen text, čísla je nutné nejprve převést funkcí `str()`.

Pozor na režim `"w"`: otevřít jím existující soubor znamená přijít o jeho obsah, i když do něj nic nezapíšete. Na doplňování používejte `"a"`.

## Zápis pomocí print

Totéž umí `print` s parametrem `file`, který navíc sám připojí nový řádek:

```python
print("třetí řádek", file=soubor)
```

## Kde soubor vznikne

Soubor se vytvoří ve stejné složce, kde program běží. Při práci ve VSCodium je to složka vašeho řešení.

## Váš úkol

1. `uloz_radky(nazev, radky)` zapíše seznam textů do souboru, **každý na vlastní řádek**; každý řádek včetně posledního končí znakem `\n`. Případný starý obsah souboru se přepíše.
2. `pridej_radek(nazev, text)` přidá na konec souboru jeden řádek s textem. Starý obsah zůstane.
3. `zkopiruj(zdroj, cil)` zkopíruje obsah souboru `zdroj` do souboru `cil` (přečte a zapíše). Funkce nic nevrací.

Soubory otevírejte vždy s `encoding="utf-8"`.
