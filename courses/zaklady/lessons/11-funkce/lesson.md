## Pojmenovaný kus kódu

**Funkce** je blok kódu s jménem. Jednou ji napíšete a pak ji můžete **volat** kolikrát chcete. Už znáte hotové funkce `print()`, `len()` nebo `input()`. Vlastní vytvoříte příkazem `def`:

```python
def pozdrav():
    print("Ahoj!")
```

Tím se kód jen **definuje**, ještě se nespustí. Spustí se až voláním se závorkami:

```python
pozdrav()
pozdrav()
```

Vypíše `Ahoj!` dvakrát.

## Pravidla zápisu

- za jménem jsou závorky a **dvojtečka**
- tělo funkce je **odsazené o 4 mezery**
- jméno píšeme malými písmeny, slova oddělujeme `_`: `vypis_menu`
- funkci musíte definovat **dřív**, než ji zavoláte

## Proč funkce

- kód se neopakuje (opravíte ho na jednom místě)
- program je přehlednější, dlouhý úkol rozdělíte na části
- funkce lze zkoušet samostatně

> Zapomenuté závorky jsou častá chyba: `pozdrav` bez `()` funkci jen pojmenuje, ale nespustí.

## Váš úkol

Napište funkci `pozdrav()`, která vypíše `Ahoj z funkce!`. Zavolejte ji dvakrát.
