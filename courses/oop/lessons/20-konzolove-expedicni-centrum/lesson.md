## Hotový průchod objednávkou

Závěr kurzu propojí všechny části konzolovým ovladačem. Máme pět knih po 250 Kč a dva obaly po 30 Kč. Vytvoříme objednávku, změníme dopravu, přidáme poznámku, zkusíme nedostupné zboží a bezpečné storno. Nové spuštění začne znovu s původními cvičnými daty; nic se neukládá na disk.

Všechny modely jsou ve files a připraví se i v pracovní složce editoru. Přiložený README.md popisuje příkazy a odpovědnosti. Soubor test_centrum.py obsahuje čtyři skutečné unittest testy rezervací, storna a dopravy.

## Ovladač překládá vstup

proved_prikaz(centrum, radek) rozdělí text pomocí split(), ověří počet částí a zavolá veřejnou metodu centra. Vrací text odpovědi, sama nepoužívá input ani print. Prázdný řádek vrátí prázdný text. Neznámý příkaz, chybný počet argumentů nebo neplatná data vyvolají ValueError bez změny dosavadního stavu.

split() bez argumentu sjednotí oddělovací mezery. int(text) převádí počty a gramy na celá čísla; například "2.5" odmítne přes ValueError. Poznámku znovu spojíme pomocí " ".join, takže mezery mezi jejími slovy budou jednotlivé. Příkazy a názvy dopravy píšeme malými písmeny.

## Příkazy a přesné odpovědi

- stav vrátí `Sklad: KNIHA=5, OBAL=2` s aktuálními dostupnými počty. Kódy se řadí přes sorted, aby výpis měl předvídatelné pořadí.
- nova ČÍSLO KNIHY OBALY GRAMY vytvoří objednávku a balík s kódem B-ČÍSLO. Počty jsou nezáporná celá čísla, dohromady aspoň jeden kus. Nulu do objednávky nepřidáváme. Hmotnost musí být kladná. Přijetí použije osobní odběr a ukázkovou adresu Javorová 1, 60200 Brno; vrátí `Přijato: ČÍSLO`.
- prehled ČÍSLO předá souhrn připravené formatuj_souhrn. Ta zobrazí stav, ceny, balík, adresu a poznámky.
- doprava ČÍSLO odber/kuryr/kolo vybere připravený objekt dopravy a vrátí například `Doprava: 59 Kč`. Neznámý způsob odmítne před změnou.
- poznamka ČÍSLO TEXT uloží poznámku a vrátí například `Poznámek: 1`. Bez textu příkaz neplatí.
- storno ČÍSLO vrátí po úspěchu `Stornováno: ČÍSLO`.

V prohlížeči má tato lekce na ukázku i vlastní řešení deset minut. Běh lze kdykoli ukončit tlačítkem Stop a spustit znovu.

Konec obslouží hlavní smyčka, nikoli proved_prikaz. Příkaz konec nebo konec vstupu ukončí program zprávou `Na shledanou.`. Funkce vytvor_demo, formatuj_souhrn, spust a hlavní blok jsou připravené.

## Chyba neukončí celou dílnu

spust čte input v cyklu. ValueError z proved_prikaz zachytí a vypíše jako `Odmítnuto: ...`, potom čeká na další řádek. EOFError při konci vstupu ukončí smyčku. Kontroly stavu a dostupnosti zůstávají v modelech; ovladač je neopisuje a nesahá na jejich privátní atributy.

## Váš úkol a vlastní ověření

Doplňte pouze proved_prikaz. Zachovejte ceny, texty odpovědí, formátování i předání chyb přes ValueError. Jednotlivé veřejné operace voláte nad předaným centrem, nevytváříte pro každý příkaz nový sklad. Při neplatném požadavku nesmí zůstat částečně vytvořená rezervace.

Spusťte ukázku a zadávejte příkazy jednotlivě, například nova A 2 1 1200, doprava A kolo, prehled A. Pak nova B 4 0 800: nyní chybějí knihy. Stornujte A a zkuste B znovu; tentokrát projde. Druhé storno A už nic neuvolní. Nakonec příkazem stav porovnejte zásoby.

V editoru spusťte `python reseni.py`. Ze stejné pracovní složky spusťte také `python -m unittest -v test_centrum`. Všechny čtyři testy mají skončit OK. Podle předchozí lekce doplňte vlastní test pro přesně 2000 a 2001 gramů kola a pro dvě nezávislá centra.

Vysvětlete vlastními slovy, proč dopravu kontrolujeme před rezervací, proč přijatý nákup uzavíráme, kde je uložené množství pro storno a co by se rozbilo při opakovaném uvolnění. Pak přidejte vlastní dopravu se stejnou cena(balik). Tím předvedete návrh a spolupráci objektů, nejen znalost zápisu class. Obsah samostatného OOP kurzu je tím dokončený; vaše připomínky poslouží k jeho revizi.
