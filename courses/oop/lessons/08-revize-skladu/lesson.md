## Když nestačí druhá položka objednávky

Máme pět knih a dva obaly. Zákazník žádá dvě knihy a tři obaly. Samostatná karta umí odmítnout nedostatek obalů, ale kdybychom postupně rezervovali každou položku hned při procházení požadavku, knihy by už byly odložené. Objednávka by uspěla jen napůl.

Sklad proto nejdřív ověří **celý požadavek**. Teprve po úspěšné kontrole provede rezervace na kartách. V naší jednovláknové ukázce se mezi těmito dvěma kroky stav sám nemění.

## Sklad obsahuje karty

Třída Sklad má vlastní vnitřní slovník. Klíčem je kód zboží, hodnotou objekt SkladovaKarta z minulé lekce. Importujeme ho z připraveného skladova_karta.py; hlavní ukázka pomocného modulu se při importu nespustí.

```python
karta = SkladovaKarta(nazev, celkem)
self._karty[kod] = karta
```

Kartu přidáme až po ověření jedinečnosti kódu a po jejím úspěšném vytvoření. Její konstruktor už umí odmítnout neplatný počet. Novou kartou nesmíme přepsat starou pod stejným kódem, protože bychom ztratili dosavadní rezervace.

Metoda `pridej(kod, nazev, celkem)` vrací počáteční dostupnost. Kódy a názvy zadáváme jako řetězce. Duplikát i neplatný počet způsobí ValueError a sklad zůstane beze změny.

## Veřejný přehled předává hodnoty

Prehled vrátí nový slovník, například `{"KNIHA": 5, "OBAL": 2}`. Hodnoty jsou dostupné celé počty z veřejné property karet, nikoli samotné karty nebo vnitřní slovník skladu.

V každém volání sestavíme nový přehled z aktuálního stavu. Když volající v přehledu přepíše KNIHA na 999, skutečná skladová karta se nezmění. Zde přehled tvoří jen řetězce a celá čísla; nevracíme v něm další měnitelné objekty. Připomeňte si rozdíl proti mělké kopii seznamu položek v lekci 4.

## Dva průchody jedním požadavkem

Vstup rezervuj je slovník kódů a požadovaných počtů, například `{"KNIHA": 2, "OBAL": 1}`. Items vrátí dvojice klíč a hodnota, které rozbalíme do kod a kolik:

```python
for kod, kolik in pozadavek.items():
    # Nejprve pouze ověřujeme.
    ...
for kod, kolik in pozadavek.items():
    self._karty[kod].rezervuj(kolik)
```

První průchod pro každou dvojici ověří známý kód, skutečný kladný int a dostatek dostupných kusů. Při jakékoli chybě vyvolá ValueError. Ještě se nevolá rezervuj žádné karty a nic se nemění.

Druhý průchod už využije veřejné rezervuj jednotlivých karet. Sklad nezasahuje přímo do jejich vnitřních atributů; každá karta vlastní svá pravidla. Nakonec vrátíme nový aktuální přehled.

Prázdný požadavek `{}` je dovolený: oba cykly nic neprovedou a výsledkem je nový přehled stejného stavu. Počet 0 uvedený u konkrétního kódu se ale odmítá stejně jako u rezervace jedné karty. Vstupní slovník nepřepisujeme ani z něj neodebíráme položky.

## Váš úkol

Doplňte Sklad.pridej, prehled a rezervuj podle popsaného rozhraní. Konstruktor je hotový. Používejte připravenou SkladovaKarta a její veřejné údaje/metody. Kontrola ověří i to, že při odmítnutí celého požadavku neproběhla rezervace žádné karty.

Kontrola zkusí také kartu se stejným veřejným rozhraním, ale jinak uloženými vnitřními počty. Sklad proto nemá spoléhat na jména jejích atributů s podtržítkem.

Ponechte připravený hlavní blok. Jeho ukázkový běh používá skutečné karty z pomocného souboru.

Ukázka nejprve odmítne dvě knihy a tři obaly: stav zůstane pět a dva. Platná rezervace dvou knih a jednoho obalu vrátí tři a jeden dostupný kus. Úprava kopie přehledu na skutečný sklad nepůsobí.

Nakonec vytvořte druhý Sklad a přidejte do něj jiné zboží. Stav prvního se nesmí změnit. Tím zakončíme revizi základních pravidel: samostatné instance, kopie přehledů a odmítnuté operace bez poškozených dat. Další blok přidá dědění a různé způsoby dopravy.
