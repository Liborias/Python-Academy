## Jak poznáme, že oprava nerozbila dopravu?

Výpis z jedné ukázky neprověří všechny hmotnosti ani zachování volby při chybě. Napíšeme automatické testy, které připraví situaci, provedou operaci a porovnají skutečný výsledek s očekáváním. Opakovat je můžeme po každé změně.

Použijeme unittest ze standardní knihovny, nic se neinstaluje. Soubory balik.py, doprava.py, expres.py a expedice.py obsahují hotová řešení lekcí 9–12. Jsou přiložené v aplikaci i pracovní složce editoru. Tentokrát doplňujete testy veřejného rozhraní těchto objektů, nikoli jejich implementaci.

## TestCase a metody test_

```python
import unittest

class TestExpedice(unittest.TestCase):
    def test_osobni_odber(self):
        # Příprava objektů, operace, ověření výsledku.
        ...
```

TestExpedice dědí z unittest.TestCase. Díky tomu má ověřovací metody a unittest umí její testy spouštět. Jména testovacích metod začínají test_, aby je nástroj našel. self označuje instanci testu, nikoli balík nebo expedici.

Každý test si připraví vlastní objekty. Nesmí spoléhat na to, že jiný test už vytvořil balík nebo přepnul dopravu. Pořadí provedení není součástí řešení úlohy.

## Tři základní způsoby ověření

- self.assertEqual(skutecnost, ocekavani) ověří rovnost přes ==. Použijeme ji pro cenu nebo text.
- self.assertIs(skutecnost, puvodni) ověří totožnost přes is. Tím prokážeme uchování stejného balíku či dopravy, nikoli kopie.
- with self.assertRaises(ValueError): očekává tuto výjimku v odsazeném bloku. Pokud blok výjimku nevyvolá nebo vznikne jiná, test neprojde.

With vytváří řízený blok: assertRaises zachytí očekávanou chybu a potom test pokračuje. U odmítnuté dopravy za blokem ověříme také původní volbu a cenu. Pouhé zachycení chyby by přehlédlo, že program před selháním poškodil stav.

Šablona používá self.fail("Doplňte test podle zadání."). To je úmyslné okamžité selhání, které nahradíte přípravou a ověřováním. Prázdný test s pass by vypadal úspěšně, přestože by nic neověřoval.

## Váš úkol: čtyři scénáře

Vytvořte v TestExpedice alespoň čtyři samostatné testy. Připravené názvy můžete ponechat.

1. Osobní odběr: expedice pro balík 1200 g vrací 0 a uchovává původní balík i objekt odběru.
2. Hranice kurýra s výchozím limitem: 5000 g stojí 99, 5001 g stojí 149 a přesně 10000 g je ještě povolených za 149 Kč.
3. Úspěšná změna z odběru na kurýra: pro 1200 g vrátí 99, uchová nového kurýra i původní balík a další nabídka je také 99.
4. Odmítnutá změna: kurýr s limitem 1000 g odmítne balík 1200 g přes ValueError. Potom zůstává původní objekt odběru, původní balík a nabídka 0.

Používejte veřejné property a metody. Nespoléhejte na _doprava nebo jiné vnitřní uložení. Pracujte se skutečnými objekty z připravených modulů, testy nepřeskakujte. Automatická kontrola kromě úspěchu nad správným modelem ověří, zda vaše testy odhalí záměrně změněné ceny, ztracené reference a změnu volby před kontrolou. Díky tomu nestačí napsat jen assertEqual(99, 99).

## Spuštění a čtení výsledku

Připravený hlavní blok používá unittest.main(verbosity=2). Najde testy v tomto souboru a vypíše jméno každého z nich. Při přímém spuštění python reseni.py se provede právě tento blok. V terminálu pracovní složky můžete také použít `python -m unittest -v reseni`: -m spustí modul unittest, -v zapne podrobný výpis a reseni je název modulu bez .py. Tehdy se soubor importuje a jeho hlavní blok se nespustí.

OK znamená, že všechna provedená ověření prošla. FAIL značí nesplněné očekávání, ERROR neočekávanou výjimku. Zpráva ukáže konkrétní metodu a místo problému. Počet testů je počet metod, nikoli počet assertEqual uvnitř. Tři hmotnostní hranice tedy mohou být jedním testem s více ověřeními.

Unittest běžně posílá tento přehled do chybového výstupu, a to i při OK. V konzoli aplikace se proto může zobrazit v této části; rozhoduje výsledek a návratový kód programu, samotné umístění textu neznamená chybu.

Nejprve spusťte hotovou ukázku se čtyřmi testy. Pak doplňte vlastní řešení a použijte Zkontrolovat. Úspěšné testy jsou důkazem uvedených scénářů, nikoli všech možných vlastností programu. V závěrečném projektu stejným postupem ověříme rezervaci, storno a celý průchod objednávky.
