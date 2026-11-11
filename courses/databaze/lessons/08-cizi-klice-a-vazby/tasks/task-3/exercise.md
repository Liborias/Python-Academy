## Pomůcka s volitelnou kategorií

Vytvořte **zapis_pomucku(con, nazev, kusy, kategorie_id=None)**. Parametrizovaně vloží novou pomůcku do relačního schématu a vrátí její skutečný lastrowid. Hodnoty neořezávejte ani jinak neupravujte.

None znamená bez kategorie. Neexistující nenulové id odmítne cizí klíč přes IntegrityError; chybu nepohlcujte. Pravidlo typeof(kusy) kontroluje uložený typ až po afinitě, nikoli přesný typ původního Python objektu. Transakci řídí volající.
