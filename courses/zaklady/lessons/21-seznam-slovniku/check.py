from dilna_check import check
c = check()
ns = c.load()
S1 = [{"jmeno": "Eva", "body": 82}, {"jmeno": "Petr", "body": 54}, {"jmeno": "Jana", "body": 91}]
S2 = [{"jmeno": "Karel", "body": 10}, {"jmeno": "Lenka", "body": 40}]
if ns is not None:
    c.returns(ns, "nejlepsi", (S1,), "Jana")
    c.returns(ns, "nejlepsi", (S2,), "Lenka")
    c.returns(ns, "nejlepsi", ([{"jmeno": "Sám", "body": 1}],), "Sám")
    c.returns(ns, "prumer_bodu", (S1,), 227 / 3)
    c.returns(ns, "prumer_bodu", (S2,), 25.0)
    c.returns(ns, "uspesni", (S1, 60), ["Eva", "Jana"])
    c.returns(ns, "uspesni", (S1, 82), ["Eva", "Jana"])
    c.returns(ns, "uspesni", (S2, 100), [])
    c.returns(ns, "pridej_studenta", ([{"jmeno": "A", "body": 1}], "B", 2), [{"jmeno": "A", "body": 1}, {"jmeno": "B", "body": 2}])
    c.returns(ns, "pridej_studenta", ([], "Z", 9), [{"jmeno": "Z", "body": 9}])
c.done()
