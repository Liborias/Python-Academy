from dilna_check import check
c = check()
ns = c.load()
if ns is not None:
    c.returns(ns, "statistika", ([4, 8, 6, 2, 10],), (2, 10, 6.0))
    c.returns(ns, "statistika", ([5],), (5, 5, 5.0))
    c.returns(ns, "statistika", ([-3, 3],), (-3, 3, 0.0))
    f = ns.get("statistika")
    c.add("Funkce statistika má docstring", bool(callable(f) and (f.__doc__ or "").strip()),
          "Pod řádek def přidejte popis ve třech uvozovkách: \"\"\"Popis.\"\"\"")
    c.returns(ns, "vydel", (17, 5), (3, 2))
    c.returns(ns, "vydel", (10, 2), (5, 0))
    c.returns(ns, "vydel", (3, 7), (0, 3))
c.done()
