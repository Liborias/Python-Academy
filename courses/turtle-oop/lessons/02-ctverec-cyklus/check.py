from dilna_check import check
import ast
import math
c = check()
near = lambda a, b, t=1.0: abs(a - b) <= t
c.uses_call("color|pencolor", "Nastavte barvu čáry: t.color(\"blue\").")
c.uses_call("pensize|width", "Nastavte tloušťku čáry: t.pensize(3).")
fwd = [n for n in ast.walk(c.tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr in ("forward", "fd")] if c.tree else []
c.add("Čtverec se kreslí cyklem for", c.tree is not None and any(isinstance(n, ast.For) for n in ast.walk(c.tree)) and len(fwd) == 1,
      "Použijte cyklus for a v něm jeden příkaz forward (nepište čtyři forward za sebou).")
r = c.turtle_run()
if c.turtle_no_error(r):
    c.add("Program končí příkazem turtle.done()", r.mainloop, "Na konec přidejte turtle.done(), aby okno zůstalo otevřené.")
    segs = r.segments
    c.add("Nakreslily se čtyři strany", len(segs) == 4, f"Počet nakreslených úseček je {len(segs)}, čekáme 4.")
    c.add("Strana má délku 80", segs and all(near(((s[2] - s[0]) ** 2 + (s[3] - s[1]) ** 2) ** 0.5, 80, 0.5) for s in segs), "Každá strana čtverce má mít délku 80.")
    box = r.bbox()
    c.add("Čtverec je zavřený a leží nad a vpravo od (0, 0)", box is not None and all(near(a, b) for a, b in zip(box, (0, 0, 80, 80))) and len(r.corners()) == 3,
          "Po čtyřech stranách a čtyřech zatáčkách o 90° se želva vrátí do bodu (0, 0).")
    c.add("Čára je modrá", r.colors() == {"blue"}, f"Barva čáry má být blue, ale je {sorted(r.colors())}.")
    c.add("Tloušťka čáry je 3", r.widths() == {3}, f"Tloušťka čáry má být 3, ale je {sorted(r.widths())}.")
c.done()
