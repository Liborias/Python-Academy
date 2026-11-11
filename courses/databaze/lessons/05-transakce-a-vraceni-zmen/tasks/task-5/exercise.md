## Zkouška bez trvalého uložení

Vytvořte **pokus_bez_ulozeni(con, radky)**. Při autocommit=False dočasně vloží dávku dvojic a vrátí celkový počet pomůcek včetně těch nových, ale potom změny vždy vrátí rollback. Již potvrzené původní řádky zůstávají.

Try/finally zajistí rollback i při návratu výsledku nebo chybě INSERT. Chybu nepohlcujte a nikdy nevolejte commit. Autocommit=True odmítněte ValueError před změnou. Radky mohou být generátor; SQL používá parametry. Funkce nezavírá spojení a vyžaduje, aby volající neměl jinou rozepsanou práci.
