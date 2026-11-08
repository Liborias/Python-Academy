## Číslice v textu ještě nejsou číselný sloupec

Text "12.5" a číslo 12.5 mohou při výpisu vypadat podobně, ale chovají se jinak. Před výpočtem si prohlédněte dtype Series nebo dtypes tabulky. Číselné kódy jako 001 naopak ponecháváme textové: nejde o množství pro výpočty a převod by odstranil důležité nuly.

`pd.to_numeric(serie, errors="coerce")` zkusí převést textové hodnoty na čísla. Coerce znamená, že z neplatného zápisu vznikne chybějící údaj. Původní Series zůstane pro kontrolu zachovaná. Bez tohoto nastavení neplatný text obvykle vyvolá chybu. V úkolech výslovně požadujeme float64, proto na výsledek použijeme `.astype("float64")`. Tak má stejný typ i prázdná Series nebo soubor samých celých čísel.

## Nepřevést potichu neznamená chybu opravit

```python
cisla = pd.to_numeric(serie, errors="coerce").astype("float64")
chybny_text = cisla.isna() & serie.notna()
print(serie.loc[chybny_text])
```

Isna označí neúspěšný výsledek a notna ověří, že původní údaj vůbec existoval. Jejich spojením přes & odlišíme chybný text od původně chybějící hodnoty. Prázdný text zde existuje, ale není číslem, takže je označen jako chybný. Nula je platné číslo. Coerce neodhadne zamýšlenou hodnotu a neopraví překlep; pouze umožní dohledat problematický vstup.

## Desetinná čárka patří do pravidel zdroje

To_numeric používá desetinnou tečku. V samostatném úkolu víme, že zdroj může místo ní použít čárku a nepoužívá tisícové oddělovače. `serie.str.replace(",", ".", regex=False)` ji v jednotlivých textech doslovně nahradí a pak můžeme použít to_numeric. Přístup str dovoluje textové operace nad celou Series; zachovává její index a chybějící hodnoty. Regex=False říká, že hledáme obyčejný text, nikoli regulární výraz.

Zápis 1,234 může podle zdroje znamenat desetinné číslo nebo oddělení tisíců. Bez znalosti formátu jej proto automaticky neopravujeme. U CSV je nejlepší správně nastavit decimal už při čtení, jak jsme dělali v lekci 5. Tady procvičujeme už načtený textový sloupec.

## Int64 s velkým I

Typ int64 je běžné celé číslo bez podpory chybějícího údaje. Pandas typ `Int64` s velkým I umí celé hodnoty i pd.NA. `serie.astype("Int64")` se proto hodí pro počty, kde některý údaj neznáme. V úkolu jsou vstupní čísla skutečně celá, například 2.0 nebo 0.0; nevyžadujeme zaokrouhlování zlomků. Převod 2.7 na počet kusů by vyžadoval jiné, výslovné pravidlo.

`tabulka.astype({"kusy": "Int64", "cena": "float64"})` převede jen pojmenované sloupce. Astype převádí na konkrétní typ a při neplatné hodnotě může selhat; na rozdíl od to_numeric s coerce zde nevymýšlí náhradu za chybný text. V tomto úkolu dostanete převoditelné hodnoty. Nepřevádíme automaticky všechny sloupce, zejména textové identifikátory.

## Váš úkol

Dokončete `preved_cisla(serie)`. Vstup má dtype str a obsahuje textové zápisy konečných čísel s desetinnou tečkou, neplatné texty nebo chybějící údaje. Vraťte float64 Series: platná čísla převedená, ostatní jako NaN. Zachovejte index, name i pořadí a nezaokrouhlujte. Prázdná Series je platná, vstup neměňte.

Další úkoly mají vlastní pravidla pro čárku, celé počty, typy vybraných sloupců a detekci chybných textů. Po převodu si porovnejte typ, počet chybějících hodnot a původní texty, které převést nešlo.
