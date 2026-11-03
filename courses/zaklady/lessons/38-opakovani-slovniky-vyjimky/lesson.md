## Slovníky, seznamy a chyby dohromady

Druhé opakování spojuje slovníky, seznamy, funkce a ošetření chyb. Opět nic nového: pokud si nejste jistí, vraťte se k lekcím o slovnících (17 až 21) a o chybách (22, 23).

## Rada na cestu

U úloh, které něco třídí nebo počítá, si nejdřív rozmyslete **co bude klíčem a co hodnotou**. Pak se úloha obvykle změní na jednoduchý cyklus, který slovník plní.

## Váš úkol

1. `obrat_slovnik(slovnik)` vrátí nový slovník, ve kterém jsou klíče a hodnoty prohozené. Hodnoty původního slovníku jsou navzájem různé: `{"a": 1, "b": 2}` se změní na `{1: "a", 2: "b"}`.
2. `seskup_podle_delky(slova)` vrátí slovník, kde klíč je délka slova a hodnota seznam slov této délky v pořadí, v jakém jsou v seznamu: `["pes", "kocka", "kun"]` dá `{3: ["pes", "kun"], 5: ["kocka"]}`.
3. `bezpecny_soucet(hodnoty)` dostane seznam čísel i textů, kde se text může dát převést na desetinné číslo (`"3.5"`), nebo ne (`"abc"`). Vrátí součet všech hodnot, které se převést dají. Ostatní přeskočí, včetně `None`.
4. `nejcastejsi_hodnota(seznam)` vrátí hodnotu, která se v seznamu vyskytuje nejčastěji. Při shodě tu, která je v seznamu dřív, pro prázdný seznam `None`.
