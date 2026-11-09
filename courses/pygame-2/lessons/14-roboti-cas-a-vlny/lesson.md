## Lov dostane časový limit a další vlny

Jedna trojice robotů je trénink. Teď je za třicet herních sekund budete chytat v dalších vlnách. Po posledním chyceném robotovi vznikne celá nová vlna; její začátek neobnoví životy, čas, skóre ani přesnost. Hra tak odměňuje rychlost i rozumné klikání.

**Kolo** vlastní hranice, generátor náhody, Lov, zbývající čas, číslo vlny a důvod konce. Predchozi.py už obsahuje Robot/Hlidac/Kyvac, najdi_robota a Lov. Skládání hotových objektů je kompozice: Kolo nemusí dědit Lov, ale používá jej jako svou součást.

## Herní čas a jednoznačný konec

```python
zbyva = 0.03
for dt in (0.016, 0.016):
    zbyva = max(0, zbyva - dt)
    print(round(zbyva, 3), zbyva == 0)
```

Zbývá 0,014 s a potom přesně nula. Max nedovolí záporný čas. Porovnání ==0 je zde v pořádku, protože na nulu výslovně omezujeme. Neporovnáváme dvě náhodně zaokrouhlená desetinná čísla.

Společná smyčka nyní volá update(dt) **před** zpracováním událostí daného snímku. Nejprve uplyne čas, potom teprve může kliknutí bodovat. Pokud čas v tomto kroku vypršel, poslední stisk už body nepřidá. Při konci se zmrazí model, ale události a kreslení dál fungují pro zavření okna. Dt=min(tick(60)/1000,0.05) je herní čas: dlouhou prodlevu záměrně nepočítá celou a pauzu později nezapočítáme vůbec.

## Reprodukovatelná náhoda

Random(seed) vytvoří generátor náležející jednomu kolu. Dvě nezávislá kola se stejným seedem zopakují stejnou posloupnost, jiný seed vytvoří jiné pozice. Seed předáváme konstruktoru, neděláme společné random.seed pro celý program. Pozdější vlny pokračují v téže posloupnosti, nedělají nový generátor. S None při konstrukci zvolí Python nový náhodný začátek.

## Váš úkol: Kolo(seed=11,limit=30)

Nekladný limit odmítněte ValueError; jinak je kladný konečný počet sekund. Vytvořte vlastní kopii HRANICE, rng=random.Random(seed), nový Lov s prázdnou Group, zbyva=float(limit), cislo=0, konec=False a duvod=''. Zavolejte dalsi_vlna, takže první viditelná vlna má číslo 1 a tři cíle.

**dalsi_vlna()** vrátí False bez změn, pokud kolo skončilo nebo v lov.roboty ještě někdo je. Jinak zvýší cislo, vytvoří min(2+cislo,6) robotů a vrátí True. I nová vlna zachová všechny čítače Lov a zbyva. Roboti se střídají od indexu 0: Hlidac, Kyvac, Hlidac…

Pro každý index losujte `rng.randint(left + 90, right - 90)` a potom `rng.randint(top + 22, bottom - 22)`. U hlídače pak `rng.choice((-1, 1))` zvolí znaménko vodorovné rychlosti. X má rezervu i pro kývání, celý obraz zůstane uvnitř. Poloměr a body mají výchozí hodnoty předchozích tříd. Hlídač má rychlost `(znaménko * min(80 + 15 * (cislo - 1), 220), 50)`. Kývač `amplituda=50` a `perioda=max(0.7, 2 - 0.15 * (cislo - 1))`. Strop rychlosti, počtu a spodní mez periody chrání hratelnost; nezačínáme nekonečně rychlými cíli.

**update(dt)** po konci nedělá nic. Jinak nejprve omezí zbyva−dt na nulu. Při nule nastaví konec=True, duvod='cas' a roboty už neposouvá. Pokud místo toho nemá Lov životy, skončí s duvod='zivoty'. Jinak provede lov.roboty.update(dt,hranice) a zkusí dalsi_vlna pro případ prázdné skupiny. Dt je nezáporný konečný počet sekund.

**klik(udalost)** po konci vrací None bez změn. Jinak předá událost do lov.klik a vrátí jeho výsledek. Při nulových životech hned ukončí kolo s důvodem 'zivoty'; jinak při prázdné skupině vytvoří další vlnu. Nově vytvořené cíle se pohnou až v příštím update, ne ještě jednou při témž kliknutí.

Vyzkoušejte všechny cíle, přibývající počet a rychlost, poslední život a krátký limit zadaný v konstruktoru. Skóre ani přesnost nesmí naskočit znovu od nuly při změně vlny. Skutečné okno používá váš Kolo, nikoli jinou předváděcí hru.
