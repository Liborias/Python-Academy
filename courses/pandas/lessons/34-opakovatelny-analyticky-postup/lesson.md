## Stejný postup pro další soubor

Když každou tabulku ručně opravíme jinak, výsledek se špatně opakuje a vysvětluje. Rozdělíme proto práci na načtení/čištění, výpočet a export. Každý krok má známý vstup a výstup; cesta k souboru je parametr, nikoli natvrdo jediný vzorový název.

## Pravidla před kódem

Mereni.csv má textové misto, hodnotu zapsanou s desetinnou čárkou a nepovinnou poznámku. Ořízneme jen krajní mezery. Prázdné místo vyřadíme, doslovný název NA zachováme. Neplatnou či neurčenou hodnotu vyřadíme, platnou nulu ponecháme. Opakované řádky jsou dvě měření, proto je neodstraňujeme. Ostatní sloupce se do čistého výsledku nedostanou. Tento jednoduchý postup vyřazování je výslovně zvolené pravidlo cvičení; u vlastních dat může být vhodný i seznam odmítnutých řádků a důvodů.

```python
import pandas as pd
data = pd.read_csv("mereni.csv", sep=";", encoding="utf-8", keep_default_na=False, dtype="str")
data = data[["misto", "hodnota"]].copy()
data["misto"] = data["misto"].str.strip().replace("", pd.NA)
text = data["hodnota"].str.strip().str.replace(",", ".", regex=False)
data["hodnota"] = pd.to_numeric(text, errors="coerce").astype("float64")
ciste = data.dropna(subset=["misto", "hodnota"]).reset_index(drop=True)
print(ciste)
```

Dtype="str" nejprve načte původní zápis. Keep_default_na=False ponechá texty NA i prázdný text k vlastnímu rozhodnutí. Copy vytvoří samostatnou tabulku. Strip ořízne krajní mezery, replace prázdné místo označí jako chybějící údaj. U hodnoty doslovně nahradíme čárku tečkou; regex=False znamená běžnou textovou náhradu. To_numeric s errors="coerce" vytvoří NaN při neplatném čísle. Astype sjednotí float64 i u prázdného vstupu. Dropna vynechá řádky jen podle dvou důležitých sloupců a reset_index vytvoří nový RangeIndex.

Funkce `zpracuj_mereni(cesta)` má vrátit tuto čistou tabulku. Stejný kód pak funguje nad jiným souborem. Výsledné hodnoty nejsou svévolně zaokrouhlené a zdroj CSV zůstává beze změny.

## Výpočet a připojení zdrojů

Souhrn_mist dostane už čistá data. Groupby podle místa, sort=True a pojmenované agregace pocet/size a prumer/mean vrátí přehled se sloupci misto, pocet a prumer. Počítáme záznamy, ne různé názvy ani počet buněk. Velikost a průměr platně zahrnují nulová i opakovaná měření.

Seznam cest zpracujeme po jedné pomocí hotové funkce a výsledky připojíme přes concat(ignore_index=True). Pořadí je pořadí cest a řádků, nikoli abeceda míst. Prázdný seznam nemá co spojovat, proto vytvoříme prázdný DataFrame s výslovnými typy str/float64.

## Malý modul místo kopírování pěti verzí

Přiložený cisteni.py obsahuje hotové funkce zpracuj_mereni a souhrn_mist. V Úkolech 3 a 5 je načteme pomocí `from cisteni import ...`. Soubor leží vedle pracovního kódu; v aplikaci se přiloží automaticky. Nepřepisujte jej. Jde o dosavadní ověřené kroky, abyste se v novém úkolu soustředili na jejich propojení. Shodu helperu s řešeními předchozích úkolů hlídá test aplikace.

Uloz_souhrn exportuje hotovou tabulku bez indexu, analyzuj_mereni propojí všechny kroky: načte, očistí, spočítá, uloží a vrátí přehled. Návratová tabulka se dá nezávisle porovnat, zatímco skutečný CSV lze znovu přečíst nebo stáhnout z aplikace. Soubory nevznikají jen jako zpráva v konzoli.

## Váš úkol

CSV má středník, UTF-8 a sloupce misto/hodnota, případně další poznámky. Načtěte text bez výchozího převodu NA. Místo ořízněte o krajní mezery; prázdné místo vyřaďte, text NA zachovejte. U hodnoty ořízněte mezery, desetinnou čárku nahraďte tečkou a převeďte na float64; neurčenou/neplatnou hodnotu vyřaďte. Vraťte pouze misto str a hodnota float64, původní pořadí a RangeIndex. Nuly a opakovaná měření ponechte. Zdroj neměňte.

Dokončete `zpracuj_mereni(cesta)`.

U dalších úkolů lze zobrazit jedno možné řešení. Kontrola použije jiný soubor, prázdná data, nulové a opakované hodnoty i neplatné zápisy. V dodaném mereni.csv zůstanou čtyři měření: Brno 1,5; Praha 2,5; NA 0; Brno 1,5. Souhrn je Brno 2/1,5, NA 1/0 a Praha 1/2,5 (počet/průměr).
