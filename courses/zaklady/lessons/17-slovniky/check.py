from dilna_check import check
c = check()
ns = c.load()
if ns is not None:
    c.returns(ns, "vytvor_kontakt", ("Eva", "777111222"), {"jmeno": "Eva", "telefon": "777111222"})
    c.returns(ns, "vytvor_kontakt", ("Petr", "602333444"), {"jmeno": "Petr", "telefon": "602333444"})
    c.returns(ns, "zmen_telefon", ({"jmeno": "Eva", "telefon": "1"}, "999"), {"jmeno": "Eva", "telefon": "999"})
    c.returns(ns, "zmen_telefon", ({"jmeno": "Jan", "telefon": "5", "vek": 20}, "6"), {"jmeno": "Jan", "telefon": "6", "vek": 20})
    c.returns(ns, "pridej_email", ({"jmeno": "Eva", "telefon": "1"}, "e@x.cz"), {"jmeno": "Eva", "telefon": "1", "email": "e@x.cz"})
    c.returns(ns, "pridej_email", ({}, "a@b.cz"), {"email": "a@b.cz"})
c.done()
