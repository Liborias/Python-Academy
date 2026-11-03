from dilna_check import check
c = check()
ns = c.load()
if ns is not None:
    for args, ocek in ((("a", 3), "d"), (("z", 1), "a"), (("Z", 1), "A"), (("m", 0), "m"), (("b", -3), "y"),
                       (("a", 29), "d"), (("!", 5), "!"), ((" ", 2), " "), (("č", 4), "č"), (("7", 3), "7")):
        c.returns(ns, "posun_pismeno", args, ocek)
    c.returns(ns, "zasifruj", ("ahoj", 3), "dkrm")
    c.returns(ns, "zasifruj", ("Ahoj, svete!", 1), "Bipk, twfuf!")
    c.returns(ns, "zasifruj", ("xyz", 3), "abc")
    c.returns(ns, "zasifruj", ("", 5), "")
    c.returns(ns, "desifruj", ("dkrm", 3), "ahoj")
    c.returns(ns, "desifruj", ("Bipk, twfuf!", 1), "Ahoj, svete!")
    c.returns(ns, "desifruj", ("abc", 3), "xyz")
    for t in ("Python je skvely", "Zebra, Zirafa a Slon."):
        for p in (1, 13, 25):
            ok, s = c.call(ns, "zasifruj", (t, p))
            ok2, d = c.call(ns, "desifruj", (s, p)) if ok else (False, None)
            c.add(f"desifruj(zasifruj({t!r}, {p}), {p}) vrátí původní text", ok and ok2 and d == t,
                  "Šifrování a dešifrování musí být navzájem opačné.")
    c.returns(ns, "rozlam", ("dkrm", "ahoj"), 3)
    c.returns(ns, "rozlam", ("Bipk twfuf", "svete"), 1)
    c.returns(ns, "rozlam", ("dkrm", "slon"), None)
    c.returns(ns, "rozlam", ("dkrm", "o"), 3)
    c.returns(ns, "rozlam", ("Dkrm", "ahoj"), 3)
    c.returns(ns, "rozlam", ("ahoj", "ahoj"), None)
    c.returns(ns, "rozlam", ("zgni", "ahoj"), 25)
    c.returns(ns, "rozlam", ("ipwr", "ahoj"), 8)
c.done()
