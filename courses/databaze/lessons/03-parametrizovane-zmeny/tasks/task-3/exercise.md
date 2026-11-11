## Změna jen vybrané pomůcky

Vytvořte **nastav_pocet(con, id_pomucky, kusy)**. Parametrizovaný UPDATE změní kusy jen u předaného id a vrátí rowcount, tedy 0 nebo 1. Pokud nová hodnota odpovídá staré, nalezený řádek se v SQLite stále počítá jako 1.

Chybějící id nic nezmění. Záporný počet odmítne CHECK přes IntegrityError. Ve WHERE musí zůstat výběr podle id, jinak byste přepsali všechny pomůcky. Sami nepotvrzujte ani nezavírejte spojení.
