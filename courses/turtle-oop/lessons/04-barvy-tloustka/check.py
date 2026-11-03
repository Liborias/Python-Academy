from dilna_check import check
import ast
import math
c = check()
near = lambda a, b, t=1.0: abs(a - b) <= t
c.uses_call("bgcolor", "Nastavte pozadí: turtle.bgcolor(\"black\").")
c.uses_call("colormode", "Pro barvu trojicí čísel přepněte turtle.colormode(255).")
r = c.turtle_run()
if c.turtle_no_error(r):
    c.add("Program končí příkazem turtle.done()", r.mainloop, "Na konec přidejte turtle.done(), aby okno zůstalo otevřené.")
    c.add("Pozadí je černé", r.bgcolor == "black", f"Pozadí má být black, ale je {r.bgcolor!r}.")
    def cara(y):
        return [s for s in r.segments if near(s[1], y, 0.5) and near(s[3], y, 0.5)]
    for y, barvy, sirka, nazev in ((0, ("red",), 2, "červená"), (-30, ("#00ff00", "green"), 4, "zelená"), (-60, ("#ffa500", "orange"), 6, "oranžová")):
        s = cara(y)
        xs = [x for g in s for x in (g[0], g[2])]
        c.add(f"Čára {nazev} je na y = {y}, od x = -100 do 100", bool(s) and near(min(xs), -100) and near(max(xs), 100) and near(sum(abs(g[2] - g[0]) for g in s), 200),
              f"Čára na výšce y = {y} má začínat v x = -100 a mít délku 200.")
        if s:
            c.add(f"Čára {nazev}: barva a tloušťka", {g[4] for g in s} <= set(barvy) and {g[5] for g in s} == {sirka},
                  f"Čekáme barvu {barvy[0]} a tloušťku {sirka}, ale je {sorted({g[4] for g in s})} a {sorted({g[5] for g in s})}.")
    c.add("Nakreslily se jen tři čáry (žádné čáry navíc)", all(any(near(g[1], y, 0.5) and near(g[3], y, 0.5) for y in (0, -30, -60)) for g in r.segments),
          "Přesun mezi čárami dělejte se zdviženým perem, ať nevznikají čáry navíc.")
c.done()
