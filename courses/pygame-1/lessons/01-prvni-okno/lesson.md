## Co je pygame

**pygame** je knihovna pro tvorbu her. Umí otevřít okno, kreslit do něj, přehrávat zvuky a číst klávesnici a myš. Používáme její moderní verzi **pygame-ce**; v kódu se píše stále `import pygame`.

Instalace je součástí přípravy prostředí (`python tools/setup_env.py --courses pygame-1`). Tlačítko **Spustit** pak u této lekce otevře skutečné okno na vašem počítači.

## Pět kroků k oknu

```python
import pygame

pygame.init()                                       # 1. zapne pygame
screen = pygame.display.set_mode((400, 300))        # 2. otevře okno 400 × 300 bodů
pygame.display.set_caption("Moje první okno")       # 3. nápis v horní liště okna
screen.fill((135, 206, 235))                        # 4. vybarví celé okno
pygame.display.flip()                               # 5. ukáže nakreslené na obrazovce
```

- `set_mode((šířka, výška))` dostává **dvojici** (tuple), proto dvoje závorky. Vrací plochu `screen`, na kterou se kreslí.
- Barva je trojice čísel 0 až 255 pro **červenou, zelenou a modrou** (RGB). `(135, 206, 235)` je světle modrá.
- Kreslení probíhá „v zákulisí“. Teprve `pygame.display.flip()` nakreslený obrázek zobrazí.

## Aby okno nezmizelo

Program po posledním řádku skončí a okno zmizí. Do konce proto přidáme čekání a úklid:

```python
pygame.time.wait(3000)      # počká 3000 milisekund = 3 sekundy
pygame.quit()               # uklidí a vypne pygame
```

V další lekci okno udržíme otevřené pomocí **herní smyčky**, jak to dělají skutečné hry.

## Váš úkol

Napište program, který otevře okno **400 × 300** s titulkem **Moje první okno**, vyplní ho světle modrou barvou `(135, 206, 235)`, zobrazí ho (`flip`), 3 sekundy počká a pak se ukončí.