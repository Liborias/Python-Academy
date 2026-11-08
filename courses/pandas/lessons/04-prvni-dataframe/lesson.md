## Dva rozměry dat

Series představovala jednu řadu hodnot. DataFrame je tabulka s řádky a sloupci; má index řádků i názvy sloupců. Každý sloupec může mít vlastní datový typ. V našich příkladech má místo textový typ str, teplota float64 a příznak může být bool.

`pd.DataFrame(data)` vytvoří tabulku ze slovníku, v němž každý klíč pojmenuje sloupec a každý seznam obsahuje jeho hodnoty. Seznamy mají shodnou délku. Zachová se pořadí vložených klíčů. Bez vlastních popisků se použije číselný RangeIndex začínající nulou. Prázdný slovník vytvoří tabulku bez řádků i sloupců.

V pandas 3 je odvozený textový sloupec běžně typu str; nemusí se zobrazovat jako object ze starších návodů. Datové typy se proto učíme číst ze skutečného výsledku, ne odhadovat podle starého obrázku výpisu.

## Slovník sloupců a seznam záznamů

Tabulku lze vytvořit také ze seznamu slovníků, kde každý slovník popisuje jeden řádek. `pd.DataFrame(zaznamy, columns=sloupce)` vybere zadané sloupce a určí jejich pořadí. Pokud jednomu řádku některá hodnota chybí, objeví se chybějící údaj. Necháváme pandas odvodit typ jednotlivých sloupců.

Argument index dovolí místo čísel použít vlastní řádkové popisky. Opět musí odpovídat počtu řádků. Tím se hodnoty nezmění, pouze je lépe identifikujeme. Zachování názvů a pořadí je stejně důležité jako samotná čísla.

## Krátký průzkum tabulky

Vlastnost shape vrací n-tici (počet řádků, počet sloupců). Columns a index poskytují obě sady popisků; pro běžný seznam lze použít jejich tolist. Dtypes vrací Series s typem každého sloupce.

Metoda head(n) vrátí prvních n řádků se stejnými sloupci a typy. Pro n=0 je výsledek bez řádků, ale se sloupci. Pokud požadujete více řádků, než tabulka má, vrátí je všechny. Head je náhled, původní tabulku nezkrátí. Srovnejte shape celého vstupu a jeho náhledu.

## Váš úkol

Dokončete `vytvor_tabulku(data)`. Vstup je slovník textových názvů sloupců a stejně dlouhých seznamů hodnot. Vraťte DataFrame v pořadí sloupců slovníku, s výchozím indexem a typy odvozenými pandas. Vstup neměňte. Platný je i prázdný slovník nebo slovník s prázdnými seznamy.

Další čtyři úkoly procvičí záznamy po řádcích, vlastní index, náhled a rozměry. Sloupce nejsou řádky: při kontrole shape si vždy ověřte pořadí obou čísel.
