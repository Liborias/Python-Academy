## Test může odhalit chybu dřív než hráč

V této lekci nepíšete další implementaci pohybu. Píšete ověření toho, co už model slibuje. Unittest.TestCase uspořádá nezávislé pokusy a assert metody porovnají skutečný výsledek s očekáváním. Test musí selhat, když se pravidlo poruší.

```python
import unittest
class MaleOvereni(unittest.TestCase):
    def test_soucet(self):
        self.assertEqual(2 + 3, 5)
sada = unittest.defaultTestLoader.loadTestsFromTestCase(MaleOvereni)
print('Počet testů:', sada.countTestCases())
```

Výstup 1 ukazuje počet nalezených metod test_. Samotný počet ale neříká nic o jejich užitečnosti. AssertTrue(True) vždy projde a pohyb neověří. Naše kontrola proto vaši sadu spustí i proti známým vadám. Musí je odlišit od správné hry.

## Příprava, krok, očekávání

Každý pokus má nový objekt, jeden zřetelný děj a ověření výsledku. Nevyvozujte očekávanou hodnotu opětovným zavoláním stejné funkce. Pro hráče rychlého 240 px/s si například spočítáme posun za 0,025 s jako 6 px předem.

AssertEqual porovnává hodnoty, assertIs/IsNot identitu a assertAlmostEqual desetinné výsledky s tolerancí. With self.subTest(...) označí více vstupů téhož pravidla, abyste při chybě poznali konkrétní případ. Výjimka ve vadném modelu může test odhalit také; nejprve ale musí projít správný model.

Model_hry importujte jako modul nebo si z něj vezměte třídy. Neotevíráte displej, nepoužíváte sleep a testy neběží přes fyzické klávesy. Zelené automatické testy nenahradí zkoušku skutečného okna.

## Váš úkol

Napište vlastní unittest testy třídy **model.Hrac** a funkci **sestav_sadu()**, která vždy vrátí novou unittest.TestSuite. Připravený hlavní blok ji spustí; vraťte se k terminálu a čtěte i stderr, kam unittest běžně píše výsledek.

Ověřte nulový vstup, skutečný posun rychlost × dt, diagonálu stejně rychlou jako přímý pohyb a celý obraz uvnitř všech okrajů arény. Použijte vlastní Hrac a Rect pro každý pokus. Konkrétně (1,0) za 0,025 s při rychlosti 240 znamená 6 pixelů. Diagonála za 0,05 s má délku 12, ne 12 v každé ose. U desetinných výsledků se hodí assertAlmostEqual.

Kontrola spustí vaši sadu na správném modelu i na třech úmyslně rozbitých modelech: chybný časový krok, rychlejší diagonála a chybějící omezení okrajů. Správný musí projít, každou vadu musí sada odhalit. Počet ani názvy testů nejsou předepsané, přeskočené testy nestačí.
