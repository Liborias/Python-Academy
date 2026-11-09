## Stejné volání, jiné chování

Robot stojí. Hlídač se pohybuje rovně a u hranice otočí směr. Kývač se vrací kolem pevné kotvy jako kyvadlo. Herní smyčka nemusí zjišťovat typ a psát tři různé větve: zavolá roboty.update(dt,hranice) a Group předá stejné argumenty metodě každého objektu.

Tomuto použití společného rozhraní říkáme **polymorfismus**. Hlidac i Kyvac dědí Robot, takže mají obrázek, obdélník, body i obsahuje. Přepíší jen konstrukci potřebných parametrů a update. Super().__init__ spustí konstruktor rodiče a zabrání opisování společných částí. Self.barva dovolí rodiči použít barvu konkrétního potomka.

Predchozi.py už obsahuje Robot a najdi_robota z kroku 11. V sestavě se tentokrát objeví dva modří hlídači a fialový kývač. Zásahy dál vycházejí ze skutečně kresleného rect.center. Spuštění, místní okno a roboti.png fungují jako minule.

## Hlídač: desetinný pohyb a odraz

Rychlost je Vector2 v pixelech za sekundu. Posun je rychlost × dt, ne jedna rychlost za každý snímek. Polohu držte desetinnou a pouze rect.center zaokrouhlete. Celý kruhový obrázek musí zůstat uvnitř hranic.

Při dosažení levé hrany nastavte x=left+radius a rychlost.x=abs(rychlost.x); při pravé x=right−radius a rychlost.x=−abs(rychlost.x). Stejně y a horní/dolní okraj. Abs zachová velikost a zvolí směr dovnitř, takže opakovaný update s dt=0 směr znovu neobrátí. Při přesném dosažení hranice se už směr nastaví dovnitř.

Je to úmyslně jednoduchý krokový model: přebytek pohybu za hranou zahodíme. Neodrážíme opakovaně celý zbytek dlouhého časového kroku. Smyčka používá dt nejvýše 0,05 s; při návratu po dlouhé prodlevě se hra neposune o celý reálný čas čekání.

## Kývač: kotva není poslední poloha

Sinus vrací číslo od −1 do 1. Násobení amplitudou určí největší výchylku v pixelech. Výraz 2π×čas/perioda převede herní čas na úhel v radiánech: jedna perioda znamená celý návrat do stejné fáze.

```python
import math
for cas in (0, 0.5, 1, 1.5, 2):
    vychylka = 50 * math.sin(2 * math.pi * cas / 2)
    print(cas, round(vychylka))
```

Výchylky jsou 0, 50, 0, −50, 0 pixelů. Kývač počítá x vždy od pevné kotvy. Přičítání výchylky k minulé poloze by způsobilo jiný pohyb a postupné ujíždění. Při malé změně času neztrácejte desetinnou část. Perioda je v sekundách, amplituda v pixelech.

## Váš úkol: dva potomci Robot

**Hlidac(stred, rychlost=(90,55), polomer=22, body=10)** použije barva=(80,170,255), konstruktor rodiče a vlastní kopii rychlosti jako Vector2. Update(dt,hranice) provede popsaný pohyb, omezení a nastavení směru pro obě osy; potom nastaví rect.center z round(pozice.x/y). Hranice jsou dost velké pro celý sprite a počáteční střed je uvnitř. Nezměňte vstupní vektory ani Rect.

**Kyvac(stred, amplituda=50, perioda=2, polomer=22, body=20)** má barva=(195,145,255). Inicializuje rodiče, vlastní kopii kotva, amplituda, perioda a cas=0.0. Nekladnou periodu odmítne ValueError; jinak je kladná a konečná, amplituda nezáporná konečná. Update přičte dt do cas a vypočítá x = kotva.x + amplituda × sin(2π × cas / perioda), y = kotva.y. Obě souřadnice omezí na předané hranice s odstupem radius a aktualizuje rect. Kotva se nemění, ani když se poloha musela oříznout.

Všem update předáváme konečné nezáporné dt. Každý objekt má vlastní polohu, rychlost či čas. Ověřte všechny čtyři okraje, roh, mnoho malých kroků a čtvrtinu periody. V jedné Group potom mohou být stojící i oba pohybliví roboti; společné volání samo vybere správnou metodu.
