from dilna_check import check
import ast
import math
c = check()
near = lambda a, b, t=1.0: abs(a - b) <= t
c.uses_call("Turtle", "Vytvořte želvu: t = turtle.Turtle().")
c.uses_call("forward|fd", "Želva jde dopředu příkazem forward.")
c.uses_call("left|lt", "Otočte želvu doleva příkazem left.")
r = c.turtle_run()
if c.turtle_no_error(r):
    c.add("Program končí příkazem turtle.done()", r.mainloop, "Na konec přidejte turtle.done(), aby okno zůstalo otevřené.")
    c.add("Čára vede z (0, 0) o 150 doprava", r.covers((0, 0)) and r.covers((75, 0)) and r.covers((150, 0)), "První čára má vést z bodu (0, 0) do bodu (150, 0).")
    c.add("Pak míří o 100 nahoru", r.covers((150, 50)) and r.covers((150, 100)), "Po otočce o 90° doleva jděte o 100 bodů nahoru, do bodu (150, 100).")
    box = r.bbox()
    c.add("Nic víc se nekreslí", box is not None and all(near(a, b) for a, b in zip(box, (0, 0, 150, 100))) and near(r.length(), 250),
          f"Obrázek má mít rozměr 150 × 100 a délku čar 250, ale délka čar je {r.length():.0f}.")
c.done()
