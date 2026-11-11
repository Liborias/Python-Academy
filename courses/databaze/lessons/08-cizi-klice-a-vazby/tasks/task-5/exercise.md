## Smazání kategorie zachová pomůcky

Vytvořte **smaz_kategorii(con, kategorie_id)**. Parametrizovaný DELETE vrátí počet smazaných kategorií 0/1. Databázové pravidlo ON DELETE SET NULL samo uvolní přiřazení souvisejících pomůcek.

Nemažte pomůcky ani výpůjčky. Druhé smazání stejného id už vrátí 0. Jde o společný efekt jedné SQL operace, který může volající s autocommit=False vrátit rollbackem i s jeho důsledky. Sami transakci neukončujte.
