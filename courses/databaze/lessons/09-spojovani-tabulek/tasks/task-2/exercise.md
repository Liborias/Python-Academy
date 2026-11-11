## LEFT JOIN zachová i nezařazené

Vytvořte **vsechny_pomucky(con)**. Vrátí stejnou čtveřici jako Úkol 1, ale pomocí LEFT JOIN zachová i pomůcky bez kategorie. Jejich název kategorie bude Python None, nikoli prázdný či náhradní text.

Řaďte podle id pomůcky a každou vraťte jednou. Podmínku spojení dejte do ON; další WHERE nad pravou tabulkou může chybějící řádky znovu vyřadit. Nezměňte nastavení ani transakci volajícího.
