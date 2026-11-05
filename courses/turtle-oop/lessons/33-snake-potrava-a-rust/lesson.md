## Had už umí cestovat. Teď dostane hlad

První část projektu měla tři články a průchozí okraje. Přidáme dvě pravidla: při snědení potravy had vyroste o jeden článek a další potrava se objeví pouze na volné buňce. Pohyb a obrázek dál zůstávají oddělené. Tato lekce běží v konzoli, abychom nové pravidlo mohli přesně pozorovat.

Soubor `had_model.py` obsahuje původní třídu Had z lekce 29. Třída `HladovyHad(Had)` ji rozšíří; nové jméno nám umožní ponechat starší lekce beze změny.

## Růst znamená ponechat původní ocas

```python
ocas = self.body[-1]
nova = super().krok()
if nova == potrava:
    self.body.append(ocas)
return nova
```

Před pohybem si uložíme poslední dvojici souřadnic. Základní krok přidá hlavu a odebere ocas jako dosud. Jestliže se **nová hlava** dostala na potravu, původní ocas vrátíme na konec. Celé původní tělo tak zůstane a vpředu přibude nová hlava.

Potrava je dvojice souřadnic v buňkách, například `(5, 1)`. Výchozí argument `potrava=None` znamená, že při tomto kroku žádná potrava ke snědení není. Metoda dál vrací novou hlavu, nikoli délku nebo výpis.

Například tělo `[(4, 1), (3, 1), (2, 1)]` jedoucí doprava dostane potravu `(5, 1)`. Po kroku má čtyři buňky `[(5, 1), (4, 1), (3, 1), (2, 1)]`. Bez potravy by poslední `(2, 1)` odpadla. Růst funguje i po průchodu přes okraj, protože používáme souřadnici vypočítanou základní metodou.

## Potravu vybíráme z volných míst

Kdybychom opakovaně losovali souřadnici, dokud nenarazíme na volnou, při úplně zaplněné ploše by cyklus nikdy neskončil. Raději sestavíme seznam všech možností:

```python
volne = []
for y in range(had.vyska):
    for x in range(had.sirka):
        if (x, y) not in had.body:
            volne.append((x, y))
```

Vnější cyklus projde řádky, vnitřní všechny sloupce. `not in` odmítne buňky obsazené hadem. Každá volná buňka se objeví právě jednou. U naší malé plochy je takový přehledný postup dostatečný.

Když je seznam prázdný, vrátíme None. Není to potrava v buňce `(0, 0)` — tuto platnou souřadnici nesmíme zaměnit za chybějící potravu. Při plné ploše se později vyhlásí výhra.

## Funkce jako vyměnitelná součást

Podpis `vyber_potravu(had, vyber=random.choice)` má druhý argument, kterým je **funkce**. Bez zadání se použije `random.choice`, tedy náhodný výběr jedné položky seznamu ze standardní knihovny. Nic se neinstaluje přes pip.

Pro neprázdný seznam zavoláme `vyber(volne)` právě jednou a vrátíme jeho výsledek. Není třeba hned vytvářet nový souřadnicový pár nebo seznam znovu náhodně míchat. Můžeme ale předat jiný způsob výběru:

```python
def prvni(volne):
    return volne[0]

potrava = vyber_potravu(had, prvni)
```

Předáváme jméno funkce bez závorek, podobně jako metodu do časovače. Uvnitř vyber_potravu dostane funkce celý seznam a vrátí jednu z jeho položek. Při testování tak můžeme předem vědět, co bude vylosováno. Pořadí volných buněk není součástí zadání; důležité je jejich úplné a správné pokrytí. Na prázdném seznamu se funkce vyber vůbec nevolá.

## Váš úkol

Doplňte `HladovyHad.krok(potrava=None)` a `vyber_potravu(had, vyber=random.choice)`. Krok využije skutečnou základní metodu přes super, při shodě nové hlavy s potravou přidá původní ocas a vrátí novou hlavu. V ostatních případech se délka nezmění.

Výběr potravy nabídne předané funkci každou volnou buňku právě jednou; při plné ploše vrátí None bez volání výběru. Nesmí měnit tělo, směr ani rozměry hada. Fungovat mají i nesymetrické a jednobuňkové plochy. Kolize s tělem zatím neřešte — to bude příští krok.

Spusťte ukázku: první výpis má hlavu `(5, 1)` a délku 4, druhý hlavu `(0, 1)` a stále délku 4. Zkuste změnit potravu na vzdálenou buňku a porovnejte délku.
