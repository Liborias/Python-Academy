## Nejdřív zjistěte, co chybí

Nula může znamenat skutečně naměřenou teplotu nebo žádný prodaný kus. Chybějící údaj znamená, že hodnotu neznáme. Prázdný text je zase platná textová hodnota, dokud si neurčíme pravidlo, že znamená nevyplněné pole. Automatickým nahrazením všeho nulou bychom tyto významy smíchali.

Pandas podle datového typu používá například NaN u float64 nebo pd.NA u typu Int64. Při konstrukci může převést None na odpovídající chybějící hodnotu. `tabulka.isna()` vrátí stejně velkou tabulku bool hodnot: True tam, kde údaj chybí. Nula, False a prázdný text chybějící nejsou. `notna()` je opačná kontrola. Místo porovnávání hodnoty s NaN pomocí == používáme tyto metody.

## Kolik údajů chybí ve sloupci a na řádku

```python
maska = tabulka.isna()
print(maska)
pocty = maska.sum()
neuplne = tabulka[["misto", "teplota"]].isna().any(axis=1)
```

Sum nad bool hodnotami počítá True jako 1 a False jako 0. Výchozí součet po řádcích každého sloupce dá Series s jedním počtem na sloupec. Pořadí názvů zachováme. Ve vzoru navíc `astype("int64")` výslovně nastaví celočíselný typ výsledku, aby jej měl i prázdný přehled bez sloupců. Převody typů podrobně probereme v příští lekci. Any odpovídá, zda existuje alespoň jedno True. Argument axis=1 znamená vyhodnotit sloupce uvnitř každého řádku; výsledkem je jedna bool hodnota na řádek. Při výběru nulového počtu sloupců není co postrádat, takže any vrátí False u všech řádků.

## Doplnění je rozhodnutí o významu dat

`tabulka.fillna({"misto": "neuvedeno"})` vrátí tabulku, kde se chybějící místo doplní tímto textem. Ostatní sloupce se nezmění a existující prázdný text zůstane prázdný. Slovník dovoluje zvolit náhradu pro každý sloupec zvlášť. Hodnota musí odpovídat jeho typu: text do textového, slučitelné číslo do číselného sloupce.

Náhradu nulou použijeme jen tehdy, když podle pravidla dat nula opravdu dává smysl. Neznámou teplotu automaticky nulou nenahrazujeme. V úkolech dostanete konkrétní slovník náhrad a kontrolujeme, že se doplní právě jím určená místa. Samotná fillna bez inplace vstup nepřepisuje.

## Kdy raději řádek vynechat

`tabulka.dropna(subset=["misto", "teplota"])` vrátí řádky, kde nechybí ani jeden z těchto povinných údajů. Chybějící poznámka v jiném sloupci nevadí. Subset tedy určuje, které sloupce posuzujeme; neznamená seznam sloupců, které chceme odstranit. Původní tabulka, index a pořadí ponechaných řádků se zachovají. Před vynecháním si porovnejte počet řádků, abyste věděli, o kolik záznamů analýza přišla.

## Poslední známý stav

`serie.ffill()` doplní chybějící hodnotu posledním dostupným předchůdcem v aktuálním pořadí. Hodí se například pro stav provozovny, který podle zadání trvá do další zaznamenané změny. Na začátku bez známého předchůdce zůstane údaj chybějící. Metoda sama index neřadí. Není to obecné pravidlo pro doplňování teplot, cen ani jiných měření; také zde musí být význam doplnění odůvodněný.

## Váš úkol

Dokončete `chybejici_pocty(tabulka)`. Vraťte Series počtů skutečně chybějících hodnot pro každý sloupec v původním pořadí. Index tvoří názvy sloupců, dtype je int64 a name=None. Nula ani prázdný text se nepočítají. Tabulka může být bez řádků nebo sloupců, obsahuje běžné textové a číselné hodnoty včetně chybějících. Vstup neměňte.

Další čtyři úkoly procvičí náhrady podle slovníku, povinné údaje, masku neúplných řádků a poslední známý stav. Každý má vlastní možné řešení. Před doplňováním nebo odstraňováním si nejprve vytiskněte isna a vysvětlete, které hodnoty vlastně měníte.
