## Co právě stavíme

Korespondenční dílna bude malé okno pro přípravu zprávy. Budeme zadávat příjemce, předmět a víceřádkový text, připojíme soubor, ověříme zprávu a předáme ji místnímu SMTP záchytu. Začneme formulářem a konceptem. Tento krok nepotřebuje síť a nic neodesílá.

Koncept je rozpracovaná práce. Může obsahovat prázdný předmět i nedopsanou adresu. Zpráva připravená k předání bude mít přísnější pravidla až v další lekci. Tím člověku dovolíme rozepsat si myšlenku a opravit ji později.

## Model uchovává obyčejná data

Funkce `vytvor_koncept(prijemce, predmet, text, priloha="")` vrací nový slovník se čtyřmi textovými hodnotami: prijemce, predmet, text a priloha. Priloha zatím zůstává prázdná; později ponese cestu k souboru. Funkce nepotřebuje okno ani připojení. Každé volání vytvoří vlastní slovník, takže dva koncepty nesdílejí jeden měnitelný záznam.

Ověřujeme jen typy. Zápis `all(isinstance(v, str) for v in (...))` projde hodnoty a vrátí True, pokud jsou všechny textové. Jiný typ odmítneme přes ValueError. Mezery, nové řádky a neúplné údaje zůstanou přesně tak, jak byly předány. Strip zde nepoužíváme: koncept má zachovat rozepsaný text.

```python
koncept = vytvor_koncept("jan@", "", "První věta\n")
print(koncept["prijemce"])  # jan@
print(repr(koncept["text"]))  # 'První věta\n'
```

## Od widgetů k náhledu

Dvě Entry obsahují příjemce a předmět, Text obsahuje tělo. Druhý Text slouží jako náhled. Parametr name dává vstupu stálé vnitřní jméno, například `name="prijemce"`; viditelný popisek vytváří sousední Label. Rodič a grid určují umístění, váha řádku a sloupce spolu se sticky dovolí oběma delším polím růst při změně velikosti okna.

Callback obnov čte `.get()` až po kliknutí na Obnovit náhled. U těla použije `get("1.0", "end-1c")`: získá uživatelský text bez koncového nového řádku, který Tk přidává samo. Nové řádky skutečně napsané uživatelem zachová. Vytvoří nový koncept a funkce nahled_konceptu z něj připraví čitelný text.

Pro výměnu obsahu náhledu krátce nastavíme state na normal, smažeme starý text, vložíme nový a vrátíme disabled. Náhled tak zůstává pouze pro čtení. Ukazuje stav po posledním kliknutí; po dalším psaní jej obnovte znovu. Text ve formuláři se při obnovení nemaže.

## Váš úkol

Dokončete vytvor_koncept. Přijměte čtyři texty, jiný typ odmítněte ValueError a vraťte nový slovník s přesnými hodnotami pod uvedenými klíči. Zachovejte připravený formulář a vnitřní jména widgetů.

Vyzkoušejte jan@, prázdný předmět a tělo se dvěma řádky zakončené Enterem. Obnovte náhled. Pak změňte všechna tři pole a klikněte znovu. Náhled musí použít čerstvé hodnoty; původní mezery ani vlastní koncový nový řádek se neztratí. Import souboru má pouze zpřístupnit funkce, hlavní blok otevře okno až při přímém spuštění.
