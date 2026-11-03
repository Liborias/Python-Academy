## Specializovaný druh objektu

Některé třídy mají společné chování, ale v něčem se liší. **Dědění** umožní popsat specializovanou třídu pomocí již existujícího základu.

```python
class Zprava:
    def __init__(self, text):
        self.text = text

    def zobraz(self):
        return f"Zpráva: {self.text}"


class DulezitaZprava(Zprava):
    def zobraz(self):
        return f"DŮLEŽITÉ: {self.text}"
```

V závorkách za názvem třídy uvádíme její **základní třídu**. `DulezitaZprava` je **odvozená třída**: přebírá dostupné chování ze Zprava a může ho doplnit nebo změnit. Zde je důležitá zpráva stále zprávou, pouze se jinak zobrazuje.

## Co se zdědí

```python
bezna = Zprava("Schůzka ve tři")
dulezita = DulezitaZprava("Změna místa")
print(bezna.zobraz())
print(dulezita.zobraz())
```

Odvozená třída zde nepíše vlastní `__init__`. Python použije zděděný inicializátor, který uloží text do právě vytvářené instance. Při volání `dulezita.zobraz()` se však použije metoda definovaná přímo v DulezitaZprava.

Tomu říkáme **přepsání metody** (override). Nepřepíše to zdrojový kód ani metodu základní třídy: obyčejná Zprava se dál zobrazuje původním způsobem. Volání metody se rozhoduje podle skutečného objektu před tečkou.

Dědí se chování, ne jedno společné nastavení všech objektů. Dvě zprávy se dál inicializují zvlášť a každá má svůj text.

## Stejné volání, jiné chování

```python
for zprava in [bezna, dulezita]:
    print(zprava.zobraz())
```

Cyklus nemusí zkoumat typ objektu a rozhodovat přes if. Použije stejné jméno metody a každý objekt provede svou verzi. Takovému použití společného rozhraní pro různé chování říkáme **polymorfismus**.

Funkce `isinstance(dulezita, Zprava)` vrátí True: důležitá zpráva je také zprávou. `isinstance(bezna, DulezitaZprava)` vrátí False. Každý specializovaný typ není automaticky typem každého jiného objektu.

Dědění používejte pro vztah „je druhem“. Když například hra obsahuje seznam hadích částí, je to vlastnictví objektů jako u Batohu, ne důvod dědit hru ze seznamu. Není nutné všechno spojovat děděním.

## Váš úkol

Napište tři třídy:

1. `Zvire(jmeno)` uloží atribut `jmeno`. Metoda `pozdrav(self)` vrátí přesně `Ahoj, jsem Ema.` pro jméno Ema.
2. `Pes` dědí ze Zvire a přepíše pozdrav na `Haf, jsem Ema.`
3. `Kocka` dědí ze Zvire a přepíše pozdrav na `Mňau, jsem Ema.`

Všechny varianty používají aktuální jméno dané instance; samozřejmě může být jiné než Ema. Jméno nijak neupravujte. Zachovejte mezery, čárku a tečku. Metody mají text vracet, nikoli pouze vypisovat.

Pes a Kocka mohou využít zděděný konstruktor, takže ho nemusíte opisovat. Každé zvíře má vlastní jméno. Pokud ho po vytvoření změníme, další pozdrav má pracovat s novým jménem. Základní Zvire musí dál používat svůj vlastní pozdrav.
