# Datový slovník

| Zdroj | Sloupec | Význam a pravidlo |
| --- | --- | --- |
| mereni.csv | den | text data; převod s formátem %Y-%m-%d, bez časového pásma |
| mereni.csv | kod | text stanice včetně nul a NA, oříznout jen krajní mezery |
| mereni.csv | teplota | °C, desetinná čárka, platné jsou i nula a záporná konečná čísla |
| mereni.csv | poznamka | nepovinná poznámka, nerozhoduje o platnosti měření |
| mista.csv | kod | jedinečný neprázdný textový klíč bez chybějících hodnot |
| mista.csv | nazev | jméno stanice, známý text |
| mista.csv | oblast | oblast stanice, známý text |

Radek ve výstupu je pořadí záznamu od 1, nikoli index DataFrame ani fyzický řádek souboru s uvozovanými novými řádky.
Důvody odmítnutí mají pořadí: chybi_kod, neplatne_datum, neplatna_teplota. Uvádíme první důvod, ne všechny najednou.
Neznámý neprázdný kód není chyba čísla/datu: zůstane mezi čistými záznamy a oddělí se při spojení jako nespárovaný.
Výchozí soubor: 11 vstupů = 4 odmítnuté + 1 nespárovaný + 6 spárovaných měření.
