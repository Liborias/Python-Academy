## Od slovníku k vlastnímu typu

Ve slovníku jsme drželi údaje o jedné věci: třeba jméno hráče a počet bodů. Teď vytvoříme vlastní **třídu**. Třída popisuje nový typ objektů, **instance** je jeden konkrétní objekt tohoto typu.

Želvu už jste vytvářeli příkazem `turtle.Turtle()`. Knihovna dodala třídu `Turtle`; proměnná `t` pak odkazovala na jednu konkrétní želvu. Tady si jednoduchou třídu napíšeme sami, zatím bez kreslení a bez herního okna.

```python
class Zvire:
    pass
```

`class` zahajuje definici třídy, za názvem je dvojtečka a odsazené tělo. Názvy tříd obvykle začínají velkým písmenem. `pass` je příkaz „zatím nedělej nic“: použijeme ho tam, kde Python vyžaduje tělo, ale ještě do něj nemáme co napsat. Samotná definice žádné konkrétní zvíře nevytvoří.

## Vytvoření instance a atributy

```python
prvni = Zvire()
prvni.jmeno = "Vydra"
prvni.energie = 8

print(prvni.jmeno)       # Vydra
print(prvni.energie)     # 8
```

Závorky `Zvire()` vytvoří nový objekt. V proměnné `prvni` máme odkaz na něj. Zatím třídě nepředáváme žádné argumenty; k tomu přijdeme v další lekci.

Údaj připojený k objektu se jmenuje **atribut**. Zápis `prvni.jmeno` znamená „atribut jmeno objektu prvni“. Přiřazením ho vytvoříme nebo přepíšeme, při čtení získáme jeho hodnotu. Na rozdíl od slovníku zde nepíšeme hranaté závorky s řetězcovým klíčem. Jméno atributu samo není samostatná globální proměnná.

Čtení atributu, který jsme ještě nepřiřadili, vyvolá `AttributeError`. Nejdříve tedy údaj vytvořte, teprve potom jej používejte.

## Dva samostatné objekty

```python
druhy = Zvire()
druhy.jmeno = "Jezevec"
druhy.energie = 3
prvni.energie = 9
print(druhy.energie)      # stále 3
```

Každé volání `Zvire()` vytváří novou instanci. Změna jedné nemá přepsat údaje druhé.

Naopak `kopie = prvni` nový objekt nevytvoří: obě proměnné ukazují na stejné zvíře. Změna `kopie.energie` se proto projeví i při čtení `prvni.energie`. Je to stejný princip sdílení, který už znáte ze seznamů. Pro jiného hráče vytvořte novou instanci.

## Váš úkol

1. Definujte třídu `Hrac`. Pro tuto lekci může její tělo obsahovat jen `pass`.
2. Napište funkci `vytvor_hrace(jmeno, body)`. Uvnitř vytvoří novou instanci `Hrac()`, přiřadí jí atributy `jmeno` a `body` z argumentů a vrátí ji.
3. Každé zavolání má vracet jiného hráče. Jméno i body pouze uložte, nijak je neupravujte. Počet bodů může být i nula nebo záporné číslo.

Například po `a = vytvor_hrace("Ema", 4)` mají `a.jmeno` a `a.body` obsahovat `"Ema"` a `4`. Vytvoření dalšího hráče ani změna jeho bodů nesmí změnit hráče `a`.

Funkce má vracet objekt, nikoli slovník ani vypsaný text. Při zkoušení si jeho atributy vypište sami. V dalších lekcích přeneseme nastavování atributů přímo do třídy.
