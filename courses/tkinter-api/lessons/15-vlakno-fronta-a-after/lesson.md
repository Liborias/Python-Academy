## Čekání nesmí obsadit hlavní smyčku

Pomalé API v callbacku zastaví zpracování dalších kliknutí. Nepomůže vložit sleep ani další mainloop. Požadavek nyní poběží v pracovním vlákně a okno zůstane v hlavním vlákně. Během načítání zkuste tlačítko Klikni během načítání: počet se má měnit hned, ještě než přijde kurz.

Soubor kurzy.py je připravená přesná kopie předchozího řešení. Používáme z něj nacti_kurz, včetně timeoutu a ověření dat. Vedle něj patří cvicne_api.py, který spouští místní server. Kurzy zůstávají cvičné, se zdrojem a pevným datem.

## Vlákno dostane hotové hodnoty

```python
threading.Thread(target=pracovnik, args=(url,), daemon=True).start()
```

Import threading zpřístupní pracovní vlákno. Thread připraví práci, start ji spustí souběžně. Target dostane funkci bez závorek; args je n-tice argumentů, proto má (url,) čárku i s jediným prvkem. Zápis target=pracovnik(url) by práci provedl hned v hlavním vlákně a okno by čekalo.

Adresu i rezim.get() přečteme před spuštěním pracovníka. Tk widgety a StringVar/IntVar používáme jen v hlavním vlákně. Pracovník smí načíst a ověřit data, ale nevolá configure, get na Tk proměnné ani after. Daemon=True znamená, že sám nebude držet ukončený proces při životě; nejde o řízené zrušení rozběhnutého požadavku. Timeout je stále potřeba. Join v callbacku nepoužíváme, protože by hlavní vlákno opět čekalo.

## Fronta je schránka mezi vlákny

Queue z modulu queue je připravená pro předávání dat mezi vlákny. Pracovník vloží přes put dvojici (True, data), při očekávané chybě (False, zprava). Fronta tak oddělí výsledek přenosu od vykreslování.

Hlavní vlákno použije get_nowait. Pokud zatím žádná zpráva není, queue.Empty znamená běžné čekání, nikoli výpadek služby. Nevoláme blokující get bez omezení. Přes `okno.after(25, vyzvedni)` požádáme Tk, aby funkci zavolal nejdříve asi za 25 milisekund. After s callbackem nečeká na místě a nezakládá nové vlákno. Funkci opět předáváme bez závorek. Když je fronta prázdná, kontrola se naplánuje znovu a vrátí řízení oknu.

## Jasný stav právě jedné operace

Při načítání je tlačítko i přepínání scénáře disabled. Zabráníme druhému požadavku a změně volby uprostřed práce. Po úspěchu i očekávané chybě vrátíme normal a dovolíme nový pokus. Chyba nezobrazuje starý kurz jako nový úspěch. Počítadlo zůstává povolené po celou dobu.

Tři volby pomohou pochopit chování: Pomalá odpověď čeká místně 0,35 s, Chyba serveru vrátí 503 a Běžná odpověď vrací data ihned. Výsledný kurz zobrazuje hodnotu, datum i zdroj. Nejsou to obchodní data.

## Váš úkol

Doplňte spuštění pracovníka a naplánování kontroly fronty v nacti. Ve vyzvedni po přijetí zprávy znovu povolte tlačítko i všechny volby. Ostatní připravené části zachovejte a vysvětlete si, ve kterém vlákně běží každá funkce.

Během Pomalé odpovědi zkuste několikrát počítadlo a opakovaný klik Načíst kurz. Smí běžet jen jeden požadavek. Potom vyzkoušejte chybu a následný nový úspěšný pokus. Po dokončení se nesmějí přidávat další widgety a smyčka zůstává jediná. Vzhled a odezvu si ověřte ve skutečném okně; automatická kontrola také sleduje čas callbacků a přístupy k Tk mimo hlavní vlákno.
