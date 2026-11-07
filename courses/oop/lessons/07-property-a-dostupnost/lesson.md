## Pět kusů ve skladu nemusí být pět kusů k objednání

Pokud ze zásoby pěti knih odložíme tři pro objednávku, fyzicky je ve skladu pořád pět. Pro dalšího zákazníka jsou ale dostupné jen dvě. Třída SkladovaKarta si proto uchová celkový počet a rezervované množství. Dostupnost bude jejich aktuální rozdíl.

Rezervace zatím pracuje s celkovým množstvím. Přiřazení rezervací konkrétním objednávkám a ochranu před opakovaným stornem doplní závěrečný projekt.

## Property se čte jako atribut

```python
@property
def dostupne(self):
    return self._celkem - self._rezervovano
```

Značka `@property` upraví následující definici tak, že ji volající čte jako atribut: `karta.dostupne`, bez závorek. Python při čtení provede tuto metodu a vrátí výsledek. Metoda pořád potřebuje self a sama nic nemění.

Tím neukládáme druhou kopii dostupného počtu. Po každé rezervaci nebo uvolnění se výsledek dalšího čtení přirozeně změní. Uložená dostupnost z konstruktoru by po změnách zastarala.

## Tři údaje pouze pro čtení

Karta zpřístupní property celkem, rezervovano a dostupne. První dvě vracejí příslušný vnitřní údaj, třetí ho vypočítává. Počet rezervovaných kusů začíná na nule.

Definujeme jen čtení property. Běžné přiřazení `karta.dostupne = 99` proto vyvolá AttributeError a hodnoty zůstanou beze změny. Stejně se chovají celkem a rezervovano. Podtržítko u vnitřních atributů dál představuje dohodu, nikoli bezpečnostní bariéru; volající používá veřejné rozhraní.

Název karta.nazev zůstává běžný údaj. V této lekci nepotřebuje zvláštní pravidla ani property.

## Změny vyjadřují metody

`rezervuj(kolik)` ověří kladný celý počet a dostatek dostupných kusů. Pak zvýší rezervované množství a vrátí novou dostupnost. `uvolni(kolik)` obdobně sníží rezervaci, nejvýš však o právě rezervovaný počet. I tato metoda vrátí dostupnost.

Fyzický celkový počet se během těchto operací nemění. Rezervovat není totéž co vydat zboží ze skladu.

Například po rezervaci 3 z 5 platí celkem 5, rezervovano 3 a dostupne 2. Uvolnění jednoho kusu změní rezervovano na 2 a dostupne na 3. Uvolnění všech rezervovaných kusů je dovoleno; uvolnění více nebo záporné, nulové či necelé množství vyvolá ValueError bez změn.

## Váš úkol

Doplňte SkladovaKarta. Konstruktor je připravený: celkem musí být nezáporný int a rezervace začíná nulou. Vytvořte tři property pouze pro čtení a metody rezervuj a uvolni podle výkladu.

Množství musí být skutečný int, stejně jako v minulé lekci; bool a jiné typy se odmítají. Nejprve se ověřuje celý požadavek, potom se mění stav. Každá karta má vlastní počty. Veřejné metody nic nevypisují a opakované čtení property nic nemění.

Spusťte ukázku a porovnejte výpis s uvedeným příkladem. Pak rezervujte všechny zbývající volné kusy a ověřte nulu. Pokus o další rezervaci zachyťte přes except ValueError a zkontrolujte, že počty zůstaly stejné.
