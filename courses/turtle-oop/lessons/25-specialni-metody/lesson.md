## Když vlastní objekt potká print nebo len

U seznamu funguje `len(seznam)` a `print(seznam)` vypíše jeho obsah. S vlastním objektem můžeme spolupracovat stejným způsobem pomocí **speciálních metod**. Jejich názvy začínají a končí dvěma podtržítky, například `__str__`. Anglické double underscore se někdy zkracuje na „dunder“.

Názvy těchto metod mají v Pythonu konkrétní význam. Nevymýšlíme proto pro běžnou metodu vlastní jméno se dvěma podtržítky na obou stranách. `__init__` už znáte; nyní přidáme další tři.

## Text pro člověka: __str__

```python
class Policka:
    def __init__(self, nazev, knihy):
        self.nazev = nazev
        self.knihy = list(knihy)

    def __str__(self):
        return f"{self.nazev}, knih: {len(self.knihy)}"
```

Při `print(policka)` Python získá text přes `str(policka)` a metodu `__str__`. Ta má **vrátit řetězec**, nikoli ho sama vypisovat. Výpis udělá až vnější print. Při návratu čísla nebo None vznikne TypeError.

Konstruktor kopíruje vstupní seznam pomocí list, aby si objekt uchoval vlastní kolekci. Není to nová vlastnost speciálních metod, jen využití dříve vysvětlených pravidel sdílení.

## Text pro ladění: __repr__

```python
    def __repr__(self):
        return f"Policka(nazev={self.nazev!r}, knihy={self.knihy!r})"
```

Tato metoda patří do stejné třídy. Funkce `repr(policka)` ji použije pro podrobnější popis při ladění. Seznam objektů jako `[policka]` také zobrazuje jejich repr, takže poznáme typ i hodnoty uvnitř.

Zápis `!r` ve f-řetězci je nová drobnost: použije reprezentaci hodnoty jako při volání `repr(hodnota)`. Text tak dostane uvozovky a potřebné escapování. Například `f"{nazev!r}"` pro název Les vytvoří text `'Les'`, včetně uvozovek. Stejně lze potřebnou část sestavit pomocí funkce repr.

Repr nemusí být vždy spustitelný Python výraz. Zde volíme podobu konstruktoru, aby byl výsledek snadno čitelný. Není důvod jej zpětně vykonávat pomocí eval.

## Délka: __len__

```python
    def __len__(self):
        return len(self.knihy)
```

`len(policka)` teď vrátí počet knih. Speciální metoda musí vracet nezáporné celé číslo; záporná hodnota způsobí ValueError a jiný nevhodný typ TypeError. U seznamu je tato podmínka přirozeně splněná.

Metody definujeme na třídě. Běžně pak používáme print, str, repr a len místo ručního volání dunder metod. Samotné formátování ani čtení délky nemá měnit obsah objektu.

## Váš úkol

Napište třídu `Trasa(jmeno, body)`. Jméno je řetězec a body je seznam dvojic souřadnic. Uložte atributy `jmeno` a vlastní kopii seznamu `body`.

1. `len(trasa)` vrátí počet bodů (nikoli délku jména nebo součet souřadnic).
2. `str(trasa)` vrátí například `Trasa Les, bodů: 2`.
3. `repr(trasa)` vrátí přesně podobu `Trasa(jmeno='Les', body=[(0, 0), (2, 3)])`, používá tedy repr aktuálního jména i seznamu. U jiných hodnot se text přizpůsobí.

Platný je i prázdný seznam, prázdné jméno nebo název s uvozovkami. Po přidání dalšího bodu do `trasa.body` se délka a oba texty hned přizpůsobí. Změna původního seznamu předaného konstruktoru se naopak do trasy automaticky přenést nemá. Čtení nesmí body odebírat ani přerovnávat.
