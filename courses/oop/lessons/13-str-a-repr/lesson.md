## Co uvidí zákazník a co potřebuje vývojář

Při print(balik) Python bez vlastního nastavení vypisuje technickou značku objektu. Pro zákazníka chceme větu o balíku, při hledání chyby zase přesně vidět jeho údaje. K tomu slouží dvě speciální metody: __str__ a __repr__. Dvojitá podtržítka na obou stranách jsou součástí jejich názvu.

Navážeme třídou PopsanyBalik(Balik). Přiložený balik.py obsahuje řešení deváté lekce, včetně kontroly hmotnosti a property pouze pro čtení. Import načte třídu bez spuštění její ukázky. Starší řešení balíku se tím nemění; rozšíření vytvoříme v potomkovi.

## __str__: čitelná zpráva

```python
def __str__(self):
    return self.popis()
```

Při str(balik), print(balik) nebo obyčejném vložení objektu do f-řetězce Python zavolá __str__. Metoda musí vrátit str, tedy text. Uvnitř nic nevypisuje. Print provede výpis až po převzetí návratové hodnoty.

Balik už má popis(), který vrací aktuální kód a hmotnost. Použijeme jej znovu, aby v programu nebyly dvě různé verze zákaznické zprávy. Změna kódu se projeví při dalším výpisu, bez ukládání druhé kopie popisu.

## __repr__: údaje vhodné při hledání chyby

```python
def __repr__(self):
    return f"PopsanyBalik({self.kod!r}, {self.hmotnost_g!r})"
```

Funkce repr(balik) zavolá __repr__. Výsledek připomíná zápis konstruktoru: `PopsanyBalik('B-001', 1200)`. Vidíme název třídy, kód i hmotnost. I tato metoda musí vrátit text a nesmí měnit stav.

Zápis !r uvnitř f-řetězce požádá o repr dané hodnoty. U textového kódu tak zahrne uvozovky a správně zapíše i apostrof, nový řádek nebo zpětné lomítko. Obyčejné vložení kódu mezi ručně napsané uvozovky by tyto případy snadno pokazilo. Mezi argumenty stačí čárka; mezery jsou pro čitelnost.

Repr je pomůcka pro člověka při vývoji. Není to ukládání dat ani pokyn tento text spouštět jako program. Pro trvalé ukládání budeme používat určené datové formáty.

## Proč seznam vypadá jinak

```python
print(balik)       # zákaznický popis přes __str__
print([balik])     # seznam zobrazí prvek přes __repr__
```

Seznam při svém zobrazení využije repr jednotlivých prvků. Proto stejný objekt jednou vidíme jako větu a podruhé jako přehled jeho údajů. Pokud vlastní __str__ chybí, výchozí chování objektu použije __repr__; tady vědomě definujeme oba účely.

## Váš úkol

Doplňte obě metody PopsanyBalik. __str__ má delegovat na aktuální popis(). __repr__ má vracet zápis `PopsanyBalik(kód, hmotnost)` s textovým kódem bezpečně zapsaným jako Python řetězec a celočíselnou hmotností v gramech. Zápis může mít jiné mezery či uvozovky, musí ale zachovat původní údaje.

Spusťte ukázku a porovnejte tři výstupy. Pak vytvořte balík s kódem obsahujícím apostrof a změňte jeho kod. Oba další výpisy musí odpovídat aktuálnímu údaji, bez změny hmotnosti nebo jiných účinků. Zděděné kontroly a rozhraní ponechte funkční.
