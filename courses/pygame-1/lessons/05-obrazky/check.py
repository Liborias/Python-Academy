import ast
from dilna_check import check
c = check()
c.uses_call("load", "Načtěte obrázky pomocí pygame.image.load(...).")
c.uses_call("convert_alpha", "Přidejte .convert_alpha() za načtení obrázku.")
c.add("convert_alpha() je u obou obrázků", c.tree is not None and sum(isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "convert_alpha" for n in ast.walk(c.tree)) >= 2,
      "Zavolejte .convert_alpha() u rakety i u hvězdy.")
c.uses_call("blit", "Vykreslete obrázky metodou screen.blit(...).")
# hrany obrázků: (bod uvnitř, bod těsně vně), souřadnice vzhledem k levému hornímu rohu
RAKETA_HRANY = [((32, 2), (200, 40, 40), (32, 1)), ((6, 62), (255, 140, 0), (5, 62)), ((58, 62), (255, 140, 0), (59, 62))]
HVEZDA_HRANY = [((16, 1), (255, 220, 0), (16, 0)), ((1, 11), (255, 220, 0), (0, 11)), ((30, 11), (255, 220, 0), (31, 11))]
body = [(200, 150), (168, 118), (232, 182), (50, 50), (66, 66), (5, 5)]
for (dx, dy), _, (ex, ey) in RAKETA_HRANY:
    body += [(168 + dx, 118 + dy), (168 + ex, 118 + ey)]
for (dx, dy), _, (ex, ey) in HVEZDA_HRANY:
    body += [(50 + dx, 50 + dy), (50 + ex, 50 + ey)]
r = c.pygame_run(frames=3, pixels=body)
if c.pg_no_error(r):
    c.add("Okno má velikost 400 × 300", r.size == [400, 300], f"Okno má velikost {r.size}.")
    c.add("Načetla se raketa.png", any(i.endswith("raketa.png") for i in r.images), "Načtěte soubor raketa.png.")
    c.add("Načetla se hvezda.png", any(i.endswith("hvezda.png") for i in r.images), "Načtěte soubor hvezda.png.")
    c.add("Obrázky se načítají jen jednou (před smyčkou)", len(r.images) == 2, f"Za 3 snímky se načítalo {len(r.images)}× (čekáme 2). Načtěte obrázky před smyčkou.")
    c.add("Střed rakety je v bodě (200, 150)", r.pixel((200, 150)) == (80, 160, 255), f"V bodě (200, 150) je {r.pixel((200, 150))}; okénko rakety má být přesně uprostřed.")
    c.add("Roh rakety je průhledný", r.pixel((168, 118)) == (20, 20, 60), f"Roh obrázku má být průhledný (použijte convert_alpha) a vidět má být pozadí (20, 20, 60), ale je tam {r.pixel((168, 118))}.")
    c.add("Hvězda je na místě (levý horní roh v (50, 50))", r.pixel((66, 66)) == (255, 220, 0), f"V bodě (66, 66) je {r.pixel((66, 66))}, čekáme žlutou.")
    c.add("Roh hvězdy je průhledný", r.pixel((50, 50)) == (20, 20, 60), f"Roh obrázku hvězdy má být průhledný (nepoužívejte .convert(), ale .convert_alpha()), ale je tam {r.pixel((50, 50))}.")
    hrany_ok = all(r.pixel((168 + dx, 118 + dy)) == bar and r.pixel((168 + ex, 118 + ey)) == (20, 20, 60) for (dx, dy), bar, (ex, ey) in RAKETA_HRANY)
    c.add("Raketa je přesně vystředěna na (200, 150)", hrany_ok, "Raketa je posunutá: její střed má být přesně v bodě (200, 150) (get_rect(center=(200, 150))).")
    hrany_ok = all(r.pixel((50 + dx, 50 + dy)) == bar and r.pixel((50 + ex, 50 + ey)) == (20, 20, 60) for (dx, dy), bar, (ex, ey) in HVEZDA_HRANY)
    c.add("Hvězda je přesně na (50, 50)", hrany_ok, "Hvězda je posunutá: její levý horní roh má být přesně v bodě (50, 50).")
    c.add("Pozadí je tmavě modré (20, 20, 60)", r.pixel((5, 5)) == (20, 20, 60), f"V bodě (5, 5) je {r.pixel((5, 5))}.")
c.done()
