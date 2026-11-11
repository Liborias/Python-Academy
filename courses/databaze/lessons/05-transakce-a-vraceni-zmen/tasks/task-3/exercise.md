## Přesun mezi dvěma zásobami

Vytvořte **presun_kusy(con, odkud, kam, kolik)**. V jedné transakci odečte kolik ze zdroje a přičte cíli; při úspěchu potvrdí a vrátí None. Id jsou celá čísla, zdroj a cíl se liší, kolik je kladný int bez bool a autocommit=False. Neplatný režim, počet, stejné id, chybějící řádek nebo nedostatek zásob znamenají ValueError.

Podmíněný UPDATE zdroje vyžaduje dostatek kusů, oba kurzory musí mít rowcount=1. Pokud zdroj už odečtete a cíl se nenajde, výjimka uvnitř with con musí vrátit i první změnu. Pouhé return False by se považovalo za úspěšný odchod a mohlo změnu potvrdit. Hodnoty předávejte jako parametry, spojení nezavírejte a nezačínejte s cizími nepotvrzenými změnami.
