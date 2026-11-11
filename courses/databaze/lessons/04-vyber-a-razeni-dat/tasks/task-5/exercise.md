## Stránkování s limitem a posunem

Vytvořte **stranka_pomucek(con, limit, posun=0)**. Vrátí seznam n-tic (id, nazev, kusy) v pořadí id, nejvýše limit řádků po vynechání prvních posun řádků. LIMIT a OFFSET předávejte jako parametry.

Limit i posun musí být nezáporný int, nikoli bool; jinak ValueError. Limit 0 i posun za konec dají []. SQLite umí záporný LIMIT vyložit jako neomezený, ale takové zadání naše funkce záměrně odmítá. Nastavení spojení a transakce nechte volajícímu.
