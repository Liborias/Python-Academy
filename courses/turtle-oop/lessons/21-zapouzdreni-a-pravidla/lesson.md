## Kdo hlídá správný stav

Minule měl každý batoh vlastní seznam. Dnes přidáme pravidla: některé změny mají smysl a jiné musíme odmítnout. Například baterii nechceme nabít na záporné procento ani nad její kapacitu.

**Zapouzdření** znamená spojit data a práci s nimi do objektu a nabídnout srozumitelné operace. Volající se pak nemusí starat o každý vnitřní krok. Použije třeba `dobij(10)` místo ručního přepisování čísla.

To souvisí s **abstrakcí**: navenek stačí vědět, co metoda dělá; její vnitřní výpočet můžeme změnit bez změny způsobu volání. Dědění a polymorfismus, další dva často uváděné pilíře OOP, potkáme v následujících lekcích. Teď začneme pravidly stavu jednoho objektu.

## Podtržítko je dohoda

```python
class Baterie:
    def __init__(self, energie):
        if energie < 0 or energie > 100:
            raise ValueError("Energie musí být od 0 do 100")
        self._energie = energie

    def stav(self):
        return self._energie
```

Jedno podtržítko v `_energie` říká „vnitřní údaj, používejte veřejné metody“. Python čtení ani zápis tohoto atributu zvenku nezakáže. Není to ochrana před úmyslným zásahem do programu. Je to dohoda pro spolupráci na kódu.

`stav()` naopak patří k veřejnému rozhraní. Vrátí hodnotu a nic nemění. Ověření v konstruktoru zajistí platný počáteční stav: `Baterie(-1)` vyvolá ValueError, takže volající nedostane normálně dokončený objekt se zápornou energií.

## Nejdřív ověřit, potom změnit

```python
    def dobij(self, kolik):
        if kolik < 0 or self._energie + kolik > 100:
            raise ValueError("Takto baterii dobít nelze")
        self._energie += kolik
        return self._energie
```

Tuto metodu přidáme do třídy Baterie na stejnou úroveň jako `stav`. První řádky ověří podmínky. Při chybě příkaz `raise` okamžitě přeruší volání; k přiřazení pod ním nedojde. Díky tomu odmítnuté dobití nemění původní energii.

Kdybychom nejdříve přičetli a teprve pak vyvolali chybu, objekt by zůstal poškozený. Samotná výjimka předchozí přiřazení automaticky nevrací zpět. Chybu můžete zachytit běžným `try/except ValueError`, který už znáte.

## Váš úkol

Vytvořte třídu `Ucet` pro celé částky:

1. `__init__(self, zacatek=0)` uloží nezáporný počáteční zůstatek. Záporný začátek odmítne výjimkou ValueError.
2. `stav(self)` vrátí aktuální zůstatek bez změny.
3. `vloz(self, castka)` přijme pouze částku větší než nula, přičte ji a vrátí nový zůstatek. Jinak vyvolá ValueError.
4. `vyber(self, castka)` přijme pouze kladnou částku nejvýše rovnou zůstatku. Odečte ji a vrátí nový zůstatek. Jinak vyvolá ValueError.

Při jakémkoli odmítnutém vkladu nebo výběru se zůstatek nesmí změnit. Dva účty mají vlastní stav. Vstupy jsou celá čísla; kontrolu jiných typů zatím neřešte. Znění chybové zprávy si zvolte sami.

Uložený zůstatek pojmenujte například `_zustatek`. Kontrola používá veřejné metody, takže vás neváže na konkrétní vnitřní název. Zůstatek nevracejte jako text a změny pouze nevypisujte: metody mají měnit objekt a vracet číslo.
