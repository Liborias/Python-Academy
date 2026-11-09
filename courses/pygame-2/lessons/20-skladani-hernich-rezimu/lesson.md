## Nabídka, hra a pauza se mohou skládat

Ve dvou hrách jsme používali názvy stavů. Při větší aplikaci pomůže oddělit části, které mají stejné rozhraní: zpracuj(udalost), update(dt), kresli(plocha). Jedna scéna řídí hru, druhá nabídku a další je průhledná pauza. Společné rozhraní neznamená, že musejí zdědit všechno z jedné obrovské třídy.

Zásobník drží režimy odspodu. Jen vrchní přijímá vstup a čas, ale kreslí se všechny v pořadí. Pauza tak může překrýt stále stejný poslední obraz hry. Vložením pauzy nezničíme rozehrané kolo a odebráním navážeme na stejný objekt.

```python
vrstvy = ['hra', 'pauza']
print('Aktivní:', vrstvy[-1])
vrstvy.pop()
print('Po návratu:', vrstvy[-1])
```

Vypíše pauza a pak hra. Ve skutečné součásti místo těchto názvů držíme objekty režimů. Poslední základní režim nenecháme odebrat, aby měla aplikace vždy co řídit.

## Požadavek není hotový přechod

Tlačítko zjistí, že na něj uživatel klikl, a vrátí akci, například 'hra'. Nabídka skládá tlačítka a rozhodne, která akce je navrchu. Řidič scén pak vytvoří nový režim nebo vloží pauzu. Kdyby tlačítko samo začalo spouštět další okna a smyčky, vznikalo by provázání obtížné pro ladění i kontrolu.

U akcí 'hra' a 'nabidka' vznikne nový zásobník; při 'pauza' zůstane původní a přidá se vrstva; 'zpet' odebere jen vršek. Nejprve úspěšně vytvoříme nový objekt a teprve potom přepneme, takže chyba továrny nezanechá napůl rozbitou scénu. QUIT se zpracuje bez ohledu na aktuální režim.

## Kdy dědit a kdy obsahovat

Hlidac z minulé hry je určitý druh Robot, dědění mu dává smysl. Nabidka ale není určitý druh Tlacitko: obsahuje jejich seznam. Řidič zase obsahuje zásobník. Kompozice tak často dovolí menší součásti, které umíme ověřit samostatně. V těchto úkolech nepotřebujeme složitou hierarchii ani vlastní framework.

První ukázky se jako dřív uloží do soucasti.png a neotevírají okno. U Úkolu 5 si navíc můžete po uložení reseni.py spustit `python ziva_dilna.py` v jeho pracovní složce. Kliknutí spustí dílnu, P přepíná pauzu, M vrací nabídku a Esc/křížek ukončí jediné okno. Potřebuje místní grafickou plochu a klávesnici/myš na počítači s Pythonem; okno se nepřenáší do webu. Zvuk nevyužívá. Běžné ukončení zachová rezimy-zive.png.

Další modul propojí získané součásti do hry Hon na dronech. Sem patří malé samostatné pokusy s více úkoly; následující projekt opět zůstane jedním návazným celkem.

## Váš úkol: Zásobník herních režimů

Vytvořte `ZasobnikRezimu(pocatecni)` s vlastním seznamem `rezimy=[pocatecni]` a čtenou vlastností `aktualni` pro poslední objekt. Každý režim poskytuje zpracuj(udalost), update(dt), kresli(plocha). `vloz(rezim)` přidá nový vršek. `odeber()` vrátí True po odebrání vršku, ale poslední základní režim ponechá a vrátí False.

Zpracuj předá událost pouze vršku a vrátí jeho výsledek. Update posune pouze vršek. Kresli naopak předá stejnou plochu všem režimům odspodu, aby průhledná pauza mohla překrýt hru. Při návratu pokračuje původní objekt, nevytvářejte jeho kopii.

Další čtyři zadání přepnete tlačítky Úkol 2–5. U každého najdete vlastní možné řešení; jeho odkrytí nemění rozepsaný kód ani splnění.
