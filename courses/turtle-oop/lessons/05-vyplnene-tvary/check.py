from dilna_check import check
import ast
import math
c = check()
near = lambda a, b, t=1.0: abs(a - b) <= t
c.uses_call("begin_fill", "Vyplňování začněte příkazem t.begin_fill().")
c.uses_call("end_fill", "Vyplňování ukončete příkazem t.end_fill().")
r = c.turtle_run()
if c.turtle_no_error(r):
    c.add("Program končí příkazem turtle.done()", r.mainloop, "Na konec přidejte turtle.done(), aby okno zůstalo otevřené.")
    c.add("Jsou dva vyplněné tvary", len(r.fills) == 2, f"Vyplněných tvarů je {len(r.fills)}, čekáme 2 (každý tvar má vlastní begin_fill a end_fill).")
    c.add("Zeď je žlutá a má plochu 100 × 100", near(r.fill_area("yellow"), 10000, 60), f"Plocha žluté výplně je {r.fill_area('yellow'):.0f}, čekáme 10000 (čtverec se stranou 100).")
    c.add("Střecha je červená a má plochu rovnostranného trojúhelníku", near(r.fill_area("red"), 4330, 60), f"Plocha červené výplně je {r.fill_area('red'):.0f}, čekáme 4330 (trojúhelník se stranou 100).")
    def ma(barva, bod):
        return any(f["color"] == barva and any(math.hypot(p[0] - bod[0], p[1] - bod[1]) < 1.5 for p in f["points"]) for f in r.fills)
    c.add("Zeď začíná v (0, 0) a sahá do (100, 100)", ma("yellow", (0, 0)) and ma("yellow", (100, 100)), "Čtverec má mít protilehlé rohy v bodech (0, 0) a (100, 100).")
    c.add("Střecha má vrchol v bodě (50, 186.6)", ma("red", (0, 100)) and ma("red", (100, 100)) and ma("red", (50, 186.6)), "Trojúhelník má stát na horní straně čtverce: rohy (0, 100), (100, 100) a (50, 186.6).")
    c.add("Čára je hnědá", r.colors() == {"brown"}, f"Čára má být brown, ale použité barvy čáry jsou {sorted(r.colors())}.")
    c.add("Mezi tvary se nekreslí", near(r.length(), 700, 1.0), f"Celková délka čar má být 700, ale je {r.length():.0f}.")
c.done()
