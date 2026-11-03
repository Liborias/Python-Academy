## Super neznamená vždy jediného rodiče

Z jednoduchého dědění už znáte `super()`. Pokud má třída více základů, musíme vědět, v jakém pořadí Python hledá metody. Tomuto pořadí se říká **MRO** (Method Resolution Order).

```python
class Popisek:
    def cesta(self):
        return ["popisek"]


class Ramovani(Popisek):
    def cesta(self):
        return ["rámeček"] + super().cesta()


class Zvyrazneni(Popisek):
    def cesta(self):
        return ["zvýraznění"] + super().cesta()


class Znacka(Ramovani, Zvyrazneni):
    pass
```

Závorky u Znacka nyní obsahují dvě základní třídy v určeném pořadí. Znacka přebírá obě chování, Ramovani i Zvyrazneni mají společný základ Popisek. Tvar vztahů připomíná kosočtverec: jde o takzvané diamantové dědění.

## Prohlédněte si skutečné pořadí

```python
print([trida.__name__ for trida in Znacka.__mro__])
# ['Znacka', 'Ramovani', 'Zvyrazneni', 'Popisek', 'object']
```

`__mro__` je n-tice tříd sestavená Pythonem. Zde se jen díváme, nic nepřepisujeme. `__name__` poskytuje jméno třídy. Zápis v hranatých závorkách postupně projde každou třídu pomocí for a vloží její jméno do nového seznamu. Výsledek se tak čte snáz než výpis samotných objektů tříd. `object` je konečný společný základ běžných Python tříd.

Python nejdříve zkouší metodu na skutečné třídě objektu, pak pokračuje podle tohoto pořadí. Není správné projít každou větev zvlášť a společný základ použít dvakrát. Také nejde obecně jen o opisování základů zleva doprava bez dalších pravidel: výsledné pořadí respektuje i jejich předky. Rozporné požadavky mohou způsobit TypeError už při definici třídy.

## Jak metody spolupracují

```python
print(Znacka().cesta())
# ['rámeček', 'zvýraznění', 'popisek']
```

1. Znacka vlastní metodu nemá, najde se tedy Ramovani.cesta.
2. `super()` uvnitř Ramovani pokračuje **za Ramovani v MRO skutečného objektu**. Pro Znacka je další Zvyrazneni, nikoli přímo Popisek.
3. Zvyrazneni opět použije super a dojde k Popisek.
4. Popisek vrátí základní seznam; ostatní metody k němu postupně připojí své části.

Proto Ramovani.cesta nemusí vědět, se kterou další třídou ji jednou použijeme. Když samostatně vytvoříme Ramovani(), jeho MRO je kratší a po Ramovani následuje Popisek. V obou případech zůstává self stejným objektem.

Společné rozhraní zde nemá další argumenty. U složitějších konstruktorů musí spolupracovat i předávání argumentů, což zatím nerozšiřujeme. Více základů není povinné: pro běžnou hru často stačí jednoduché dědění a skládání objektů. Tato lekce hlavně pomůže správně číst super a hledat chyby v cizím kódu.

## Váš úkol

Napište pět tříd s metodou `cesta(self)`:

1. `Zaklad` vrací nový seznam `["Zaklad"]` a řetězec volání ukončí.
2. `Levy(Zaklad)` pomocí super získá další seznam a přidá před něj `"Levy"`.
3. `Pravy(Zaklad)` obdobně přidá `"Pravy"`.
4. `Oba(Levy, Pravy)` využije zděděné chování.
5. `Obracene(Pravy, Levy)` má opačné pořadí základů.

Očekáváme `Oba().cesta() == ["Levy", "Pravy", "Zaklad"]` a `Obracene().cesta() == ["Pravy", "Levy", "Zaklad"]`. Samostatné Levy a Pravy fungují také. Společný základ se v jednom řetězci použije jen jednou.

V obou větvích skutečně použijte super; nevolejte Zaklad přímo a nesepisujte seznam pro konkrétní kombinaci natvrdo. Kontrola může změnit návrat základní metody a ověří, že se změna přenese dál. Každé volání má vrátit nový seznam, který může volající měnit bez ovlivnění příštího volání.
