## Přesun pomůcky mezi kategoriemi

Vytvořte **presun_do_kategorie(con, pomucka_id, kategorie_id)**. Parametrizovaný UPDATE změní jen přiřazení vybrané pomůcky a vrátí rowcount 0/1. None odstraní přiřazení, pomůcka zůstává.

Pokud odpovídající pomůcka existuje, neplatná kategorie vyvolá IntegrityError. Pokud pomůcka neexistuje, není co měnit a vrací se0. Počet kusů, název i historie výpůjček zůstávají beze změny. Spojení a transakci neukončujte.
