## Kdy můžeme projekt předat?

Aplikace už má formulář, změny, mazání, vazby i kapacitu. Teď ověříme, že data přežijí nové spuštění a že chybná akce nezničí původní záznam. Hotové GUI a model z lekce 14 jsou v prihlasky.py; v tomto kroku píšete **testy**, ne další kopii stejného okna.

```python
# Assert se ptá na konkrétní očekávání, ne pouze na to, že se nic nestalo.
skutecny_pocet = 2
assert skutecny_pocet == 2
print('Počet odpovídá očekávání.')
```

Ve vlastních unittest případech použijeme self.assertEqual, assertTrue/False a assertRaises. Sada dostane Model jako parametr. Díky tomu ji spustíme nad běžným modelem i nad porouchanou variantou. Test, který projde při každém výsledku, nás před chybou neochrání.

## Izolace místo testování vašich dat

Každý test vytvoří vlastní TemporaryDirectory a nový SQLite soubor. AddCleanup registruje úklid hned: nejprve zaregistrujeme složku, potom model.close. Úklid běží v opačném pořadí, takže nejprve zavřeme spojení, pak odstraníme složku. Funguje i při selhání testu. Nepoužívejte svůj krouzky.sqlite3.

Test trvalosti model zavře a otevře stejnou cestu novým modelem. Čtení původním spojením by neodhalilo chybějící commit. Test chyby navíc ověří, že po výjimce nezbyl půlhotový řádek.

## Spuštění a interpretace

Po uložení pracovní složky spustí `python reseni.py` vaši sadu. Textový výpis ukáže názvy testů a OK nebo FAILED. Program vrátí 0 při úspěchu a 1 při selhání, aby šel použít i v automatické kontrole. Okno se při testování neotevře.

`python spust_krouzky.py` otevře dokončené GUI z lekce 14 se skutečným krouzky.sqlite3 vedle spouštěče. `--db CESTA` zvolí jiný soubor, `--help` nic nezapisuje ani neotevírá. Pro ověření uložení přidejte kroužek, zavřete okno, znovu spusťte aplikaci a najděte záznam. Ovládání modelu je v prihlasky.py/upravy.py/model_zaklad.py, vzhled v pohled.py; všechny soubory patří do jedné složky. Záznamy z uložené lekce 14 lze otevřít přes --db s absolutní cestou k jejímu krouzky.sqlite3.

## Váš úkol

Doplňte **vytvor_sadu(Model)**. Vrátí unittest.TestSuite s alespoň šesti nepřeskakovanými testy, sama je ještě nespustí. Používejte předaný Model, nikoli napevno importovanou třídu uvnitř funkce. Připravený hlavní blok sadu provede a nastaví návratový kód.

Pokryjte: trvalé uložení po close/reopen (včetně oříznutí názvu a apostrofu), jedinečnost názvu kroužku, odmítnutí plného kroužku bez přidaného člena, odmítnutí duplicitní přihlášky, nemožné snížení kapacity se zachováním starého názvu/kapacity a ochranu kroužku před smazáním s přihláškou. V posledním případě po odhlášení ověřte možnost smazání i opakované False při odhlášení/mazání.

Jeden test může ověřit několik souvisejících výsledků. Nezáleží na názvech testovacích metod ani na tom, zda sadu složí loader či TestSuite ručně. Možné řešení ukazuje jednu strukturu; vaše vlastní testy mohou být jiné, musí ale skutečně odhalit popsané poruchy. Je-li něco červené, opravte příčinu a testy spusťte znovu.
