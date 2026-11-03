## Když objekt vlastní seznam

Atribut nemusí obsahovat jen číslo nebo text. Může držet seznam, například seznam předmětů v batohu nebo později seznam částí hada. Potřebujeme, aby si každá instance vytvořila svůj vlastní seznam.

```python
class Playlist:
    def __init__(self, nazev):
        self.nazev = nazev
        self.skladby = []

    def pridej(self, skladba):
        self.skladby.append(skladba)
        return len(self.skladby)
```

Závorky `[]` uvnitř `__init__` se vyhodnotí při každém vytvoření objektu znovu. `self.skladby.append(...)` mění seznam patřící právě tomuto playlistu. `len(...)` vrací jeho novou délku. Po zavolání `rano.pridej("Lesní cesta")` tedy očekáváme nejen návratovou hodnotu 1, ale i uloženou skladbu v objektu.

## Past: seznam na třídě

```python
class ChybnyPlaylist:
    skladby = []
```

Toto přiřazení je přímo v těle třídy, nikoli uvnitř `__init__`. Vytváří **atribut třídy**, společný pro její instance. Když Python nenajde atribut na instanci, může ho přečíst ze třídy. Dvě instance by pak mohly měnit tentýž seznam přes append. Pro naše vlastní seznamy proto používejte `self.skladby = []` v inicializátoru.

Sdílené atributy tříd mohou mít své použití, ale nejsou správným místem pro obsah konkrétního batohu. Stejně tak zde nepoužívejte měnitelný výchozí argument `skladby=[]`; pravidlo o sdílení takového argumentu už znáte z funkcí.

## Vrátit seznam nebo jeho kopii

```python
    def seznam_skladeb(self):
        return list(self.skladby)
```

Tato metoda patří do třídy Playlist na stejnou úroveň jako `pridej`. `list(...)` vytvoří nový seznam. Stejně by posloužilo `.copy()` nebo řez `[:]`, které už znáte. Obsahujeme pouze řetězce, proto nám tato kopie stačí.

Kdyby metoda vracela přímo `self.skladby`, volající by dostal odkaz na její vnitřní seznam. Příkaz `vysledek.append(...)` by potom měnil i playlist. S kopií si volající může svůj výsledek upravit a vnitřní stav zůstane stejný.

Při druhém volání metoda znovu vrátí aktuální obsah. Dřívější kopie se sama nedoplňuje o později přidané skladby.

## Váš úkol

Vytvořte třídu `Batoh`:

1. `__init__(self)` vytvoří prázdný seznam `self.veci` pro každou novou instanci zvlášť.
2. `pridej(self, predmet)` přidá zadaný řetězec na konec seznamu a vrátí nový počet věcí.
3. `obsah(self)` vrátí **nový seznam** s aktuálními věcmi ve stejném pořadí. Vrácený seznam může volající měnit, aniž by změnil batoh.

Duplicity jsou dovolené: dvě přidání vody znamenají dvě věci. Předměty jsou řetězce, mohou být i prázdné; v tomto úkolu je nijak neověřujte a neupravujte. Dva batohy musí fungovat nezávisle. Ani vytvoření dalšího batohu nesmí vymazat starší.

Příklad: po vytvoření `b = Batoh()` vrátí `b.obsah()` prázdný seznam. `b.pridej("mapa")` vrátí 1, další `b.pridej("mapa")` vrátí 2. Obsahem je `['mapa', 'mapa']`.

Tím propojujeme konstruktor, metody a měnitelné atributy. U Snake bude podobně důležité, aby každá nová hra měla svůj stav a aby se změny prováděly na správném objektu.
