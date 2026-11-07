## Kolikrát se co vyskytuje

Slovník se skvěle hodí na počítání. Klíčem je to, co počítáme, hodnotou počet. Postup pro každý prvek:

1. Pokud už ho ve slovníku máme, počet zvýšíme o 1.
2. Pokud ne, založíme ho s počtem 1.

```python
pocty = {}
for pismeno in "banan":
    if pismeno in pocty:
        pocty[pismeno] += 1
    else:
        pocty[pismeno] = 1
# {'b': 1, 'a': 2, 'n': 2}
```

Řetězec `"banan"` má pět znaků: jedno `b`, dvě `a` a dvě `n`.

Stejný výsledek dostaneme kratším zápisem s `get`. Pro chybějící klíč použije výchozí počet 0:

```python
pocty = {}
for pismeno in "banan":
    pocty[pismeno] = pocty.get(pismeno, 0) + 1
# {'b': 1, 'a': 2, 'n': 2}
```

## Slova z věty

Metoda `split()` rozdělí text na seznam slov podle mezer: `"to je to".split()` dá `["to", "je", "to"]`. Metoda `lower()` převede text na malá písmena, takže `Ahoj` a `ahoj` spočítáme jako stejné slovo.

## Největší hodnota

Funkce `max` umí vybírat podle libovolného pravidla. Parametr `key` říká, **čím** se mají prvky porovnávat. Pro slovník `pocty` vrátí

```python
max(pocty, key=pocty.get)    # "a"
```

klíč s největší hodnotou. Zápis `pocty.get` bez závorek znamená: předej funkci samotnou, `max` ji pak zavolá pro každý klíč a porovná výsledky. Při shodě vyhrává ten, který je ve slovníku dřív. Zde mají `a` i `n` počet 2; vyjde `a`, protože bylo vloženo dříve.

## Váš úkol

1. `pocet_slov(text)` vrátí slovník, kde klíč je slovo malými písmeny a hodnota počet jeho výskytů. Slova oddělují mezery.
2. `nejcastejsi(text)` vrátí nejčastější slovo (malými písmeny). Při shodě to, které se v textu objeví první.
