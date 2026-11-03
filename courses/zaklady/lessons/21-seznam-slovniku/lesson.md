## Tabulka záznamů

Skutečná data se skládají z více záznamů, třeba studentů. Každý student je jeden slovník a všichni dohromady tvoří **seznam slovníků**:

```python
studenti = [
    {"jmeno": "Eva", "body": 82},
    {"jmeno": "Petr", "body": 54},
]
```

Seznam se prochází cyklem `for`, a proměnná cyklu je pak vždy jeden slovník:

```python
for student in studenti:
    print(student["jmeno"], student["body"])
```

Zápis `studenti[0]["body"]` znamená „vezmi první slovník a v něm hodnotu klíče body“.

## Hledání nejlepšího

Nejlepšího studenta najdete podobně jako maximum v seznamu čísel. Při procházení si pamatujete nejlepšího zatím nalezeného a porovnáváte s ním každý další záznam. Funkce `max` to umí i zkráceně: `max(studenti, key=...)` potřebuje pravidlo, které z každého záznamu vybere číslo k porovnání. Můžete ho zapsat jako **lambda**, malou funkci bez jména: `lambda s: s["body"]`.

> Zkratku s `lambda` nemusíte používat. Cyklus s pomocnou proměnnou je naprosto v pořádku a pro začátek čitelnější.

## Váš úkol

Seznam `studenti` obsahuje slovníky s klíči `"jmeno"` a `"body"`.

1. `nejlepsi(studenti)` vrátí **jméno** studenta s nejvíce body.
2. `prumer_bodu(studenti)` vrátí průměr bodů všech studentů.
3. `uspesni(studenti, hranice)` vrátí seznam jmen studentů, kteří mají **alespoň** `hranice` bodů, v původním pořadí.
4. `pridej_studenta(studenti, jmeno, body)` přidá nový slovník na konec seznamu a seznam vrátí.
