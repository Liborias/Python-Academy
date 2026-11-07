## Vrátit tři kusy, ne celý sklad

První objednávka rezervuje tři z pěti knih a druhá zbývající dvě. Když první zrušíme, dostupné budou tři knihy. Dvě musejí zůstat pro druhou objednávku. Opakované storno nesmí přidat další tři.

Rozšíříme původní Sklad třídou RezervacniSklad. Konstruktor přes super připraví skladové karty a přidá vlastní slovník rezervací. Staré pridej, prehled i rezervuj zůstávají funkční. Anonymní rezervace přes původní rezervuj se stornem konkrétní objednávky neuvolňují.

Pomocné moduly obsahují hotová předchozí řešení včetně NakupniObjednavka. Pracujeme s jejich veřejným rozhraním, postupně v jednom programu. Nevkládáme souběžné změny ani ruční zásahy do vnitřních karet.

## Rezervace se váže na číslo objednávky

rezervuj_objednavku(objednavka) přijme NakupniObjednavka. Před změnou odmítne prázdnou, již uzavřenou nebo objednávku s číslem, které sklad už eviduje. Číslo se neuvolní pro nové použití ani po stornu.

Potom si vezme požadavek a zavolá původní rezervuj přes super. Ten už ověřuje všechny kódy a počty před první změnou karty. Nedostatek druhé položky proto nezablokuje první. Při odmítnutí objednávka zůstane otevřená a sklad o ní nezaloží záznam.

Po úspěchu objednávku uzavřeme a uložíme kopii skutečně rezervovaných počtů se stavem "rezervovana". V tomto pořadí uzavření platné neprázdné otevřené objednávky nemá důvod selhat. Metoda vrátí nový přehled dostupnosti ze skladu.

## Přechody stavu jsou záměrně malé

```text
dosud nepřijatá objednávka
    -> úspěšná úplná rezervace -> rezervovana
    -> jedno úspěšné storno   -> stornovana
```

stav(cislo) vrací "rezervovana" nebo "stornovana". Neznámé číslo vyvolá ValueError. Nepřijatá objednávka nemá záznam; její stav si nevymýšlíme.

storno(cislo) nejdřív ověří, že objednávka je rezervovaná. Z uložené kopie zjistí přesné počty a zavolá uvolni na příslušných kartách. Teprve potom označí záznam jako "stornovana" a vrátí nový přehled. Druhé storno a neznámé číslo vyvolají ValueError bez změn.

## Která data smí rozšíření používat

Slovník _karty je vnitřní uložení zděděné části téhož skladového objektu. V této rodině tříd ho používáme pro nalezení karty. Do vnitřních počtů cizí karty ale nezasahujeme: uvolnění provede její veřejná metoda uvolni. Fyzický celkový počet se při rezervaci ani stornu nemění, mění se pouze rezervované a dostupné množství.

Tato evidence si pamatuje, kolik kusů patří jednotlivým objednávkám. Storno proto neuvolní všechny rezervace karty ani současně jinou objednávku. Vrácený slovník přehledu je stále jen kopie čísel.

## Váš úkol

Doplňte rezervuj_objednavku a storno. Konstruktor a stav jsou připravené. Zachovejte úplnou rezervaci přes základní metodu, uzavření až po úspěchu a uvolnění přes rozhraní karet. Metody nic nevypisují; každý sklad má vlastní evidenci.

Spusťte ukázku se dvěma objednávkami. Potom zkuste požadavek na knihu a nedostupný obal: nesmí se rezervovat ani kniha. Ověřte také, že storno první objednávky ponechá rezervaci druhé a že změna kopie přehledu sklad neovládá.
