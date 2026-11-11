## Textový vzor LIKE

Vytvořte **podle_vzoru(con, vzor)**. Vrátí (id, nazev, kusy) s názvem odpovídajícím SQL LIKE, v pořadí id. Vzor předávejte jako parametr. % zastupuje libovolnou posloupnost včetně prázdné, _ právě jeden znak.

Používáme výchozí SQLite LIKE bez změny PRAGMA: písmena ASCII se porovnávají bez velikosti, ale nelze očekávat stejné chování pro všechny znaky Unicode. Například 'karty%' najde i 'Karty', zatímco 'šachy' není obecně stejné jako 'Šachy'. Neměňte nastavení spojení.
