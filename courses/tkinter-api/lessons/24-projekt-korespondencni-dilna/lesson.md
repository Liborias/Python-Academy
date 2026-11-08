## Celý průchod aplikací

Závěrečný krok projektu propojí formulář, ověřený náhled, přílohu a přenos s ukládáním konceptů. Díky souboru můžete zavřít program a pokračovat později. Ukázka začíná prázdným formulářem; soubor koncept-ukazka.json v pracovních souborech lze načíst tlačítkem Načíst koncept.

Pomocné moduly obsahují dřívější hotové kroky: koncept.py model z 21, priprava.py sestavení zprávy z 22, prenos.py pracovníka z 23, zpravy.py a prilohy.py základ e-mailu a nastaveni.py s odesilani.py místní SMTP. Hlavní blok otevře pouze současnou aplikaci. Nejde o přihlášení do osobní schránky; záchyt stále nic nepřeposílá.

## Soubor ukládá rozpracovanou práci

Formát JSON má verzi a čtyři textová pole:

```json
{
  "verze": 1,
  "koncept": {
    "prijemce": "jan@",
    "predmet": "",
    "text": "Nápad na zprávu",
    "priloha": ""
  }
}
```

Verze umožní později rozpoznat jiný formát. Kontrolujeme `type(verze) is int` a hodnotu 1; samotné `verze == 1` by přijalo i True. Koncept musí být slovník se všemi čtyřmi textovými poli. Neznámé další klíče můžeme ignorovat, ale všechny požadované údaje ověříme před použitím.

V over_ulozitelny_koncept je pořadí klíčů uložené v n-tici klice. Zápis `vytvor_koncept(*(koncept[k] for k in klice))` projde hodnoty v tomto pořadí a hvězdičkou je rozbalí do čtyř argumentů funkce. Vznikne nový slovník; předaný model se nemění.

Neúplné údaje a vlastní mezery jsou platné. Uložit koncept proto nevolá sestav_zpravu a nevyžaduje existující přílohu. Načtený text půjde opravit. Soubor neobsahuje SMTP nastavení, přístupové údaje, stav přenosu ani obsah přílohy.

Vybraná příloha se ukládá jako absolutní cesta, kterou získal dialog a Path.resolve. Pomocná funkce over_ulozitelny_koncept zkopíruje všechna pole a přes Path.is_absolute ověří, že neprázdná cesta je úplná. Relativní cestu v ručně upraveném JSON odmítne, aby jiná pracovní složka nevybrala jiný soubor. Samotný soubor přílohy se nekopíruje. Po přestěhování nebo smazání původní přílohy koncept dál načtete a můžete vybrat nový soubor; existenci a velikost znovu ověří až sestavení zprávy.

## Uložení přes dočasný soubor

Uloz_koncept(cesta, koncept) nejprve ověří celý model a vytvoří dokument. `json.dumps(..., ensure_ascii=False, indent=2)` připraví čitelný JSON s českými znaky. Přidané `"\n"` zakončí textový soubor. Kandidáta připravíme ještě před otevřením souboru, aby neplatné vstupy nepoškodily starší uloženou práci.

NamedTemporaryFile vytvoří pomocný soubor ve stejné složce jako cíl. Parametr dir určuje složku, prefix/suffix rozeznatelné dočasné jméno, delete=False jej ponechá po uzavření a encoding="utf-8" určí kódování. V bloku with zapíšeme obsah. Potom už je soubor zavřený, což je důležité také pro nahrazení ve Windows.

`os.replace(docasny, cil)` nahradí cílové jméno novým souborem. Stejná složka zajistí stejný disk a umožní tento způsob nahrazení bez postupného přepisování původního cíle. Pokud příprava nebo nahrazení selže, původní cíl zůstane zachovaný. Finally uklidí zbytek pomocí `unlink(missing_ok=True)`; chybějící dočasný soubor po úspěšném přesunu není chyba. Tento postup chrání před nedokončeným běžným zápisem, sám o sobě nezaručuje obnovu po výpadku disku nebo napájení.

## Načtení mění formulář až nakonec

Nacti_koncept(cesta) použije `Path.read_text(encoding="utf-8")`, json.loads a ověření verze i všech polí. Vrátí nový čtyřpoložkový slovník. Chybný JSON, kódování, verze nebo pole vyvolá ValueError či jejího potomka; chybu otevření souboru dostane volající jako OSError.

Callback načtení nejprve získá úplného kandidáta. Teprve po úspěchu přepíše obě Entry, tělo a cestu přílohy. Zrušení dialogu nebo chyba zachová celý dosavadní formulář, přílohu i náhled. Platný prázdný koncept naopak pole vyprázdní. Nově načtený náhled je označený jako zatím neověřený. Uložení ani načtení není potvrzení odeslání.

Během SMTP přenosu se souborová tlačítka zablokují spolu s ostatními operacemi. Do polí lze dál psát. Výsledek přenosu pozdější text nepřepíše a nic automaticky neodesílá. Po nejistém výsledku platí povinnost ruční kontroly záchytu i tehdy, když načtete jiný koncept; souborová operace historii právě proběhlého pokusu nemaže. Nastavení krátkého timeoutu vyzkoušíte přímým spuštěním v terminálu podle lekce 23.

## Váš úkol

Dokončete uloz_koncept a nacti_koncept podle popsaného formátu. Použijte připravené over_ulozitelny_koncept. Uložení má vrátit None, načtení nový koncept. Koncept předaný funkci neměňte a import souboru nesmí otevřít okno.

Projděte celý scénář:

1. Napište neúplnou adresu, vlastní předmět a víceřádkový text. Uložte koncept a znovu jej načtěte; mezery i řádky se musí zachovat.
2. Vyberte poznamka.txt. Zrušte další výběr a zkuste načíst poškozený JSON. Rozpracovaný obsah i příloha zůstanou zachované.
3. Opravte adresu na jan@example.test, ověřte náhled a vyzkoušejte odmítnutí příjemce. Zpráva se nezachytí a formulář zůstane použitelný.
4. Vyberte Přijetí a ručně předání opakujte. Zkontrolujte záchyt. Během pomalého přenosu pište další koncept a po dokončení ověřte zachování nové práce.
5. Zavřete program, znovu jej spusťte a načtěte uložený koncept. Pole se obnoví, ale místní záchyt začíná prázdný: jeho zprávy se do JSON neukládaly.

Další blok kurzu doplní vlastní testy, předání projektu a volitelné balení. Nyní máte funkční místní aplikaci, ve které umíte vysvětlit cestu dat od pole přes koncept a hotovou zprávu až do záchytu.
