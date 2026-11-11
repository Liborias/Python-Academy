## Pozdrav jako výsledek SQL dotazu

Vytvořte **pozdrav_sql(jmeno)**. Otevře vlastní paměťové spojení, přes SQL vrátí 'Ahoj, ' spojené s předaným textem a spojení zavře. V SQLite spojuje text operátor ||. Jméno předejte jako oddělený parametr, například (jmeno,).

Zachovejte apostrofy, češtinu i krajní mezery; nevytváříme validaci jména. Výstup pro "Žofie O'Neil" je "Ahoj, Žofie O'Neil", pro prázdný text 'Ahoj, '. Čárka v jednočlenné n-tici je důležitá: (jmeno) je jen tentýž text, nikoli n-tice parametrů.
