## Data se strukturou

CSV je tabulka. Pro složitější data, například slovník se seznamem uvnitř, se hodí formát **JSON**. Je to textový zápis téměř stejný jako slovníky a seznamy v Pythonu, používá ho spousta webových služeb.

```json
{
  "jmeno": "Eva",
  "vek": 31,
  "zajmy": ["šachy", "kolo"],
  "ridic": true
}
```

## Modul json

```python
import json

with open("profil.json", encoding="utf-8") as soubor:
    profil = json.load(soubor)          # ze souboru na slovník či seznam

with open("kopie.json", "w", encoding="utf-8") as soubor:
    json.dump(profil, soubor, ensure_ascii=False, indent=2)    # zápis do souboru
```

- `json.load(soubor)` načte celý soubor a vrátí slovník, seznam nebo jinou hodnotu.
- `json.dump(data, soubor)` zapíše data do souboru. Parametr `indent=2` zápis hezky odsadí. Parametr `ensure_ascii=False` nechá češtinu čitelnou: bez něj se `č` zapíše jako `\u010d`.
- Pro práci s textem místo souboru slouží `json.dumps(data)` (data na text) a `json.loads(text)` (text na data).

## Jak se hodnoty překládají

| Python | JSON |
|---|---|
| slovník | objekt `{...}` |
| seznam, n-tice | pole `[...]` |
| text | text v uvozovkách |
| `int`, `float` | číslo |
| `True`, `False` | `true`, `false` |
| `None` | `null` |

JSON nezná n-tice ani množiny: n-tice se po zápisu a načtení vrátí jako **seznam** a množinu je nutné převést na seznam. Klíče slovníku jsou v JSON vždy **texty**, takže číselný klíč `1` se vrátí jako `"1"`.

## Váš úkol

1. `nacti_json(nazev)` vrátí data ze souboru JSON.
2. `uloz_json(nazev, data)` zapíše data do souboru s odsazením 2 a čitelnou češtinou.
3. `nastav_hodnotu(nazev, klic, hodnota)` načte slovník ze souboru, nastaví v něm klíč, uloží ho zpět a vrátí. Pokud soubor neexistuje, začne s prázdným slovníkem.
4. `pocet_hotovych(nazev)` vrátí počet úkolů s `"hotovo": true` v souboru `ukoly.json` (seznam slovníků).
