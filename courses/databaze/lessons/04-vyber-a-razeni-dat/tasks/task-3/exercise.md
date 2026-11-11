## Zásoby pod hranicí

Vytvořte **malo_na_sklade(con, minimum)**. Vrátí n-tice (id, nazev, kusy) pro kusy < minimum, seřazené podle kusy, nazev a id vzestupně. Hranici předejte jako SQL parametr, je to celé číslo.

Rovnost s hranicí se nepočítá. Nula či záporná hranice může dát prázdný seznam, protože sklad nemá záporné kusy. Výpis nemění nastavení, data, transakci ani vlastnictví spojení.
