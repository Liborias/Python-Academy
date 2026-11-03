from dilna_check import check
import ast
import math
c = check()
near = lambda a, b, t=1.0: abs(a - b) <= t
fn = [n for n in ast.walk(c.tree) if isinstance(n, ast.FunctionDef) and n.name == "mnohouhelnik"] if c.tree else []
c.add("Existuje funkce mnohouhelnik se třemi parametry", bool(fn) and len(fn[0].args.args) == 3, "Napište def mnohouhelnik(t, strany, delka):")
volani = [n for n in ast.walk(c.tree) if isinstance(n, ast.Call) and getattr(n.func, "id", "") == "mnohouhelnik"] if c.tree else []
c.add("Funkce se volá", len(volani) >= 1, "Nakreslete oba tvary pomocí funkce mnohouhelnik.")
r = c.turtle_run()
if c.turtle_no_error(r):
    c.add("Program končí příkazem turtle.done()", r.mainloop, "Na konec přidejte turtle.done(), aby okno zůstalo otevřené.")
    s3 = 86.6025
    trojuhelnik = [(-150, 0), (-50, 0), (-100, s3), (-150, 0)]
    sest = [(50, 0), (100, 0), (125, 43.3013), (100, s3), (50, s3), (25, 43.3013), (50, 0)]
    def okraj(body):
        return all(r.covers(((a[0] + b[0]) / 2, (a[1] + b[1]) / 2), 1.0) for a, b in zip(body, body[1:]))
    c.add("Trojúhelník se stranou 100 začíná v (-150, 0)", okraj(trojuhelnik), "Středy všech tří stran trojúhelníku mají ležet na čáře. Zatáčka je 360 / 3 = 120°.")
    c.add("Šestiúhelník se stranou 50 začíná v (50, 0)", okraj(sest), "Středy všech šesti stran šestiúhelníku mají ležet na čáře. Zatáčka je 360 / 6 = 60°.")
    c.add("Mezi tvary se nekreslí", near(r.length(), 300 + 300, 1.0), f"Celková délka čar má být 600 (3 × 100 a 6 × 50), ale je {r.length():.0f}. Přesun udělejte se zdviženým perem.")
c.done()
