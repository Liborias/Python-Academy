## Kolizi posoudíme dřív, než změníme stav

Třída `BezpecnyHad(HladovyHad)` doplní ochranu před vstupem hlavy do vlastního těla. Soubory had_model.py a had_potrava.py obsahují funkční předchozí kroky. Průchozí okraje zůstávají: samotné překročení okraje není prohra.

Nejprve ze současné hlavy, směru a rozměrů spočítáme **budoucí hlavu** stejným způsobem jako v modelu:

```python
nova = ((x + dx) % self.sirka, (y + dy) % self.vyska)
```

Tento výpočet ještě nemění seznam. Pokud krok není dovolený, vyvoláme `ValueError("Had narazil do těla")`. Výjimku už znáte z pravidel objektů; nyní označuje odmítnutou herní operaci. Po odmítnutí mají zůstat tělo, směr i rozměry beze změny.

## Odcházející ocas je zvláštní případ

Představte si stočeného hada s tělem:

```python
[(1, 1), (1, 0), (0, 0), (0, 1)]
```

Hlava leží v `(1, 1)`, ocas v `(0, 1)`. Při kroku doleva chce hlava vstoupit právě na místo ocasu. Jestliže se had neprodlužuje, ocas při témže kroku tuto buňku opustí. Takový pohyb je dovolený.

Proto při běžném pohybu považujeme za překážku jen `self.body[:-1]`. Poslední článek z kontroly vyloučíme. Není správné odmítnout každou buňku celého starého těla, ale ani všechny kolize ignorovat.

Kdyby nová hlava současně snědla potravu, ocas zůstane a překážkou je celé tělo. Běžný generátor potravu na hada nepoloží, přesto pravidlo růstu a kontrolu modelu udržujeme vzájemně správné i při takto zadaném kroku.

## Po úspěšné kontrole navážeme na předka

```python
if nova in obsazene:
    raise ValueError("Had narazil do těla")
return super().krok(potrava)
```

`obsazene` je seznam překážek vybraný podle předchozího pravidla. Zápis `in` zjišťuje shodu dvojic souřadnic. Teprve po úspěšné kontrole zavoláme předchozí růstový krok se stejnou potravou a využijeme jeho návrat.

Nejprve pohnout hadem a až potom vyvolat výjimku by ponechalo neplatný obrázek a změněná data. Podobně by volání základního kroku dvakrát posunulo hada o dvě buňky. Zde děláme jeden výhledový výpočet a jeden skutečný pohyb.

## Jak číst ukázku

Ukázka nejprve dovoleně vstoupí do odcházejícího ocasu `(0, 1)`. Pak se pokusí vstoupit do již obsazeného článku `(1, 1)` a zachytí ValueError. Výpis ukáže poslední platné tělo.

Směr v konzolové ukázce přiřazujeme přímo, abychom mohli vyzkoušet ochranu samotného modelu. Při hraní dál platí také zákaz otočky a jedna zatáčka na tik z lekce 32. Kontrola modelu doplňuje pravidla ovládání.

## Váš úkol

Doplňte `BezpecnyHad.krok(potrava=None)`. Odmítněte kolizi výjimkou ValueError před jakoukoli změnou modelu. Bez růstu povolte vstup do odcházejícího ocasu; při růstu se kontroluje celé tělo. Platný krok musí skutečně využít `super().krok(potrava)` a vrátit jeho novou hlavu.

Ověřte i kolizi přes průchozí okraj: například při šířce 4 se krok doleva z x = 0 posuzuje v buňce x = 3. Pokud je tam nepřechodná část těla, jde o kolizi. Jednočlánkový had může bez potravy oběhnout i plochu 1 × 1.
