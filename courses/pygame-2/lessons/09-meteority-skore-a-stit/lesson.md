## Skóre má vyjadřovat konkrétní výsledek

Za kámen, kterému jste se vyhnuli a který celý odletěl spodem, získáte bod. Kolizí odstraněný kámen bod nedává. Stav proud.minulo už správné průlety počítá, proto skóre nebude záviset na počtu snímků ani na tom, kolikrát se vykreslil text.

Teď součásti spojí vlastní třída Kolo. Používá Hrac, ProudMeteoritu a Zdravi z predchozi.py. Nejde o další dědění z „větší hry“, ale o kompozici: kolo tyto objekty vlastní a koordinuje. Podklad bonus.py dodává BonusStitu s radius=12, obrázkem a rychlostí pádu 80 px/s; nemusíte znovu psát stejný pohyb. Jeho update uchovává přesnou pozici jako u meteoritů.

## Pořadí může změnit výsledek

Pokud seberete štít a současně do vás narazí kámen, v naší hře vás právě sebraný štít ochrání. Proto nejprve sbíráme bonusy, až potom posuzujeme zásah. Není to obecný zákon her, ale výslovné pravidlo tohoto projektu.

```python
import pygame
from podklady import HRANICE
from predchozi import Hrac
from bonus import BonusStitu
hrac = Hrac((320, 420), HRANICE)
bonusy = pygame.sprite.Group(BonusStitu(hrac.rect.center))
chycené = pygame.sprite.spritecollide(hrac, bonusy, True, pygame.sprite.collide_circle)
print('Chyceno:', len(chycené), 'zbývá:', len(bonusy))
```

Výsledek je 1 chycený a 0 zbývajících bonusů. True odstraní zasažený Sprite ze všech skupin. Získaný štít budeme uchovávat jako bool, ne jako počet: další bonus aktivní štít nenásobí.

## Váš úkol: Kolo(seed=7)

Připravte vlastní kopii HRANICE, hráče na (320, 420), proud s vlastním random.Random(seed), Zdravi(), prázdnou Group bonusy, bonus_cas=0.0, skore=0 a stit=False. Atributy se jmenují hranice, hrac, proud, zdravi, bonusy, bonus_cas, skore a stit. Dvě kola nesmějí sdílet měnitelný svět. Stejné semeno dá stejný začátek náhodné posloupnosti.

**update(smer, dt)** postupuje takto:

1. Při zivoty=0 nic neměňte. Jinak proveďte zdravi.tick(dt), hrac.update(smer, dt), proud.update(dt, hranice) a nastavte skore na proud.minulo.
2. Aktualizujte existující bonusy a ty s rect.top >= hranice.bottom odstraňte pomocí kill.
3. Přičtěte dt do bonus_cas. Za každý celý interval **6 sekund** odečtěte 6 a vytvořte BonusStitu na (hranice.centerx, hranice.top−12). Nové bonusy se v témž kroku ještě nepohnou.
4. Seberte zasažené bonusy kruhovou kolizí s odstraněním. Aspoň jeden nastaví stit=True.
5. Najděte a odstraňte všechny kruhové zásahy meteoritů. Během nezranitelnosti už dál nic neodečítejte ani nespotřebovávejte štít. Jinak aktivní štít přepněte na False a nastavte nezranitelnost na zdravi.ochrana; bez štítu zavolejte zdravi.zasah().

Dt je nezáporný konečný čas, směr má stejný význam jako u hráče. Štít tedy pohltí jednu dávku zásahů a poskytne stejnou krátkou ochranu jako ztráta života. Při konci kola se zmrazí pohyb, čas bonusu, průlety i skóre. Společná sestava jen zobrazí váš skutečný model.

V ukázce se první bonus objeví po šesti sekundách nad středem a pak padá dolů; na přílet k hráči potřebuje další čas. Zelený kruh značí aktivní štít. Vyzkoušejte sebrání a zásah, odhalení vzoru použijte pro porovnání pořadí operací. Nový let a pauzu doplní poslední krok.
