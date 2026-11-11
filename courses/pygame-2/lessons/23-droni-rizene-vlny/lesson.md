## Soupeři přicházejí postupně

Drony přicházejí po intervalech z osmi okrajových vstupů. Předem vybereme místa daleko od hráče; nekonečné náhodné zkoušení by se v malé aréně mohlo zaseknout. Pokud žádný vstup nesplní odstup, zvolíme nejvzdálenější možný. Malý svět nemusí umožnit požadovanou vzdálenost.

**N** v tomto tréninku zahájí další vlnu. V misi 24–25 se vlny střídají po čase a N už nic nepřeskakuje. Okno, pohyb a uložení droni.png fungují jako minule.

```python
import random
moznosti = ['sever', 'východ', 'jih', 'západ']
a = random.Random(23)
b = random.Random(23)
print([a.choice(moznosti) for _ in range(4)])
print([b.choice(moznosti) for _ in range(4)])
```

Obě posloupnosti jsou stejné. Každá instance má vlastní generátor místo společného random.seed. Nová vlna pokračuje v jeho posloupnosti; nový let se stejným seed zopakuje začátek, None zvolí nový náhodný začátek.

## Váš úkol: Vlny(seed=23, interval=0.75)

Nekladný interval odmítněte ValueError, jinak je kladný konečný počet sekund. Vytvořte vlastní rng=Random(seed), interval, prázdnou Group drony, cislo=0, cekaji=0, cas=0.0 a vytvoreno=0. Konstruktor zavolá zahaj: první vlna má číslo 1, tři čekající a žádného vytvořeného drona.

**zahaj()** odstraní staré drony přes kill ze všech členství, zvýší cislo, nastaví cekaji=min(2+cislo,6), cas=0 a vytvoreno=0. Group zůstává táž; nemění hráče ani data.

**pridej(hrac,hranice)** vezme osm bodů z připravené vstupy(hranice), zachová pořadí a vybere body alespoň 150 px od přesné hrac.pozice. Pokud jsou, provede právě jedno rng.choice nad tímto seznamem. Jinak zvolí nejvzdálenější bod (při shodě první), bez losování.

Rychlost je `min(90 + 10 * (cislo - 1), 140)`. Podle dosavadního vytvoreno se od nuly střídá Dron, HlidacBodu, Dron… Hlídač má rychlost o 10 nižší a dosah=200. Přidejte nový objekt do drony, zvyšte vytvoreno a vraťte tentýž objekt. Samotné pridej nemění čas ani cekaji.

**update(dt,hrac,hranice)** při prázdné frontě nic nemění. Jinak přičte čas a za každý celý interval zavolá pridej, odečte interval a jednoho čekajícího. Dohánějte více intervalů, nestačí jediné if. Zbytek zachovejte, po vyčerpání fronty jej vynulujte. Existující drony tato součást neposouvá. Potom je společný pohyb zapojí všechny, včetně právě vytvořených. Při herním dt nejvýše 0,05 s jde nejvýše o sedm pixelů, vstupní odstup chrání hráče před okamžitým zásahem.
