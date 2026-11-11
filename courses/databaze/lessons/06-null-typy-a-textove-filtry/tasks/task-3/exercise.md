## Doslovné hledání části názvu

Vytvořte **najdi_doslovne(con, text)**. Z pomucky vrátí (id, nazev, kusy), kde nazev obsahuje přesně zadaný podřetězec, v pořadí id. Rozlišuje velikost písmen, % a _ jsou obyčejné znaky. Prázdný hledaný text najde všechny názvy, i prázdný.

Pomůže instr(nazev, ?): vrací pozici od 1, nebo 0 při nenalezení. Text je SQL parametr. Nezaměňujte tento kontrakt za vzor LIKE; procento v názvu 'Karty 100%' má být hledáno doslovně. Data, nastavení a cizí transakci zachovejte.
