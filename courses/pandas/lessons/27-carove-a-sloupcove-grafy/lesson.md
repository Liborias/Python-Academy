## Čára říká, že pořadí má význam

Čárový graf použijeme pro vývoj: například den a teplotu. `ax.plot(dny, hodnoty, marker="o")` používá skutečné hodnoty x, nikoli automaticky jejich pořadová čísla. Dny 1, 3 a 7 proto nebudou stejně daleko od sebe. Čára spojuje body v dodaném pořadí a sama data neseřadí.

```python
from matplotlib.figure import Figure
fig = Figure(layout="constrained")
ax = fig.subplots()
ax.plot([1, 3, 7], [8.0, float("nan"), 9.0], marker="o")
ax.set(title="Chybějící měření", xlabel="Den", ylabel="Teplota (°C)")
fig.savefig("graf.png", dpi=120)
```

NaN v řadě přeruší čáru. Kdybychom hodnotu nahradili nulou, tvrdili bychom nulovou teplotu. Kdybychom řádek prostě odstranili, spojili bychom jeho sousedy přes chybějící údaj. Obojí může změnit význam. Značky ukazují známá měření; spojnice není důkaz, že mezi nimi probíhal vývoj právě takto.

U neuspořádané tabulky nejdřív vytvoříme kopii pomocí `sort_values("den", kind="stable")`, pak kreslíme její sloupce den/hodnota. Stable zachová pořadí shodných dnů; opakované pozorování samo není chyba. Původní tabulku nepřepisujeme. Tohle pravidlo jste už procvičili při řazení dat.

## Sloupec porovnává kategorie

`ax.bar(nazvy, pocty)` vytvoří svislé sloupce. Názvy kategorií mají pořadí, které mu předáme, ale čára mezi čajem a kávou by naznačovala neexistující průběh. V těchto úkolech jsou názvy jedinečné: opakovaný textový název by mohl vykreslit sloupce na stejné místo a překrýt je. Opakované záznamy nejdřív vědomě agregujeme, pokud je taková otázka cílem.

`ax.set_ylim(bottom=0)` nastaví dolní mez y na nulu, horní se přizpůsobí datům. Délka sloupce vyjadřuje velikost, proto by useknutí spodku mohlo rozdíl přehánět. I nulová kategorie zůstává v popiscích, přestože její sloupec má nulovou výšku. Se zápornými sloupci by bylo potřeba volit jiná pravidla; zde jsou počty nezáporné.

## Dlouhé názvy a čitelné porovnání

`ax.barh(nazvy, hodnoty)` kreslí vodorovné sloupce: velikost je nyní na x a kategorie na y. `ax.set_xlim(left=0)` nastaví nulový začátek číselné osy. Výchozí první kategorie je dole; `ax.invert_yaxis()` obrátí směr y, takže bude nahoře. Seznam hodnot se tím neobrací ani nepřiřadí jinému názvu.

## Dvě řady musí být rozpoznatelné

Dvě volání plot do stejné Axes přidají dvě čáry. První označíme label="Ráno" a marker="o", druhou label="Večer" a marker="s". Legenda podle label vysvětlí názvy a různé značky pomohou i bez rozlišení barev. Obě řady mají stejné jednotky a stejnou číselnou osu; nemusíme tedy vytvářet dvojitou osu s jiným měřítkem.

## Váš úkol

Vraťte Figure s jednou Axes a jednou čárou se značkou o. Na x použijte skutečné číselné dny, na y hodnoty. Seznamy mají stejnou délku, dny jsou vzestupné; hodnoty mohou obsahovat NaN, které nesmíte doplnit nulou ani odstranit. Titulek Vývoj měření, popisky Den a Hodnota. Prázdné seznamy jsou platné, zdroj neměňte.

Dokončete `vyvoj(dny, hodnoty)`.

Další procvičování zahrnuje svislé sloupce, dvě řady s legendou, vodorovné sloupce a seřazenou kopii tabulky. Kontrola ověřuje skutečné x/y a mezery v datech, značky předepsané zadáním, pořadí kategorií i nulovou základnu; barvu a písmo si zvolte. Všechny funkce vracejí Figure, které uloží zkušební volání do graf.png. Po spuštění v aplikaci uvidíte náhled; v editoru soubor otevřete ze své pracovní složky.
