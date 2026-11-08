## Okenní aplikace, API a e-maily

Z plánovaných 28 lekcí je hotových prvních 16. Kurz začíná Tkinterem, potom propojí okna se soubory, HTTP API a přípravou e-mailů. Celková náročnost je 3/4; úvod navazuje na základní funkce a podmínky. Doporučené Základy Pythonu a Soubory a web pomohou, samostatný OOP je užitečný, ale úvod jej nevyžaduje. Turtle ani Pygame nejsou potřeba.

Každá hotová lekce obsahuje výklad nových konstrukcí před použitím, komentovanou ukázku, samostatné zadání, vzor, automatickou kontrolu a tři kvízové otázky. Kontroly ověřují nastavení a chování, skutečný vzhled se zkouší také v Tk. Okno vzniká na počítači s Pythonem, nikoli uvnitř webové stránky.

## Prostředí a průběh

Vstupní příprava nabízí Windows, macOS a Linux i VS Code, VSCodium a PyCharm. Tkinter je systémová součást instalace Pythonu/Tk, ne pip balíček. Prvních dvanáct lekcí používá jen standardní knihovnu; requests je potřeba od lekce 13 pro HTTP část a PyInstaller je volitelný až pro balení. Stejný interpreter z .venv musí fungovat v terminálu i editoru. Ověření: python -m tkinter na grafické ploše.

Základní projekty půjdou vyzkoušet s místními daty. Síťová část dostane předvídatelné odpovědi a chyby pro testování. E-mailová část nejprve použije lokální záchytný server a cvičné adresy, aby nepotřebovala osobní schránku. Přístup k reálné službě a konkrétní závislosti se ověří při realizaci příslušných lekcí.

Celkový odhad je 16–22 hodin včetně procvičování a projektů. Témata budeme doplňovat po menších blocích, přesná rozhraní vysvětlíme před úkoly.

## Modul 1 — První okna a události

**Hotovo: lekce 1–4.**

1. Hlavní okno, titulek, počáteční a nejmenší rozměry, mainloop a grafická plocha.
2. Widgety ttk.Label, rodič, umístění pack a vnější mezery.
3. Button, předání funkce bez závorek, změna existujícího popisku a obnovení zprávy.
4. Entry.get, aktuální vstup, prázdný text a rozložení grid včetně roztažení sloupce.

Výstup: ovladatelný formulář se jménem a srozumitelnou reakcí na prázdný vstup.

## Modul 2 — Uspořádané formuláře

**Hotovo: lekce 5–8.**

5. Frame, seskupování a kombinace správců v různých rodičích, změny velikosti.
6. Události bind, argument události, Enter a fokus klávesnice.
7. StringVar/IntVar, Checkbutton a Radiobutton, čtení nastavení.
8. Projekt převodníku vzdálenosti: samostatný výpočet, převod textu na číslo a zpráva místo pádu.

Výstup: převodník kilometrů a metrů ovládaný tlačítkem i Enterem, s odděleným výpočtem a opravou chybného vstupu.

## Modul 3 — Úkolníček a soubory

**Hotovo: lekce 9–12.**

9. Listbox a model dat, výběr a bezpečná práce s indexy.
10. Scrollbar a Text, delší seznamy a obsah.
11. Načtení/uložení JSON v UTF-8, dialogy souborů a jejich zrušení.
12. Hotový úkolníček: přidat, dokončit, odstranit, uložit a znovu načíst.

Výstup: úkolníček se samostatným modelem, podrobnostmi výběru a uložením/obnovením JSON. Zrušený dialog ani vadný soubor nerozpracovaná data nenahradí.

## Modul 4 — HTTP API bez zamrzání okna

**Hotovo: lekce 13–16.** První dvě jsou konzolová příprava backendu, další dvě mají okno.

13. REST, GET, parametry a JSON přes requests, časový limit, místní cvičné API.
14. Stavové kódy, nedostupná služba a neplatná odpověď, jasné stavy načítání.
15. Tk.after, pracovní vlákno a fronta výsledků; widgety se mění jen v hlavním vlákně.
16. Převodník měn 2.0: zdroj a datum kurzu, ruční cvičná data a ověřená síťová varianta.

Výstup: převodník měn se dvěma jasně označenými místními zdroji a datem cvičného kurzu. Načítání neblokuje okno, chyba i změna volby zneplatní starý kurz.

## Modul 5 — E-maily nejdříve lokálně

17. EmailMessage, hlavičky, předmět, český text a náhled zprávy.
18. SMTP a lokální záchytný server, zachycení zprávy bez osobní schránky.
19. Přílohy a výběr souboru, typ obsahu, zrušený dialog a chybějící soubor.
20. Nastavení služby a chybové stavy, údaje z prostředí; reálná schránka jako volitelné rozšíření.

## Modul 6 — Projekt Korespondenční dílna

21. Model zprávy a okno pro příjemce, předmět, text a náhled.
22. Ověření vstupů a příloh, srozumitelná chyba u konkrétního pole.
23. Odeslání do lokálního záchytu bez blokování, stav probíhající operace a ochrana před dvojím kliknutím.
24. Celý průchod včetně odmítnutí, místního zachycení a nového pokusu řízeného uživatelem.

## Modul 7 — Testy, balení a předání

25. Testy výpočtů a spolupráce, simulovaná síť a praktické GUI scénáře.
26. PyInstaller jako volitelná cesta; ověření verze Pythonu a sestavení pro cílový systém.
27. Cesty k datům, čitelné chyby, klávesnice a kontrolní seznam na skutečném počítači.
28. Předvedení hotové aplikace, README, vlastní vysvětlení návrhu a závěrečné ověření.

## Hranice rozsahu

První blok nic neodesílá na síť. HTTP příklady 13–16 mají výslovný místní zdroj a testovací režimy. E-mailové příklady budou mít také místní záchyt; textové hodnoty ani hesla se nebudou vkládat do zdrojových souborů jako skutečné přihlašovací údaje. Produkční hromadné rozesílání, složitá autentizace a automatické nasazení nepatří do tohoto kurzu.
