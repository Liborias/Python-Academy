## Co skutečně uloží typová afinita

Vytvořte **zkus_typy(hodnoty)**. Otevře vlastní paměťové spojení a tabulku hodnoty se sloupci volna bez uvedeného typu a cele INTEGER. Pro každou vstupní hodnotu vloží tutéž hodnotu do obou sloupců přes parametry. Vrátí řádky (typeof(volna), typeof(cele), volna, cele) v pořadí vložení a spojení zavře.

Vstup může být generátor podporovaných SQLite hodnot: None, int v rozsahu SQLite, konečný float, str, bytes či bool. Prázdný vstup dává []. Text '003' se v INTEGER může uložit jako číslo 3, float 2.0 jako integer 2; bytes zůstanou blob a None null. Neodhadujte typ jen pomocí Python type: zkoumáme skutečně uložený SQLite typ.
