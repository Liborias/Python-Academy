## Pygame 2: od objektu ke třem vlastním hrám

**Připraveno prvních 15 z 30 lekcí.** Navazujeme na Pygame 1 a základní OOP. Herní kód rozdělíme na objekty, kterým rozumíme a jejichž chování umíme ověřit. Obtížnost úvodu je 3/4, celku 4/4: čas, spolupráce objektů, kolize a řízení herních stavů. Předpoklady jsou doporučení, nikoli zamčené vstupy. Samostatný OOP kurz pomůže stejně jako OOP z Turtle.

V prvním modulu má každá lekce tři přepínatelné ukázky a pět úkolů s možným řešením a vlastní kontrolou. V úvodu je **15 ukázek a 25 úkolů**. Projekty Meteority a Chyť robota přidávají po pěti ukázkách a návazných zadáních s řešeními: celkem **25 ukázek a 35 úkolů**. Ukázky prvního modulu kreslí skutečné Surface a ukládají PNG přímo v aplikaci; nejde ještě o animované herní okno. Oba projekty už otevírají skutečné herní okno; po jeho zavření lze zobrazit poslední PNG. Navazující projekty tvoří souvislé kroky, bez nesouvisejících variant.

## Prostředí

Použijte Python 3.14 a stejnou .venv pro terminál i VS Code, VSCodium nebo PyCharm. `python tools/setup_env.py --courses pygame-2` připraví pygame-ce, v kódu import pygame. Ověřeno na Pythonu 3.14.8 a pygame-ce 2.5.8. Vlastní grafiku kreslíme kódem, žádné cizí obrázky, účty ani síťová data nepotřebujeme. Prvních pět lekcí funguje bez grafické plochy a zvuku; Meteority a Chyť robota vyžadují místní grafickou plochu a klávesnici, druhá hra také myš. Zvuk nepotřebují. Nativní editory mají společný připravený postup instalace před lekcemi.

## Modul 1 — Herní objekty, které jdou ověřit

**Hotovo: lekce 1–5.**

1. Sprite: vlastní image a rect, střed proti levému hornímu rohu, nezávislost instancí.
2. Vector2 a dt: desetinná poloha, rychlost v pixelech za sekundu, normalizace a hranice.
3. Group: update/draw, sdílené členství, remove/kill a výběr typů.
4. Kolize: obdélníky, skutečné objekty výsledku, bonusy, dvě skupiny a kruhové pravidlo.
5. Stav hry: pauza při pokračujícím vstupu, časovač, životy, režimy a obnova světa.

Výstup: malé testovatelné herní součásti a obrázkové náhledy výsledku. Každá nová operace má vysvětlený účel, vstupy a pravidla. Kontrola připouští jiné správné postupy; odkrytí vzoru nemění rozepsaný kód ani splnění úkolu.

## Modul 2 — Meteority (lekce 6–10)

**Hotovo: lekce 6–10.** Jeden návazný projekt s možným řešením každého kroku. Živé okno 640×480, šipky, životy/nezranitelnost, bonusový štít, skóre za minuté kameny a v závěru P/R/Escape. Vlastní grafika i smyčka používají pygame-ce; zvuk v této kapitole není nutný. Okno se otevře na počítači s Pythonem, ne uvnitř webu. Po běžném ukončení vznikne meteority.png. Modely se importují bez okna a kontrolují s řízeným časem, vstupem a náhodou.

6. Herní smyčka a hráč: vstup, dt a hranice okna.
7. Vytváření a odstraňování meteoritů s řízenou náhodou.
8. Zásahy, životy a krátká nezranitelnost.
9. Skóre, bonusový štít a přehledný stav kola.
10. Celá hra Meteority: pauza, konec a nový pokus.

## Modul 3 — Chyť robota (lekce 11–15)

**Hotovo: lekce 11–15.** Jeden návazný projekt s řešením každého kroku. Vlastní roboti, kruhový výběr navrchu podle pozice kliknutí, hlídač a kývač se společným rozhraním, přesnost oddělená od bodů, další vlny bez resetu čítačů a 30 herních sekund. Okno 720×520, levé tlačítko, v závěru Mezerník pro nabídku/start, P pro pauzu, R pro nový lov, Esc pro konec. Při běžném zavření vznikne roboti.png. Modely se importují bez okna; čas se vyhodnotí před kliknutími stejného snímku.

11. Cíle a pozice myši z události.
12. Pohyb robotů, směry a různá chování přes společné rozhraní.
13. Kliknutí, zásahy, životy a bodování.
14. Časový limit, kola a obtížnost.
15. Celá hra s nabídkou a restartem.

## Modul 4 — Součásti větší hry (lekce 16–20, plán)

16. Správa společných obrázků, fontů a zvuků.
17. Animace s časem a změnou snímků.
18. Masky, kruhy a volba přesnosti kolize.
19. Svět, kamera a souřadnice na obrazovce.
20. Skládání herních režimů a přechodů, hranice vhodného dědění.

## Modul 5 — Hon na dronech (lekce 21–25, plán)

21. Hra, Hrac a Dron jako spolupracující třídy.
22. Pronásledování, rozestupy a několik chování dronů.
23. Vlny protivníků a kontrolované vytváření objektů.
24. Bezpečná zóna, pauza a restart.
25. Hratelný celek a ladění pravidel podle skutečného hraní.

## Modul 6 — Ověření a předání (lekce 26–30, plán)

26. Deterministické scénáře: řízený čas, vstup a náhoda.
27. Vlastní testy pohybu, kolizí a stavů.
28. Uložení výsledků do JSON, chybějící/poškozený soubor.
29. Spuštění z čisté složky, závislosti a volitelné balení pro vlastní systém.
30. Vlastní varianta hry a závěrečné předání s návodem.

Odhad celku 18–25 hodin plus vlastní úpravy. PyInstaller nebo webové balení jsou volitelné, jejich možnosti a systémové limity ověříme při realizaci příslušné lekce. Aktuálně se neinstalují. Dalším krokem je modul Součásti větší hry 16–20.
