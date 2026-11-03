## Samostatný kurz OOP v Pythonu

Toto je **plán nového podkurzu**, nikoli rozšíření Turtle ani kurz tvorby her. Výukové lekce a závěrečný projekt zatím neimplementujeme. Kurz bude mít vlastní místo v katalogu a půjde studovat bez grafických knihoven a bez předchozí práce s Turtle.

## Pro koho a jak náročný

**3 ze 4 — středně pokročilé.** Úvod bude přístupný na úrovni 2/4: od známých funkcí, seznamů a slovníků přejdeme k první třídě. Celý kurz řadíme na 3/4, protože závěrem budou spolupracovat různé objekty, hlídat pravidla stavu a procházet testy. Není to jen syntaxe class.

Předpoklady: základní Python, funkce a return, podmínky, seznamy a slovníky, jednoduché výjimky. Doporučený předchozí kurz je Základy Pythonu. Turtle, Pygame, síť, databáze ani tvorba webu nejsou předpokladem.

Navrženo je 20 lekcí s postupným procvičováním a závěrečným projektem. Orientačně 10–14 hodin podle rozsahu vlastních pokusů; časové odhady se ověří až na hotových lekcích. Části lze rozdělit do kratších setkání. Náročnost není měřena rychlostí studenta.

## Nosný projekt: Chytré expediční centrum

Vytvoříme malou konzolovou aplikaci, která přijímá objednávky, rezervuje zboží a připravuje zásilky. Je to praktický systém s viditelnými reakcemi na příkazy, ne hra. Student si může zvolit sortiment: knihy, deskové hry nebo vlastní výrobky. Pracujeme pouze s vymyšlenými daty.

Zajímavost přinesou situace ze života: dvě objednávky chtějí poslední kus, zákazník objednávku zruší, těžký balík se nevejde do pravidel dopravce nebo je potřeba přidat nový způsob doručení. Cílem není napsat nejvíce tříd; je potřeba umět vysvětlit jejich odpovědnosti a spolupráci.

Na konci student předvede scénář: přijme objednávku, ukáže změnu dostupných zásob, zvolí dopravu, odmítne neplatný krok bez poškození dat a vypíše srozumitelný souhrn. Databáze ani internet pro základní variantu nejsou potřeba.

## Jak bude výuka probíhat

Každá lekce začne krátkou situací nebo otázkou „co se teď stane?“. Následuje malá ukázka, vysvětlení toku programu a úkol s okamžitou zpětnou vazbou. U každého příkazu bude jasné, který objekt jej provádí, co přijímá, co mění a co vrací.

Student nejdřív uvidí jednoduché řešení pomocí funkcí a slovníků. Potom stejný problém převede na objekty a porovná, co se zpřehlednilo a co ne. Prázdné definice tříd bez účelu nejsou cílem.

Průběžně se objeví malé „detektivní opravy“: sdílený seznam dvou objednávek, dvakrát vrácené zboží po stornu nebo změna stavu před vyvoláním výjimky. Správný test ukáže konkrétní problém. Opravou získá student důkaz, že princip chápe, ne jen další definici k zapamatování.

## Navržená osnova: 20 lekcí

### Modul 1 — Od funkcí k vlastním objektům

1. Kdy mají objekty smysl: srovnání funkcí, slovníků a tříd na stejném problému.
2. Třída, instance, konstruktor a self; vytváření více nezávislých objektů.
3. Metody, argumenty, návratové hodnoty a změna stavu; čtení průběhu volání.
4. Reference a skládání objektů; vlastní seznam položek každé objednávky.

Výstup: malá objednávka, která obsahuje své položky a umí spočítat součet. Student vysvětlí rozdíl mezi novou instancí a dalším odkazem na tentýž objekt.

### Modul 2 — Objekty, kterým lze věřit

5. Zapouzdření, veřejné rozhraní a vnitřní údaje; co znamená podtržítko.
6. Pravidla stavu a výjimky; nejprve ověřit, potom změnit.
7. Property a vypočítané údaje pouze pro čtení; cena nebo dostupné množství.
8. Malá revize skladu: samostatné instance, kopie kolekcí a odmítnuté operace.

Výstup: sklad nepřipustí zápornou zásobu a chybný požadavek neodečte část položek. Vnitřní kolekce nelze nechtěně změnit přes vrácený seznam.

### Modul 3 — Spolupráce a různé chování

9. Dědění: vztah „je druhem“ a jeho hranice.
10. Přepisování metod a polymorfismus: stejné rozhraní, různé provedení.
11. super: rozšíření základní inicializace a metody bez opisování.
12. Dědění nebo složení: volba způsobu dopravy jako spolupracujícího objektu.

Výstup: osobní odběr a kurýr pracují přes stejné rozhraní. Liší se nejen cenou, ale také pravidly: například kurýr ověřuje adresu a hmotnost, osobní odběr výdejní místo. Pokud změna znamená jen jinou sazbu, stačí parametr; dědění nepoužijeme samoúčelně.

### Modul 4 — Čitelný model a testy

13. Srozumitelný výpis objektů: __str__ a __repr__, bez vedlejších změn stavu.
14. Identita a rovnost: kdy dvě položky představují stejná data a kdy jiný objekt.
15. dataclass pro jednoduché záznamy; co vygeneruje a proč má vlastní seznam použít default_factory.
16. Testování objektů a spolupráce: běžné scénáře, hranice a chyby, základní použití unittest.

Výstup: testy odhalí typické chyby bez závislosti na grafice nebo konkrétním vnitřním názvu atributu. Student pozná, kdy je dataclass vhodná a kdy potřebuje vlastní logiku třídy.

### Modul 5 — Závěrečný praktický projekt

17. Návrh odpovědností: položka, objednávka, sklad, zásilka a způsob dopravy. Kresba jejich vztahů.
18. Rezervace a storno: změny více údajů, odmítnutí nedostupného zboží a ochrana před dvojitým stornem.
19. Doprava jako vyměnitelná spolupráce; přidání nové varianty bez přepisování celého systému.
20. Konzolový ovladač, předvedení scénáře, testy a vlastní vysvětlení návrhu.

Výstup: fungující expediční centrum s jasnými pravidly a krátkým README. Teprve při realizaci se stanoví přesné názvy metod, rozsah šablon a testovací kontrakty. Návrh je nebude studentovi skrytě měnit.

## Minimální rozsah a další možnosti

Základní projekt bude mít několik výrobků, objednávky v paměti a dva způsoby doručení. Konzole bude ukazovat stav a vysvětlovat odmítnuté operace. Student dostane připravený jednoduchý ovladač, aby první práci věnoval modelu; jeho samostatné doplnění může být závěrečnou výzvou.

JSON ukládání, databáze, webové API, grafické rozhraní, platby, asynchronní běh, rozsáhlé návrhové vzory a produkční nasazení do základního kurzu nepřidáváme. Taková rozšíření by posouvala náročnost směrem ke 4/4 a patřila by do dalšího bloku.

## Jak poznáme, že kurz funguje

- Každá ukázka bude spustitelná a komentovaná, každá nová konstrukce vysvětlená před použitím.
- Každý úkol bude mít zadání, šablonu, řešení a kontroly více vstupů i mezních případů.
- Kontroly přijmou správná alternativní řešení a odmítnou typické chyby se sdílenými daty nebo poškozeným stavem.
- Závěrečný projekt projde scénářem úspěšné objednávky, nedostatku zásoby, storna a nepovolené dopravy. Selhání musí zanechat smysluplný stav.
- Student vlastními slovy vysvětlí odpovědnosti objektů a proč použil složení či dědění. Samotná znalost názvů čtyř pilířů nestačí.

## Inspirace a její hranice

Praktické pojetí a postupný vývoj reálné aplikace inspiruje [Cosmic Python — příkladová aplikace](https://github.com/cosmicpython/code) ke knize Architecture Patterns with Python. Na veřejné GitHub stránce bylo 3. 11. 2026 ověřeno **2 726 hvězdiček**. To je údaj o komunitním zájmu, nikoli hodnocení studentů nebo záruka vhodnosti pro začátečníka.

Předloha má vlastní pokročilejší architekturu a starší instalační pokyny včetně Dockeru. Ty do kurzu nepřebíráme. Vlastní jednodušší projekt bude cílit na Python 3.14 a standardní knihovnu; nebude potřeba zdroj inspirace instalovat. Žádný cizí kód ani jiné podklady se nekopírují.

## Současný stav

Připravený je pouze tento návrh a panel v aplikaci. Samostatný kurz zatím nemá výukové lekce, řešení ani implementovaný projekt. Nevyžaduje Turtle ani hraní her. Dosavadní obsah existujících podkurzů se kvůli tomuto návrhu automaticky nepřesouvá.
