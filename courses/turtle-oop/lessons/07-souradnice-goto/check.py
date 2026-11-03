from dilna_check import check
import ast
import math
c = check()
near = lambda a, b, t=1.0: abs(a - b) <= t
c.add("Body se procházejí cyklem for x, y in body", c.tree is not None and any(
    isinstance(n, ast.For) and isinstance(n.target, ast.Tuple) and len(n.target.elts) == 2 for n in ast.walk(c.tree)), "Použijte rozbalení dvojice: for x, y in body:")
r = c.turtle_run()
if c.turtle_no_error(r):
    c.add("Program končí příkazem turtle.done()", r.mainloop, "Na konec přidejte turtle.done(), aby okno zůstalo otevřené.")
    body = [(-100, -50), (-50, 50), (0, -50), (50, 50), (100, -50)]
    segs = r.segments
    c.add("Čára má čtyři úseky", len(segs) == 4, f"Úseků je {len(segs)}, čekáme 4 (mezi pěti body). Na první bod se přesuňte se zdviženým perem.")
    ok = len(segs) == 4 and all(near(s[0], a[0], 0.5) and near(s[1], a[1], 0.5) and near(s[2], b[0], 0.5) and near(s[3], b[1], 0.5) for s, a, b in zip(segs, body, body[1:]))
    c.add("Čára prochází body v daném pořadí", ok, "Úseky mají vést (-100, -50), (-50, 50), (0, -50), (50, 50), (100, -50).")
    c.add("Čára je červená a tlustá 3", r.colors() == {"red"} and r.widths() == {3}, f"Barvy čáry {sorted(r.colors())}, tloušťky {sorted(r.widths())}.")
    tecky = sorted({(round(d[0]), round(d[1]), d[2], d[3]) for d in (r.dots or [])})
    c.add("V každém bodě je modrá tečka velikosti 8", tecky == sorted((x, y, 8, "blue") for x, y in body), f"Tečky: {tecky}.")
c.done()
