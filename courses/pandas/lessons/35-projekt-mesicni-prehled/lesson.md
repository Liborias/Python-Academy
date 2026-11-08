## Jeden přehled, kterému umíme vysvětlit původ

Cílem je vybrat kalendářní měsíc, spočítat tržby kavárny a předat tři skutečné soubory: CSV podle dnů, Excel s více listy a graf tržeb podle produktů. Projekt navazuje na předchozí témata, proto má jeden souvislý úkol se třemi funkcemi, jednou ukázkou a možným řešením. Nepřepínáme zde nesouvisející varianty.

## Zdroj a předpoklady

Přiložený prodeje.csv je smyšlený čistý seznam položek prodeje z ledna až března 2026. Sloupce den/produkt jsou text, kusy int64 a cena float64 s desetinnou čárkou. Datum převedeme na datetime64[us] bez NaT a pásma. Počet kusů i cena jsou nezáporné a známé; nulový počet je platný. Text NA je skutečný produkt, ne chybějící údaj. Každý řádek je položka, nikoli zákazník. Dvě stejné položky neodstraňujeme jako chybnou duplicitu. Cena platí pro konkrétní řádek.

Kavarna.py obsahuje hotové prehled_kavarny a over_soucty z projektu 20. Součty proto nemusíte znovu opisovat; soubor se přiloží v aplikaci i pracovním editoru. V tomto projektu se zaměříte na měsíční výběr a předání výsledků. Zdroj ani helper nepřepisujte.

```python
import pandas as pd
data = pd.read_csv("prodeje.csv", sep=";", decimal=",", encoding="utf-8",
                   keep_default_na=False,
                   dtype={"den":"str", "produkt":"str", "kusy":"int64", "cena":"float64"})
data["den"] = pd.to_datetime(data["den"], format="%Y-%m-%d").astype("datetime64[us]")
zacatek = pd.Timestamp("2026-02-01")
konec = zacatek + pd.offsets.MonthBegin(1)
unor = data.loc[(data["den"] >= zacatek) & (data["den"] < konec)].copy()
print(unor)
```

MonthBegin(1) posune začátek na první den dalšího měsíce, i přes konec roku. Nepřičítáme třicet dní. Levá hranice je včetně, pravá bez ní; březnová půlnoc nepatří do února a přestupný únor má 29 dní. Parametr mesic bude platný text YYYY-MM. Výběr zachová původní index, pořadí a sloupce.

## Tři navazující funkce

`vyber_mesic(tabulka, mesic)` vrátí samostatnou kopii pouze vybraných řádků. Vstup má den datetime64[us], produkt str, kusy int64 a cena float64. Prázdný vstup i měsíc bez prodeje jsou platné. Původní data neměňte.

`prehled_mesice(tabulka, mesic)` použije výběr. Pro helper kavárny převede den v této kopii zpět na text přes `data["den"].dt.strftime("%Y-%m-%d").astype("str")`. Strftime formátuje datum, nepřesouvá jej do jiného dne. Vrátí stejný slovník jako projekt 20: podle_dnu (den/radky/kusy/trzba), podle_produktu (produkt/radky/kusy/trzba) a celkem (radky/kusy/trzba). Klíče jsou řazené, počty int64 v tabulkách, tržba float64. Prázdný potvrzený seznam prodejů znamená celkové nuly a prázdné souhrnné tabulky, nikoli neznámá měření. Výpočet je kusy × řádková cena; nezaokrouhlujte mezivýsledky. Tržba není zisk.

`uloz_report(prehled, slozka)` složku vytvoří včetně rodičů a vrátí slovník csv/excel/graf s Path k následujícím výstupům. Přehled ani jiné soubory ve složce nezmění, tyto tři pojmenované výstupy může nový běh přepsat.

- `podle_dnu.csv`: UTF-8 bez BOM, středník, desetinná čárka, hlavičky den/radky/kusy/trzba bez indexu.
- `prehled.xlsx`: listy Dny, Produkty a Celkem v tomto pořadí, tabulky bez indexu; Celkem je jeden řádek hodnot radky/kusy/trzba. Názvy souborů v kódu pište malými písmeny podle šablony: podle_dnu.csv a prehled.xlsx.
- `trzby.png`: Figure 6 × 4 palce, DPI 120, jedna Axes se sloupci tržeb v pořadí produktů, osa y od nuly. Titulek Měsíční tržby podle produktů, popisky Produkt a Tržba (Kč). U prázdného přehledu vznikne platný prázdný graf. Soubor se jmenuje trzby.png.

Složku vytvoří `Path(slozka).mkdir(parents=True, exist_ok=True)`. Do jednoho ExcelWriter zapíšete oba přehledy a `pd.DataFrame([prehled["celkem"]])`, která převádí slovník celkových hodnot na jednořádkovou tabulku. Figure a export PNG znáte z lekcí 26–30; zde propojujete stejné kroky. Barvu a písmo si můžete zvolit.

## Jak poznáme správný výsledek

Dodaný únor má šest řádků, deset kusů a 563 Kč. Denní tržby jsou 270, 45 a 248 Kč. Produkt caj má 135 Kč, kava 428 Kč a doslovný produkt NA nulovou tržbu. Právě dvě stejné položky z 28. února se obě započítají. Lednový ani březnový řádek ve výsledku není. Přehled nevyplňuje dny bez prodeje; obsahuje dny přítomné ve zdroji.

Kontrolujte součty i jednotlivé řádky. Samotný shodný součet by neodhalil prohozené skupiny. Automatická kontrola počítá očekávané přehledy nezávislým Python cyklem a zkouší jiná data, hranice měsíce, přestupný den i konec roku. Exporty skutečně otevře a porovná tabulky i data grafu, nestačí vytvořit prázdné soubory.

Po spuštění ukázky v aplikaci uvidíte PNG a odkazy ke stažení CSV/XLSX včetně zdroje. Předávané výstupy jsou ve složce vystupy. Po reloadu se nové odkazy vytvoří spuštěním zachovaného kódu. V editoru výstupy zůstanou na disku v pracovní složce procesu. Přiložené README připomíná význam dat a očekávaná čísla.
