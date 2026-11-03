## Zachovat základ a přidat něco navíc

Přepsáním metody jsme změnili celé její chování. Často ale chceme původní část zachovat a jen ji rozšířit. K tomu pomůže `super()`.

```python
class Zamestnanec:
    def __init__(self, jmeno):
        self.jmeno = jmeno

    def vizitka(self):
        return f"Jméno: {self.jmeno}"


class Technik(Zamestnanec):
    def __init__(self, jmeno, obor):
        super().__init__(jmeno)
        self.obor = obor

    def vizitka(self):
        return f"{super().vizitka()}, obor: {self.obor}"
```

V našem jednoduchém řetězci dědění dovolí `super()` zavolat metodu ze základní třídy pro **stejný objekt**. Nevytvoří nového zaměstnance. Obecně hledá další implementaci v pořadí dědění; složitější pořadí s více základy si necháme na další lekce.

## Inicializátor se nepřidá automaticky

V minulé lekci odvozená třída vlastní konstruktor neměla a používala zděděný. Jakmile ale definujeme vlastní `__init__`, jeho tělo určuje, co se skutečně provede.

Při `t = Technik("Ema", "elektro")` nastane:

1. Vznikne nová instance Technik a její inicializátor dostane jméno i obor.
2. `super().__init__(jmeno)` použije inicializátor Zamestnanec pro tuto instanci. Ten nastaví `self.jmeno`.
3. `self.obor = obor` doplní další atribut.
4. Výsledný objekt má oba údaje a můžeme na něm volat metody.

Kdyby první volání chybělo, pouhé dědění by naše nové tělo `__init__` automaticky nerozšířilo a atribut `jmeno` by zde nevznikl. Také nepište `Zamestnanec(jmeno)` jako náhradu: tím byste vytvořili jiný objekt, nikoli připravili tento.

## Rozšíření obyčejné metody

Při `t.vizitka()` se nejprve zavolá odvozená metoda. Výraz `super().vizitka()` získá text podle základní implementace a f-řetězec k němu přidá obor.

Do `super().__init__` ani `super().vizitka()` nepředáváme self navíc. Volání přes super ho naváže automaticky. Kdyby odvozená vizitka volala `self.vizitka()`, znovu by volala sama sebe a skončila chybou rekurze.

Výhoda je praktická: změníme-li později společný formát vizitky v základu, odvozená třída jej dál využije. Opisováním stejného textu do všech potomků bychom tuto vazbu ztratili.

## Váš úkol

Napište dvě třídy:

1. `Hrac(jmeno)` uloží `jmeno`. Jeho `popis(self)` vrátí `Hráč: Ema` pro jméno Ema.
2. `BodovanyHrac(Hrac)` má `__init__(self, jmeno, body=0)`. Použije super k inicializaci základních údajů a přidá atribut `body`.
3. Přepsaný `popis(self)` použije super k získání základního popisu a doplní jej na `Hráč: Ema, body: 3`, má-li hráč 3 body.
4. `pridej_body(self, kolik)` přičte celé číslo k aktuálním bodům a vrátí nový počet. Přírůstek může být nulový i záporný; v této lekci jej neomezujeme.

Jméno a počáteční body pouze uložte. Změna atributů se projeví v dalším popisu. Každý hráč má vlastní stav.

Oba přepsané postupy mají skutečně využívat základní implementaci přes super, ne její text nebo nastavení opisovat. Kontrola proto ověří i situaci, kdy se základní popis změní. Obyčejný Hrac dál funguje samostatně a nepotřebuje body.
