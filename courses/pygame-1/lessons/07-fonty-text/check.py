import ast
from dilna_check import check
c = check()
c.uses_call("Font", "Vytvořte písmo: pygame.font.Font(None, velikost).")
c.uses_call("render", "Text vyrobte metodou font.render(...).")
promenne = {t.id for n in ast.walk(c.tree) if isinstance(n, ast.Assign) for t in n.targets if isinstance(t, ast.Name)} if c.tree else set()
c.add("Existuje proměnná skore", "skore" in promenne, "Uložte skóre do proměnné skore.")
c.add("Text skóre je sestaven f-řetězcem", c.tree is not None and any(isinstance(n, ast.JoinedStr) for n in ast.walk(c.tree)), "Použijte f-řetězec: f\"Skóre: {skore}\".")
ZLUTA = (255, 220, 0)
BILA = (255, 255, 255)
r = c.pygame_run(frames=3, pixels=[(5, 5)], colors=[ZLUTA, BILA, ZLUTA + (0, 30, 400, 40), BILA + (0, 165, 400, 35), ZLUTA + (0, 0, 200, 100), ZLUTA + (200, 0, 200, 100), BILA + (0, 140, 200, 60), BILA + (200, 140, 200, 60), BILA + (0, 0, 400, 100)])
if c.pg_no_error(r):
    c.add("Okno má velikost 400 × 200", r.size == [400, 200], f"Okno má velikost {r.size}.")
    c.add("Pozadí je (0, 0, 40)", r.pixel((5, 5)) == (0, 0, 40), f"V bodě (5, 5) je {r.pixel((5, 5))}.")
    c.add("Je vykreslen text „Sběratel hvězd“", r.rendered("Sběratel hvězd"), "Nadpis má znít přesně: Sběratel hvězd.")
    c.add("Je vykreslen text „Skóre: 0“", r.rendered("Skóre: 0"), "Text má znít přesně: Skóre: 0.")
    vlevo, vpravo = r.color_count(ZLUTA, region=(0, 0, 200, 100)), r.color_count(ZLUTA, region=(200, 0, 200, 100))
    c.add("Nadpis je žlutý a nahoře", vlevo > 40 and vpravo > 40, f"Žlutých bodů v horní polovině okna: vlevo {vlevo}, vpravo {vpravo}.")
    c.add("Nadpis je vodorovně vystředěný", vlevo > 40 and vpravo > 40 and 0.5 <= vlevo / vpravo <= 2.0,
          f"Žlutých bodů vlevo je {vlevo}, vpravo {vpravo}; nadpis má být uprostřed (get_rect(center=(200, 50))).")
    zl, bi = r.color_count(ZLUTA), r.color_count(BILA)
    c.add("Nadpis je ve výšce kolem y = 50", zl > 0 and r.color_count(ZLUTA, region=(0, 30, 400, 40)) == zl, "Střed nadpisu má být v bodě (200, 50): get_rect(center=(200, 50)).")
    c.add("Nadpis má velikost písma 48", 1650 <= zl <= 2050, f"Žlutých bodů je {zl} (čekáme zhruba 1850). Použijte pygame.font.Font(None, 48).")
    c.add("Skóre je dole u spodního okraje", bi > 0 and r.color_count(BILA, region=(0, 165, 400, 35)) == bi, "Levý dolní roh skóre má být v bodě (10, 190): get_rect(bottomleft=(10, 190)).")
    c.add("Skóre má velikost písma 32", 330 <= bi <= 400, f"Bílých bodů je {bi} (čekáme zhruba 360). Použijte pygame.font.Font(None, 32).")
    dole = r.color_count(BILA, region=(0, 140, 200, 60))
    c.add("Skóre je bílé v levém dolním rohu", dole > 30 and r.color_count(BILA, region=(200, 140, 200, 60)) == 0,
          f"Bílých bodů vlevo dole je {dole}. Levý dolní roh textu má být v bodě (10, 190).")
c.done()
