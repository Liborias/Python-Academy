## Loď dostane obraz a místo ve světě

V Pygame 1 jsme často drželi obrázek a obdélník v různých proměnných. Ve větší hře jich budou desítky. Sprite spojí vzhled a polohu jednoho objektu a dovolí přidat jej do skupin. Není to automatická fyzika ani vlastní herní smyčka: chování stále píšeme my.

První blok kurzu vytvoří modely, které se dají prohlížet i ověřovat bez otevřeného okna. Ukázky uloží skutečný PNG z pygame Surface a aplikace jej zobrazí. Další blok z těchto principů postaví Meteority v běžném herním okně. Teď nepoběží animace; obrázek zachytí stav po provedených krocích.

## Příprava prostředí

Použijte vlastní .venv a vyberte ji ve VS Code, VSCodium nebo PyCharm. Pod seznamem kurzů je podrobná příprava pro váš systém a editor. V kořenové složce Akademie spusťte:

```text
python tools/setup_env.py --courses pygame-2
```

Pomocník připraví projektové prostředí a pygame-ce. V kódu se píše import pygame; neinstalujte současně původní balíček pygame. Příkaz `python -c "import sys, pygame; print(sys.executable); print(pygame.version.ver)"` ověří interpreter a import. Nativní okno tento příkaz neověřuje. První blok funguje bez grafické plochy a zvuku, hraní dalších projektů bude potřebovat místní plochu. Ověřeno na Pythonu 3.14.8 s pygame-ce 2.5.8. Pro běh těchto ukázek nejsou potřeba internet, obrázky ke stažení ani účet.

## Tři části jednoho objektu

`class Lod(pygame.sprite.Sprite)` říká, že Lod rozšiřuje Sprite. Konstruktor `__init__` připraví jednu konkrétní loď. `super().__init__()` nastaví také vnitřní členství Sprite; bez inicializace rodiče se může práce se skupinami rozbít až později.

- `self.image` je Surface: vlastní obrázek v paměti. Souřadnice uvnitř něj začínají vlevo nahoře od (0, 0).
- `self.rect` je Rect: umístění a rozměry ve světě hry. Obdélník sám obrázek neposune na obrazovce; kreslení použije jeho souřadnice.
- `self` odkazuje na právě tuto instanci. Dvě lodě nemají sdílet jednu proměnlivou polohu nebo obrázek, pokud to výslovně nezamýšlíme.

```python
import pygame
image = pygame.Surface((32, 24), pygame.SRCALPHA)
image.fill((80, 180, 255))
rect = image.get_rect(center=(100, 80))
print(rect.topleft, rect.center, rect.size)
```

Výsledek je (84, 68), (100, 80), (32, 24). Šířka 32 znamená polovinu 16 na každou stranu od středu, výška 24 polovinu 12. `get_rect(center=...)` vytvoří nový Rect podle obrázku. Nepoužívejte tutéž dvojici jako topleft, to by posunulo celou loď. `fill` vyplní pixely barvou RGB; SRCALPHA navíc umožní průhlednost.

## Co sledovat v ukázkách

První vytvoří jednu loď. Druhá má dvě nezávislé instance a posune jen první. Třetí ukáže, že změna rect.center nemění rozměry image. Nahled.py připraví mřížku, vykreslí sprity a uloží nahled.png; šedé okraje a souřadnice doplňuje pouze pro vysvětlení. Vlastní kresbu lodi vytváří vaše třída.

Pomocné soubory jsou ve files a aplikace je při běhu i otevření pracovního souboru přiloží vedle reseni.py. V jiném editoru otevřete vypsanou pracovní složku. PNG zůstane v pracovní složce; v aplikaci jej lze prohlédnout a stáhnout. Po obnovení stránky se náhled vytvoří dalším spuštěním.

## Váš úkol

Vytvořte třídu `Lod(stred)` odvozenou od `pygame.sprite.Sprite`. Každá instance má vlastní `image` typu Surface o velikosti **32 × 24**, vyplněný barvou **(80, 180, 255)**, a vlastní `rect` se středem `stred`. Vstup je dvojice celých souřadnic, klidně záporných. Zdrojovou dvojici neměňte; změna obrázku nebo polohy jedné lodě nesmí změnit druhou.

Další tlačítka procvičí kruhový meteorit, parametry rozměrů/barvy, kopii Surface a přidání do Group. Každé má vlastní zadání a možné řešení. Po odkrytí řešení se váš kód nepřepíše; porovnejte hlavně vlastnictví obrázku a význam souřadnic. Nemusíte opisovat konkrétní zápis, správných postupů může být více.
