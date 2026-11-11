## Konflikt názvu bez přepsání dat

Vytvořte **pridej_pokud_chybi(con, nazev, kusy)**. Nový záznam vloží a vrátí True; při konfliktu stejného názvu nechá starý záznam beze změny a vrátí False. Všechny hodnoty předávejte jako parametry. Jiná porušení, například záporné kusy nebo NULL název, dál vyvolávají IntegrityError.

Pomůže INSERT ... ON CONFLICT(nazev) DO NOTHING. Rowcount pozná vložení; lastrowid po ignorovaném konfliktu nemusí znamenat nový řádek. Obecné INSERT OR IGNORE by potlačilo také CHECK/NOT NULL, což zde nechceme. Při záporných kusech má být chyba i tehdy, když název už existuje. Nepotvrzujte ani nezavírejte spojení.
