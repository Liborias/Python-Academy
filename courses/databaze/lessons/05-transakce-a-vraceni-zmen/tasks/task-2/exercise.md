## Odběr do dostupného množství

Vytvořte **odeber_kusy(con, id_pomucky, kolik)**. Vyžaduje autocommit=False a kolik jako kladný int bez bool, jinak ValueError před změnou. V transakci odečte pouze tehdy, pokud vybrané id má alespoň kolik kusů. Úspěch potvrdí a vrátí True, chybějící id nebo nedostatek False bez změny.

Podmínku kusy >= ? spojte přímo s UPDATE ... SET kusy = kusy - ?. Rowcount pozná, zda řádek odpovídal. Všechny hodnoty jsou parametry. Připravená kladny_pocet řeší kontrolu počtu. Před voláním žádná jiná rozepsaná práce, spojení se nezavírá.
