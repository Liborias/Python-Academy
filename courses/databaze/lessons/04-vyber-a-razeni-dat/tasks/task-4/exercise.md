## Pojmenované sloupce bez změny spojení

Vytvořte **prehled_jako_slovniky(con)**. Vrátí obyčejné slovníky s klíči id/nazev/kusy v pořadí id vzestupně. Neměňte con.row_factory, který patří volajícímu; můžete použít lokální kurzor s row_factory=sqlite3.Row.

Row umožní číst radek['nazev'] a dict(radek) vytvoří slovník. Kurzor si při vytvoření převezme výchozí nastavení spojení, pak může mít vlastní nastavení. Úkol funguje, ať volající používá obyčejné n-tice nebo sqlite3.Row. Prázdná tabulka dává []; spojení ani transakci neukončujte.
