## Práce s cizím kódem

Při práci programátor často nepíše nový kód, ale opravuje cizí. Dnešní úkol vypadá takto: kolega napsal čtyři funkce, které nefungují přesně podle zadání a nemají popis. Vaším úkolem je každou opravit a doplnit docstring.

Postup, který se osvědčil:

1. Přečtěte zadání v docstringu nebo komentáři.
2. Vyzkoušejte funkci na jednoduchém případě i na **krajním případu** (prázdný seznam, jeden prvek).
3. Když výsledek nesedí, přidejte `print` nebo použijte ladicí program.
4. Opravte, spusťte znovu a ověřte i předchozí případy.

## Váš úkol

V editoru jsou čtyři funkce s chybami v logice a bez docstringů. Opravte je podle popisu v komentáři a ke každé přidejte docstring (popis ve třech uvozovkách pod řádek s `def`). Řádky nesmí být delší než 79 znaků.

1. `prumer(cisla)` vrací průměr, pro prázdný seznam `0`.
2. `druha_nejvetsi(cisla)` vrací druhou největší **různou** hodnotu, nebo `None`, pokud neexistuje (například pro `[5, 5]`).
3. `kolik_slov(veta)` vrací počet slov ve větě.
4. `bez_duplicit(seznam)` vrací seznam bez opakování, **v pořadí prvního výskytu**.
