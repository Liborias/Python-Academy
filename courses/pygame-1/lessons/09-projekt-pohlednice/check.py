import ast
from dilna_check import check
c = check()
promenne = {t.id: n for n in ast.walk(c.tree) if isinstance(n, ast.Assign) for t in n.targets if isinstance(t, ast.Name)} if c.tree else {}
if c.tree:
    promenne.update({n.target.id: n for n in ast.walk(c.tree) if isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name) and n.value is not None})
c.add("Existuje seznam HVEZDY", "HVEZDY" in promenne and isinstance(promenne["HVEZDY"].value, ast.List) and len(promenne["HVEZDY"].value.elts) == 5, "Uložte polohy hvězd do seznamu HVEZDY.")
c.add("Hvězdy se kreslí cyklem for přes seznam HVEZDY", c.tree is not None and any(isinstance(n, ast.For) and isinstance(n.iter, ast.Name) and n.iter.id == "HVEZDY" for n in ast.walk(c.tree)),
      "Projděte seznam HVEZDY cyklem: for pozice in HVEZDY:.")
HV = [(50, 60), (120, 100), (300, 70), (350, 150), (80, 200)]
body = {f"hvězda {i + 1}": ((x + 16, y + 16), (255, 220, 0)) for i, (x, y) in enumerate(HV)}
body.update({f"horní špička hvězdy {i + 1}": ((x + 16, y + 4), (255, 220, 0)) for i, (x, y) in enumerate(HV)})
body["planeta"] = ((330, 230), (200, 60, 60))
body["raketa"] = ((200, 180), (80, 160, 255))
body["okraj planety"] = ((330 + 38, 230), (200, 60, 60))
body["mimo planetu"] = ((330 + 45, 230), (10, 10, 40))
body["okraj planety vpravo"] = ((330 + 39, 230), (200, 60, 60))
body["okraj planety nahoře"] = ((330, 230 - 39), (200, 60, 60))
body["mimo planetu nahoře"] = ((330, 230 - 42), (10, 10, 40))
body["okraj planety vlevo"] = ((330 - 39, 230), (200, 60, 60))
body["mimo planetu vlevo"] = ((330 - 42, 230), (10, 10, 40))
body["hrot rakety"] = ((200, 150), (200, 40, 40))
body["nad hrotem rakety"] = ((200, 149), (10, 10, 40))
body["pozadí"] = ((5, 290), (10, 10, 40))
BILA = (255, 255, 255)
r = c.pygame_run(frames=3, pixels=[p for p, _ in body.values()], colors=[BILA, BILA + (0, 0, 200, 50), BILA + (200, 0, 200, 50)])
if c.pg_no_error(r):
    c.add("Okno má velikost 400 × 300", r.size == [400, 300], f"Okno má velikost {r.size}.")
    c.add("Titulek je „Pohlednice“", r.caption == "Pohlednice", f"Titulek je {r.caption!r}.")
    for jmeno, (bod, barva) in body.items():
        c.add(f"Správně: {jmeno}", r.pixel(bod) == barva, f"V bodě {bod} je {r.pixel(bod)}, čekáme {barva}.")
    c.add("Obrázky se načítají jen jednou", len(r.images) == 2, f"Za 3 snímky se načítalo {len(r.images)} obrázků (čekáme 2: hvězda a raketa).")
    c.add("Nadpis má velikost písma 40", 1100 <= r.color_count(BILA) <= 1400, f"Bílých bodů je {r.color_count(BILA)} (čekáme zhruba 1250). Použijte pygame.font.Font(None, 40).")
    c.add("Je vykreslen nadpis „Pozdrav z kosmu“", r.rendered("Pozdrav z kosmu"), "Nadpis má znít přesně: Pozdrav z kosmu.")
    vl, vp = r.color_count(BILA, region=(0, 0, 200, 50)), r.color_count(BILA, region=(200, 0, 200, 50))
    c.add("Nadpis je bílý a vystředěný nahoře", vl > 40 and vp > 40 and 0.5 <= vl / vp <= 2.0, f"Bílých bodů nahoře: vlevo {vl}, vpravo {vp}.")
c.done()
