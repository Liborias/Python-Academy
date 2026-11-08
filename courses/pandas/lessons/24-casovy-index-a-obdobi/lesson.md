## Čas jako skutečná osa tabulky

Datumový sloupec jsme už převedli přes to_datetime. Nyní z něj vytvoříme DatetimeIndex, tedy index skutečných časových hodnot. `tabulka.set_index("cas")` přesune sloupec cas do indexu a ostatní sloupce ponechá v původním pořadí. Původní číselný či textový index se jako nový datový sloupec nepřidá.

```python
casova = tabulka.set_index("cas").sort_index(kind="stable")
```

Sort_index seřadí řádky podle času. Stable zachová původní pořadí tam, kde se čas shoduje; dvě měření ve stejném okamžiku sama o sobě nejsou chyba. V našich úkolech je čas datetime64[us], bez časového pásma a bez NaT. Jednotku us, mikrosekundy, už známe. Původní tabulku neměníme.

## Přesný okamžik proti celému dni

`casova.loc[pd.Timestamp(od):pd.Timestamp(do)]` u seřazeného indexu vybere úsek včetně obou přesných hranic. Timestamp vytvoří jednu časovou hodnotu, takže celý řez nemá význam zkráceného textového označení dne. Pokud se hraniční čas opakuje, zahrnou se všechny jeho řádky.

Chceme-li celý den, použijeme jinou otázku: od jeho půlnoci včetně do půlnoci následujícího dne bez ní. `pd.Timedelta(days=1)` představuje jednodenní časový rozdíl; jeho přičtením k počátečnímu Timestamp získáme druhou hranici. Maska porovnává index pomocí >= začátek a < konec. Nepoužíváme pevný konec 23:59:59, protože by chyběla měření s mikrosekundami těsně před půlnocí. Naše hodnoty nemají časové pásmo, převody pásem zde neřešíme.

## Pravidelná mřížka není součet

`pd.date_range(zacatek, konec, freq="D", name=serie.index.name)` vytvoří denní časové popisky včetně obou mezních dnů. Freq="D" znamená krok jednoho dne a name nastaví název indexu. Metoda indexu `.as_unit("us")` výslovně sjednotí jeho jednotku na mikrosekundy. To nemění význam kalendářních dnů.

Series potom přeindexujeme pomocí reindex z lekce 21. Pokud máme hodnoty pro 1. a 3. února, u 2. února vznikne NaN. Žádný součet se nepočítá a žádná předchozí hodnota se automaticky nedoplňuje. V tomto úkolu jsou původní popisky jedinečné půlnoci, aby šlo každému dni přiřadit právě jednu existující hodnotu. Naopak při více měřeních za den potřebujeme agregaci z další lekce.

## Vrácení času do sloupce

`tabulka.reset_index()` přesune pojmenovaný index do prvního sloupce a vytvoří nový RangeIndex. Tentokrát nepoužíváme drop=True, protože čas je důležitý údaj, který chceme zachovat. Úkol zaručuje, že se název indexu nekříží s existujícím sloupcem. Samotné reset_index řádky neřadí a hodnoty času nepřevádí na text.

## Váš úkol

Dokončete `nastav_casovy_index(tabulka, sloupec)`. Existující sloupec má dtype datetime64[us], bez NaT a časového pásma. Vraťte DataFrame s tímto sloupcem jako pojmenovaným DatetimeIndex, vzestupně seřazený stabilně. Opakované časy zachovejte, původní sloupec už mezi datovými sloupci nebude. Ostatní hodnoty a pořadí sloupců zachovejte, prázdný vstup se sloupci je platný. Zdroj neměňte.

Další čtyři úkoly procvičí přesný úsek, celý den, pravidelnou mřížku a návrat indexu do sloupce. Pokaždé si určete, zda vybíráte existující řádky, vytváříte chybějící časové pozice, nebo měníte tvar tabulky.
