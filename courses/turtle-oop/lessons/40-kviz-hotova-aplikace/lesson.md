## Závěrečný projekt celého kurzu

Vytvoříme konzolovou aplikaci, která nabídne zdroj, postupně položí otázky, vyhodnotí odpovědi a ukáže výsledek. Model, načítání i síťový klient jsou v připravených modulech z lekcí 37–39. Váš úkol je propojit je se vstupem uživatele.

Kvíz běží v konzoli pod editorem, takže funguje bez grafického prostředí. Snake zůstává samostatným hotovým projektem v lekci 36. Toto zakončení procvičuje stejné OOP v jiném prostředí.

## Nejdřív vybereme zdroj

Hotová hlavni se zeptá na zdroj. Enter použije přiložené české otázky, text api požádá o online otázky z Open Trivia DB. Ty jsou anglické. Jiný text ponechá výchozí offline režim.

Ziskej_otazky vrátí seznam, skutečný zdroj a případnou zprávu. Hlavni zdroj vypíše. Když síť selže nebo vrátí nepoužitelná data, ukáže důvod a pokračuje se zálohou. Pokud nelze přečíst ani tu, oznámí chybu a skončí bez spuštění prázdného či neplatného kvízu.

## Vstup a výpis jako předané funkce

```python
def hraj(otazky, vstup=input, vypis=print):
    kviz = Kviz(otazky)
```

Při běžném spuštění vstup čte pomocí input a vypis pracuje jako print. V kontrolách ale můžeme předat připravené odpovědi a funkci, která si uloží řádky. Díky tomu testujeme skutečnou herní logiku bez ručního psaní.

Volání `vstup("Pravda (a), nepravda (n), konec (q): ")` zobrazí nápovědu a přečte jeden řádek. `.strip().casefold()` odstraní krajní mezery a sjednotí velikost písmen. Přijímáme právě a, n a q.

Z písmene vytvoříme bool pomocí `volba == "a"`. Teprve tento výsledek předáme Kviz.odpovez. Neprázdný řetězec n sám o sobě neznamená False, proto znovu nepoužíváme bool(volba).

## Proč jsou zde dva cykly

Vnější cyklus běží, dokud kviz.aktualni() nevrátí None. Vypíše číslo otázky v podobě 1/5 a její text. Vnitřní cyklus čeká na použitelnou odpověď:

1. Neplatné písmeno zobrazí nápovědu a pomocí continue zopakuje vstup ke stejné otázce. Nemění skóre ani index.
2. Q ukončí hru, ukáže průběžné skóre a vrátí výsledek bez zodpovězení této otázky.
3. A nebo n zavolá model právě jednou. Vypíše Správně, nebo Nesprávně včetně správného písmene. Break pak ukončí vnitřní cyklus a vnější přejde k další otázce.

Při nesprávné odpovědi potřebujeme informaci o právě zodpovězené otázce. Proto si objekt uložíme ještě před odpovez; aktuální index modelu už po vyhodnocení ukazuje dál.

## Konec vstupu není chybná odpověď

Pokud vstupní proud skončí, input vyvolá EOFError. Zachytíme ji, vypíšeme Vstup skončil a průběžné skóre a vrátíme se. Není důvod další vstup zkoušet donekonečna.

Po běžném dokončení všech otázek vypíšeme Výsledek: skóre/počet. Funkce hraj při každém způsobu ukončení vrací dvojici `(skore, pocet_zodpovezenych)`. Prázdný seznam znamená výsledek 0/0 bez čtení vstupu. Otázky ani jejich správné odpovědi neměníme.

## Váš úkol

Doplňte hraj podle uvedených pravidel a používejte předané funkce vstup a vypis. Model Kviz, hlavni i hlavní blok jsou připravené. Neplatné vstupy se opakují, a/n vyhodnocují, q nebo EOF ukončují. Ve zpětné vazbě používejte texty Správně, Nesprávně a správné písmeno; na konci zobrazte výsledek nebo průběžné skóre.

Spusťte ukázku. U volby zdroje odešlete prázdný řádek, pak napište odpověď do vstupního pole konzole a odešlete ji. Vyzkoušejte velké A, mezery, neplatné písmeno i q. Pro všech pět správných odpovědí v přiložené sadě platí a, n, a, n, a. Online režim zkuste zadáním api při novém spuštění.

V editoru ponechte reseni.py, kviz_model.py, kviz_data.py, kviz_api.py a otazky.json pohromadě. V terminálu s aktivním projektovým virtuálním prostředím přejděte do této pracovní složky a spusťte `python reseni.py`. Příkaz spustí hlavní blok; modulové importy pouze zpřístupní ostatní části. Při změně pracovního adresáře se jinak relativní cesta k otazky.json může vztahovat jinam.

## Co máte hotové

Kurz teď tvoří 40 lekcí: kreslení želvou, práce s typy, návrh objektů, hotový Snake a tento kvíz s volitelným API. Na obou projektech jste oddělili stav, pravidla a vstup či zobrazení. Modely lze ověřovat samostatně a vnější služby nahradit při zkoušení předvídatelnými daty.
