## Objekt umí pracovat se svým stavem

Máme položku se jménem, cenou za kus a počtem. Přidáme dvě metody: jedna změní množství a druhá spočítá současnou cenu. Metoda je funkce definovaná ve třídě, která obvykle pracuje s konkrétní instancí.

Připravený konstruktor je stejný jako v minulé lekci. Každý objekt si dál uchovává vlastní údaje. Nové chování přidáváme přímo do Polozka; zatím nepotřebujeme dědění.

## Přečtěme volání krok po kroku

```python
novy_pocet = kniha.pridej(2)
```

1. Kniha označuje instanci, na které chceme pracovat.
2. Python najde její metodu pridej a doplní tento objekt do self.
3. Číslo 2 se předá jako kolik.
4. Metoda upraví `self.pocet` a pomocí return předá nový počet.
5. Vrácené číslo se uloží do proměnné novy_pocet v místě volání.

Podpis metody je `pridej(self, kolik=1)`. Vynechání argumentu přidá jeden kus; při explicitním kolik=0 se množství nezmění. V této lekci přidáváme pouze nezáporné celé počty kusů.

Lokální proměnná `pocet = self.pocet + kolik` by sama atribut nezměnila. Použijeme přiřazení do self.pocet, například zkrácené `self.pocet += kolik`.

## Čtení součtu nic nemění

```python
def celkem(self):
    return self.cena_za_kus * self.pocet
```

Celkem vrací součin dvou aktuálních atributů. U ceny 250 a počtu 2 je výsledek 500. Po přidání jednoho kusu bude další volání vracet 750. Neuchováváme si starý součet z konstruktoru, který by po změně množství přestal platit.

Metoda celkem sama nic nepřidává, nic nevypisuje a nemění cenu. Stejné čtení lze bezpečně opakovat. Výsledek může použít jiný objekt nebo ho hlavní program zobrazí přes print.

Vrácené číslo není živý odkaz na budoucí součet. Když si uložíme `cena = kniha.celkem()` a potom změníme množství, proměnná cena stále obsahuje původní výsledek. Nový součet získáme dalším voláním metody.

## Detektivní pokus

Spusťte ukázku a pozorujte 500, nový počet 3 a cenu 750. Druhé čtení má znovu vrátit 750. Změňte přidaný počet na nulu nebo dva. Potom vytvořte vedle knihy i obal a ověřte, že změna knihy neposune množství obalu.

Co by se stalo, kdyby celkem použila print místo return? Text by se zobrazil, ale volající by pro další výpočet dostal None. Tím by se později rozbil součet celé objednávky.

## Váš úkol

Doplňte `Polozka.pridej(kolik=1)` a `Polozka.celkem()`. Pridej změní počet této položky a vrátí nový počet. Celkem vrátí aktuální cenu za kus násobenou počtem a nic nemění.

Vstupní cena, počáteční počet i přidané množství jsou nezáporná celá čísla, včetně nuly. Jejich ověřování přijde v dalším bloku. Zachovejte konstruktor, názvy atributů a návratové hodnoty; metody samy nic nevypisují. Fungovat musí opakované přidávání, výchozí jeden kus i více nezávislých položek.
