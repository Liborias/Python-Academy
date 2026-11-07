## Křehký balík je pořád balík

Sklad umí rezervovat zboží. Nyní se na chvíli zaměříme na jeho dopravu: potřebujeme znát kód a hmotnost zabalené zásilky. Použijeme nový model Balik. Objednávka může mít mnoho položek, ale balík zde představuje jeden fyzický kus k přepravě. Přiřazování objednávek a balíků přijde v závěrečném projektu.

Balik uchovává kod a kladnou celočíselnou hmotnost v gramech. Kód předpokládáme jako text. Konstruktor odmítá nulovou, zápornou nebo necelou hmotnost pomocí ValueError; odmítne i bool. Property hmotnost_g je jen pro čtení. Metoda popis() vrací například `Balík B-001, 1200 g`. Návratová hodnota je text; na obrazovku ji vypíše až print.

Křehký balík má stejné údaje a navíc potřebuje pokyny pro manipulaci. Nemusíme kopírovat konstruktor a popis do druhé třídy.

## Jméno v závorce znamená základní třídu

```python
class KrehkyBalik(Balik):
    def pokyny(self):
        return "Chránit před nárazy."
```

Balik je základní třída, KrehkyBalik je odvozená třída neboli potomek. Závorka za názvem říká, odkud má Python převzít dostupné chování. To je dědění.

Při `KrehkyBalik("K-002", 800)` Python nenajde vlastní __init__ potomka, a proto použije zděděný konstruktor Balik. Jeho self přitom označuje právě vznikající křehký balík. Nevzniká další balík schovaný uvnitř. Křehký balík tak dostane vlastní kod a _hmotnost_g.

Při `krehky.popis()` Python hledá metodu stejným způsobem: nejprve u potomka, potom v základní třídě. Zděděná metoda pracuje s údaji tohoto konkrétního objektu. Totéž platí pro property hmotnost_g. Podtržítko u uložené hodnoty dál znamená dohodu používat veřejné rozhraní.

## Ověření vztahu přes isinstance

```python
print(isinstance(krehky, KrehkyBalik))  # True
print(isinstance(krehky, Balik))        # True
```

Vestavěná funkce isinstance(objekt, trida) vrací, zda je objekt instancí uvedené třídy nebo jejího potomka. Křehký balík je i obecný balík. Obyčejný Balik však není automaticky KrehkyBalik a nemá pokyny().

## Kdy dědění dává smysl

Použijte větu „křehký balík je balík“. Tam dědění vyjadřuje vztah dobře. Věta „objednávka je položka“ neplatí: objednávka položky obsahuje, jak jsme použili ve čtvrté lekci. Takový vztah vyjádříme uložením spolupracujících objektů.

Nový kód nebo jiná hmotnost samy o sobě novou třídu nepotřebují; stačí jiné hodnoty konstruktoru. Tady potomek přidává skutečné chování, pokyny(). Později uvidíme, jak měnit chování zděděné metody.

## Váš úkol

Balik je připravený. Změňte definici KrehkyBalik tak, aby dědil z Balik, a doplňte pokyny(), které vrátí přesně `Chránit před nárazy.`. Konstruktor, property a popis zděďte; nevytvářejte jejich kopie. Metody nic nevypisují ani nemění stav.

Spusťte ukázku. Potom zkuste dva různé křehké balíky a ověřte, že mají vlastní údaje. Změňte jednomu kod a znovu zavolejte popis(): má obsahovat aktuální kód. Pokus přiřadit hmotnost_g vyvolá AttributeError, protože property poskytuje pouze čtení. Neplatnou hmotnost odmítá i zděděný konstruktor.
