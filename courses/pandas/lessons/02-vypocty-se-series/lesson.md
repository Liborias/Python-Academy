## Jeden výpočet pro všechny hodnoty

U seznamu jsme pro převod každé položky často psali cyklus. Series umí použít aritmetický operátor na všechny hodnoty: `ceny / kurz`, `body + bonus` nebo `teploty - 2`. Vznikne nová Series se stejnými popisky a názvem. Původní vstup se tím nemění. Zápis je vektorová operace; pracujeme s celým sloupcem dat.

V ukázce dělíme korunové ceny kladným kurzem Kč za euro. Cvičně volíme 25, nejde o dnešní tržní kurz. Výsledek 50 / 25 je 2. Float je přibližná desetinná aritmetika; později formátujeme zobrazení, nyní výsledek nezaokrouhlujeme. Účetní výpočty vyžadují vlastní pravidla přesnosti.

## Popisky drží související údaje u sebe

Při násobení dvou Series se pandas řídí jejich popisky, ne pouze pořadím položek. Cena s indexem caj se spojí s počtem pro caj i tehdy, když je druhá Series v jiném pořadí. V doplňkovém úkolu zaručujeme stejné jedinečné popisky v obou vstupech. Chybějící protějšky a spojování nestejných dat přijdou později.

`(ceny * pocty).sort_index().rename("trzba")` nejprve provede násobení, seřadí výsledek podle indexu a pojmenuje celou Series. Metody se volají nad výsledkem předchozí operace. Sort_index zachová spojení popisku a hodnoty; neřadí podle velikosti hodnot.

## Souhrny a prázdná data

`serie.sum()` vrátí součet a `serie.mean()` aritmetický průměr. Ve výchozím nastavení vynechají chybějící hodnoty. Pro [10, None, 20] je součet 30 a průměr 15: dělí se dvěma skutečně dostupnými hodnotami. Prázdná Series má při tomto výchozím chování součet 0 a průměr NaN. NaN se za nulovou hodnotu nevydává.

Odchylku od průměru vytvoříme jako `serie - serie.mean()`. Od každého dostupného měření se odečte stejný průměr. Původní chybějící místo zůstane NaN. Ke všem hodnotám lze obdobně přidat předaný bonus. Všechny tyto operace vracejí data; print používáme až pro jejich zobrazení.

## Váš úkol

Dokončete `preved_na_eura(ceny_kc, kurz)`. Vstup je float64 Series s cenami a konečný kladný číselný kurz Kč za euro. Vraťte každou cenu dělenou kurzem, bez zaokrouhlení a beze změny vstupu. Zachovejte popisky, name i chybějící místa. Prázdná Series je platná.

Změňte pořadí názvů zboží a zkuste jiný kurz. U dalších úkolů porovnejte násobení podle popisků se souhrnem, odchylkou a bonusem. Kontrola porovnává výsledky včetně indexu a názvu a dovolí malé běžné odchylky desetinné aritmetiky.
