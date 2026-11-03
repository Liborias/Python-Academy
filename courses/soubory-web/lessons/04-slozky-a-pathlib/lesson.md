## Cesty jako objekty

Pro práci se složkami a cestami k souborům slouží modul `pathlib`. Cesta se v něm zapisuje objektem `Path`:

```python
from pathlib import Path

slozka = Path("poznamky")
soubor = slozka / "pondeli.txt"      # lomítko spojí cesty, funguje na Windows i jinde
```

Lomítko `/` mezi cestami je správný způsob, jak je spojit. Zápis není závislý na operačním systému.

## Co se s cestou dá zjistit

| Zápis | Význam |
|---|---|
| `soubor.exists()` | existuje soubor nebo složka? |
| `soubor.is_file()` | je to soubor? |
| `slozka.is_dir()` | je to složka? |
| `soubor.name` | jméno s příponou (`pondeli.txt`) |
| `soubor.stem` | jméno bez přípony (`pondeli`) |
| `soubor.suffix` | přípona (`.txt`) |

## Čtení, zápis a procházení

```python
text = soubor.read_text(encoding="utf-8")       # přečte celý soubor
soubor.write_text("ahoj\n", encoding="utf-8")  # zapíše (přepíše) soubor

for polozka in slozka.glob("*.txt"):             # soubory s příponou txt v této složce
    print(polozka.name)

slozka.mkdir(exist_ok=True)                      # vytvoří složku, když ještě není
slozka.mkdir(parents=True, exist_ok=True)        # založí i chybějící nadřazené složky
```

`glob("*.txt")` hledá podle vzorku, kde `*` zastupuje libovolný text. Pořadí nálezů **není zaručené**, proto je seřaďte funkcí `sorted`. Pokud složka neexistuje, `glob` nevrátí nic.

## Váš úkol

Ve složce `poznamky` jsou soubory `pondeli.txt`, `utery.txt`, `seznam.md` a podsložky `archiv` a `stare.txt` (ta je složka, přestože jméno vypadá jako soubor).

1. `najdi_txt(slozka)` vrátí **seřazený seznam jmen** souborů s příponou `.txt` přímo ve složce (jen jména, např. `["pondeli.txt", "utery.txt"]`). Soubory v podsložkách se nepočítají a složky vůbec ne, ani když jejich jméno končí na `.txt`.
2. `obsah_slozky(slozka)` vrátí seřazený seznam jmen všeho, co je přímo ve složce (soubory i podsložky). K výpisu použijte `iterdir()`: `for polozka in Path(slozka).iterdir():` projde všechno, co je ve složce (soubory i podsložky), a `polozka.name` je jméno položky.
3. `zapis_poznamku(slozka, nazev, text)` vytvoří složku (pokud ještě není), zapíše do ní soubor `nazev` s textem a vrátí cestu k souboru jako objekt `Path`.
