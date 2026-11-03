from dilna_check import check
c = check()
ns = c.load()
if ns is not None:
    c.returns(ns, "pocet_slov", ("to je to",), {"to": 2, "je": 1})
    c.returns(ns, "pocet_slov", ("Ahoj ahoj AHOJ svete",), {"ahoj": 3, "svete": 1})
    c.returns(ns, "pocet_slov", ("",), {})
    c.returns(ns, "nejcastejsi", ("a b a c b a",), "a")
    c.returns(ns, "nejcastejsi", ("Pes kocka KOCKA pes ptak",), "pes")
    c.returns(ns, "nejcastejsi", ("jedno",), "jedno")
c.done()
