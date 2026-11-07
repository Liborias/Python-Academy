## Reakce podle aktuálního vstupu

Entry je jednořádkové vstupní pole. Uživatel do něj může napsat jméno; metoda get() vrátí jeho aktuální obsah jako text. Tlačítko potom zobrazí pozdrav. Nahradíme tak konzolový input ovládáním, které může uživatel opakovaně měnit.

V ukázce je připravený popisek Vaše jméno:, Entry, tlačítko Pozdravit a výsledek. Zobrazíme je v rozložení grid, tedy v mřížce řádků a sloupců.

## Souřadnice v mřížce začínají nulou

row určuje řádek, column sloupec. Vstup patří na row=0, column=1, popisek na row=0, column=0. Tlačítko je ve druhém řádku a výsledek ve třetím. columnspan=2 znamená, že widget zabere oba sloupce.

sticky určuje, ke kterým okrajům buňky se widget přitáhne. w je levý okraj a e pravý; sticky="ew" roztáhne vstup do šířky jeho buňky. Samotné grid neurčuje, který sloupec má získat volné místo při zvětšování okna. Proto okno.columnconfigure(1, weight=1) přidělí volnou šířku sloupci se vstupem. padx a pady zachovávají význam vnějších mezer z minulé lekce.

V jednom rodiči nemícháme pack a grid pro jeho děti. Tato lekce používá pro všechny prvky stejného okna grid. Později budeme prvky seskupovat do Frame a různé správce použijeme v různých rodičích.

## Kdy se čte jméno

```python
def pozdrav():
    text = jmeno.get().strip()
```

Čtení patří dovnitř funkce tlačítka. Kdybychom get zavolali pouze při vytváření okna, uložili bychom počáteční prázdný vstup a pozdější psaní by výsledek neaktualizovalo.

strip() odstraní krajní mezery. Zachová diakritiku, velikost písmen i mezery uvnitř jména. Řetězec složený jen z mezer se změní na prázdný text. Podmínka if not text jej rozpozná a zobrazí Zadejte jméno. Při neprázdném vstupu nastavíme výsledek na Ahoj, Ema! nebo pozdrav s jiným zadaným jménem.

Výsledek měníme přes configure na stejném popisku. Samotné vyplnění Entry zprávu nemění, teprve kliknutí ji přepočítá.

## Váš úkol

Rozložení a připojení command jsou připravené. Doplňte pozdrav: přečtěte aktuální Entry, odstraňte krajní mezery a upravte popisek podle pravidel. Při otevření okna má zůstat text Zadejte jméno a klikněte. Prázdný vstup po kliknutí zobrazí Zadejte jméno. Jinak zobrazte Ahoj, jméno! se skutečným obsahem pole.

Vyzkoušejte prázdné pole, několik mezer, jméno s diakritikou a nové jméno po prvním pozdravu. Například vstup se dvěma mezerami před i za Ema má dát Ahoj, Ema! Původní mezery uvnitř vícečlenného jména zůstávají. Nakonec zvětšete okno a sledujte, jak se roztáhne pole ve druhém sloupci.
