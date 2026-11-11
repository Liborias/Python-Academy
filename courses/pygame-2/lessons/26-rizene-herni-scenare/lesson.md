## Stejný pokus i bez stopování času

Ruční hraní odhalí nepohodlné ovládání, ale těžko dvakrát přesně zopakuje stejný okamžik kolize. Model Kolo už přijímá směr a dt, takže ho můžeme posouvat bez okna, skutečného čekání nebo klávesnice. Řízený pokus má tři vstupy: počáteční seed, posloupnost směrů a délky kroků.

Model_hry.py obsahuje přesné herní třídy z21–25; podklady dodávají stejné obrázky i režimy. Není to zjednodušená náhrada hry. Snimek v scenare.py vytvoří hodnotový záznam, takže pozdější pohyb nepřepíše historii. Import neotevírá okno.

```python
import math
a, b, c = (0, 0), (3, 4), (0, 0)
print('Délka cesty:', math.dist(a, b) + math.dist(b, c))
print('Vzdálenost začátku a konce:', math.dist(a, c))
```

Vypíše se 10 a 0. Celá dráha a vzdálenost od začátku jsou různé veličiny. Podobně shoda konečné polohy neznamená shodu celé herní stopy.

## Čas, vstup a náhoda

Ve skutečném okně dt vzniká z Clock.tick(60), ve scénáři ho zadáme sami. Herní hraniční krok je nejvýše 0,05 s. Seed opakuje posloupnost losování jen při stejné posloupnosti volání. Stejný seed s jinými vstupy nemusí dát stejné dění: vstupní místa závisejí i na poloze hráče.

Nečekáme shodu mezi libovolnými verzemi Pythonu, změněnými pravidly nebo různým rozdělením času. Jde o opakovatelnost stejného modelu a vstupů v daném prostředí. Seed=None záměrně vybírá nový začátek.

## Váš úkol

Vytvořte **prehraj(seed, kroky)**. Vždy založí nové Kolo(seed), do seznamu uloží snimek(kolo) ještě před prvním krokem a pak po každém kolo.update(smer, dt). Vrátí celý seznam. Kroky mohou být i jednorázový generátor dvojic (smer, dt); čtěte ho jen jednou. Každý dt je herní krok 0 až 0,05 s.

Připravená snimek vrací nový slovník: cas (zaokrouhlený na šest desetinných míst), pozice, skore, zivoty, vlna, droni, konec a duvod. Droni jsou n-tice typu a polohy, žádné živé objekty. Nečekejte přes sleep ani tick a neotevírejte okno. Čas předává volající. Po konci model sám nic nemění, ale stopa stále zachytí každý požadovaný krok.
