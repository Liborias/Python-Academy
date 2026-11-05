## Šipka požádá o zatáčku, časovač posune hada

Rozšíříme třídu Hra pomocí dědění. `RizenaHra(Hra)` využije její start i časovač, ale před každým krokem může změnit směr. Soubor `had_hra.py` obsahuje vzorové řešení předchozí lekce; model a zobrazení dál zůstávají v dalších dvou souborech.

Nová klávesová událost nemá volat `had.krok()`. Jinak by rychlost závisela na počtu stisků a opakování klávesy. Pohyb nadále řídí pouze tik.

## Připojení kláves

```python
self.okno.onkey(self.nahoru, "Up")
self.okno.listen()
```

`onkey` přiřadí klávese metodu bez argumentů. Opět předáváme metodu **bez závorek**. Názvy šipek jsou `"Up"`, `"Down"`, `"Left"`, `"Right"`. Metody nahoru, dolu, vlevo a vpravo jsou připravené: každá předá odpovídající dvojici do `nastav_smer`.

`listen()` požádá okno o příjem kláves. Klikněte do herního okna, pokud mají šipky stále fokus v editoru nebo prohlížeči. Turtle pomocí onkey obvykle zpracovává uvolnění klávesy; pro vyzkoušení šipku krátce stiskněte a pusťte. Držení klávesy není potřeba — had pokračuje sám.

## Proč potřebujeme čekající směr

Had s více články nesmí okamžitě otočit hlavu do krku. Když se pohybuje doprava `(1, 0)`, zakážeme směr doleva `(-1, 0)`. Opačnou dvojici získáme změnou obou znamének: `(-dx, -dy)`.

Pouhý zákaz opačného směru ale nestačí. Představte si dva rychlé stisky mezi tiky: nahoru a vlevo. Kdybychom hned přepisovali aktuální směr, povolili bychom obě změny a had by ve skutečnosti skočil z pohybu doprava přímo doleva.

Proto uložíme **nejvýš jednu změnu na jeden krok** do `self.cekajici`. Hodnota None znamená, že žádná změna nečeká. Současný `self.had.smer` zůstává až do tiku beze změny.

Metoda `nastav_smer(smer)` postupuje takto:

1. Neplatná dvojice se odmítne. Podporujeme právě `(1, 0)`, `(-1, 0)`, `(0, 1)`, `(0, -1)`.
2. Pokud už čeká změna, další stisk ji nepřepíše.
3. Stejný směr odmítneme také; takový stisk nemusí zbytečně obsadit čekající změnu.
4. Opačný směr vůči aktuálnímu pohybu odmítneme.
5. Zbývající kolmý směr uložíme do cekajici a vrátíme True. Ve všech odmítnutých případech vrátíme False a stav ponecháme.

Podmínka `self.cekajici is not None` zjišťuje přítomnost čekající hodnoty. Návrat True/False je užitečný pro testování, samotná obsluha kláves ho nepotřebuje vypisovat.

## Rozšíření tiku přes super

V přepsané metodě `tik` nejdřív případný čekající směr přiřadíme do `self.had.smer` a cekajici nastavíme zpět na None. Pak právě jednou zavoláme `super().tik()`.

Základní třída provede krok, kreslení, update a další časovač. Díky tomu se tato logika neopisuje a další úprava základního tiku se přenese i do ovládané verze. Jde o tentýž objekt Hra, ne o druhou hru.

Když dostane hra jedoucí doprava rychle za sebou Up a Left, přijme jen Up. První tik tedy posune hada nahoru. Až po tomto kroku může nový stisk Left připravit zatáčku doleva. Stisk opačné či stejné šipky čekající místo neobsadí.

## Vyzkoušejte rozpracovanou hru

Spusťte ukázku, aktivujte herní okno a vyzkoušejte čtyři šipky. Zkuste i zakázanou otočku do protisměru a dvě rychlé zatáčky mezi kroky. Pro snazší pozorování lze hlavní konstrukci změnit na `RizenaHra(okno, had, pero, interval=500)`.

Had prochází okraji a stále má tři články. Potrava, růst, kolize s tělem, skóre a restart budou následující části. Zatím se mohou části těla překrýt bez ukončení hry. Konec ověřování: zavřete okno nebo použijte Stop v aplikaci.

## Váš úkol

Doplňte `nastav_smer`, přepsaný `tik` a `pripoj`. V pripoj přiřaďte čtyři připravené směrové metody odpovídajícím šipkám a zapněte listen. Připojení samo nesmí měnit směr, pohybovat hadem nebo spouštět časovač.

Konstruktor, čtyři krátké obslužné metody a hlavní blok ponechte. Nezapomeňte na return True/False při přijímání směru, uvolnění čekající změny při každém tiku a skutečnou spolupráci se základní metodou přes super. Každá instance má vlastní čekající změnu i hada.
