### Cache velikostí fontu

Vytvořte `BankaFontu(vytvor)` a `font(velikost)`. Předaná funkce vytváří font pro kladnou celočíselnou velikost. Pro tutéž velikost vraťte tentýž font a továrnu volejte jen jednou po úspěchu; jiná velikost či jiná banka má vlastní vytvoření. Výjimku továrny neukrývejte a neúspěch necachujte.

Font zde považujeme za sdílený prostředek: po získání neměňte jeho bold, italic a další nastavení. Na rozdíl od obrázku nepotřebujeme vlastní měnitelnou kopii. Inicializaci fontů dělá připravený pokus před použitím továrny.
