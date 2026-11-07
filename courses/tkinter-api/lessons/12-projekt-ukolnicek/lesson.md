## Úkol má název i stav

Spojíme tři předchozí lekce do úkolníčku. Model je seznam slovníků s klíči nazev a hotovo. Při spuštění je prázdný. Listbox ukazuje [ ] před čekajícím úkolem a [hotovo] před dokončeným. Při výběru vypíše Text název a stav. Tato značka je jen zobrazení, není součást názvu v datech.

```python
ukoly = [{"nazev": "Přečíst zadání", "hotovo": False}]
```

Stejné názvy jsou povolené, proto dokončení i odstranění stále používá vybraný index. Dokončení nastaví True: druhý klik na stejný úkol jej nepřepne zpět. Úkoly se nespojují podle textu a při uložení zachovají pořadí i stav.

## Výběr ovládá podrobnosti

`seznam.bind("<<ListboxSelect>>", zobraz_detail)` připojí událost změny výběru. Dvojité úhlové závorky označují virtuální událost Tk: zprávu o změně widgetu, nikoli konkrétní klávesu. Handler přijme objekt události stejně jako dříve u Enteru.

Bez výběru detail říká Vyberte úkol pro podrobnosti. Jinak obsahuje dva řádky: Úkol: název a Stav: čeká nebo Stav: hotovo. Text slouží jen pro čtení. Stav disabled brání úpravám; když do něj zapisuje program, funkce nastav_detail jej nejprve přepne na normal, nahradí obsah a vrátí disabled. Zapisování do zakázaného Text by se neprojevilo.

## Model se mění, zobrazení se obnovuje

Obnov znovu vytvoří řádky Listbox a vymaže výběr. Proto dokonci po obnově opět vybere původní index přes selection_set, posune k němu seznam přes see a přímo zavolá zobraz_detail. Programové selection_set samo nevyvolá stejnou událost jako uživatelský klik, proto podrobnosti aktualizujeme výslovně.

Přidání i odstranění naopak nechává výběr prázdný. Úspěšné přidání vyprázdní Entry. Prázdné zadání a akce bez výběru nic v modelu nezmění. Všechny zprávy zůstanou v jednom stavovém popisku.

Pět ovládacích tlačítek vzniká v jednom cyklu. Seznam dvojic obsahuje popisek a odkaz na hotovou funkci, enumerate přidá číslo sloupce. Zápis `for sloupec, (nazev, funkce) in enumerate(...)` rozbalí číslo i vnitřní dvojici do tří proměnných. Každé tlačítko dostane command=funkce bez závorek, takže se příslušná akce provede až při kliknutí.

## Načteme buď celý platný model, nebo nic

JSON soubor obsahuje seznam záznamů. Hodnoty true/false JSON se v Pythonu změní na True/False. Nacti_ukoly nejprve načte celý soubor a ověří, že každý záznam je slovník s neprázdným textovým názvem a skutečnou hodnotou bool u hotovo. Číslo 0/1 místo bool nepřijímáme. Prázdný seznam je platný a dovolí začít znovu. Další klíče navíc lze ignorovat.

Funkce vytvoří nový seznam ověřených slovníků. Dokud neprojde i poslední položka, callback nesmí měnit stávající model. Po úspěchu použije:

```python
ukoly[:] = nactene
```

Prázdný řez vlevo nahradí celý obsah původního seznamu, zachová však jeho objekt. Callback tak nemusí jménu ukoly přiřazovat jiný objekt ani zavádět nonlocal. Význam řezu při čtení znáte, zde přes něj měníme obsah. Načtení úkoly nahradí, nepřipojí je ke starým. Potom obnovíme zobrazení a vymažeme starý výběr i podrobnosti.

Ukládání používá UTF-8, ensure_ascii=False a přímý zápis z minulé lekce. Při chybě zápisu zachováme model v paměti; tento jednoduchý postup nezaručuje obnovu starého souboru po přerušení zápisu. Zrušení dialogu nikdy neotevírá soubor.

Soubor ukládejte do vlastní známé složky a při dalším spuštění jej vyberte přes Načíst JSON. Nový běh sám nevyhledává dříve uložené soubory a začíná s prázdným modelem.

## Váš úkol

V připraveném projektu doplňte tři označená místa: přidání záznamu s hotovo=False, dokončení právě vybraného indexu a nahrazení obsahu seznamu po ověřeném načtení. Ponechte ostatní pravidla, pomocné funkce i rozložení. Zkuste si vysvětlit celý průchod od Entry přes model do Listbox a potom přes JSON zpět.

Program má zvládnout přidat úkol s krajními mezerami, odmítnout prázdný název, vybrat a opakovaně dokončit úkol, odstranit správnou položku i mezi opakovanými názvy, uložit, změnit a znovu načíst. Podrobnosti musejí odpovídat aktuálnímu výběru. Zprávy používají Přidáno:, Dokončeno: a Odstraněno: s názvem a tečkou; bez výběru Nejprve vyberte úkol. a bez názvu Napište název úkolu.

Uložení hlásí Úkoly uloženy., načtení Úkoly načteny. Zrušení i chyby mají stejné zprávy jako minulá lekce. Po neplatném souboru musí zůstat zachované úkoly, jejich pořadí, stav, výběr i podrobnosti. Vyzkoušejte také platný soubor s prázdným seznamem. Uložený model lze znovu načíst po restartu programu; bez výběru souboru začíná nové spuštění prázdné.
