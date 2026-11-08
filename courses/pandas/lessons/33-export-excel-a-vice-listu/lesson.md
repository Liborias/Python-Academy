## XLSX uchová více než prostý text

Sešit má listy a buňky s typy. Číslo ceny uložíme jako číslo, identifikátor 001 jako text. Výsledek má být čitelný i po novém načtení. Použijeme pandas a openpyxl ze stejné .venv jako v lekci 31; Excel nemusí být nainstalovaný.

```python
import pandas as pd
data = pd.read_csv("data.csv", sep=";", decimal=",", encoding="utf-8",
                   keep_default_na=False, dtype={"kod":"str", "nazev":"str", "cena":"float64"})
with pd.ExcelWriter("prehled.xlsx", engine="openpyxl") as zapis:
    data.to_excel(zapis, sheet_name="Ceník", index=False)
    data[["kod", "nazev"]].to_excel(zapis, sheet_name="Kódy", index=False)
print(pd.read_excel("prehled.xlsx", sheet_name="Ceník", engine="openpyxl",
                    keep_default_na=False, dtype={"kod":"str", "nazev":"str", "cena":"float64"}))
```

To_excel uloží tabulku do listu sheet_name, index=False vynechá řádkové popisky a zachová datové hlavičky. Při jedné tabulce může dostat přímo cestu. Pro více tabulek použijeme jeden ExcelWriter, tedy správce zápisu do společného sešitu. With na konci uloží a zavře celý soubor i uvolní prostředky. Výsledek ověřujte až po opuštění tohoto bloku.

## Více listů patří jednomu writeru

Dvě nezávislá volání to_excel se stejnou cestou by obvykle vytvořila druhý nový sešit a první výstup přepsala. Zde oba listy zapisujeme do stejného otevřeného writeru. Vytváříme nový sešit, neřešíme připojování do cizího existujícího souboru. Používejte jinou cestu než pro vstup; při novém spuštění se právě zvolený výstup může přepsat.

Slovník `{jmeno: tabulka}` dovolí zapsat další listy cyklem přes items(). Pořadí slovníku je pořadí listů, ne abecední seznam. Každá tabulka má vlastní schéma; i prázdná má své hlavičky. Jména listů musí být platná pro Excel (nejvýše 31 znaků a bez zakázaných znaků jako / nebo *); v úkolech je tato podmínka zaručená.

## Textový typ není zobrazovací formát

Kódy vstupují jako str a tak se mají uložit i do buněk. Nastavit číslu 1 formát 000 by pouze změnilo zobrazení; číselná hodnota zůstane 1. V Úkolu 4 proto kontrola ověří i skutečný typ buňky, ne jen to, jak ji tabulkový program ukazuje. Nuly musíme chránit už při původním čtení, z neúplné informace je později neuhádneme. Doslovné NA nepovažujeme za chybějící kód.

Naše cvičná data obsahují běžný text a čísla, ne excelové vzorce. Zápis/čtení hodnot neznamená automatický přepočet vzorců jiného sešitu; tomu by odpovídal jiný postup a další předpoklady.

## Přečíst konkrétní list a porovnat

Stejně jako u CSV ověříme sloupce, pořadí a hodnoty po novém načtení. Read_excel dostane jméno listu a správné dtype, nikoli jen první list. Assert_frame_equal porovná tabulky s malou tolerancí čísel 1e-12, textové kódy přesně. Kontrola skutečných buněk může navíc ověřit, zda kod není omylem uložen jako číslo. False při změně hodnoty je užitečnější než True jen proto, že soubor existuje.

## Váš úkol

Tabulka má kod/nazev str a cena float64 bez chybějících hodnot, včetně textových kódů 001 a NA. Vytvořte XLSX s právě jedním listem podle parametru. Zachovejte hlavičky, pořadí a skutečné textové typy kódů, neexportujte index. Prázdná tabulka má hlavičky. Název je platný, rodič cesty existuje; vraťte Path, zdroj neměňte.

Dokončete `uloz_excel(tabulka, cesta, list)`.

Další procvičování zapíše dvě tabulky, slovník listů, skutečné textové kódy a ověří hotový list. V aplikaci jsou XLSX ke stažení po dokončení běhu, v editoru zůstávají v pracovní složce. Kontrola otevře skutečný sešit a zkouší listy, hlavičky, typy buněk, čísla i prázdné tabulky; správný alternativní postup je v pořádku.
