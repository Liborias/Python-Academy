## Náhradní text pomocí COALESCE

Vytvořte **zobraz_poznamky(con, nahrada='bez poznámky')**. Vrátí seznam (id, popis, zobrazená_poznámka) v pořadí id. Jen NULL nahraďte zadaným textem, prázdný řetězec zůstane prázdný. Hodnotu nahrada předejte jako SQL parametr.

COALESCE vybírá první hodnotu, která není NULL. Upravuje výsledek dotazu, nepřepisuje sloupec v databázi. Zachovejte i mezery a apostrofy náhradního textu. Spojení a transakci neukončujte.
