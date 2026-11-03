from dilna_check import check
c = check()
ns = c.load()
if ns is not None:
    c.returns(ns, "pozdrav", ("Eva",), "Ahoj, Eva!")
    c.returns(ns, "pozdrav", ("Petr",), "Ahoj, Petr!")
    c.returns(ns, "vek_za_rok", (30,), 31)
    c.returns(ns, "vek_za_rok", (0,), 1)
    c.returns(ns, "obsah_obdelniku", (3, 4), 12)
    c.returns(ns, "obsah_obdelniku", (5, 5), 25)
    c.returns(ns, "posledni", ([1, 2, 3],), 3)
    c.returns(ns, "posledni", (["a"],), "a")
    c.returns(ns, "posledni", (["x", "y", "z", "w"],), "w")
c.done()
