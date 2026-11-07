## Expres přidává termín a příplatek

Expresní kurýr zůstává kurýrem: potřebuje adresu, dodržuje hmotnostní limit a počítá základní cenu. Navíc nabízí dopolední nebo odpolední doručení a přidává příplatek. Výchozí limit expresu je přísnější, 5000 g. Chceme zachovat všechna pravidla z minulé lekce a rozšířit je.

V pracovním prostoru jsou připravené balik.py a doprava.py s předchozími řešeními. `from doprava import Kuryr` načte základní třídu. Nyní doplníme ExpresniKuryr(Kuryr).

## Vlastní konstruktor převzal odpovědnost

V deváté lekci KrehkyBalik vlastní __init__ neměl, a proto Python použil zděděný. ExpresniKuryr ho ale definuje. Python provede tuto novou metodu a základní konstruktor už sám automaticky nespustí.

```python
super().__init__(adresa, limit_g)
```

super() umožní navázat na další implementaci v pořadí dědění. V naší jednoduché hierarchii jde o Kuryr. __init__ zavoláme na stejném vznikajícím objektu; základní metoda tak nastaví adresu a limit expresního kurýra. self se předá automaticky. Nevytváříme druhou instanci pomocí Kuryr(...).

Kopírování základní kontroly by znamenalo udržovat dvě verze téhož pravidla. Zavoláním super().__init__ převezmeme kontrolu neprázdné adresy i kladného celočíselného limitu, včetně odmítnutí bool.

## Co přibývá v expresu

Konstruktor má rozhraní `ExpresniKuryr(adresa, termin, priplatek=50, limit_g=5000)`. Hodnota termin je přesně "dopoledne" nebo "odpoledne"; jiná vyvolá ValueError. Příplatek je nezáporný int, nikoli bool: nula je povolená. Vlastní kontroly jsou už připravené.

Po základní inicializaci uložíme termín a příplatek. Property termin a priplatek poskytují čtení, stejně jako zděděné adresa a limit_g. Každá instance má vlastní hodnoty. Metody nic nevypisují ani nemění balík.

## Rozšíření ceny místo kopírování

```python
return super().cena(balik) + self.priplatek
```

Základní cena se vypočítá se skutečným limitem této instance. U balíku 1200 g vrátí 99 a expres přičte výchozích 50, tedy 149 Kč. Při překročení limitu základní metoda vyvolá ValueError; výpočet se přeruší a příplatek se už nepřičítá.

Pevné `99 + self.priplatek` by přeskočilo kontrolu limitu i dražší pásmo. Při vlastním limitu 8000 g je balík 6000 g povolený a základ stojí 149 Kč. S příplatkem 50 tedy expres stojí 199 Kč.

Pozor také na `self.cena(balik)` uvnitř cena: volalo by znovu tutéž metodu bez konce. super().cena navazuje na základní implementaci, takže se toto opakování nestane.

## Váš úkol

Doplňte jedno volání super v konstruktoru a druhé v cena. Základní konstruktor i základní výpočet ceny použijte právě jednou, na stejné instanci a s předanými hodnotami. Ponechte připravené kontroly a property. Výsledek ceny vraťte, nevypisujte jej uvnitř metody.

Spusťte ukázku. Potom zkuste termín "odpoledne", nulový příplatek a vlastní limit 8000 g. Porovnejte ceny balíků o hmotnosti 5000 a 5001 g při výchozím limitu: první projde, druhý vyvolá ValueError. Stejně jako dříve zachycení chyby nemění údaje kurýra ani balíku.
