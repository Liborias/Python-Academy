## Kdy jsou dva záznamy stejné

Dvakrát načtený řádek může být chyba importu. Dvě objednávky stejného produktu však mohou být dva skutečné obchody. Nejdřív určíme, podle čeho shodu posuzujeme. V první úloze porovnáváme hodnoty všech sloupců, v dalších jen zadaný klíč. Index je v těchto cvičeních popisek řádku, nikoli součást datového klíče.

`tabulka.drop_duplicates(keep="first")` vrátí první výskyt každé kombinace hodnot všech sloupců. Řádky se stejným kódem a různou cenou proto zůstanou oba. Původní popisky a pořadí ponechaných řádků se zachovají, vstup se bez inplace nezmění. Po odstranění si porovnejte počet řádků a ověřte, zda použité pravidlo odpovídá zdroji.

## Klíč a poslední výskyt

```python
posledni = tabulka.drop_duplicates(subset=["kod"], keep="last")
vsechny_shody = tabulka.duplicated(subset=["kod"], keep=False)
```

Subset vyjmenuje sloupce klíče. Keep="last" ponechá poslední výskyt podle současného pořadí tabulky. Není to automaticky nejnovější čas; k tomu bychom museli nejprve vyřešit pořadí dat a případné shody času. Výsledné řádky se neobracejí: zůstávají v pořadí, v jakém se v tabulce nacházely.

Více názvů v subset vytvoří složený klíč. Stejný kód s jinou cenou pak může tvořit jinou skupinu. Při detekci duplicit pandas seskupuje i odpovídající chybějící hodnoty. Chybějící identifikátor proto není automatická záruka jedinečnosti; při práci se skutečnými daty musíme rozhodnout, zda je vůbec platným klíčem.

## Označit není totéž co odstranit

Duplicated vrací bool Series se stejným řádkovým indexem. Keep=False označí všechny členy opakované skupiny včetně prvního. Výchozí keep="first" první výskyt neoznačí a True dá až dalším. Pro kontrolní přehled všech podezřelých řádků tedy zvolíme False a potom můžeme masku předat loc. Funkce duplicated sama řádky nevyřazuje.

## Jedinečné hodnoty a četnosti

`serie.drop_duplicates().tolist()` vrátí běžný seznam hodnot podle prvního výskytu. Není to abecední řazení a není to neuspořádaná množina. V tomto úkolu má Series textové hodnoty bez chybějících údajů; prázdný text je platná hodnota.

`serie.value_counts(dropna=False, sort=False)` vrátí Series četností. Dropna=False zahrne i chybějící hodnotu, která se jinak standardně vynechává. Sort=False ponechá skupiny v pořadí prvního výskytu, ne podle počtu. Pro [B, A, B, chybí, C, chybí] jsou počty 2, 1, 2, 1 v pořadí B, A, chybí, C. U našeho str vstupu má výsledek dtype int64 a name="count"; jeho index nese původní název Series. Součet četností se tak rovná celkovému počtu prvků včetně chybějících.

## Váš úkol

Dokončete `odstran_duplicity(tabulka)`. Tabulka má alespoň jeden sloupec běžných textových nebo číselných hodnot, případně chybějící údaje. Vraťte jen první výskyt každého celého datového řádku podle všech sloupců. Index se do porovnání nepočítá; původní index, typy, pořadí řádků a sloupců zachovejte. Prázdná tabulka se sloupci je platná, vstup neměňte.

Další úkoly procvičí poslední výskyt podle klíče, masku všech duplicit, jedinečné texty a počty včetně chybějících hodnot. U každého výsledku si vysvětlete, proč některé stejně vypadající záznamy zůstaly a jiné se vyřadily.
