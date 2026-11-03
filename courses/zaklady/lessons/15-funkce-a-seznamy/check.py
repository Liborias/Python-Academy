from dilna_check import check
c = check()
ns = c.load()
if ns is not None:
    c.returns(ns, "zdvojnasob", ([1, 2, 3],), [2, 4, 6])
    c.returns(ns, "zdvojnasob", ([],), [])
    c.returns(ns, "zdvojnasob", ([-1, 0.5],), [-2, 1.0])
    c.returns(ns, "jen_kladna", ([-1, 2, 0, 3],), [2, 3])
    c.returns(ns, "jen_kladna", ([],), [])
    c.returns(ns, "jen_kladna", ([-5, -6],), [])
    for jmeno in ("zdvojnasob", "jen_kladna"):
        f = ns.get(jmeno)
        if callable(f):
            zdroj = [3, -1, 0, 7]
            kopie = list(zdroj)
            try:
                f(zdroj)
            except Exception:
                pass
            c.add(f"{jmeno} nezměnila původní seznam", zdroj == kopie, f"Funkce {jmeno} nesmí měnit předaný seznam. Vytvořte nový seznam a vraťte ten.")
c.done()
