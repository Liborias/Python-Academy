## Menší obsah a přenosový zápis

Zlib komprimuje bajty, Base64 je zapíše pomocí ASCII znaků. Base64 obvykle přidává velikost; krátký text se všemi obaly nemusí být menší. První doplňková ukázka porovná krátkou a opakovanou poznámku. Ani komprese, ani Base64 nejsou šifrování.

```python
# UTF-8 zachová češtinu a nové řádky i při cestě tam a zpět.
text = 'Žofie; poznámka'
print(text.encode('utf-8').decode('utf-8') == text)
```

Balíček začíná `z1:`. Verze určuje postup UTF-8 -> zlib -> Base64, aby šlo později poznat jiný formát. Hesla a účty se tímto způsobem nepřenášejí.

## Limity jsou součást formátu

Nejvýše 65536 bajtů rozbaleného UTF-8, nikoli znaků. Znak ž má dva bajty. Balíček má nejvýše 100000 ASCII znaků. Rozbalování musí mít max_length, nikoli nejprve vytvořit libovolně velký text a až potom měřit délku.

Po rozbalení vyžadujeme dokončený zlib proud, žádné připojené bajty ani druhý proud. Zkrácený obsah je chyba, nikoli prázdná poznámka. UTF-8 dekódujeme přísně. Prázdný text je pro samotný kodek platný, pravidla poznámek jsou samostatná vrstva.

## Váš úkol

Doplňte **zabal_text(text)** a **rozbal_text(balicek)**. Zabal ověří text_utf8, komprimuje zlib.compress a vrátí PREFIX + Base64 dekódované jako ASCII. Zachová přesný obsah včetně krajních mezer a prázdného textu.

Rozbal ověří str, prefix a délku; provede base64.b64decode(validate=True) a kontrolu kanonického zápisu zpětným b64encode. Vytvoří zlib.decompressobj a použije decompress s limitem MAX_TEXT+1. Překročení MAX_TEXT, neukončený proud, unused_data nebo unconsumed_tail vyvolají ValueError. Jinak výstup dekóduje UTF-8. Chyby formátu/data převede na ValueError, nikdy na tiché prázdno.

## Přenos vlastních poznámek

V uložené složce je hotové sezení z 23 a prenos.py, který používá právě vaše funkce z reseni.py. Žádná kopie odpovědi kodeku není v helperu. Po vytvoření účtu a poznámek:

```powershell
python spust_ucty.py export Zofie moje-poznamky.txt
python spust_ucty.py import Zofie moje-poznamky.txt
```

Obě operace vyžádají heslo přes getpass. Export přenáší jen JSON s verzí a seznamem vlastních textů; neobsahuje hesla ani otisky. Cíl se při úspěchu nahradí atomicky, nesmí být zdrojovou DB. Import validuje celý formát a dávku před jedním zápisem. Při chybě se nic částečně nepřidá.

Import přidává poznámky, staré nemaže. Opakovaný import vytvoří kopie. Přenos není šifrovaný soubor ani úplná záloha účtů. --db CESTA patří před příkaz, výchozí ucty.sqlite3 je vedle spouštěče. Použijte stejnou DB z předchozí uložené složky, chcete-li pracovat se stejnými účty. Ukázky tlačítkem Spustit jsou naopak dočasné.
