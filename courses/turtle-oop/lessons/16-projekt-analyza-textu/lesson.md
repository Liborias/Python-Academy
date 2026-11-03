## Zadání

V projektu spojíte řetězce, seznamy, množiny a slovníky. Funkce `analyza(text)` vrátí **slovník** se statistikou textu.

## Příprava slov

Slova se oddělí mezerami, zahodí se interpunkce na okrajích slov a všechno se převede na malá písmena:

```python
"Kočka běží.".split()                       # ["Kočka", "běží."]
"běží.".strip(".,!?;:\"()-")               # "běží"   strip odstraní uvedené znaky na obou koncích
"Kočka".lower()                             # "kočka"  malá písmena, aby Kočka a kočka byla jedno slovo
```

Za interpunkci se tu považují znaky `. , ! ? ; : " ( ) -`.

Pokud po očištění zbyde prázdný řetězec (například samotná pomlčka nebo `...`), slovo se **vynechá**.

## Počítání pomocí slovníku

```python
pocty = {}
for slovo in slova:
    pocty[slovo] = pocty.get(slovo, 0) + 1     # get vrátí 0, pokud slovo ještě není
```

Průměrnou délku spočítáte jako součet délek slov děleno počtem slov. Součet jde napsat cyklem, nebo zkráceně `sum(len(s) for s in slova)`, což je součet přes všechna slova. Nejčastější slovo se vybere funkcí `min` s klíčem, což je malá funkce `lambda`, která z každého slova udělá dvojici (klíč). Řadíme podle počtu sestupně (proto záporný počet) a při shodě abecedně: `min(pocty, key=lambda s: (-pocty[s], s))`.

## Váš úkol

`analyza(text)` vrátí slovník s klíči:

- `"slov"`: počet slov,
- `"unikatnich"`: počet různých slov,
- `"nejdelsi"`: nejdelší slovo (při shodě **první** v pořadí v textu), pro prázdný text `""`,
- `"nejcastejsi"`: nejčastější slovo (při shodě abecedně první), pro prázdný text `""`,
- `"prumerna_delka"`: průměrná délka slova zaokrouhlená na dvě desetinná místa (`round(…, 2)`), pro prázdný text `0`.

Příklad: `analyza("Kočka běží. Kočka spí, pes běží!")` → `{"slov": 6, "unikatnich": 4, "nejdelsi": "kočka", "nejcastejsi": "běží", "prumerna_delka": 4.0}`. Slova jsou `kočka běží kočka spí pes běží`. Kočka a běží jsou obě dvakrát, abecedně první je „běží“.