## Hotovo, skoro

Poslední lekce spojuje celý kurz. Napíšete program, který rozebere zadaný text, a pak odpovíte na deset otázek v kvízu.

## Dvě nové drobnosti

`slovo.strip(".,!?;:")` odstraní z okrajů slova uvedené znaky, takže z `"ahoj!"` zůstane `"ahoj"`. Rozdíl proti `strip()` bez parametru je v tom, že odebírá právě vyjmenované znaky.

`round(cislo, 1)` zaokrouhlí desetinné číslo na jedno desetinné místo: `round(4.666, 1)` je `4.7`.

## Váš úkol: rozbor textu

Slova se oddělují mezerami, z okrajů se jim odstraní `. , ! ? ; :` a převedou se na malá písmena. Prázdná slova (samotná interpunkce) se ignorují.

1. `analyzuj_text(text)` vrátí slovník s klíči:
   - `"slov"`: počet slov,
   - `"unikatnich"`: počet různých slov,
   - `"nejdelsi"`: nejdelší slovo (při shodě první z nich),
   - `"prumerna_delka"`: průměrná délka slova zaokrouhlená na 1 desetinné místo.

   Pro text bez slov vrátí `{"slov": 0, "unikatnich": 0, "nejdelsi": "", "prumerna_delka": 0}`.
2. `popis_analyzy(vysledek)` vrátí text o čtyřech řádcích spojených `\n`:

   ```text
   Slov: 6
   Unikátních: 5
   Nejdelší: python
   Průměrná délka: 4.2
   ```
3. `hlavni()` načte jeden řádek pomocí `input("Text: ")`, vypíše `popis_analyzy(analyzuj_text(...))`. Spuštění hlavní funkce dejte do bloku `if __name__ == "__main__":`, jinak by se `hlavni()` při kontrole spustila sama a čekala na vstup.

Pod úlohou je kvíz s deseti otázkami z celého kurzu.
