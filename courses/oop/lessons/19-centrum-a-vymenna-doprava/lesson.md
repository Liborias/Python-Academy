## Kdo spojí nákup, sklad a balík?

ExpedicniCentrum přijme hotovou nákupní objednávku, balík, dopravu a adresu. Sklad hlídá zásoby, Expedice dopravu a ExpedicniStitek adresu s poznámkami. Centrum řídí pořadí spolupráce a uchovává odkazy. Dosavadní rozhraní těchto tříd se nemění; všechny potřebné moduly jsou přiložené.

Konstruktor ExpedicniCentrum(sklad) dostane existující RezervacniSklad. Property sklad zpřístupní právě tento objekt pouze pro čtení. Každé centrum má vlastní slovník přijatých objednávek.

## Přijetí musí mít správné pořadí

prijmi(objednavka, balik, doprava, adresa) nejprve odmítne číslo již známé centru. Vytvořením Expedice ověří přepravitelnost balíku. Připraví datový štítek s číslem objednávky a původním objektem Adresa. Teprve potom požádá sklad o rezervaci a po úspěchu uloží záznam centra. Vrátí číslo objednávky.

Pokud doprava odmítne hmotnost, sklad se vůbec nemění. Pokud chybí zásoba, nevznikne přijatý záznam centra a objednávka zůstane otevřená. Připravené místní objekty se prostě neuloží. Nedáváme uživateli napůl přijatou objednávku.

## Společné rozhraní dovolí novou dopravu

Cyklodoprava(zona) vyžaduje neprázdný text rozvozové zóny, který uchová beze změny v property zona pouze pro čtení. cena(balik) vrací 59 Kč do 2000 g včetně a nad tuto hmotnost vyvolá ValueError. Nic nemění ani nevypisuje.

Nemusí dědit z Doprava. Expedice používá veřejnou cena(balik), takže kolo přidáme bez větvení podle tříd v centru. Stejně může spolupracovat jiná doprava se stejnou dohodou: cena vrací celé koruny, je dotazem bez změn a nepřepravitelný balík odmítne přes ValueError.

## Veřejné operace centra

- zmen_dopravu(cislo, nova) u rezervované objednávky deleguje změnu na její Expedice a vrátí novou cenu. Odmítnutí zachová původní dopravu.
- pridej_poznamku(cislo, text) u rezervované objednávky použije metodu štítku a vrátí počet poznámek. Zachová text i opakování.
- storno(cislo) nejdřív ověří, že centrum objednávku zná, a deleguje na sklad. Vrátí přehled. Druhé storno už sklad odmítne.
- souhrn(cislo) připraví nový slovník s aktuální nabídkou. Je dostupný i po stornu, abychom mohli přečíst poslední volbu a stav.

Stornované objednávce se doprava ani poznámky měnit nedají. Neznámé číslo všechny tyto operace odmítnou přes ValueError. Záznam zůstává po stornu uložený; stejné číslo se znovu nepoužívá.

Souhrn má klíče cislo, stav, zbozi, doprava, celkem, balik, adresa a poznamky. Zbozi je cena nákupu, doprava aktuální cena vybrané dopravy a celkem jejich součet. Balik obsahuje kód balíku. Adresa je text ve tvaru `Javorová 1, 60200 Brno`. Poznamky jsou nový seznam textů. Změnou souhrnu nebo jeho seznamu nelze přepsat centrum. Početní údaje jsou nabídka, nikoli provedená platba. V tomto projektu připravujeme rezervaci a údaje pro dopravu; fyzické kusy neodesíláme.

## Váš úkol

Doplňte cenu cyklodopravy a metody prijmi, zmen_dopravu, pridej_poznamku a souhrn. Konstruktor, vyhledání, kontrola aktivního stavu a storno jsou připravené. Používejte veřejné metody spolupracovníků a zjišťujte cenu aktuálně, bez vlastní kopie ceníku. Metody nic nevypisují.

Ukázka přepne dvě knihy z kurýra na kolo: nabídka je 500 + 59 = 559 Kč. Po stornu se vrátí jen jejich rezervace a změna dopravy už neprojde. Zkuste také přijmout balík 2001 g rovnou s kolem: zásoba i otevřená objednávka musejí zůstat beze změny.
