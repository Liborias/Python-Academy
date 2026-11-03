import ast
from dilna_check import check
c = check()
konstanty = {t.id for n in ast.walk(c.tree) if isinstance(n, ast.Assign) for t in n.targets
             if isinstance(t, ast.Name) and t.id.isupper()} if c.tree else set()
c.add("Barvy jsou pojmenované konstanty MODRA, BILA, CERVENA", {"MODRA", "BILA", "CERVENA"} <= konstanty,
      "Přiřaďte barvy do proměnných MODRA, BILA a CERVENA (velkými písmeny).")
hodnoty = {}
for n in (ast.walk(c.tree) if c.tree else []):
    if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
        try:
            hodnoty[n.targets[0].id] = tuple(ast.literal_eval(n.value))
        except Exception:
            pass
c.add("Konstanty mají správné hodnoty", hodnoty.get("MODRA") == (0, 85, 164) and hodnoty.get("BILA") == (255, 255, 255) and hodnoty.get("CERVENA") == (239, 65, 53),
      "MODRA = (0, 85, 164), BILA = (255, 255, 255), CERVENA = (239, 65, 53).")
pouzito = {n.id for n in ast.walk(c.tree) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)} if c.tree else set()
c.add("Konstanty se při kreslení opravdu používají", {"MODRA", "BILA", "CERVENA"} <= pouzito,
      "Použijte konstanty MODRA, BILA a CERVENA v příkazech pro kreslení, ne přímo čísla.")
body = [(0, 0), (50, 100), (99, 199), (100, 0), (150, 100), (199, 199), (200, 0), (250, 100), (299, 199)]
r = c.pygame_run(frames=3, pixels=body)
if c.pg_no_error(r):
    c.add("Okno má velikost 300 × 200", r.size == [300, 200], f"Okno má velikost {r.size}.")
    for jmeno, barva, xs in (("modrý", (0, 85, 164), (0, 50, 99)), ("bílý", (255, 255, 255), (100, 150, 199)), ("červený", (239, 65, 53), (200, 250, 299))):
        spatne = [(x, y) for (x, y) in body if x in xs and r.pixel((x, y)) != barva]
        c.add(f"{jmeno.capitalize()} pruh je na místě", not spatne,
              f"V bodě {spatne[0] if spatne else ''} je barva {r.pixel(spatne[0]) if spatne else ''}, čekáme {barva}.")
c.done()
