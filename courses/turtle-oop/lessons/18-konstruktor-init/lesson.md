## Atributy připravené při vytvoření

Minule jsme objekt nejdříve vytvořili a potom k němu připojili údaje. Snadno bychom zapomněli některý nastavit. Třída může přípravu provést sama pomocí metody `__init__`.

**Metoda** je funkce definovaná uvnitř třídy. `__init__` je její zvláštní jméno: před i za `init` jsou dvě podtržítka. Python ji automaticky zavolá při vytváření nové instance. Běžně se jí říká konstruktor; přesněji zde inicializuje už vytvořený objekt.

```python
class Kniha:
    def __init__(self, nazev, stran):
        self.nazev = nazev
        self.stran = stran
```

`def` už znáte z funkcí. Tentokrát je definice odsazená uvnitř `class`. Tělo metody je odsazené o další úroveň. Parametr `self` označuje konkrétní objekt, se kterým metoda právě pracuje. Není to magické globální jméno: dostaneme ho jako první parametr a podle konvence mu říkáme `self`.

## Co se stane při volání třídy

```python
kniha = Kniha("Cesta lesem", 120)
print(kniha.nazev)       # Cesta lesem
print(kniha.stran)       # 120
```

1. Python vytvoří novou instanci třídy `Kniha`.
2. Do jejího `__init__` předá instanci jako `self`, text jako `nazev` a číslo jako `stran`.
3. `self.nazev = nazev` uloží argument do atributu nového objektu. Levá strana je atribut, pravá lokální parametr metody; nejde o tutéž proměnnou.
4. Po dokončení inicializace získáme připravený objekt a uložíme jej do proměnné `kniha`.

`self` při volání `Kniha(...)` sami nedopisujeme. `__init__` má provést nastavení, nikoli vracet nový objekt. Může skončit bez `return` (implicitně vrátí None); nepište do něj `return self`, protože to vyvolá `TypeError`.

Také nevolejte `kniha.__init__(...)` ručně místo vytvoření nové knihy: tím byste znovu nastavovali existující objekt.

## Každá instance má své hodnoty

```python
prvni = Kniha("Řeka", 80)
druha = Kniha("Hory", 200)
prvni.stran = 81
print(druha.stran)        # stále 200
```

Inicializátor běží pro každou novou instanci znovu. Nastavujte proto údaje přes `self.stran`. Přiřazení jen do lokálního `stran` by po skončení metody nezaložilo atribut objektu. Přiřazení přes `Kniha.stran` by naopak měnilo údaj třídy; ten bychom mezi knihami nechtěli sdílet.

## Váš úkol

Napište třídu `Obdelnik` s metodou `__init__(self, sirka, vyska)`. Uloží oba argumenty do stejně pojmenovaných atributů instance `sirka` a `vyska`.

Příkaz `r = Obdelnik(3, 5)` má hned vytvořit objekt s `r.sirka == 3` a `r.vyska == 5`. Rozměry v tomto úkolu neověřujte ani neměňte: pouze je uložte. Zkoušíme nulu, desetinné hodnoty i několik různých obdélníků současně. Změna jednoho se nesmí projevit u druhého.

Zatím nepřidávejte metody pro obsah nebo obvod; ty procvičíme později. Pro ověření použijte `print(r.sirka, r.vyska)`.
