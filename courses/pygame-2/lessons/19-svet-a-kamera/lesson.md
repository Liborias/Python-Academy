## Svět je větší než obrazovka

Místo přesouvání všech objektů při každém kroku kamery uchováme jejich světové souřadnice a změníme jen pohled. Kamera má posun, tedy levý horní roh viditelné části světa, a vyhled — obdélník na obrazovce, do kterého kreslí. Výhled nemusí začínat v (0,0), například nad ním necháme prostor pro HUD.

Náhledy ukazují jiný pohled na stejný svět, omezení na jeho okraji a svět menší než výhled. Jsou to PNG, ne pohybující se okno. Prostředí z lekce 16 je stejné, zvuk ani displej nejsou potřeba.

```python
import pygame
svetovy_bod = pygame.Vector2(760, 450)
posun = pygame.Vector2(460, 320)
roh_vyhledu = pygame.Vector2(60, 100)
obrazovka = svetovy_bod - posun + roh_vyhledu
zpet = obrazovka + posun - roh_vyhledu
print('Na obrazovce:', tuple(obrazovka))
print('Zpět ve světě:', tuple(zpet))
```

Bod je na obrazovce (360,230) a zpět získáme (760,450). Odečtení posunu zajišťuje pohyb pohledu opačný k pohybu světa. Přičtení rohu výhledu umístí výsledek do správné části okna. Zaokrouhlení odložíme až do kreslení; desetinná kamera jinak zbytečně cuká.

## Sledování a omezení

Chceme-li mít hráče ve středu, od jeho polohy odečteme polovinu šířky a výšky výhledu. Kamera nesmí za okraj světa. U malého světa si zvolíme jednoduché pravidlo: připnout jej vlevo nahoře. Jiná hra by jej mohla centrovat, ale nesmí se tato rozhodnutí náhodně míchat.

Kliknutí z události je v souřadnicích okna. Před porovnáním se světovým objektem je převeďte zpět do světa. Stejný bod po převodu tam a zpět musí vyjít stejně, včetně desetinné části. Body mimo výhled neodmítá převod, případné filtrování udělá až ovladač hry.

## Neviditelný objekt pořád existuje

Viditelne vybere objekty pro kreslení, neodstraní je ze světa. Objekt za kamerou může dál patřit do simulace. Průnik počítáme ze skutečné desetinné polohy pohledu a Rect objektu, při pouhém dotyku hrany jej nezobrazíme.

Set_clip chrání okolí výhledu. Už před námi však volající mohl nastavit užší výřez, proto použijeme průnik obou. Try/finally obnoví původní výřez také při chybě, aby další kreslení nemělo skryté vedlejší účinky. Zdrojové obrázky i světové Rect se během kreslení nemění. Úkoly 2–5 mají potřebné předchozí funkce připravené v kamera.py.

## Váš úkol: Kamera sleduje bod

Vytvořte `Kamera(vyhled, svet)`: vlastní kopie obou Rect s kladnými rozměry a `posun=Vector2(svet.topleft)`. Vstupem může být Rect nebo čtveřice (x,y,šířka,výška). Vyhled je obdélník na obrazovce, svet obdélník světových souřadnic. `sleduj(bod)` nejprve vypočítá levý horní roh tak, aby bod byl uprostřed výhledu; odečte poloviny šířky a výšky. Potom omezí obě souřadnice na svět a uloží přesný Vector2 posun.

Horní mez pro x je max(svet.left, svet.right − vyhled.width), obdobně y. Je-li svět menší než výhled, kotví se vlevo nahoře; necentrujeme jej ani nevracíme zápornou šířku intervalu. Bod může být desetinný nebo mimo svět. Neměňte vstupní Rect ani bod, souřadnice nezaokrouhlujte.

Další čtyři zadání přepnete tlačítky Úkol 2–5. U každého najdete vlastní možné řešení; jeho odkrytí nemění rozepsaný kód ani splnění.
