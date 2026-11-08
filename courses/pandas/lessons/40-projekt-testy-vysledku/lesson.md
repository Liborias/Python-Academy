## Souhlas součtu není celý test

Dvě špatně pojmenované skupiny mohou mít stejný počet měření i součet. Porovnáme proto celý výsledek: klíče slovníku, sloupce, řádky, typy, popisky a číselné hodnoty. Testy mají umět přijmout správná data i odmítnout úmyslně poškozená.

## Porovnání přes pandas.testing

```python
import pandas as pd
a = pd.DataFrame({"kod":["001","NA"], "pocet":[2,1], "prumer":[1.5,-2.0]})
b = a.copy()
pd.testing.assert_frame_equal(a, b, check_exact=False, rtol=1e-12, atol=1e-12)
print("Tabulky souhlasí.")
```

Assert_frame_equal při shodě nic zvláštního nevrací a při rozdílu vyvolá AssertionError. Typy i názvy zůstávají součástí porovnání. Check_exact=False a rtol/atol=1e-12 dovolí malou odchylku desetinné aritmetiky. Tím se neschová rozdíl 0,01 ani změna počtu na bool. Není to povolení svévolně zaokrouhlovat výsledky.

## Váš úkol

Dokončete `over_prehled(prehled, ocekavane)`. Oba vstupy jsou slovníky mapující textové názvy na DataFrame. Vraťte bool: True právě tehdy, když mají stejné klíče a všechny tabulky souhlasí včetně dtype, pořadí a popisků, s uvedenou číselnou tolerancí. Na pořadí samotných klíčů slovníku nezáleží. Prázdné tabulky se správným schématem jsou platné. Vstupy neměňte; zachyťte rozdíl porovnání a vraťte False místo změny tabulek.

Keys vrátí pohled na klíče a jejich porovnání ověří stejnou množinu. Potom cyklus projde jednotlivé tabulky. Try/except zachytí AssertionError; u neodpovídajícího objektu může porovnání vyvolat TypeError nebo ValueError. Samotné porovnání seznamu klíčů nebo existence souborů nestačí.

## Osm veřejných testů

Přiložený test_dilna.py obsahuje skutečný unittest.TestCase. Ověřuje shodu, změnu čísla, chybějící klíč, prohozené kódy, změnu datového typu, pořadí sloupců, prázdné tabulky a malou tolerovanou odchylku. U každého porovnání hlídá také zachování vstupů. Nejsou to všechna možná data; automatická kontrola lekce přidá další případy.

Ukázka zavolá `spust_testy(over_prehled)`, což předá vaši funkci veřejné sadě. True znamená, že celá sada prošla. Unittest běžně píše průběh na stderr; tečky nebo text OK v tomto kanálu samy neznamenají chybu. Rozhoduje skutečný výsledek testu, ne barva výpisu.

V terminálu v pracovní složce s uloženým reseni.py lze také spustit `python -m unittest -v test_dilna`. Python vyhledá třídu testů a zavolá funkci z reseni. Příkaz -m spouští modul, -v vypíše názvy testů. Použijte Python ze stejné .venv. Pozdější předaný projekt už použije vlastní modul predchozi a uvede to ve svém README.

Možné řešení je k dispozici, ale zkuste nejprve chybnou variantu return True: sada musí ukázat, proč nestačí. Test pomáhá zjišťovat problém; nenahrazuje otázku, zda je původní datový model pro zamýšlený závěr vhodný.
