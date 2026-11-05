## Začínáme vlastní Snake

V dalších lekcích sestavíme jednu hru po částech. Nyní napíšeme její **model**: údaje o hadovi a pravidlo jednoho kroku. Model nepotřebuje okno ani želvu. Díky tomu můžeme pohyb snadno zkontrolovat výpisem a později připojit jiné zobrazení.

Naše varianta má průchozí okraje: co odjede vpravo, objeví se vlevo; totéž platí nahoře a dole. Toto pravidlo zůstane i v dalších krocích projektu. Potrava, růst, střet s vlastním tělem a skóre přijdou později. Teď had pouze cestuje a zachovává délku.

## Buňka není pixel

Herní plocha je mřížka. Pro šířku 6 jsou sloupce `0, 1, 2, 3, 4, 5`, pro výšku 4 jsou řádky `0, 1, 2, 3`. Souřadnice `(0, 0)` označuje buňku vlevo dole; vyšší y znamená pohyb nahoru. Zatím neurčujeme velikost buňky na monitoru.

```python
body = [(4, 1), (3, 1), (2, 1)]
smer = (1, 0)
```

`body[0]` je hlava. Další dvojice popisují části těla směrem k ocasu. Směr `(1, 0)` znamená přidat 1 ke sloupci a 0 k řádku. Ostatní směry jsou `(-1, 0)` vlevo, `(0, 1)` nahoru a `(0, -1)` dolů. Jsou to posuny v buňkách, nikoli úhly želvy.

## Co se stane během jednoho kroku

Pro uvedené tělo a pohyb doprava vznikne nová hlava `(5, 1)`. Nový stav má být `[(5, 1), (4, 1), (3, 1)]`:

1. Z původní hlavy přečteme x, y a ze směru dx, dy.
2. Spočítáme novou hlavu.
3. `self.body.insert(0, nova)` vloží novou dvojici na začátek.
4. `self.body.pop()` odstraní poslední dvojici, takže se had zatím neprodlouží.
5. Metoda vrátí novou hlavu pomocí return.

Nestačí posunout jen první položku: zbytek těla musí následovat původní polohu hlavy. Dvojice nepřepisujeme uvnitř; vytváříme novou dvojici a upravujeme seznam.

## Jak funguje průchod přes okraj

```python
nove_x = (x + dx) % self.sirka
nove_y = (y + dy) % self.vyska
```

Operátor `%` už znáte jako zbytek po dělení. Při kladné šířce udržuje souřadnici v rozsahu `0` až `sirka - 1`: `6 % 6` je 0, ale také `-1 % 6` je 5. Posun z levého okraje doleva se tedy objeví na posledním sloupci. Pro řádky použijeme výšku, která nemusí být stejná jako šířka.

Konstruktor vytváří vlastní seznam pomocí `list(body)`. Každá instance si tak mění svůj stav. Vstupní dvojice jsou neměnné n-tice, takže zde postačuje kopie samotného seznamu.

## Vyzkoušejte ukázku

Spusťte ji v aplikaci. Počáteční hlava `(4, 1)` postupně projde buňkami `(5, 1)`, `(0, 1)` a `(1, 1)`. Výpis „Nahoru“ pak ukáže `(1, 2)`. Po každém kroku zůstávají tři části těla. Změňte směr na `(0, -1)` a sledujte přechod přes dolní okraj.

Blok `if __name__ == "__main__":` ve vašem úkolu spouští malou demonstraci pouze při přímém spuštění souboru. Při pozdějším importu třídy Had se výpisy neprovedou.

## Váš úkol

Doplňte metodu `Had.krok(self)` podle popsaného postupu. Vraťte novou hlavu jako dvojici a udržte pořadí i počet částí těla. Čtěte aktuální `self.smer`, `self.sirka` a `self.vyska`; nespoléhejte na jednu pevnou velikost nebo směr.

Konstruktor v šabloně je připravený. Vstupem je neprázdný seznam platných buněk, kladné celé rozměry a jeden ze čtyř uvedených směrů. Není třeba přidávat další validaci nebo řešit kolize. Fungovat má i had s jedinou buňkou a plocha široká či vysoká jednu buňku. Opakované volání mění jen tohoto hada, nikoli původní vstupní seznam nebo jinou instanci.
