## Když třída hlavně uchovává údaje

U některých tříd opakujeme pořád totéž: konstruktor přiřadí argumenty, repr ukáže pole a rovnost porovná jejich hodnoty. Modul `dataclasses` ze standardní knihovny umí tento běžný kód vytvořit.

```python
from dataclasses import dataclass


@dataclass
class Vyprava:
    cil: str
    pocet_dni: int = 1
```

`@dataclass` je další konkrétní dekorátor, podobně jako dřívější @property mění význam následující definice. Zde upraví třídu podle jejích deklarovaných **polí**. Nepotřebujeme instalovat pip balíček.

## Co znamená dvojtečka u pole

Zápis `cil: str` je **typová anotace**: říká člověku a editoru, že očekáváme řetězec. `pocet_dni: int = 1` má navíc výchozí hodnotu. Dataclass podle těchto anotací rozezná pole a jejich pořadí.

Anotace sama hodnotu nepřevede ani nezkontroluje za běhu. Pro zakázání záporného počtu dní bychom museli doplnit skutečnou validaci. Samotný zápis `cil: str` v obyčejné třídě také nevytváří konstruktor — zde jej doplní až dataclass.

```python
a = Vyprava("Les")
b = Vyprava("Les")
print(a)              # Vyprava(cil='Les', pocet_dni=1)
print(a == b)         # True
print(a is b)         # False
```

Dekorátor běžně vytvoří __init__, __repr__ a __eq__. Hodnotovou rovnost porovnává podle polí mezi instancemi stejné konkrétní třídy; identitu objektů neslučuje. Povinná pole zapisujte před poli s výchozí hodnotou, stejně jako parametry funkcí.

## Vlastní seznam přes default_factory

Pro účastníky výpravy potřebujeme nový seznam při každém vytvoření:

```python
from dataclasses import dataclass, field


@dataclass
class Vyprava:
    cil: str
    ucastnici: list[str] = field(default_factory=list)
```

Anotace `list[str]` znamená seznam řetězců. `field(...)` doplní pravidla pro dané pole. `default_factory=list` předá **funkci list bez závorek**, aby ji vygenerovaný konstruktor zavolal pokaždé znovu, když účastníky výslovně nezadáme.

Nejde o jediný seznam vytvořený při definici třídy. Pole `ucastnici: list[str] = []` má nevhodný měnitelný výchozí stav a dataclass takový zápis odmítá výjimkou ValueError. `default_factory=list()` je také chyba: místo továrny bychom předali už vytvořený seznam.

Výslovně předaný seznam se automaticky nekopíruje. Factory zajišťuje nový **výchozí** seznam, nikoli obecnou hlubokou kopii libovolného argumentu. Běžné metody můžeme do dataclass doplnit stejně jako do předchozích tříd.

## Kdy dataclass použít

Hodí se pro přehledné datové záznamy. Nenahradí návrh odpovědností, pravidla stavu ani promyšlenou spolupráci objektů. Pokud potřebujeme vlastní logiku, pořád ji musíme napsat. Tento rozdíl nám pomůže při přípravě herního stavu pro Snake.

## Váš úkol

Pomocí dataclass vytvořte třídu `ZaznamHrace` s poli v tomto pořadí:

1. `jmeno: str` — povinný údaj.
2. `body: int = 0` — výchozí počet bodů.
3. `udalosti: list[str]` — nový prázdný seznam pomocí field a default_factory pro každou instanci.

Doplňte metodu `zapis(self, text)`, která přidá text na konec událostí a vrátí jejich nový počet. Duplicity i prázdný text jsou dovolené. Nepřidávejte validaci ani převody jména nebo bodů. Pole jsou měnitelná, body lze později přepsat.

Využijte automatický konstruktor, repr a rovnost dataclass místo jejich opisování. Dva záznamy se stejnými hodnotami všech tří polí mají být rovné, ale zůstávají různými instancemi. Změna bodů nebo událostí se do rovnosti promítne. Metoda zapis má měnit pouze záznam, na kterém ji voláme.
