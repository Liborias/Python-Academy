from dilna_check import check
c = check()
ns = c.load()
if ns is not None:
    c.returns(ns, 'rozloz_cas', (0,), '0:00:00')
    c.returns(ns, 'rozloz_cas', (59,), '0:00:59')
    c.returns(ns, 'rozloz_cas', (60,), '0:01:00')
    c.returns(ns, 'rozloz_cas', (3600,), '1:00:00')
    c.returns(ns, 'rozloz_cas', (3725,), '1:02:05')
    c.returns(ns, 'rozloz_cas', (86399,), '23:59:59')
    c.returns(ns, 'rozloz_cas', (90000,), '25:00:00')
    c.returns(ns, 'na_cislo', ('3,5',), 3.5)
    c.returns(ns, 'na_cislo', (' 7 ',), 7.0)
    c.returns(ns, 'na_cislo', ('2.25',), 2.25)
    c.returns(ns, 'na_cislo', ('abc',), None)
    c.returns(ns, 'na_cislo', ('',), None)
    c.returns(ns, 'je_cele', (5,), True)
    c.returns(ns, 'je_cele', (5.0,), True)
    c.returns(ns, 'je_cele', (5.5,), False)
    c.returns(ns, 'je_cele', (0,), True)
    c.returns(ns, 'je_cele', (-2.0,), True)
    c.returns(ns, 'je_cele', (0.30000000000000004,), False)
    r = ns["na_cislo"]("3,5") if callable(ns.get("na_cislo")) else None
    c.add("na_cislo vrací typ float", isinstance(r, float), f"Vrácená hodnota má typ {type(r).__name__}, má to být float.")
    for vstup in (" 7 ", "2", "0,25"):
        v = ns["na_cislo"](vstup) if callable(ns.get("na_cislo")) else None
        c.add(f"na_cislo({vstup!r}) vrací typ float", isinstance(v, float), f"Vrácená hodnota má typ {type(v).__name__}, má to být float (i pro celé číslo, například 7.0).")
    t = ns["rozloz_cas"](3725) if callable(ns.get("rozloz_cas")) else None
    c.add("rozloz_cas vrací text", isinstance(t, str), "Funkce má vracet text, ne tisknout.")
c.done()
