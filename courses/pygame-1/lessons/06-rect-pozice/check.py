import re
from dilna_check import check
c = check()
c.uses_call("get_rect", "Polohu rakety určete obdélníkem: raketa.get_rect(...).")
BAREVNE_OKNO = (80, 160, 255)     # střed obrázku raketa.png
stredy = {"vlevo nahoře": (42, 42), "vpravo nahoře": (358, 42), "vlevo dole": (42, 258), "vpravo dole": (358, 258), "uprostřed": (200, 150)}
hrany = []        # hrot a boky rakety (uvnitř a těsně vně), souřadnice od levého horního rohu = střed - (32, 32)
for sx, sy in stredy.values():
    tx, ty = sx - 32, sy - 32
    hrany += [(tx + 32, ty + 2, (200, 40, 40)), (tx + 32, ty + 1, (20, 20, 60)), (tx + 6, ty + 62, (255, 140, 0)), (tx + 5, ty + 62, (20, 20, 60)),
              (tx + 58, ty + 62, (255, 140, 0)), (tx + 59, ty + 62, (20, 20, 60))]
r = c.pygame_run(frames=3, pixels=list(stredy.values()) + [(200, 40), (5, 5)] + [(x, y) for x, y, _ in hrany])
if c.pg_no_error(r):
    c.add("Okno má velikost 400 × 300", r.size == [400, 300], f"Okno má velikost {r.size}.")
    for jmeno, bod in stredy.items():
        c.add(f"Raketa {jmeno}", r.pixel(bod) == BAREVNE_OKNO, f"Okénko rakety má být v bodě {bod}, ale tam je {r.pixel(bod)}.")
    c.add("Rakety jsou přesně na svých místech", all(r.pixel((x, y)) == bar for x, y, bar in hrany), "Některá raketa je posunutá o pár bodů: použijte přesně zadané středy a rohy.")
    c.add("Pozadí je (20, 20, 60)", r.pixel((200, 40)) == (20, 20, 60) and r.pixel((5, 5)) == (20, 20, 60), "Pozadí okna má být (20, 20, 60).")
    c.add("Obrázek se načítá jednou", len(r.images) == 1, f"Obrázek se načetl {len(r.images)}×. Načtěte ho jednou před smyčkou.")
    c.add("Vypsán střed prostřední rakety", re.search(r"200\D+150", r.out) is not None, f"Program vypsal: {r.out.strip()!r}. Čekáme (200, 150).")
c.done()
