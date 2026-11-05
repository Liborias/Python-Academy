## Položka má být připravená hned po vytvoření

V minulé lekci jsme po vytvoření zásilky přiřazovali její údaje jednotlivě. Tentokrát připravíme položku objednávky rovnou s názvem, cenou za kus a množstvím:

```python
kniha = Polozka("Průvodce Pythonem", 250, 2)
```

V úvodu pracujeme s celými korunami a nezápornými celými počty kusů. Cena 0 může označovat dárek, počet 0 zatím prázdný řádek. Pravidla odmítání nevhodných hodnot doplníme v dalším bloku; teď se soustředíme na vznik instance.

## Co Python udělá při volání třídy

```python
class Polozka:
    def __init__(self, nazev, cena_za_kus, pocet=1):
        self.nazev = nazev
        self.cena_za_kus = cena_za_kus
        self.pocet = pocet
```

Volání Polozka vytvoří objekt a Python pro něj použije metodu `__init__`, která připraví jeho počáteční stav. Dvě podtržítka jsou součástí přesného názvu metody; nepřejmenovávejte ji na init.

`self` označuje právě připravovanou instanci. Není to zvláštní klíčové slovo, ale běžně používané jméno prvního parametru. Python objekt doplní automaticky. Ve volání `Polozka("Obal", 30)` proto sami self nepíšeme.

## Stejné jméno může mít dvě různé role

Na řádku `self.pocet = pocet` je vlevo atribut objektu, vpravo argument aktuálního volání. Hodnotu argumentu uložíme do této instance, aby byla k dispozici i po skončení metody.

Pouhé `pocet = pocet` by nic do objektu neuložilo. Zápis `Polozka.pocet = pocet` by naopak pracoval se třídou a mohl vytvářet společný stav. Pro údaje jedné položky používáme instanci self.

Init nic nevrací pomocí return objekt. Instanci jako výsledek volání poskytne Python; úkolem init je nastavit její stav. Explicitní return s jinou hodnotou než None by způsobil chybu.

## Výchozí počet

Parametr `pocet=1` znamená, že když poslední argument vynecháme, použije se jednička. Pokud výslovně zadáme 0, uloží se nula. Není správné vyhodnotit nulu jako žádnou hodnotu a nahradit ji výchozí jedničkou.

Každé volání konstruktoru má své argumenty i instanci. Dvě knihy stejného názvu nejsou automaticky jeden objekt. Můžeme vytvořit několik položek současně a měnit je nezávisle.

## Vyzkoušejte ukázku

První položka dostane dva kusy, druhá použije výchozí jeden. Pak změníme počet první na tři. Druhá má dál jeden kus. Zkuste jednu položku vytvořit výslovně s nulovým počtem nebo s jiným názvem a porovnejte výpis.

## Váš úkol

Doplňte konstruktor třídy `Polozka(nazev, cena_za_kus, pocet=1)`. Uložte stejnojmenné atributy na vytvořené instanci a zachovejte všechny předané hodnoty. Název je řetězec, cena a počet jsou nezáporná celá čísla.

Konstruktor nic nevypisuje a nevrací jinou hodnotu než obvyklé None. Ponechte výchozí počet 1. Hlavní blok je hotový; později s touto položkou budeme počítat a měnit její množství pomocí metod.
