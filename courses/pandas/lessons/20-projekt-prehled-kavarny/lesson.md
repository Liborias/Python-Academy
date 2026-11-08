## Otázky malé kavárny

Který den přinesl jakou tržbu? Kolik kusů jednotlivých produktů se prodalo? Souhlasí souhrny s původními položkami? V tomto projektu spojíme výběr, nové sloupce, groupby, pojmenované agregace a kontrolní součty. Jde o jeden celek se dvěma funkcemi, proto jej nerozdělujeme na nesouvisející varianty úkolu.

Soubor prodeje.csv obsahuje vlastní syntetické položky kavárny. Den je text YYYY-MM-DD, produkt textový kód, kusy počet prodaných jednotek na řádku a cena cena jedné jednotky v Kč právě na tomto řádku. Cena se může mezi řádky měnit. Řádek není automaticky jeden zákazník ani celá objednávka. Tržba také není zisk, protože neodečítáme náklady.

## Přečtěte známý formát

Ukázka používá read_csv se středníkem, desetinnou čárkou, UTF-8 a slovníkem dtype. Den a produkt zůstávají str, kusy je int64 a cena float64. Nastavení dtype už známe; zde určí typy rovnou při čtení. Relativní cesta prodeje.csv hledá soubor v pracovní složce. V aplikaci i ve složce otevřené pro editor se pomocné soubory připraví vedle reseni.py. Při ručním běhu v terminálu přejděte do této složky.

Pro úkol dostanete už připravený DataFrame bez chybějících údajů. Obsahuje platné dny v uvedeném formátu, neprázdné kódy produktů, nezáporné celé kusy a konečné nezáporné ceny v běžném rozsahu. Nové sloupce s odlišným typem ani neplatné vstupy zatím neřešíme. Prázdná tabulka se správnými sloupci zde znamená potvrzený prázdný seznam prodejů, nikoli neznámá měření.

## Výpočet začíná na každém řádku

V kopii tabulky vytvoříme trzba = kusy * cena. Teprve potom tržby sčítáme. Násobení součtu kusů průměrnou cenou všech řádků by při různých cenách a množstvích obecně nedalo správný výsledek. Původní cenu, počet kusů ani zdrojovou tabulku nepřepisujeme. Stejně vypadající prodejní řádky automaticky neodstraňujeme jako duplicity: každý předaný řádek zde představuje platnou položku.

Pro každý den a zvlášť pro každý produkt vytvoříme pojmenovanou agregaci: radky používá size, kusy sum počtů a trzba sum vypočtených částek. Zde žádná hodnota nechybí a prázdný platný seznam prodejů má celkem nula; standardní sum je tedy vhodné pravidlo. Dny i produkty řadíme vzestupně. ISO zápis dnů dovoluje technické řazení v kalendářním pořadí, jednoduché produktové kódy nevyžadují české abecední řazení.

## Váš úkol

Dokončete `prehled_kavarny(tabulka)` a `over_soucty(prehled)`. Funkce musí fungovat i nad jinými platnými daty, ne jen nad přiloženým CSV. Vstupy neměňte a číselné výsledky nezaokrouhlujte.

První funkce dostane DataFrame se sloupci den (str), produkt (str), kusy (int64), cena (float64). Vraťte slovník s právě třemi položkami:

- podle_dnu: DataFrame se sloupci den, radky, kusy, trzba, řazený podle dne.
- podle_produktu: DataFrame se sloupci produkt, radky, kusy, trzba, řazený podle produktu.
- celkem: slovník radky, kusy, trzba. Radky je počet všech zdrojových řádků včetně řádků s nulovým množstvím, kusy součet kusů a trzba součet jednotlivých kusy * cena.

Obě tabulky mají RangeIndex bez názvu, klíč typu str, radky a kusy typu int64 a trzba float64. Celkové počty jsou celá čísla a tržba číselná hodnota. Prázdný vstup vrátí prázdné tabulky se stejnými sloupci a typy a celkové nuly.

Druhá funkce dostane slovník stejného tvaru a s těmito typy. Ověří, že v každé z obou tabulek součet radky, kusy a trzba odpovídá příslušné hodnotě celkem. Vraťte True pouze tehdy, když souhlasí všech šest porovnání, jinak False. Struktura je zaručená, nemusíte ošetřovat chybějící klíče nebo špatné typy. Funkce nesmí součty opravovat ani měnit tabulky.

## Proč desetinné tržby neporovnáváme jen přes ==

Počty porovnáme přesně. Částky jsou zde float, a proto mohou součty v různém pořadí nepatrně odlišit poslední desetinná místa. `math.isclose(a, b, rel_tol=1e-12, abs_tol=1e-9)` z knihovny math rozhodne, zda jsou hodnoty v malé toleranci stejné. Rel_tol porovnává rozdíl vzhledem k velikosti hodnot, abs_tol stanoví malou absolutní toleranci také kolem nuly. Toto je pravidlo úkolu pro float; nejde o účetní pravidlo ani zaokrouhlení na koruny. Změnu tržby o celou korunu již kontrola odmítne.

Souhlas součtů je užitečný, ale sám nezaručuje správné rozdělení do skupin. Prohozené tržby mezi produkty mohou mít stejný celkový součet. Proto automatická kontrola porovnává i jednotlivé řádky, klíče a sloupce přehledu.

## Ověření nad přiloženými daty

Soubor má 7 řádků, celkem 15 kusů a tržbu 687 Kč. Denní tržby jsou 270, 148 a 269 Kč. Produktové tržby pro caj, kava a voda jsou 282, 305 a 100 Kč. Jeden řádek má nulový prodej, ale stále se počítá mezi řádky. Všimněte si i změny ceny stejného produktu.

Spusťte ukázku a potom vlastní řešení. Zkuste kopii dat v jiném pořadí nebo s jinými cenami; zdrojové CSV ponechte. Obě tabulky i celkový souhrn musí stále souhlasit. Pomocný README vysvětluje formát a očekávané výsledky. Pod úkolem je možné řešení celého projektu s připomenutím, že správný postup může být i jiný.
