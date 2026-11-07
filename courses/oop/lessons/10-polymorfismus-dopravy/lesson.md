## Stejná otázka, různé odpovědi

Za osobní odběr se neplatí, ale potřebujeme výdejní místo. Kurýr potřebuje adresu a má hmotnostní limit. Oběma možnostem chceme položit stejnou otázku: kolik stojí doprava tohoto balíku?

Soubor balik.py obsahuje řešení předchozí lekce. Je přiložený v pracovním prostoru a `from balik import Balik` načte třídu. Jeho ukázka se při importu nespustí díky podmínce __name__ == "__main__". Není potřeba nic instalovat.

## Přepsání zděděné metody

Základní Doprava definuje metodu cena(balik). Obecná doprava však ještě neví, jak cenu vypočítat:

```python
class Doprava:
    def cena(self, balik):
        raise NotImplementedError("Cenu určuje konkrétní doprava")
```

NotImplementedError zde znamená „tuto operaci musí dodat konkrétní třída“. Liší se od ValueError, která v našem modelu označuje neplatný vstup nebo nepřepravitelný balík. Jde o běžné výjimky Pythonu, nepotřebujeme další knihovnu.

OsobniOdber a Kuryr dědí z Doprava. Každá třída znovu definuje cena se stejným způsobem volání. Tím metodu přepisuje. Python u instance OsobniOdber použije její cena, u kurýra cenu kurýra. Základní nehotovou metodu při tom nevolá.

## Naše přepravní pravidla

- OsobniOdber(misto) potřebuje neprázdný text výdejního místa. Vrací 0 Kč a nemá hmotnostní limit.
- Kuryr(adresa, limit_g=10000) potřebuje neprázdnou textovou adresu a kladný celý limit v gramech. Do 5000 g včetně stojí 99 Kč, nad 5000 g stojí 149 Kč, nejvýš však do limit_g.

Konstruktory a property jsou připravené. Text obsahující jen mezery nestačí; kontrola strip() ověřuje jeho obsah, uložený původní text ale nemění. Limit musí být skutečný int, nikoli bool. Údaje misto, adresa a limit_g jsou pouze pro čtení.

V cena nejprve ověřte limit kurýra, teprve potom cenové pásmo. Kurýr s limitem 3000 g odmítne i balík o 4000 g, přestože by patřil do levnějšího pásma. Balík přesně na limitu je přípustný. Odmítnutí přes ValueError nemění dopravu ani balík. Výpočet ceny nic nerezervuje ani neodesílá.

## Polymorfismus v obyčejném cyklu

```python
for doprava in dopravy:
    ceny.append(doprava.cena(balik))
```

Proměnná doprava postupně odkazuje na různé objekty. Cyklus pokaždé volá stejnou metodu, konkrétní odpověď ale určuje daný objekt. Tomu říkáme polymorfismus. Funkce se nemusí ptát, zda právě drží kurýra, nebo osobní odběr.

To dovoluje přidat další možnost s metodou cena, aniž bychom cyklus upravovali. V Pythonu dokonce nemusí zdědit Doprava, pokud poskytuje stejné potřebné chování. Společná základní třída přesto může zpřehlednit rodinu našich možností dopravy. Samotné dědění správnost cen nezaručí.

## Váš úkol

Doplňte cena v OsobniOdber a Kuryr a funkci ceny_dopravy(dopravy, balik). Ta vrátí nový seznam výsledků volání cena pro tentýž balík, ve stejném pořadí jako vstup. Duplicitní dopravy zachovejte; prázdný seznam vrátí []. Vstupní seznam ani objekty neměňte, nic nevypisujte. Výjimku při odmítnutí balíku nechte projít k volajícímu.

Vyzkoušejte 5000, 5001, 10000 a 10001 gramů. Poslední hmotnost běžný kurýr odmítne. Potom v seznamu prohoďte pořadí možností: ceny se mají prohodit také. Vyhněte se větvení podle názvů tříd; výsledek má určit volání cena každé možnosti.
