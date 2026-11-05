## Jedna partie má vlastní pravidla a výsledek

Tělo hada ještě není celá hra. Potřebujeme také potravu, skóre a informaci, zda se smí pokračovat. Třída `Partie` proto **obsahuje** instanci BezpecnyHad; nedědí z něj. Jde o skládání objektů: partie používá hada a přidává pravidla celé hry.

Tato část opět běží v konzoli. Stejné pravidlo pak použije grafická aplikace. Výběr volného místa a kontrola pohybu jsou v připravených souborech z lekcí 33–34.

## Tři pojmenované stavy

- `"hra"`: partie běží a může provést další krok.
- `"konec"`: hlava narazila do těla.
- `"vyhra"`: na celé ploše už nezůstala volná buňka.

Jsou to obyčejné řetězce, jejichž přesná jména si mezi částmi programu domluvíme. `self.skore` začíná na nule. Za každou snědenou potravu přidáme 10 bodů; běžný pohyb ani kolize body nemění.

Konstruktor je připravený. Vytvoří vlastního hada, uloží funkci výběru, připraví první potravu a zvolí počáteční stav. Je-li plocha plná už na začátku, jde rovnou o výhru bez pohybu a bez bodů za neexistující potravu.

## Pořadí jednoho kroku partie

1. Pokud stav není hra, vrátíme ho a nic jiného neprovedeme.
2. Zkusíme `self.had.krok(self.potrava)` a uložíme vrácenou hlavu.
3. Při ValueError nastavíme konec a tento stav vrátíme.
4. Když hlava snědla současnou potravu, přidáme 10 bodů a vybereme další potravu nad **novým** tělem.
5. Pokud další potrava neexistuje, přepneme do výhry. Vrátíme aktuální stav.

```python
try:
    hlava = self.had.krok(self.potrava)
except ValueError:
    self.stav = "konec"
    return self.stav
```

Kontrola předchozí lekce zachovává při kolizi platné tělo. Partie nyní navíc nechá skóre i potravu na posledních hodnotách a změní jen stav. Nechytáme obecně každou možnou chybu — zachycujeme konkrétní signál odmítnutého kroku.

## Proč nejprve růst a až potom nová potrava

Nová hlava a zachovaný ocas jsou už součástí hada. Kdybychom potravu vybírali ze starého těla, mohla by se objevit pod právě přidanou hlavou. Proto nejdřív provedeme krok a potom zavoláme `vyber_potravu(self.had, self.vyber)`.

Tuto funkci nevoláme při běžném pohybu. Existující potrava zůstává na stejném místě, dokud ji had nesní. Nepoužíváme souřadnici `(0, 0)` jako test pravdivosti — je to platná buňka. Chybějící potravu poznáváme pomocí `is None`.

Jestliže snědení poslední volné buňky vyplní plochu, přičteme i za tuto poslední potravu 10 bodů a teprve pak vyhlásíme výhru. Další volání krok už nevybírá potravu, nezvyšuje skóre a nehýbe tělem.

## Vyzkoušejte předvídatelnou partii

Ukázka předává funkci prvni místo náhodného výběru. Při uvedeném procházení buněk tak připraví potravu rovnou před hada. Po prvním kroku uvidíte skóre 10 a délku 3, po druhém skóre 20 a délku 4.

Zkuste malou plochu `Partie([(0, 0)], 2, 1, prvni)`. Jediné volné místo je `(1, 0)`. Po kroku je plocha zaplněná, skóre je 10 a stav vyhra. Druhý krok už nesmí nic změnit.

## Váš úkol

Doplňte `Partie.krok()` podle uvedeného pořadí. Vraťte vždy aktuální řetězec stavu. Využijte vlastní model, současnou potravu a uloženou funkci výběru. Po snědení aktualizujte potravu, při běžném pohybu ji ponechte.

Konstruktor v šabloně zachovejte. Kontrola vyzkouší různé plochy, více potrav, kolizi, poslední volnou buňku i další volání po ukončení. Každá partie má nezávislé tělo, skóre a výsledek.
