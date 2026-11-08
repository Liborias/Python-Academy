## Kolik hodnot spadá do kterého intervalu

Histogram rozděluje číselné hodnoty do intervalů a počítá jejich četnosti. Sloupce nyní nejsou názvy nápojů: šířka nese význam rozsahu čísel. `ax.hist(hodnoty, bins=hranice)` v této lekci dostává výslovně určené hranice intervalů. Například [0, 2, 4, 6] znamená tři intervaly, nikoli čtyři sloupce.

```python
from matplotlib.figure import Figure
fig = Figure(layout="constrained")
ax = fig.subplots()
pocty, okraje, obdelniky = ax.hist([0, 1, 2, 2, 3, 4, 6], bins=[0, 2, 4, 6])
ax.set(title="Rozložení dob", xlabel="Doba (min)", ylabel="Četnost")
print("Četnosti:", pocty.tolist())
fig.savefig("graf.png", dpi=120)
```

Hist vrátí počty, okraje a vykreslené obdélníky. Počty zde vyjdou [2.0, 3.0, 2.0]. Intervaly jsou [0, 2), [2, 4), poslední [4, 6] včetně posledního pravého okraje. Hodnota 2 patří do druhého, 4 a 6 do třetího. Hodnoty mimo zadaný rozsah nejsou započtené; součet sloupců pak může být menší než počet původních pozorování. Prázdný seznam s platnými hranicemi dává nulové četnosti.

## Spočítat výsledek odděleně od kreslení

NumPy je číselná knihovna nainstalovaná jako závislost pandas a Matplotlibu. `import numpy as np` dá její obvyklou zkratku. `pocty, okraje = np.histogram(hodnoty, bins=hranice)` vypočítá stejné četnosti bez vytváření Figure. Počty jsou pole NumPy, metoda `.tolist()` z něj vrátí obyčejný seznam celých čísel. Podtržítko v `pocty, _ = ...` jen označuje druhou návratovou hodnotu, kterou zde nepotřebujeme.

Výpočet lze napsat také cyklem; zvlášť je potřeba ošetřit zahrnutí posledního pravého okraje. Kontrola přijímá jiný správný postup. Nevystačíme s round nebo jediným pevným intervalem, protože hranice mohou mít jiné šířky.

## Nula a chybějící doba jsou různé údaje

Před kreslením můžete u float64 Series použít `serie.dropna()`. To vynechá neznámá měření, ale ponechá skutečnou nulovou dobu i názvy řádků. Nahrazení NaN nulou by uměle zvýšilo první interval. V datovém úkolu proto vrátíte očištěnou Series a zachováte původní zdroj.

## Počet, hustota a plocha

Běžné hist počítá četnost. S `density=True` má součet ploch sloupců hodnotu 1: výška krát šířka se sečtou přes všechny intervaly. Výška je četnost intervalu dělená počtem zahrnutých hodnot a šířkou intervalu. Neznamená to, že součet výšek je 1 nebo že každá výška musí být nejvýše 1. Jednotka hustoty je převrácená jednotka x, zde 1/min.

Pro hodnoty [0, 1, 2, 4] a hranice [0, 1, 4] jsou četnosti 1 a 3. Šířky jsou 1 a 3 minuty. Hustoty tedy 1/(4×1)=0,25 a 3/(4×3)=0,25; součet výšek je 0,5, ale plocha 0,25×1 + 0,25×3 = 1. Hustota zde vyžaduje alespoň jednu hodnotu v rozsahu; výpočet nad prázdným výběrem nedává normalizované rozložení.

## Volba intervalů mění vzhled

Jemnější dělení ukáže více podrobností, ale může udělat malé rozdíly nápadnými. Hrubší je může zakrýt. Při porovnání dvou skupin použijeme stejné hranice a společné měřítko y. `fig.subplots(1, 2, sharey=True)` vytvoří dvě Axes se sdílenou svislou stupnicí. Každá skupina pak má svůj titulek Ráno/Večer a celý obrázek společný suptitle. Samotné četnosti stále závisejí na počtu pozorování v každé skupině; u různě velkých skupin může pro jinou otázku dávat smysl hustota.

## Váš úkol

Jedna Axes, běžný sloupcový histogram četností s přesně předanými hranicemi (alespoň dvě přísně rostoucí konečná čísla). Hodnoty jsou seznam konečných čísel, může být prázdný. Intervaly jsou zleva uzavřené a zprava otevřené, poslední zahrnuje i pravý kraj; hodnoty mimo rozsah se nezapočítají. Titulek Rozložení dob, popisky Doba (min), Četnost. Vstupy neměňte.

Dokončete `histogram(hodnoty, hranice)`.

Další úkoly spočítají četnosti bez obrázku, vyčistí Series, vykreslí hustotu a porovnají dvě rozložení. Kontrola skutečně zkouší hraniční hodnoty, mimo rozsah, různé šířky i prázdné vstupy tam, kde jsou přípustné. Barvy a písmo nejsou předepsané.
