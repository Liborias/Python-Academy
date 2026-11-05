## Expediční centrum přijímá první zásilky

Představte si malou dílnu, která posílá knihy a vlastní výrobky. Každá zásilka má kód, příjemce a stav. Začneme tím, jak tyto údaje v programu pojmenovat a jak vytvořit více nezávislých záznamů. V dalších lekcích k nim přidáme společné chování a pravidla.

Kurz potřebuje jen základy Pythonu a standardní knihovnu. Nevyžaduje Turtle ani hry. Ukázky a úkoly spustíte v konzoli pod editorem; příprava prostředí je nad seznamem lekcí.

## Od známého slovníku k vlastnímu typu

Seskupení údajů už známe:

```python
zasilka = {"kod": "Z-101", "prijemce": "Ema", "stav": "prijata"}
print(zasilka["kod"])
```

Slovník je vhodný například pro jednoduchá vstupní data. Třída nám umožní pojmenovat vlastní druh objektu a postupně k němu přidat metody, které s jeho údaji pracují. Dnes uděláme první malý krok:

```python
class Zasilka:
    pass

zasilka = Zasilka()
zasilka.kod = "Z-101"
```

`class` začíná definici třídy. Zasilka je její jméno; u tříd se obvykle začíná velkým písmenem. `pass` znamená prázdné tělo, aby byla definice zatím platná.

Volání `Zasilka()` vytvoří konkrétní **instanci**. Třída popisuje druh objektů, instance je jedna zásilka. Zápis `zasilka.kod` pomocí tečky označuje **atribut**, tedy pojmenovaný údaj této instance. Přiřazení uloží hodnotu právě do ní. V další lekci přeneseme počáteční přiřazování do konstruktoru.

## Funkce pořád mají své místo

Funkce vytvor_zasilku může vytvořit instanci, naplnit její atributy a vrátit ji. Volající pak dostane objekt, který může dál číst nebo měnit. Return předává hodnotu; print by pouze zobrazil text a sám místo objektu vracel None.

Stejná jména atributů na dvou nově vytvořených instancích neznamenají stejnou paměť pro jejich hodnoty. Když změním příjemce zásilky Z-101, zásilka Z-102 má zůstat pro Jana. Každé volání funkce proto musí vytvořit novou instanci.

Samotný údaj stav nic neodesílá. Hodnota `"prijata"` je zde domluvený programový zápis pro přijatou zásilku. Oprávněné přechody mezi stavy budeme řešit později.

## Zkuste nejprve odhadnout výstup

Ukázka vytvoří dva balíčky s hmotností 2 a 5. Pak změní první na 3. Před spuštěním si tipněte, jakou hmotnost vypíše druhý. Po spuštění změňte kódy nebo hmotnosti a sledujte, ke kterému objektu se jednotlivá přiřazení vztahují.

Objekty mají smysl, když jejich údaje a související operace tvoří vlastní pojem našeho programu. Není nutné převádět každý slovník na třídu. V expedičním centru ale budou mít zásilky, položky a objednávky vlastní chování, proto si je postupně pojmenujeme.

## Váš úkol

Doplňte `vytvor_zasilku(kod, prijemce)`. Vytvořte novou instanci třídy Zasilka, uložte přesně předané hodnoty do atributů kod a prijemce, nastavte stav na `"prijata"` a vraťte vytvořený objekt.

Vstupy jsou řetězce. Zachovejte jejich obsah včetně mezer, diakritiky nebo uvozovek; není třeba je upravovat ani ověřovat. Funkce nic nevypisuje. Nevracejte samotnou třídu, slovník nebo jeden společný objekt používaný pro všechny zásilky.

Hlavní blok v šabloně vytvoří dvě zásilky a jejich údaje vypíše. Podmínka `if __name__ == "__main__":` odděluje přímé spuštění tohoto souboru od jeho případného importu.
