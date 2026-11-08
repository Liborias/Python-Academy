## Kurz není jen jedno číslo

Převodník měn spojí načtení na pozadí, ověření dat a vlastní výpočet. Vyberete EUR nebo USD a Cvičné API nebo Cvičný soubor. Oba zdroje jsou místní a smyšlené; jejich různé datum a hodnoty jsou záměrné. API má EUR=25, USD=20 a datum 2026-01-15. Soubor kurzy.json má EUR=24, USD=19 a datum 2026-01-14. Nejde o automatickou zálohu ani aktuální tržní data: uživatel zdroj vybere a musí jej v okně poznat.

Kurz je vždy CZK za jednu jednotku vybrané měny. Částku v EUR nebo USD proto kurzem násobíme. Jedna EUR při kurzu 25 dá 25 CZK, dvě EUR 50 CZK. Program neprovádí opačný převod, směnu ani platbu.

## Stejné ověření pro API i soubor

Připravené kurzy.py je přesná kopie lekce 14. Funkce over_kurz ověří i záznam načtený z JSON souboru, proto mají oba zdroje stejné požadavky na měnu, kladný konečný kurz, datum a zdroj. Při kopírování projektu mimo Akademii patří vedle programu cvicne_api.py, kurzy.py a kurzy.json z files. Relativní cesta souboru vychází z pracovní složky; v terminálu se před spuštěním přepněte do složky projektu.

Nacti_kurz_soubor vybere z JSON slovníku záznam podle měny a předá jej over_kurz. Neplatný či chybějící soubor se zobrazí jako neúspěšné načtení. API používá místní pomalý režim, aby šla odezva okna vyzkoušet. Soubor může být rychlejší, přesto používá stejný vzor pracovníka a fronty.

## Změna volby zneplatní načtený kurz

Během načítání jsou volby i další načtení zakázané. Entry zůstane použitelné, ale Převést je disabled. Pracovník dostane měnu a zdroj jako obyčejné texty a výsledek předá přes Queue. Tk zůstává jen v hlavním vlákně, stejně jako minule.

Po úspěchu uložíme ověřený záznam do seznamu nacteno s jediným prvkem a povolíme převod. Seznam zde dovoluje callbackům měnit obsah bez přiřazování nového objektu jménu. Nacteno[0] tedy znamená jediný právě platný kurz. Při novém načítání nebo změně měny či zdroje se vyprázdní přes clear. Radiobutton má pro tuto akci command=zmen_volbu. Starý výsledek i kurz se skryjí a Převést čeká na nové načtení. Nesmí se tak použít EUR kurz pro nově vybraný USD ani starý kurz po chybě.

## Výpočet a zobrazení mají různou přesnost

Preved_castku(castka, kurz) vrací číselný součin bez zaokrouhlení. Přijímá konečné číslo int/float pro nezápornou částku a kladný kurz. Bool, NaN, nekonečno, neplatné typy i přetečení odmítá ValueError. Čísla převádíme na float a příliš velký int překládáme z OverflowError na ValueError, stejně jako při ověření kurzu. Podobné kontroly už znáte z převodníku vzdálenosti.

Callback preved přečte aktuální Entry, přijme desetinnou čárku i tečku a použije načtený kurz. Výsledek v okně formátuje přes .2f na dvě desetinná místa. Běžné float je pro tuto ukázku dostačující, ale kvůli binární reprezentaci není plnohodnotnou účetní aritmetikou; finanční výpočty by potřebovaly přesně stanovené zaokrouhlování a například decimal.Decimal. Zde se učíme spolupráci GUI a dat.

Při chybě částky nezahodíme ověřený kurz, jen skryjeme chybný výsledek. Uživatel částku opraví a zkusí znovu. Při chybě načítání naopak žádný platný kurz nemáme a další převod zůstane zakázaný. Entry se při žádné z těchto operací nemaže.

## Váš úkol

Dokončete preved_castku a část callbacku preved. Zbytek načítání a rozložení je připravený podle minulé lekce. Výpočet vrací číslo; callback zobrazí Výsledek: 250.00 CZK pro 10 EUR z API a hlášení Převod dokončen. Jde o cvičný výpočet. Neplatná částka zobrazí Zadejte platnou nezápornou částku. a původní výsledek skryje.

Vyzkoušejte 10 EUR z obou zdrojů: API dává 250.00 CZK, soubor 240.00 CZK, a v okně vidíte jejich různé datum i zdroj. Po změně měny či zdroje se nejprve musí načíst nový kurz. Ověřte také nulu, zápornou částku, prázdné pole, inf, desetinnou čárku a opravu po chybě. Během načítání zkuste psát do Entry; okno má reagovat a žádné druhé načítání ani změna volby se nesmí spustit.
