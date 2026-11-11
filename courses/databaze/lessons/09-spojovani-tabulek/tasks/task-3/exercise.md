## Souhrn včetně prázdných kategorií

Vytvořte **prehled_kategorii(con)**. Pro každou kategorii vrátí (id, název, počet_pomůcek, součet_dostupných_kusů), v pořadí id kategorie. I prázdná kategorie má jeden výsledný řádek s počtem 0 a součtem0.

Začněte kategoriemi a LEFT JOIN pomůcek. Počítejte COUNT(p.id), ne COUNT(*): levé spojení vytváří řádek i tam, kde pomůcka chybí. Součet nahraďte přes COALESCE nulou a GROUP BY uveďte id i název kategorie. Bez kategorií je výsledek [].
