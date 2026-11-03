from dilna_check import check
import ast
import math
c = check()
near = lambda a, b, t=1.0: abs(a - b) <= t
c.uses_call("circle", "Kruhy kreslete příkazem t.circle(poloměr).")
c.uses_call("dot", "Oči nakreslete příkazem t.dot(6, \"black\").")
r = c.turtle_run()
if c.turtle_no_error(r):
    c.add("Program končí příkazem turtle.done()", r.mainloop, "Na konec přidejte turtle.done(), aby okno zůstalo otevřené.")
    def na_kruhu(stred, rad, uhly=range(0, 360, 30)):
        return all(r.covers((stred[0] + rad * math.cos(math.radians(a)), stred[1] + rad * math.sin(math.radians(a))), 1.5) for a in uhly)
    c.add("Spodní kruh má poloměr 60 a střed (0, -40)", na_kruhu((0, -40), 60), "Největší kruh začíná v (0, -100) a je nad tímto bodem: circle(60).")
    c.add("Prostřední kruh má poloměr 40 a střed (0, 60)", na_kruhu((0, 60), 40), "Prostřední kruh začíná v nejvyšším bodě spodního, v (0, 20): circle(40).")
    c.add("Horní kruh má poloměr 25 a střed (0, 125)", na_kruhu((0, 125), 25), "Horní kruh začíná v nejvyšším bodě prostředního, v (0, 100): circle(25).")
    oci = sorted((round(d[0]), round(d[1]), d[2], d[3]) for d in (r.dots or []))
    c.add("Dvě černé oči v bodech (-8, 130) a (8, 130)", oci == [(-8, 130, 6, "black"), (8, 130, 6, "black")], f"Tečky: {oci}. Čekáme dvě černé tečky velikosti 6 v bodech (-8, 130) a (8, 130).")
    c.add("Úsměv je spodní půlkruh se středem (0, 115)", na_kruhu((0, 115), 10, range(180, 361, 30)) and not r.covers((0, 125), 0.5),
          "Úsměv: setheading(270) a circle(10, 180) z bodu (-10, 115). Vede přes bod (0, 105) a horní půlka kruhu se nekreslí.")
    c.add("Mezi částmi se nekreslí", near(r.length(), 2 * 3.14159 * (60 + 40 + 25) + 3.14159 * 10, 25), f"Délka čar má odpovídat třem kruhům a půlkruhu (asi 816), ale je {r.length():.0f}.")
c.done()
