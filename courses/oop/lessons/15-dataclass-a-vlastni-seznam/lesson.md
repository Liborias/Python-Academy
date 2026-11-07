## Štítek je hlavně záznam údajů

Expediční štítek potřebuje kód, adresu a poznámky. U takové třídy bychom opakovali podobný konstruktor, repr a porovnání údajů. Standardní knihovna dataclasses umí tuto pravidelnou část vytvořit. Pravidla skladu nebo volbu dopravy ale stále navrhujeme sami.

Přiložený adresa.py obsahuje řešení minulé lekce. Adresa má vlastní hodnotovou rovnost, takže dva štítky mohou obsahovat stejné adresní údaje, i když odkazují na dva samostatné objekty adresy.

## Dekorátor a popis polí

```python
from dataclasses import dataclass, field

@dataclass
class ExpedicniStitek:
    kod: str
    adresa: Adresa
```

Značka @dataclass je dekorátor: po vytvoření třídy ji doplní o běžné metody. Z typových anotací kod: str a adresa: Adresa pozná datová pole. Vytvoří __init__, který tato pole přijme, __repr__ s jejich názvy a hodnotami a __eq__, která porovná pole dvou instancí stejné třídy.

Anotace říkají čtenáři a editoru, jaké typy očekáváme. Python je sám automaticky nekontroluje. Dataclass proto nenahrazuje validaci v modelu, který ji potřebuje. Zde předpokládáme textový kód, objekt Adresa a textové poznámky.

U anotace není přiřazení nutné: kod a adresa budou povinné argumenty konstruktoru. Pole s výchozí hodnotou přijde za povinnými poli. Běžné vlastní metody, například přidání poznámky, můžeme definovat dál.

## Každý štítek potřebuje vlastní seznam

```python
poznamky: list[str] = field(default_factory=list)
```

list[str] popisuje seznam textů. field upřesní, jak se má datové pole vytvořit. default_factory=list předá funkci list bez závorek. Vygenerovaný konstruktor ji zavolá pokaždé, když argument poznamky vynecháme. Vznikne nový prázdný seznam pro danou instanci.

Kdyby se seznam vytvořil jednou společně, poznámka prvního štítku by se objevila také u druhého. Dataclass navíc běžnou výchozí hodnotu [] odmítá jako nevhodný měnitelný default. Ani list() místo list zde není správně: vytvořilo by seznam už při definici, místo předání funkce, která jej má teprve vytvořit.

Když seznam výslovně předáme jako třetí argument, konstruktor uchová právě tento seznam. Továrna se v takovém případě nevolá a nic automaticky nekopíruje. Stejně tak uchová původní objekt adresy. Vlastní výchozí seznam není hluboká kopie všech spolupracujících objektů.

## Co dostaneme a co doplníme

ExpedicniStitek("E-001", adresa) má prázdné poznámky. Repr ukáže název třídy i pole; print bez vlastního __str__ využije tento záznam. Rovnost zahrnuje kód, hodnotu adresy i celý seznam poznámek v jeho pořadí. Dva právě shodné štítky přestanou být rovné, když jednomu přidáme poznámku.

Naše metoda pridej_poznamku(text) připojí text na konec seznamu a vrátí nový celkový počet poznámek. Zachová i dvě stejné poznámky a jejich pořadí; v této lekci jejich obsah neověřujeme. Metoda nic nevypisuje.

## Váš úkol

Doplňte dekorátor dataclass, výchozí seznam přes field(default_factory=list) a metodu pridej_poznamku. Použijte generovaný konstruktor, repr a hodnotové porovnání. Vlastní __init__, __repr__ a __eq__ tentokrát nejsou potřeba.

Spusťte ukázku se dvěma štítky. Potom vytvořte třetí se samostatnou, hodnotově stejnou adresou a poznámkami prvního. Ověřte jejich rovnost. Přidejte poznámku jen jednomu a ověřte rozdíl i nezměněný druhý seznam. Nakonec zkuste výslovně předat vlastní seznam a sledujte, že přidání poznámky změní právě tento předaný seznam.
