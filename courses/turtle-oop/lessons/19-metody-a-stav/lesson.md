## Objekt si pamatuje stav

Objekt obsahuje atributy a může nad nimi provádět činnosti. Jeho aktuální hodnoty tvoří **stav**. Metoda může stav přečíst, změnit a případně vrátit výsledek. Stejný princip později použijeme pro hráčovy body nebo polohu hada.

```python
class Teplomer:
    def __init__(self, teplota):
        self.teplota = teplota

    def posun(self, rozdil):
        self.teplota += rozdil
        return self.teplota
```

Metodu `posun` definujeme na stejné úrovni odsazení jako `__init__`, nikoli uvnitř něj. `self.teplota += rozdil` vezme dosavadní hodnotu a přičte rozdíl. Změnu si objekt uchová i po skončení volání.

## Jak se předává self

```python
venku = Teplomer(18)
nove = venku.posun(3)
print(nove)                # 21
print(venku.teplota)       # také 21
```

Tečka vybírá metodu objektu `venku`. Python jej předá jako první argument `self` a číslo 3 jako `rozdil`. Proto při volání zadáváme jen 3, přestože v definici jsou dva parametry. Kdybychom `self` v definici vynechali, počet předaných argumentů by neseděl.

Zápis `teplota = teplota + rozdil` by pracoval s lokálním jménem, nikoli s atributem. Používejte `self.teplota`, když chcete číst nebo měnit údaj objektu.

## Změnit, vrátit, nebo vypsat

Tyto tři věci se dějí zvlášť:

- Přiřazení do `self.teplota` mění stav.
- `return self.teplota` posílá novou hodnotu volajícímu.
- `print(...)` pouze vypisuje text. Výpis nenahrazuje návratovou hodnotu ani změnu stavu.

Pokud metoda žádný `return` nemá, vrátí None, stejně jako obyčejná funkce. Metoda tak může měnit objekt a současně nic nevracet. Naopak metoda může vypočíst výsledek bez změny atributů. Rozhoduje její zadání.

```python
uvnitr = Teplomer(22)
venku.posun(-2)
print(venku.teplota)       # 19: změnil se jen venkovní teploměr
print(uvnitr.teplota)      # 22
```

Každá metoda pracuje s tím objektem, na kterém ji právě voláme. Stav se nesmí automaticky sdílet mezi všemi instancemi.

## Váš úkol

Vytvořte třídu `Pocitadlo`:

1. `__init__(self, zacatek=0)` uloží počáteční hodnotu do atributu `hodnota`. Výchozí parametr znáte z funkcí; funguje také u metod.
2. `pridej(self, kolik)` přičte `kolik` k dosavadní hodnotě, uloží ji a **vrátí novou hodnotu**. Argumenty jsou celá čísla a mohou být kladná, nulová i záporná.
3. `vynuluj(self)` nastaví hodnotu na 0 a vrátí None. Stačí skončit bez return.

Po `p = Pocitadlo(5)` a `print(p.pridej(2))` očekáváme 7 a také `p.hodnota == 7`. Po vynulování musí další přičítání pokračovat od nuly. Dvě počítadla fungují nezávisle. Metody nemusí nic vypisovat; při zkoušení si výsledky vypište mimo třídu.
