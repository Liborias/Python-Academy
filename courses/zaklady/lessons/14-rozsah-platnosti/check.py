import ast
from dilna_check import check
c = check()
ns = c.load()
if ns is not None:
    c.add("Konstanta DPH je 0.21", ns.get("DPH") == 0.21, "Na začátku souboru vytvořte DPH = 0.21.")
    f = ns.get("pridej_dph")
    if callable(f):
        for cena, ocek in ((100, 121.0), (0, 0.0), (50, 60.5)):
            try:
                got = f(cena)
                ok = isinstance(got, (int, float)) and abs(got - ocek) < 1e-9
            except Exception as e:
                got, ok = repr(e), False
            c.add(f"pridej_dph({cena}) vrátí {ocek}", ok, f"Funkce vrátila {got!r}, očekávám {ocek}.")
        c.add("Konstanta DPH zůstala 0.21", ns.get("DPH") == 0.21, "Funkce nesmí měnit globální konstantu DPH.")
    else:
        c.add("Funkce pridej_dph", False, "Chybí funkce pridej_dph(cena).")
    for s, o in (([1, 2, 3], 6), ([], 0), ([-1, 1], 0), ([2.5, 2.5], 5.0)):
        c.returns(ns, "soucet_seznamu", (list(s),), o)
    zdroj = [4, 5, 6]
    kopie = list(zdroj)
    if callable(ns.get("soucet_seznamu")):
        ns["soucet_seznamu"](zdroj)
        c.add("Funkce seznam nezměnila", zdroj == kopie, "Funkce nesmí seznam měnit (žádné pop, remove ani append).")
fs = c.function("soucet_seznamu")
c.add("soucet_seznamu nepoužívá sum()", not (fs and c.calls_in(fs, "sum")), "V soucet_seznamu nepoužívejte sum(), sečtěte čísla cyklem.")
c.add("soucet_seznamu používá cyklus", bool(fs and any(isinstance(n, (ast.For, ast.While)) for n in ast.walk(fs))), "Použijte cyklus for nebo while.")
fd = c.function("pridej_dph")
c.add("pridej_dph používá konstantu DPH", bool(fd and any(isinstance(n, ast.Name) and n.id == "DPH" for n in ast.walk(fd))), "Ve funkci použijte konstantu DPH, nepište 0.21 ani 1.21 natvrdo.")
c.done()
