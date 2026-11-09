## Pauza je stav hry, ne přestávka v programu

Pauzu neuděláme nekonečným čekáním ani time.sleep. Kdybychom přestali číst události, okno by nemuselo reagovat ani na zavření. Oddělíme zpracování událostí, aktualizaci herních objektů a kreslení. V pauze dál čteme vstup a můžeme kreslit poslední stav, ale neposouváme svět.

Tato lekce připraví malé třídy s jasnými pravidly. Skutečnou smyčku s Clock a display vytvoříme v Meteoritech. Teď předáváme události a časy ručně, abychom mohli pozorovat i ověřit přesné přechody.

## Událost se dá vytvořit i bez okna

```python
import pygame
udalost = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_p)
print(udalost.type == pygame.KEYDOWN)
print(udalost.key == pygame.K_p)
```

Oba výsledky jsou True. Event je datový objekt: nejprve zkontrolujeme type, teprve u KEYDOWN čteme key. QUIT atribut key vůbec mít nemusí. V živé hře dostaneme události přes event.get; tady je vytvoříme pro konkrétní scénář. KEYUP klávesy P nemá pauzu přepínat podruhé.

## Tři situace pro HerniStav

- Běží a není pauza: skupina dostane update(dt).
- Běží a je pauza: svět zůstane stát, P jej může znovu spustit.
- Neběží: update se neprovádí a P už ukončenou hru neobnoví.

`not self.pauza` přepne bool. Stav patří do instance, protože pauza jedné hry nemá změnit druhou. HerniStav neobsahuje konkrétní loď, jen dostane skupinu, se kterou má pracovat. Tomuto skládání spolupracujících objektů říkáme kompozice.

## Váš úkol

`HerniStav()` začíná s bezi=True a pauza=False. `zpracuj(udalost)` na QUIT nastaví bezi=False, na KEYDOWN klávesy P přepne pauzu jen pokud hra ještě běží; jiné události nic nemění. `update(skupina, dt)` zavolá update(dt) na členech právě jednou, pouze pokud bezi a není pauza. Pauza nezastaví čtení událostí, proto i v pauze musí fungovat ukončení. Metody nemusí nic vracet. Každá instance má vlastní stav.

## Časovač, životy a nový začátek

Další úkoly oddělují součásti, které brzy využije hra. Casovac hlásí vypršení jen v jednom kroku, nikoli v každém dalším snímku. Zivoty nikdy neklesnou pod nulu a restart obnoví výchozí počet. Rezimy mají výslovnou tabulku přechodů menu/hra/pauza/konec. Nezaměňujte vstup Enter s pokynem „vždy začni znovu“, jeho význam závisí na stavu.

NovaHra dostane funkci tvorba. Při konstrukci i restartu ji zavolá a převezme novou skupinu, starý svět přitom nevyprazdňuje. Předání funkce bez závorek dovolí vytvořit svět až v okamžiku, kdy jej hra potřebuje. Díky tomu můžeme snadno vyměnit počáteční sestavu a otestovat počet vytvoření.

Možné řešení každého úkolu je pod zadáním. Zkuste si ještě před odkrytím říct, co má udělat druhé P, opakovaný QUIT nebo krok časovače po jeho vypršení. Tím máte základ pro další kapitolu: hratelné Meteority se smyčkou, vstupem, životy a restartem.
