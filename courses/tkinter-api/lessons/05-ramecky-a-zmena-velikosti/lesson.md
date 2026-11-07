## Formulář rozdělíme na menší části

Frame je kontejner neboli rámeček pro další widgety. Nemusí mít viditelný okraj: jeho hlavní úlohou je seskupit součásti formuláře a spravovat jejich rozložení. Vytvoříme okno Příprava výpravy se dvěma rámečky. Horní obsahuje popisek Název výpravy: a vstup. Dolní obsahuje zprávu Formulář je připravený.

Rodič určuje skutečné uspořádání. V zápisu `ttk.Entry(formular)` je vstup potomkem rámečku formular, nikoli hlavního okna. Pouhé pojmenování proměnné ani vizuálně podobná poloha rodiče nezmění.

## Každý rodič má své rozložení

```python
formular = ttk.Frame(okno, padding=12)
formular.pack(fill="x", padx=16, pady=12)
ttk.Label(formular, text="Název výpravy:").grid(row=0, column=0, padx=8)
```

První řádek vytvoří rámeček v okně. `padding=12` u ttk.Frame přidá vnitřní prostor mezi hranou rámečku a jeho obsahem. Naproti tomu padx a pady u pack vytvářejí vnější odstup od okolí. `fill="x"` dovolí rámečku vyplnit dostupnou vodorovnou šířku.

Hlavní okno spravuje oba rámečky přes pack. Horní rámeček spravuje své děti přes grid. Dolní má svůj popisek umístěný přes pack. To je správná kombinace: pack a grid se nemíchají mezi dětmi stejného rodiče. Naopak vstup vytvořený omylem s rodičem okno by se přes grid dostal mezi rámečky spravované pack a způsobil chybu.

## Aby se vstup roztahoval

```python
formular.columnconfigure(1, weight=1)
nazev.grid(row=0, column=1, sticky="ew", padx=8)
```

Volná šířka musí projít celou cestou: okno nabídne místo rámečku, pack s fill="x" jej využije, sloupec 1 s kladnou váhou místo přidělí a sticky="ew" dovolí vstupu vyplnit buňku. Chybějící článek poznáte při zvětšení okna: některá část zůstane stejně úzká.

Zde měníme šířku, ne výšku. Volba `expand=True` u pack by navíc přidělovala volný prostor kolem prvků; pro tento formulář ji nepotřebujeme. Není náhradou za fill.

## Váš úkol

Do připraveného okna přidejte právě dva rámečky, oba přímo v okně a oba přes pack s fill="x" (fill="both" je také možné). Horní musí být umístěn před dolním. V horním vytvořte popisek Název výpravy: na řádku 0 ve sloupci 0 a jedno Entry na řádku 0 ve sloupci 1. Použijte grid, kladnou váhu sloupce 1 a sticky="ew" u vstupu. V dolním umístěte přes pack popisek Formulář je připravený.

Neměňte titulek Příprava výpravy. Vnitřní a vnější mezery z ukázky můžete upravit podle sebe; ověřujeme rodiče, pořadí a roztažení, nikoli přesný vzhled. Zvětšete skutečné okno do šířky a sledujte vstup. Zkuste vysvětlit, proč je pack spolu s grid v tomto programu v pořádku.
