## Jedinečné kategorie

Vytvořte **vytvor_kategorie(con)**. Tabulka kategorie má id INTEGER PRIMARY KEY a nazev TEXT NOT NULL UNIQUE. Opakované volání nesmí zničit řádky a funkce nic nevrací.

Zkuste vložit dvě kategorie se stejným názvem a také NULL. Databáze má obě porušení odmítnout, přestože samotný Python umí obě hodnoty předat. Předané spojení ani transakci neukončujte. Zatím jde o samostatnou tabulku; vazbu mezi tabulkami přidáme později.
