## Hledání všech značek

Metoda `find` najde jen první výskyt. Na **všechny** slouží `find_all`, která vrátí seznam nalezených značek (prázdný, pokud žádná není):

```python
for polozka in soup.find_all("li"):
    print(polozka.get_text(strip=True))
```

I tady se dá omezit hledání atributy: `soup.find_all("li", class_="ovoce")` najde jen položky s třídou `ovoce`. Parametr `href=True` znamená „značky, které atribut `href` mají (hodnota je jedno jaká)“: `soup.find_all("a", href=True)`.

## Hledání uvnitř značky

`find` i `find_all` se dají volat i na **nalezené značce** a hledají jen uvnitř ní. Tak se čtou tabulky: najdete řádky `<tr>` a v každém buňky `<td>`:

```python
for radek in soup.find_all("tr"):
    bunky = radek.find_all("td")
    texty = [b.get_text(strip=True) for b in bunky]
```

Řádek s hlavičkou obsahuje místo `<td>` značky `<th>`, proto v něm `find_all("td")` vrátí prázdný seznam. Podle toho se dá poznat a přeskočit.

## Váš úkol

Funkce dostávají HTML jako **text** (soubor `obchod.html` leží vedle programu). Ve funkcích `polozky`, `odkazy` a `tabulka` použijte `find_all`; `ceny` můžete postavit na `tabulka`.

1. `polozky(html, trida=None)` vrátí seznam textů všech `<li>`. Pokud je zadána `trida`, jen těch s touto třídou.
2. `odkazy(html)` vrátí seznam dvojic `(text, adresa)` všech `<a>`, které mají atribut `href`.
3. `tabulka(html)` vrátí seznam řádků tabulky, každý řádek je seznam textů buněk `<td>`. Řádky bez buněk `<td>` (hlavička) přeskočí.
4. `ceny(html)` vrátí slovník `{zboží: cena}` z tabulky, kde cena je celé číslo.
