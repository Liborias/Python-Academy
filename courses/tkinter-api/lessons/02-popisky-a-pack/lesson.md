## Okno začne něco sdělovat

Textové pole bez úprav nazýváme popisek, v Tkinteru Label. Obecné slovo widget označuje součást okna: popisek, tlačítko nebo vstupní pole. Každý widget má rodiče, který ho obsahuje. Dnešní dva popisky budou přímo v hlavním okně.

Použijeme from tkinter import ttk. Modul ttk je součást Tkinteru a poskytuje prvky, jejichž vzhled vychází z tématu systému. Nepřidává další pip balíček. Barvy a detaily se mezi systémy mohou lišit; texty a chování zůstávají stejné.

## Vytvoření a umístění jsou dvě věci

```python
nadpis = ttk.Label(okno, text="Expediční přehled")
nadpis.pack(padx=16, pady=12)
```

První řádek vytvoří popisek s rodičem okno. Pojmenovaný argument text určuje jeho obsah. Objekt uložíme do nadpis. Samotné vytvoření ještě neurčuje, kde se má widget zobrazit.

Druhý řádek požádá správce rozložení pack o umístění. Výchozí pack skládá prvky pod sebe podle pořadí umístění a uprostřed dostupné šířky. Pozdější volání pro druhý popisek jej tedy umístí pod nadpis.

padx je vnější vodorovná mezera kolem widgetu, pady svislá mezera. U jednoho čísla se použije na obou stranách. Mezery pomáhají čitelnosti a oddělují součásti formuláře.

## Proč si necháme odkaz na popisek

Label vrací objekt popisku. pack() vrací None. Zápis nadpis = ttk.Label(...).pack() by proto do nadpis uložil None a později bychom přes tuto proměnnou nemohli měnit text. Když budeme widget dál používat, vytvoření a umístění zapíšeme samostatně, jako v ukázce.

Popisky neumístěné přes správce rozložení neuvidíme. Druhé hlavní Tk okno by také nebylo správným rodičem naší nástěnky. Program potřebuje jedno hlavní okno a dva jeho potomky.

## Váš úkol

Ponechte připravené okno Nástěnka a mainloop. Doplňte přesně dva popisky: nejprve Expediční přehled, pod něj Stav: připraveno. Oba umístěte přes pack přímo do stejného hlavního okna a nastavte jim padx i pady alespoň 8 pixelů. V ukázce jsou hodnoty 16 a 12, jiný dostatečný odstup je také správně.

Spusťte ukázku a porovnejte pořadí. Zkuste si změnit mezery a velikost okna. Potom na chvíli vynechte pack jednoho popisku a všimněte si rozdílu mezi vytvořeným a skutečně zobrazeným widgetem. Před kontrolou se vraťte k oběma textům a jejich umístění.
