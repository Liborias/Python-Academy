## Spojení znalostí

Tato lekce nepřináší téměř nic nového. Úkoly zkoušejí, jestli umíte spojit podmínky, cykly, seznamy a texty. Pokud něco nevíte, vraťte se do lekce, kde se to vysvětlovalo. Není to selhání, stejně to dělají všichni programátoři.

## Jediná novinka: str

Funkce `str()` převede číslo na text, takže přes něj půjde procházet po znacích. Opak `int()` už znáte:

```python
str(472)           # "472"
int("4")           # 4
for znak in str(472):
    print(znak)    # 4, 7, 2
```

## Váš úkol

1. `fizzbuzz(n)` vrátí seznam textů pro čísla od 1 do `n`: pro násobky 3 text `"Fizz"`, pro násobky 5 text `"Buzz"`, pro násobky obou `"FizzBuzz"`, jinak samotné číslo jako text. `fizzbuzz(5)` je `["1", "2", "Fizz", "4", "Buzz"]`.
2. `je_prvocislo(n)` vrátí `True`, pokud je `n` prvočíslo (celé číslo větší než 1 dělitelné jen jedničkou a sebou samým). Čísla menší než 2 prvočísly nejsou.
3. `obrat_slova(veta)` vrátí větu s obráceným pořadím slov: z `"ahoj svete dnes"` udělá `"dnes svete ahoj"`.
4. `pocet_samohlasek(text)` vrátí počet samohlásek `a e i o u y` v textu. Velikost písmen nehraje roli, písmena s diakritikou se nepočítají.
5. `ciferny_soucet(n)` vrátí součet číslic nezáporného celého čísla: `ciferny_soucet(472)` je `13`.
