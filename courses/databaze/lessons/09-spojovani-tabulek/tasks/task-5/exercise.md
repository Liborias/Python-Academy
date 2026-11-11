## Aktivní výpůjčky vybraného člena

Vytvořte **vypujcky_clena(con, clen)**. JOIN spojí výpůjčku s názvem pomůcky a vrátí (id_výpůjčky, název_pomůcky) pro přesného člena a vraceno=0. Člen je SQL parametr; zachovejte mezery a velikost písmen. Řaďte podle id výpůjčky.

Dvě aktivní půjčení stejné pomůcky jsou dva různé záznamy s různými id, neslučujte je DISTINCT. Vrácená půjčení nepatří do výsledku. Prázdný výsledek je [], cizí rozepsané změny neukončujte.
