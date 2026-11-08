## Datum není libovolný text

Text 01.02.2026 má podle českého zápisu znamenat 1. února. V jiném zdroji by pořadí dne a měsíce mohlo být opačné. Místo odhadu proto určíme formát. `pd.to_datetime(serie, format="%d.%m.%Y", errors="coerce")` převede hodnoty na datumy. Značka %d znamená den, %m měsíc a %Y čtyřmístný rok; tečky jsou oddělovače zdroje.

Coerce změní neplatný text, neexistující datum a původně chybějící údaj na NaT, tedy chybějící datum/čas. Kalendář se skutečně kontroluje: 29.02.2024 existuje, 29.02.2026 ani 31.02.2026 nikoli. Výpis potom používá běžný tvar 2026-02-01. Neznamená to, že se prohodil den a měsíc; je to zobrazení již převedené hodnoty.

## Jednotka a časové pásmo

V těchto úkolech výsledek výslovně sjednotíme přes `.astype("datetime64[us]")`. Us znamená mikrosekundy, rozlišení použitého datového typu. Nejde o americké pořadí měsíce a dne. Starší návody často ukazují ns, nanosekundy; pandas 3 může pracovat s různými jednotkami. Jednotku proto čteme z dtype a zde ji pro přehledné výsledky určujeme konkrétně. Astype už známe z předchozí lekce.

V tomto bloku používáme místní kalendářní hodnoty bez časového pásma. Zápis 08:30 sám neurčuje světový okamžik. Časová pásma a jejich převody zde automaticky nedoplňujeme.

## Datum a čas v jednom údaji

Pro text 2026-02-01 08:30 použijeme `format="%Y-%m-%d %H:%M"`. H je hodina ve 24hodinovém zápisu a velké M minuty; malé m stále znamená měsíc. Čas 25:00 je neplatný. Předem známý formát je spolehlivější než zkoušet různé nastavení, dokud se řádek nějak nepřevede.

```python
datumy = pd.to_datetime(serie, format="%d.%m.%Y", errors="coerce")
chybny_text = datumy.isna() & serie.notna()
print(serie.loc[chybny_text])
```

Tato maska označí chybný existující text, nikoli původně chybějící údaj. Funguje stejně jako u čísel. NaT rozeznává isna; kvůli rozpoznání chybějící hodnoty jej nepřevádíme na text. Prázdný řetězec se v úkolu počítá jako neplatný textový zápis.

## Rok a výběr období

`serie.dt.year` získá rok z každé již datové hodnoty. Přístup dt slouží pro datumové vlastnosti podobně jako str pro textové operace. Výsledek převedeme na Int64, aby roky zůstaly celými čísly a NaT dalo pd.NA.

`pd.Timestamp("2026-02-01")` vytvoří jednu datumovou hranici pro porovnání. Dvě porovnání >= a <= spojená přes & vyberou uzavřené období včetně obou mezí. Pořadí tabulky se tím nemění a NaT nevyhoví. Úkol s obdobím zaručuje datumy o půlnoci a meze YYYY-MM-DD. Kdyby sloupec obsahoval i hodiny, hranice do na půlnoc by nezahrnula celý poslední den; pro taková data bychom museli zvolit jiné pravidlo intervalu.

## Váš úkol

Dokončete `preved_data(serie)`. Textová str Series používá český formát DD.MM.YYYY, případně obsahuje neplatný text nebo chybějící hodnotu. Vraťte datetime64[us] Series bez časového pásma; neplatná i chybějící místa jako NaT. Zachovejte name, index a pořadí, prázdný vstup je platný. Původní Series neměňte.

Další čtyři úkoly procvičí čas, rok, období a označení chybných textů. Vyzkoušejte přestupný rok i datum, u kterého by odhad pořadí dne a měsíce mohl dát jiný výsledek.
