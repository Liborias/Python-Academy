## Spojení vracíme volajícímu

Vytvořte **otevri_databazi(cesta)**. Vrátí nové otevřené sqlite3.Connection s autocommit=True k předané cestě. Může jít i o ':memory:'. Funkce tentokrát nevrací řádek, ale samotné spojení; nezavírejte ho před návratem.

Vlastnictví přebírá volající, který po práci použije close nebo closing. Dvě oddělená ':memory:' spojení mají nezávislá data. Autocommit=True znamená, že jednotlivé úspěšné příkazy nejsou součástí dlouhé neukončené transakce. Jak uložit několik změn jako celek vysvětlí lekce5.
