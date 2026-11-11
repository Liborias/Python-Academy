## Počet vlastních tabulek

Vytvořte **pocet_tabulek(cesta)**. Otevře databázi, spočítá její vlastní tabulky v hlavním schématu a po zavření vrátí int. Pohledy a indexy se nepočítají, stejně tak interní jména začínající sqlite_. Prázdná ':memory:' databáze má nulu.

`sqlite_schema` obsahuje popis objektů, sloupec type rozlišuje table/view/index. COUNT(*) vrátí jeden řádek s počtem. Pro interní prefix se hodí name NOT GLOB 'sqlite_*': u GLOB je _ obyčejný znak a * znamená libovolný zbytek. LIKE používá _ jako zástupný znak, proto by naivní LIKE 'sqlite_%' odfiltrovalo i vlastní tabulku sqlitex. Databázi neměňte.
