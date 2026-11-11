## Počítání přes SQL parametry

Vytvořte **secti_sql(a, b)**. Pro předaná celá čísla otevře vlastní ':memory:' spojení, provede parametrizovaný SQL součet a vrátí první hodnotu prvního řádku. Nakonec spojení zavře.

SELECT ? + ? se dvěma parametry ukáže, že execute přijímá odděleně příkaz a hodnoty. Výsledek fetchone je například (5,), proto pro samotné číslo čteme index 0. Záporná čísla i nula jsou platná. V tomto zadání neřešíme čísla mimo rozsah celých čísel SQLite.
