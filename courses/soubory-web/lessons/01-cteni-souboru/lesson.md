## Programy a soubory

Dosud jste data psali přímo do kódu nebo je zadával uživatel. Většina skutečných programů ale data **čte ze souborů** a výsledky do souborů **ukládá**. Tato lekce ukazuje, jak přečíst textový soubor.

Soubory lekce (`zvirata.txt`, `basen.txt`) najdete ve stejné složce jako váš program, proto stačí jen jméno souboru.

## open a with

```python
with open("zvirata.txt", encoding="utf-8") as soubor:
    text = soubor.read()
```

- `open("zvirata.txt", ...)` otevře soubor. Výsledkem je objekt, přes který se soubor čte. Říkáme mu **soubor** a v příkladu jej ukládáme do proměnné `soubor`.
- `encoding="utf-8"` říká, jak jsou v souboru uložena písmena. **UTF-8** je dnes standard a zvládá i češtinu. Parametr píšeme vždy, jinak by na některých počítačích (zejména s Windows) vznikla místo `č` nesmyslná písmena.
- `with ... as ...:` se postará o to, aby se soubor po skončení odsazeného bloku **sám zavřel**, i kdyby uvnitř nastala chyba.
- `soubor.read()` přečte celý obsah jako jeden **řetězec**.

Po bloku `with` už se soubor číst nedá. Text, který jste si uložili do proměnné `text`, ale zůstává.

## Znak nového řádku

Konec řádku v souboru je zvláštní znak `\n`. Soubor `zvirata.txt` se z Pythonu čte jako `"pes\nkocka\nkralik\nzelva\n"`. Při výpisu se `\n` projeví jako přechod na další řádek. Už znáte `text.split()`, které umí takový text rozdělit na slova.

> Cesta `"zvirata.txt"` bez složky znamená „soubor ve stejné složce, kde program běží“.

## Váš úkol

1. `nacti(nazev)` vrátí celý obsah souboru jako řetězec.
2. `pocet_znaku(nazev)` vrátí počet znaků v souboru (včetně znaků nového řádku).
3. `slov_v_souboru(nazev)` vrátí počet slov v souboru (slova oddělují mezery i nové řádky).

Funkce dostávají **jméno souboru** jako parametr. Můžete je vyzkoušet na `zvirata.txt` a `basen.txt`. Při otevření vždy uveďte `encoding="utf-8"`.
