## CSV je text s pravidly

CSV ukládá řádky a sloupce jako text. Může používat čárku nebo středník a hodnoty v uvozovkách mohou obsahovat oddělovač i nový řádek. Proto pro načtení použijeme parser pandas, nikoli prosté split nebo počítání fyzických řádků souboru.

Soubory v této lekci jsou vlastní syntetická data v UTF-8. Při otevření lekce v editoru se zkopírují vedle reseni.py; při běhu z prohlížeče je server vloží k dočasnému kódu. Relativní cesta "mereni.csv" se vyhodnocuje vůči pracovní složce. V terminálu proto přejděte do pracovní složky lekce, případně předejte úplnou cestu.

## Oddělovač a desetinný znak

`pd.read_csv(cesta, sep=";", decimal=",", encoding="utf-8")` otevře soubor a vrátí DataFrame. Sep odděluje sloupce, decimal určuje znak desetinné části čísel a encoding kódování textu. Jsou to různé vlastnosti: čárka v čísle 18,5 není v našem souboru hranice sloupce.

První řádek je zde hlavička s názvy misto, teplota, vlhkost, a proto se mezi datové záznamy nezahrnuje. Načtená čísla jsou skutečná čísla, nikoli texty obsahující čárku. Automatický index je oddělený od sloupců ze souboru. Uvozovky zajistí, že se text "Čaj, velký" nebo víceřádková poznámka nerozbije na několik záznamů.

## Jiný soubor potřebuje jiné nastavení

Ceník cenik.csv používá čárku mezi sloupci a desetinnou tečku; tam použijeme sep="," a výchozí desetinnou tečku. Bez-hlavicky.csv záhlaví nemá: `header=None` zabrání použití prvního měření jako názvu sloupců a `names=["misto", "hodnota"]` jim dá naše názvy. Tyto argumenty používáme podle známého formátu, ne náhodným zkoušením, dokud něco neprojde.

Identifikátory nejsou vždy čísla pro výpočty. U kódu 001 záleží na počátečních nulách. `dtype={"kod": "str"}` určí textový typ tohoto sloupce, ostatní typy ponechá odvozené. Řetězec 001 se pak nezmění na celé číslo 1. Zadání zaručuje neprázdné kódy a celé počty kusů.

## První průzkum

Po načtení vytiskněte tabulku, head, shape a dtypes. Zjistíte, zda odpovídá počet řádků/sloupců, názvy i typy. `len(tabulka)` vrací počet datových řádků. V řádně uzavřeném textovém poli může být Enter, proto tento počet nemusí být počet znaků nového řádku mínus jedna. Soubory s hlavičkou a žádnými záznamy mají počet nula.

V tomto bloku dostáváme existující místní soubory známého formátu a nesmíme je přepisovat. Ošetření chyb souboru, neplatných dat a čištění přidáme v dalších lekcích. Dnes ověřujeme, že parser použijeme podle zadaného formátu a výsledek vrátíme volajícímu.

## Váš úkol

Dokončete `nacti_mereni(cesta)`. Načtěte celý místní CSV soubor s hlavičkou, oddělovačem středníkem, desetinnou čárkou a kódováním UTF-8. Vraťte DataFrame se všemi řádky a sloupci, výchozím indexem a odvozenými typy. Soubor neměňte.

Další zadání mění formát, přítomnost hlavičky, význam kódu a otázku na počet řádků. Každé má vlastní možné řešení. Při zkoušení upravujte kopii cvičných dat a porovnejte předpověď s tím, co parser skutečně načetl.
