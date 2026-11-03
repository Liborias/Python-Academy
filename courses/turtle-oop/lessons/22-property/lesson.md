## Atribut s pravidly

V minulé lekci jsme stav měnili přes metody. Někdy se hodí přirozený zápis `ctverec.strana = 5`, ale stále chceme ověřit novou hodnotu. K tomu slouží **property**: navenek atribut, uvnitř řízené čtení nebo nastavení.

```python
class Ctverec:
    def __init__(self, strana):
        self.strana = strana

    @property
    def strana(self):
        return self._strana

    @strana.setter
    def strana(self, hodnota):
        if hodnota < 0:
            raise ValueError("Strana nesmí být záporná")
        self._strana = hodnota
```

Řádek začínající `@` je **dekorátor**: upraví význam následující definice. V této lekci potřebujeme znát pouze konkrétní dvojici `@property` a `@strana.setter`; vlastní dekorátory zatím neprogramujeme.

První metoda je **getter**: Python ji zavolá při čtení `c.strana`, bez závorek. Druhá je **setter**: zavolá se při přiřazení `c.strana = 5` a dostane novou hodnotu do parametru `hodnota`. Obě definice se jmenují `strana`. Setter se zapisuje až za getterem.

## Co se děje krok za krokem

Při `c = Ctverec(3)` konstruktor provede `self.strana = 3`. Tím už zavolá setter; teprve ten ověří číslo a uloží ho do obyčejného vnitřního atributu `_strana`. Stejná pravidla se tak použijí při vytvoření i pozdější změně.

Čtení `c.strana` spustí getter, který vrátí `_strana`. Nevolejte `c.strana()` — výsledkem getteru je číslo, nikoli metoda k dalšímu volání.

Uvnitř getteru nepište `return self.strana`: znovu by se vyvolal sám getter a opakoval by se až do chyby RecursionError. Podobně setter nemá při ukládání znovu přiřazovat `self.strana`. Proto oddělujeme veřejné jméno od vnitřního `_strana`.

## Vypočítaná property pouze pro čtení

```python
    @property
    def obsah(self):
        return self._strana * self._strana
```

Tuto metodu opět přidáme do třídy Ctverec. Obsah se vypočítá při každém čtení, takže se přizpůsobí nové straně. Není třeba ukládat druhé číslo a udržovat ho ručně v souladu.

Protože k `obsah` není setter, přiřazení `c.obsah = 100` vyvolá AttributeError. Veřejnou property tak můžeme nabídnout i jen ke čtení. Vnitřní atributy s podtržítkem dál zůstávají dohodou, nikoli bezpečnostní bariérou.

## Váš úkol

Vytvořte třídu `Teplomer`:

1. `__init__(self, teplota=20)` nastaví počáteční teplotu; platné hodnoty jsou od -50 do 100 včetně.
2. Property `teplota` dovolí čtení i přiřazení. Nastavení hodnoty mimo rozsah vyvolá ValueError a ponechá dosavadní teplotu. Totéž pravidlo platí při konstrukci.
3. Property `fahrenheit` dovolí pouze čtení a vždy vrátí aktuální převod `teplota * 1.8 + 32`. Při pokusu o přiřazení má vzniknout AttributeError.

Vstupy jsou běžná celá nebo desetinná čísla; jiné typy ani zvláštní hodnoty jako nan zde neřešíme. Fahrenheit nezaokrouhlujte a nevracejte text. Dvě instance mají vlastní teplotu.

Doporučení: v konstruktoru přiřaďte do veřejné property, aby se využil setter a nebylo nutné opisovat ověření. Například `t = Teplomer(0)` má `t.teplota == 0` a `t.fahrenheit == 32`. Po `t.teplota = 10` se převod změní na 50.
