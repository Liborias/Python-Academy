from dilna_check import check
c = check()
ns = c.load()
if ns is not None:
    c.returns(ns, "cena", ({"mleko": 25, "chleba": 40}, "chleba"), 40)
    c.returns(ns, "cena", ({"mleko": 25, "chleba": 40}, "sul"), 0)
    c.returns(ns, "cena", ({}, "x"), 0)
    c.returns(ns, "celkem", ({"a": 10, "b": 5, "c": 7},), 22)
    c.returns(ns, "celkem", ({},), 0)
    c.returns(ns, "drahe", ({"mleko": 25, "chleba": 40, "maslo": 60}, 30), ["chleba", "maslo"])
    c.returns(ns, "drahe", ({"mleko": 25, "chleba": 40}, 40), [])
    c.returns(ns, "drahe", ({"a": 1, "b": 2}, 0), ["a", "b"])
    c.returns(ns, "drahe", ({"zeta": 50, "alfa": 60, "mid": 5}, 10), ["zeta", "alfa"])
c.done()
