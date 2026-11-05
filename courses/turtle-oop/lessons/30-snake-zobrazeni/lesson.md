## Stejný model, první obrázek

V předchozí lekci jsme ověřili pohyb výpisem. Nyní oddělíme **zobrazení**: přečte tělo hada a nakreslí je. Kreslení nemá provádět krok, měnit souřadnice nebo řadit seznam. Stejný stav modelu tak můžeme opakovaně zobrazit.

Připravený soubor `had_model.py` obsahuje vzorovou třídu Had z lekce 29. Zápis `from had_model import Had` načte tuto třídu z vedlejšího souboru. Není to pip balíček a nic dalšího se neinstaluje. Každá projektová lekce dostane potřebné soubory, takže není závislá na tom, co máte rozepsané v minulé lekci.

## Převod buněk na pixely

Zvolíme buňku velkou 20 pixelů. Želva má střed okna v `(0, 0)`, zatímco naše buňky začínají vlevo dole. Nejprve proto posuneme střed mřížky na nulu a teprve pak násobíme velikostí buňky:

```python
pixel_x = (x - (sirka - 1) / 2) * 20
pixel_y = (y - (vyska - 1) / 2) * 20
```

Pro mřížku 6 × 4 je prostředek mezi sloupci 2 a 3 a mezi řádky 1 a 2. Buňka `(0, 0)` se zobrazí v `(-50, -30)`, buňka `(5, 3)` v `(50, 30)`. Rozdíl mezi dvěma sousedními středy je vždy 20 pixelů. Půlky ve výpočtu jsou správně: při sudém počtu buněk leží střed mezi nimi.

Funkce `na_pixely(bod, sirka, vyska)` vrátí vypočítanou dvojici. Model si dál pamatuje buňky; do jeho seznamu pixely nezapisujeme.

## Jedno pero, více otisků

Želva nemusí představovat jediný článek hada. Použijeme jedno pomocné pero a jeho otisky:

```python
pero.clear()
for i, bod in enumerate(had.body):
    pero.goto(na_pixely(bod, had.sirka, had.vyska))
    if i == 0:
        pero.color("yellow")
    else:
        pero.color("green")
    pero.stamp()
```

`clear()` smaže předchozí kresbu a otisky tohoto pera. Nevymaže celé okno ani model. Bez něj by při pohybu zůstávaly staré články jako stopa.

`enumerate` nám dá index i buňku. Index 0 patří hlavě, proto dostane žlutou barvu, ostatní články zelenou. `goto` přesune pero a `stamp()` zanechá kopii jeho tvaru na aktuálním místě. Každou buňku vykreslíme právě jednou a ve stejném pořadí jako v modelu.

## Co připravuje hotová funkce priprav_okno

- `turtle.Screen()` získá okno; `setup(...)` nastaví jeho velikost včetně okraje 20 pixelů na každé straně.
- `title(...)` nastaví název okna a `bgcolor("black")` černé pozadí.
- `tracer(0)` vypne průběžné animované překreslování. Celý snímek zveřejníme najednou přes `okno.update()`, až budou otisky hotové.
- `shape("square")` vybere čtverec. `shapesize(0.8, 0.8)` zmenší standardní dvacetipixelový čtverec na přibližně 16 × 16 pixelů, takže mezi články zůstane mezera.
- `penup()` zabrání spojovacím čarám při přesunech. `hideturtle()` schová pohyblivé pomocné pero; jeho otisky přesto zůstávají vidět.

Funkce vrátí okno a pero. Na konci hlavního programu zavoláme `okno.mainloop()`: Python předá řízení obsluze událostí a okno zůstane otevřené. Ukončíte ho křížkem nebo tlačítkem Stop v aplikaci.

## Spuštění na vlastním počítači

Jde o skutečné samostatné okno Turtle na počítači, kde běží Python. V prohlížeči se nekreslí do stránky. Při práci ve vzdáleném prostředí potřebujete jeho grafickou plochu. Na místním počítači lze ověřit Tk příkazem `python -m tkinter` (ve Windows případně `py -m tkinter`); má se otevřít testovací okno. Příprava kurzu popisuje instalaci Tkinteru pro váš systém.

Při otevření úkolu v editoru použijte jeho pracovní složku včetně `had_model.py`. Aplikace soubor připraví vedle vašeho kódu. Při ručním kopírování musí zůstat oba soubory vedle sebe; nepojmenovávejte vlastní soubor `turtle.py`.

## Váš úkol

Doplňte `na_pixely` a `vykresli`. První funkce vrací dvojici podle uvedeného výpočtu pro libovolné kladné rozměry. Druhá nejdřív jednou smaže otisky daného pera, pak vykreslí všechny buňky v pořadí: žlutá hlava a zelené tělo. Nic nevypisuje, nemění model a nemusí nic vracet.

Přípravu okna a hlavní blok ponechte. Výsledkem jsou tři čtverce; pohyb přidáme až v následující lekci. Zkuste do seznamu v hlavním bloku přidat další navazující buňku a spusťte program znovu.
