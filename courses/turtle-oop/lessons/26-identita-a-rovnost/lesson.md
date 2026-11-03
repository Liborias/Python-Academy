## Stejný objekt, nebo stejná hodnota?

U seznamů už známe rozdíl mezi kopií a dalším odkazem. Pro vlastní objekty teď rozlišíme dvě otázky:

- `a is b`: je to **tentýž objekt**? Tomu říkáme identita.
- `a == b`: mají objekty **stejnou hodnotu podle pravidla jejich typu**? To je rovnost.

`b = a` vytvoří druhý odkaz, takže `a is b` je True. Dva zvlášť vytvořené objekty mohou mít stejná data a současně různou identitu.

U třídy bez vlastního porovnání se dva odlišné obyčejné objekty obvykle nebudou považovat za rovné jen proto, že jsme do nich uložili stejné atributy. Pravidlo pro hodnotovou rovnost si musíme stanovit.

## Metoda __eq__

```python
class Karta:
    def __init__(self, kod):
        self.kod = kod

    def __eq__(self, other):
        if not isinstance(other, Karta):
            return NotImplemented
        return self.kod == other.kod
```

`__eq__` je speciální metoda použitá při porovnání pomocí `==`. Dostane současný objekt jako self a druhou hodnotu jako other. Jméno other je běžná konvence, ne zvláštní příkaz Pythonu.

Zde platí: dvě karty mají stejnou hodnotu, pokud mají stejný kód. Jiné třídy mohou porovnávat jiné atributy. Pro bod v rovině bude důležitá dvojice souřadnic, nejen jedna z nich.

```python
a = Karta("A1")
b = Karta("A1")
kopie = a
print(a == b)       # True: stejné kódy
print(a is b)       # False: dvě instance
print(a is kopie)   # True: dva odkazy na jednu instanci
```

## Když druhému typu nerozumíme

`NotImplemented` je vestavěná zvláštní hodnota. V porovnávací metodě znamená: „tento typ neumím porovnat, dej možnost druhé straně“. Nejde o výjimku NotImplementedError a nic zde nevyvoláváme pomocí raise.

Kdyby metoda vracela pro každý cizí typ rovnou False, neumožnila by běžné pokračování porovnání na druhé straně. Když podporu odmítnou obě strany, Python pro `==` nakonec použije porovnání identity. Pro naši kartu a běžný text proto výsledek bude False.

V podporovaném případě metoda vrací True nebo False, nikoli větu ani číslo vzdálenosti. Kontrolujeme typ ještě před čtením jeho atributů, aby například `karta == "A1"` neskončilo AttributeError.

## Praktická pravidla

Pro hodnoty jako čísla a texty používejte `==`, ne is. Python může některé hodnoty interně sdílet a takový detail nemá řídit logiku programu. `is None` naopak dává smysl, protože se ptáme na konkrétní zvláštní objekt None.

Po definici __eq__ je běžná měnitelná třída bez další úpravy nehashovatelná: nelze ji použít jako klíč slovníku nebo prvek množiny. V tomto úkolu hashování neprogramujeme. Pro souřadnicový klíč lze dál použít neměnnou n-tici `(x, y)`.

## Váš úkol

Napište třídu `Bod(x, y)` s vlastními atributy `x`, `y` a metodou __eq__:

1. Pro jiný Bod vrátí True právě tehdy, když se rovnají **obě** souřadnice, jinak False.
2. Pro jiný typ vrátí NotImplemented. Použijte isinstance, takže za bod lze považovat i případný odvozený typ Bod.
3. Porovnání čte aktuální atributy a nemění ani jeden objekt.

Souřadnice jsou celá čísla, mohou být záporná i nulová. Dva nově vytvořené body se stejnými souřadnicemi mají být rovné, ale nesmějí být jediným sdíleným objektem. Změníme-li později souřadnici, další porovnání musí reagovat na nový stav. Stačí __eq__; samostatnou metodu __ne__ pro operátor `!=` nepotřebujete.
