## Závěrečný projekt

Napíšete malého sběrače cen, který spojí celý kurz: pravidla `robots.txt`, stažení stránky s ošetřením chyb, zpracování HTML a uložení do JSON. Pracujte po částech a každou zkoušejte zvlášť.

Použijete stránku `/knihy.html` z lekce 18 (knihy `.kniha`, třída `vyprodano` znamená „není skladem“, cena je text typu `249 Kč`) a místní server z lekce 16.

## Funkce

1. `nejlevnejsi(knihy)` vrátí slovník nejlevnější knihy ze seznamu (`None` pro prázdný seznam). Knihy jsou slovníky `{"nazev", "cena", "skladem"}`.
2. `prumerna_cena(knihy)` vrátí průměrnou cenu zaokrouhlenou na 1 desetinné místo (`0` pro prázdný seznam).
3. `sber_cen(adresa, nazev_json, cesta="/knihy.html")` provede vše:
   - nejdřív přečte `adresa + "/robots.txt"` a když robot `Dilna-Sberac` na `cesta` nesmí, **nic nestahuje** a vrátí `None`;
   - stránku stáhne s `timeout` a `raise_for_status`, při chybě vrátí `None` a nevytvoří soubor;
   - z knih **skladem** vytvoří (každá kniha je slovník jen s klíči `nazev`, `cena`, `skladem`, kde `skladem` je `True`) slovník `{"pocet": ..., "nejlevnejsi": ..., "prumer": ..., "knihy": [...]}`, kde `nejlevnejsi` je jméno nejlevnější knihy;
   - uloží ho do JSON (UTF-8, čitelná čeština) a vrátí ho.

Při stahování se představte hlavičkou `User-Agent: Dilna-Sberac/1.0`.

Tip: hotovou práci z lekcí 17 až 20 můžete využít jako vzor, ale zkuste to bez kopírování.