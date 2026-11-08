## Datová analýza v Pandas

**Připraveno 20 ze 42 lekcí.** Začneme vlastními měřeními a ceníkem malé kavárny. Postupně z nich vznikne Analytická dílna: od otázky přes kontrolu dat až po graf a srozumitelnou zprávu. Data jsou cvičná a smyšlená, součástí projektu; jejich získávání nebude záviset na cizí službě.

Kurz navazuje na seznamy, slovníky, funkce a soubory ze Základů Pythonu. Úvod má náročnost 2/4, celek 3/4 kvůli datovým typům, chybějícím hodnotám, spojování tabulek a ověřování výsledků. Odhad je 25–35 hodin základního průchodu; další procvičování podle potřeby.

## Prostředí a způsob práce

Příprava před lekcemi nabízí Windows/macOS/Linux a VS Code/VSCodium/PyCharm. Použijte stejnou .venv pro editor i terminál. Instalaci obstará python tools/setup_env.py --courses pandas. Pandas řady 3 pracuje s tabulkami, matplotlib připraví grafy, openpyxl soubory Excelu a ipykernel volitelné notebooky či buňky. Prvních dvacet lekcí potřebuje pouze pandas.

První čtyři moduly jsou ověřené na Pythonu 3.14.8 s pandas 3.1.1 a NumPy 2.5.4. Ověřená instalace obsahuje také matplotlib 3.11.2, openpyxl 3.1.5 a ipykernel 7.4.0; jejich konkrétní použití přijde v dalších blocích. V prohlížeči spouštíme obyčejné .py soubory. Komentáře # %% dovolují volitelné rozdělení do buněk v podporovaném editoru. Vždy zůstává možnost spustit celý skript v terminálu. Notebook ani Anaconda nejsou podmínkou studia.

Každá dostupná lekce vysvětluje nové operace před použitím. Samostatné lekce 1–19 mají tři přepínatelné ukázky a pět úkolů. Projekt kavárny v lekci 20 tvoří jeden celek se dvěma funkcemi, přiloženým CSV, řešením a pěti kvízovými otázkami; nemá nesouvisející varianty. Každý úkol nabízí možné řešení a kontrolu výsledku na různých vstupech. Jiný správný postup je v pořádku. Další běžná témata budou tento způsob procvičování zachovávat; navazující projektové kroky budou tvořit jeden celek. Odkrytí řešení nepřepisuje rozepsaný kód ani neoznačuje úkol za splněný.

## Modul 1 — Od seznamu k datové tabulce

**Hotovo: lekce 1–5.**

1. Series: hodnoty, popisky indexu, název, float64 a chybějící údaj.
2. Výpočty se Series: vektorové operace, přiřazení podle popisků, součet a průměr.
3. Výběr loc/iloc: popisky proti pozicím, řezy, přejmenování a řazení indexu.
4. První DataFrame: sloupce, záznamy, názvy řádků, head a shape.
5. CSV a první průzkum: oddělovač, desetinná čárka, UTF-8, hlavička a textové kódy.

Výstup: načtená tabulka místních měření, ve které rozumíte řádkům, sloupcům, typům i významu popisků.

## Modul 2 — Vyberte jen to, co potřebujete

**Hotovo: lekce 6–10.** Každá má tři ukázky a pět úkolů s možnými řešeními.

6. Jeden sloupec a více sloupců: Series proti DataFrame.
7. Výběr řádků a sloupců přes loc/iloc v tabulce.
8. Podmínky a logické masky, závorky, & a |, prázdný výběr.
9. Řazení podle hodnot a více klíčů, pořadí a chybějící hodnoty.
10. Nové sloupce a cílené změny přes loc: Copy-on-Write v pandas 3 bez řetězeného přiřazení.

Výstup: přehled vybraných měření a ceník s vypočtenými částkami. Rozlišujete Series/DataFrame, popisky/pozice, &/| a sort_index/sort_values. Umíte stabilní řazení, umístění NaN, zachování indexu a změnu přes loc v samostatné kopii. Návazný blok 11–15 přidává čištění a datové typy.

## Modul 3 — Data nejsou vždy čistá

**Hotovo: lekce 11–15.** Každá má tři ukázky a pět úkolů s možnými řešeními.

11. isna, fillna a dropna: chybějící údaj není nula.
12. Datové typy a to_numeric: ověřit převod i neplatné hodnoty.
13. Datum a čas: to_datetime, formát a chyby převodu.
14. Duplicitní záznamy, jedinečné hodnoty a pravidlo pro ponechání řádku.
15. Textové sloupce: mezery, velikost písmen a čištění bez ztráty původních dat.

Výstup: vyčištěná kopie tabulky a vysvětlení každé provedené změny. Rozlišujete chybějící údaj, prázdný text a neplatný zápis. Umíte Int64 s pd.NA, datumový formát a NaT, pravidlo klíče duplicit i cílené čištění textu. Původní data zachováte pro porovnání. Modul 16–20 pokračuje souhrny a groupby.

## Modul 4 — Ptejte se na souvislosti

**Hotovo: lekce 16–20.** Lekce 16–19 mají po třech ukázkách a pěti úkolech; projekt 20 je jedna ukázka a jedno souvislé zadání s možným řešením.

16. Souhrny sloupců a řádků, axis, count a size.
17. groupby: rozdělení do skupin a jejich porovnání.
18. Více agregací, pojmenované výsledky a přehledná tabulka.
19. Průměr, medián, minimum a maximum: co mohou zakrýt odlehlé hodnoty.
20. Mini-projekt kavárny: tržby podle dne a výrobku, kontrolní součet.

Výstup: odpovědi na konkrétní otázky doložené tabulkou a kontrolou počtů. Rozlišujete řádky, buňky a dostupné hodnoty, neznámý součet a nulu i průměr a medián. Projekt kavárny počítá denní/produktové přehledy a kontrolní součty nad vlastním CSV, zachovává zdroj a nepovažuje řádky za zákazníky. Celkem je dostupných 58 ukázek a 96 úkolů. Další blok 21–25 naváže spojováním tabulek a časem.

## Modul 5 — Spojte tabulky a čas

**Plán: lekce 21–25.**

21. Zarovnání indexu a concat: připojení dalších měření.
22. merge a klíče: propojení objednávek s ceníkem.
23. Typy spojení, validate a kontrola násobení řádků či nespárovaných klíčů.
24. Časový index a výběr období se správným pořadím.
25. Resample a souhrny za den či měsíc, prázdná období.

Výstup: propojená data se zdokumentovanými klíči a pravidly pro časový souhrn.

## Modul 6 — Graf jako odpověď

**Plán: lekce 26–30.**

26. Matplotlib Figure/Axes: titulek, popisky, jednotky a legenda.
27. Čárový a sloupcový graf: vývoj proti porovnání kategorií.
28. Bodový graf: vztah dvou veličin, korelace sama nevysvětluje příčinu.
29. Histogram a rozložení hodnot: volba intervalů a četnosti.
30. Uložení PNG, čitelný rozměr a grafy i bez grafické plochy.

Výstup: několik čitelných grafů s popisem, co z nich lze a nelze vyvodit.

## Modul 7 — Soubory a opakovatelný postup

**Plán: lekce 31–35.**

31. Excel přes openpyxl: list, hlavička a zachování textových kódů.
32. Export CSV v UTF-8, oddělovač a vědomá volba index=False.
33. Export Excelu, více listů a ověření načteného výsledku.
34. Funkce pro načtení, čištění a souhrn: stejný postup nad dalšími daty.
35. Mini-projekt měsíčního přehledu kavárny s tabulkou a grafem.

Výstup: opakovatelný postup, který vytváří nové výstupy a zachovává zdrojová data.

## Modul 8 — Projekt Analytická dílna

**Plán: lekce 36–42.** Projektové kroky na sebe navazují.

36. Otázka, datový slovník, jednotky, zdroje a očekávané sloupce.
37. Načtení a čištění s přehledem odmítnutých či chybějících údajů.
38. Propojení a skupinové souhrny s kontrolou klíčů a součtů.
39. Grafy a stručná zpráva oddělující fakta, domněnky a omezení dat.
40. Testy přes pandas.testing: hodnoty, typy, indexy a krajní případy.
41. Volitelný notebook: restart jádra a spuštění všech buněk od začátku; souběžný běžný skript.
42. Předání projektu: README, závislosti, vstupy, výstupy a závěrečné ověření.

Výstup: malý předatelný analytický projekt, který lze znovu spustit nad stejnými daty a ověřit jeho výsledky.
