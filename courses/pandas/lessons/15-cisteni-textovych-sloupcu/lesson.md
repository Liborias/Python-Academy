## Praha, PRAHA a mezery navíc

Před seskupováním potřebujeme vědět, zda hodnoty "Praha", " PRAHA " a "praha" představují stejnou kategorii. Samotná odlišnost textu ale není vždy chyba: velikost písmen může být důležitá například v kódu. V úkolech proto vždy určujeme, které úpravy se mají provést a co se má zachovat.

`serie.str.strip()` odstraní bílé znaky pouze na okrajích jednotlivých textů. `serie.str.lower()` převede písmena na malá včetně české diakritiky. Spojením `.str.strip().str.lower()` vznikne například z " ŽĎÁR  " hodnota "žďár". Vnitřní mezery tím nezmizí. Vstup má dtype str a obsahuje text nebo chybějící údaj; metody zachovají index, name a chybějící místa. Původní Series se nemění.

Nejprve používáme skutečné textové operace, nepřevádíme chybějící hodnoty na obyčejná slova "nan" nebo "None". Změna na malá písmena neodstraňuje diakritiku a automaticky nevyřeší všechny názvové varianty stejného místa.

## Jedna mezera mezi slovy

```python
ciste = serie.str.strip().str.replace(r"\s+", " ", regex=True)
```

Zde záměrně používáme regulární výraz. Značka \s odpovídá bílému znaku a + znamená jeden nebo více výskytů za sebou. Patří sem mezera, tabulátor, nový řádek i nezlomitelná mezera. Každý takový souvislý úsek nahradíme jednou běžnou mezerou. Písmeno r před řetězcem zachová zpětné lomítko pro výraz; regex=True zapíná jeho vyhodnocení. Strip před náhradou odstraní také okrajové úseky. Velikost písmen se v tomto samostatném úkolu nemění.

V lekci o číslech jsme pro náhradu čárky používali regex=False, protože šlo o doslovný znak. Rozdíl je důležitý například u tečky: v regulárním výrazu má zvláštní význam. Pokud nahrazujeme obyčejný text, nastavíme doslovnou náhradu.

## Jednotka jen na konci

`serie.str.strip().str.removesuffix("kg").str.strip()` nejprve ořízne okraje, pak odstraní právě jednu přesnou koncovou příponu kg a znovu ořízne zbytek. Z " 12 kg " vznikne "12", ale "kg12" a "12 kg navíc" zůstanou zachované. Removesuffix pracuje s doslovným textem a nepoužívá regex. Hodnoty zatím zůstávají textové, převod na čísla je samostatný krok z lekce 12.

## Prázdný text teprve podle pravidla

Strip může z několika mezer udělat prázdný text, ale ten stále není NaN. Pro úkol, kde prázdné pole znamená chybějící údaj, použijeme `ciste.replace("", float("nan"))`. Series.replace zde mění celé hodnoty rovné prázdnému řetězci. Je to jiná operace než str.replace, která nahrazuje části uvnitř textů. Neprázdné texty a původně chybějící údaje zůstanou zachované.

Ve skutečné tabulce můžeme mít vedle místa poznámku, jejíž mezery a velikost písmen mají zůstat původní. V posledním úkolu vytvoříme kopii tabulky a upravíme jen předaný sloupec. Čištění samo neodstraňuje duplicity ani řádky; po sjednocení názvů teprve posuzujeme, co má být jedinečné.

## Váš úkol

Dokončete `vycisti_text(serie)`. Vraťte str Series po oříznutí okrajových bílých znaků a převodu písmen na malá. Vnitřní mezery, diakritiku, prázdné texty, index, name a chybějící hodnoty zachovejte. Prázdný vstup je platný a původní Series se nesmí změnit.

Další čtyři úkoly samostatně procvičí sjednocení bílých znaků, koncovou příponu, prázdné hodnoty a vybraný sloupec. Každý má vlastní možné řešení; žádný krok se nemá provést navíc jen proto, že je obvyklý v jiném příkladu.
