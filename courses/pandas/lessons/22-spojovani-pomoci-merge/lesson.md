## Cena patří k produktu, ne k pořadí řádku

V jedné tabulce máme prodané produkty a počty kusů. V druhé jejich ceny, ale v jiném pořadí. Připojení ceny jako obyčejného seznamu by mohlo prohodit čaj a kávu. `prodeje.merge(cenik, on="produkt", how="left", sort=False)` spojí tabulky podle společné hodnoty ve sloupci produkt.

Klíč není automaticky řádkový index. Parametr on označuje datový sloupec, který existuje v obou tabulkách. V našich prvních úkolech jsou klíče str bez chybějících hodnot a každý produkt se v ceníku vyskytuje nejvýše jednou. Opakované prodeje stejného produktu jsou naopak platné a každý dostane odpovídající cenu.

## Co zachová left a co vybere inner

Left spojení ponechá všechny řádky levé tabulky. Pokud produkt v ceníku není, cenu doplní NaN; prodejní řádek se nezahodí. Sort=False v těchto úkolech zachovává levé pořadí. Vstupní indexy se při spojení přes sloupce nepoužijí jako identifikátory a výstup má nový RangeIndex. Sloupce levé tabulky zůstanou, za nimi se přidají pravé neklíčové sloupce; společný klíč je ve výsledku jednou.

`how="inner"` vrací pouze spárované řádky. Hodí se pro jinou otázku, ale může potichu vynechat produkt, kterému cenu neznáme. Před výpočtem tržeb proto musíme vědět, zda chceme tyto řádky zachovat k prověření, nebo zda opravdu analyzujeme jen spárovanou část dat.

```python
vsechny_prodeje = prodeje.merge(cenik, on="produkt", how="left", sort=False)
jen_s_protejskem = prodeje.merge(cenik, on="produkt", how="inner", sort=False)
```

V obou případech původní tabulky zůstávají zachované. Neznámou cenu nenahrazujeme automaticky nulou: to by znamenalo bezplatný prodej, nikoli neznámý údaj.

## Klíče se mohou jmenovat jinak

`objednavky.merge(produkty, left_on="kod", right_on="id", how="left", sort=False)` spojí hodnoty levého kod s pravým id. Ve výsledku zůstanou oba názvy klíče. U nespárovaného řádku proto může být pravé id chybějící, i když levý kod existuje. Není potřeba přejmenovávat zdrojové tabulky jen kvůli tomuto spojení.

## Dvě hodnoty tvoří jeden klíč

Cena stejného produktu se může měnit podle dne. `on=["den", "produkt"]` vyžaduje shodu obou hodnot zároveň. Ceník tak může mít čaj pro dva různé dny, ale každou dvojici nejvýše jednou. Spojení jen podle produktu by mohlo přidat nesprávnou cenu nebo vytvořit více kombinací řádků. Ověření této jedinečnosti budeme v příští lekci vyžadovat přímo parametrem validate.

V úkolech používáme známá schémata, jedinečné pravé klíče a nekolizní názvy ostatních sloupců. Neřešíme zatím dvě různé veličiny se stejným názvem; jejich suffixes přijdou spolu s kontrolou spojení.

## Váš úkol

Dokončete `pripoj_cenik(prodeje, cenik)`. Prodeje mají sloupce produkt (str), kusy (int64), ceník produkt (str), cena (float64). Klíče nechybějí a v ceníku jsou jedinečné. Vraťte left spojení se sloupci produkt, kusy, cena a RangeIndex: všechny levé řádky v původním pořadí, chybějící cena jako NaN. Prázdné vstupy se správnými sloupci jsou platné. Vstupy neměňte.

Další čtyři úkoly procvičí inner spojení, předaný název klíče, různé názvy klíčů a denní ceník. Vždy nejprve vysvětlete, které řádky mají ve výsledku zůstat a proč.
