## Od textového pole k uloženému řádku

Přiložený `model_zaklad.py` obsahuje model z lekce 11 beze změny jeho definic. `pohled.py` pouze skládá widgety. Váš kód propojí akci tlačítka s modelem. SQL nepatří do callbacku formuláře.

```python
# Entry vrací text, i když do něj člověk napíše číslo.
text_z_pole = ' 12 '
kapacita = int(text_z_pole)
print(type(text_z_pole).__name__, kapacita, type(kapacita).__name__)
```

Výsledek str 12 int vysvětluje převod. `cti_kapacitu` z priprava.py provede int a ověří kladnost. '1.5', prázdný text nebo nula znamenají chybu. Pokud převod selže, do databáze ještě nic neodešlo.

## Co se děje po kliknutí

Tlačítko dostane `command=self.pridej`, tedy funkci pro pozdější zavolání. Zápis self.pridej() by ji provedl při stavbě okna. Obsluha nejprve načte a ověří pole, pak model provede INSERT a commit. Teprve potom znovu načteme seznam a vyčistíme formulář. Při chybě necháme oba vstupy rozepsané, aby je člověk mohl opravit.

`self.data` je seznam skutečných databázových řádků. Listbox zobrazuje jejich čitelný text, není zdrojem pravdy. Obnovit načte řádky z modelu znovu, nevrství kopie pod staré položky. Posuvník a roztažení okna zajišťuje přiložený pohled.

## Spuštění: ukázka a vlastní soubor

Spustit otevře jedno skutečné okno na počítači, kde běží Akademie; v prohlížeči se jeho obsah nevykresluje. Ukázka používá paměť se dvěma kroužky, po zavření se zahodí. Ve vzdáleném prostředí potřebujete přístup k jeho grafické ploše.

Pro vlastní evidenci uložte pracovní složku a v terminálu se stejnou .venv spusťte `python spust_krouzky.py`. Tento spouštěč importuje vaši Aplikace z reseni.py a otevře trvalý krouzky.sqlite3 vedle skriptu. `--help` vysvětlí volbu `--db CESTA` a nic nevytváří; rodič cílového souboru musí existovat. Nepoužívejte klub.sqlite3 z jiného projektu. Nová vlastní evidence začíná prázdná, ukázková data se do ní nevkládají. Každý další uložený krok má svou složku; chcete-li pokračovat ve stejných záznamech, zadejte --db s absolutní cestou k předchozímu krouzky.sqlite3. Schéma se v tomto projektu nemění.

## Váš úkol

Doplňte `Aplikace.obnov()` a `Aplikace.pridej()`. Konstruktor a slovník widgetů self.w jsou připravené. Obnov uloží výsledek model.seznam do self.data, vyprázdní Listbox a zobrazí každý řádek jako `id: název (kapacita číslo)`.

Pridej převede kapacitu pomocí cti_kapacitu a zavolá model.pridej s názvem z pole. ValueError vypíše do stavového popisku, IntegrityError oznámí „Název kroužku už existuje.“ Při obou chybách zůstanou vstupy i seznam beze změny.

Po úspěchu obnoví seznam, vyprázdní název a vrátí kapacitu na 10. Stav oznámí „Přidán kroužek ID číslo.“ Zachovejte jedno okno, jednu smyčku a pomocné soubory vedle reseni.py. Porovnejte možné řešení se svým, jiné správné propojení je v pořádku.
