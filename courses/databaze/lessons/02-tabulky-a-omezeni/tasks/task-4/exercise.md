## Událost s volitelnou poznámkou

Vytvořte **vytvor_udalosti(con)**. Tabulka udalosti má id INTEGER PRIMARY KEY, popis TEXT NOT NULL a poznamka TEXT. Poznámka je volitelná: bez ní se načte Python None, ne prázdný text.

Opakované volání zachová data, funkce nic nevrací a neukončuje spojení ani transakci volajícího. Rozdíl mezi None a '' je význam dat: v prvním případě poznámka chybí, ve druhém existuje prázdný text.
