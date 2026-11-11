## Jeden záznam nebo None

Vytvořte **najdi_pomucku(con, id_pomucky)**. Parametrizovaným SELECT vrátí n-tici (id, nazev, kusy), nebo None, pokud id neexistuje. Fetchone má právě tento význam; není to [] ani n-tice obsahující None.

Id zůstává hodnotou, text podobný SQL se nevykoná jako příkaz. Neuzavírejte spojení, nepotvrzujte transakci a nesahejte na jiné řádky.
