## Poznámka přežije zavření okna

Obsah Text je zatím jen v paměti. Přidáme jeho zápis do souboru a opětovné načtení. Použijeme JSON ve tvaru `{"text": "Vaše poznámka"}`. Jde o data, která json.load převede na objekty Pythonu; nespouští je jako kód. I syntakticky platný JSON však může mít pro náš program špatný tvar.

Výpočet jsme minule oddělili od okna. Teď stejně oddělíme `uloz_poznamku(cesta, text)` a `nacti_poznamku(cesta)`. Dostanou cestu jako argument; samy neotevírají dialogy ani Tk okno. Hlavni se nadále volá jen v hlavním bloku, takže lze pomocné funkce importovat.

## Jak se data zapisují a ověřují

`with open(cesta, "w", encoding="utf-8") as soubor` otevře soubor pro zápis a po dokončení jej zavře i při chybě. Režim w přepíše existující obsah. Ukládejte nejprve do vlastního cvičného souboru, který můžete přepsat. `json.dump({"text": text}, soubor, ensure_ascii=False, indent=2)` zapíše objekt; ensure_ascii=False nechá česká písmena přímo čitelná a indent=2 přidá odsazení.

Vlastní nové řádky poznámky budou uvnitř JSON řetězce zapsané jako \n. Není to ztráta zalomení: json.load tyto zápisy při čtení opět převede na znaky nového řádku.

Při čtení použijeme `json.load(soubor)` a ověříme výsledek. Isinstance(data, dict) zjistí, zda jde o slovník; data.get("text") přečte hodnotu nebo vrátí None, pokud klíč chybí. Teprve po ověření slovníku použijeme get a zkontrolujeme isinstance(..., str). Číslo, seznam ani null jako poznámku nepřijímáme. Prázdný text je naopak platný. Cizí klíče navíc nevadí.

## Dialog vrací cestu, ne otevřený soubor

```python
cesta = filedialog.asksaveasfilename(
    parent=okno, defaultextension=".json", filetypes=[("JSON", "*.json")]
)
```

Filedialog importujeme z tkinter. Asksaveasfilename nechá vybrat cestu pro zápis, askopenfilename existující soubor pro čtení. Parent přiřadí dialog k našemu oknu, filetypes filtruje nabídku a defaultextension doplní příponu při ukládání. Filtr nezaručuje správný obsah souboru, ten stále musíme ověřit.

Zrušení dialogu vrátí prázdný řetězec. Podmínka if not cesta vrátí řízení ještě před open. Dialog sám obsah programu nenačte ani neuloží. Načítání i ukládání provádíme až po získání neprázdné cesty.

Při ukládání vyberte vlastní snadno dohledatelnou složku, například Dokumenty/Python, a zapamatujte si název souboru. Každý běh ukázky v prohlížeči má jinou pracovní složku; nespoléhejte proto, že další dialog začne právě tam, kam jste uložili minule. Pro obnovení vyberte původní soubor výslovně.

## Chyba nesmí vymazat poznámku

OSError pokrývá například nedostupnou cestu nebo odmítnutý přístup k souboru. ValueError pokryje poškozený JSON, námi odmítnutý tvar i chybné kódování textu. Ošetříme je v callbacku a zobrazíme srozumitelnou zprávu. Text widgetu nahradíme až po úspěšném načtení a ověření celé poznámky. Zrušení ani chyba proto současný text nezničí.

Při zápisu chyba nemusí znamenat, že starý soubor zůstal beze změny: režim w jej mohl už otevřít a přepsat. Tato lekce používá jednoduchý přímý zápis a slibuje zachování poznámky v okně, nikoli obnovu po přerušení zápisu na disk.

## Váš úkol

Dokončete obě souborové funkce; připravené callbacky a rozložení ponechte. Uložení zapisuje přesně aktuální text bez automatického koncového znaku Text, včetně diakritiky a vlastních nových řádků. Načtení vrátí text z objektu s textovým klíčem text; ostatní typy či chybějící klíč odmítne ValueError. Chyby souboru nechte dojít ke callbacku, který je už ošetřuje.

Zkuste vlastní českou poznámku uložit, změnit a načíst. Otevřete JSON také v editoru. Potom oba dialogy zrušte a zkuste neplatný soubor. Zprávy rozlišují Poznámka uložena., Poznámka načtena., Ukládání zrušeno., Načítání zrušeno. a Soubor se nepodařilo uložit./načíst. Text při neúspěchu musí zůstat stejný. Vyzkoušejte i uložení a načtení prázdné poznámky.
