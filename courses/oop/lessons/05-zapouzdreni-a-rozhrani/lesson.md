## Jeden údaj, několik cest ke změně

V prvním bloku jsme do atributů položky zapisovali přímo. U zásoby zboží chceme, aby volající popsal operaci: příjem nebo výdej. Objekt pak bude mít jedno místo, kam později doplníme pravidla. Této práci s veřejným rozhraním a vnitřními údaji říkáme **zapouzdření**.

Zavedeme třídu `Zasoba(nazev, pocet=0)`. Název je běžný veřejný údaj. Počet uchováme ve vnitřním atributu, například `self._pocet`.

## Co znamená podtržítko

Jedno podtržítko na začátku názvu vyjadřuje dohodu: tento údaj patří vnitřnímu provedení objektu. Ostatní části programu by ho neměly přepisovat přímo. Python přístup k němu technicky dovolí; podtržítko není heslo ani zámek.

```python
sklad = Zasoba("Kniha", 5)
novy_pocet = sklad.prijmi(3)
print(novy_pocet)                 # 8
```

Volající nemusí znát jméno vnitřního atributu. Stačí mu dohoda o veřejných metodách. Kdybychom později změnili způsob uložení množství, ostatní části mohou dál používat stejné operace.

## Rozhraní naší zásoby

- `stav()` vrátí současný počet a nic nezmění.
- `prijmi(kolik)` přičte příjem a vrátí nový počet.
- `vydej(kolik)` odečte výdej a vrátí nový počet.

```python
def prijmi(self, kolik):
    self._pocet += kolik
    return self._pocet
```

Při `sklad.prijmi(3)` Python sváže metodu s objektem sklad a předá mu self, podobně jako u položky v minulé lekci. Mění se atribut tohoto objektu. Název ani jiná zásoba se měnit nemají. Metoda vrací číslo, které hlavní program může zobrazit nebo využít dál.

Zatím používáme pouze platné operace: počáteční nezáporný celý počet, kladné celé množství příjmu a výdej nejvýš do aktuálního stavu. Ochranu před chybnou operací přidáme příště. Samotné schování údaje za podtržítko pravidla ještě nevytváří.

## Detektivní pokus

Ukázka má zásobu knih a zásobu obalů. Knihy přejdou z 5 přes příjem na 8 a po výdeji na 6. Obaly zůstanou na 2. Před spuštěním zkuste vyznačit, na kterou instanci každé volání působí.

Přidejte v hlavním bloku druhý výpis `knihy.stav()`. Opakované čtení má vrátit stále 6. Potom vytvořte zásobu bez druhého argumentu a sledujte výchozí nulu.

## Váš úkol

Doplňte konstruktor a tři metody třídy Zasoba. Název uložte do nazev a počet do vlastního vnitřního atributu s podtržítkem. Jeho jméno můžete zvolit; kontrola stav zjišťuje přes veřejné metody.

Příjem i výdej vracejí nový počet, stav pouze čte. Metody nic nevypisují. Platné operace mají fungovat opakovaně, včetně výdeje posledních kusů na nulu. Každá instance má samostatný stav. U tohoto úkolu se nezadávají neplatná množství; další lekce už je bude muset odmítnout.
