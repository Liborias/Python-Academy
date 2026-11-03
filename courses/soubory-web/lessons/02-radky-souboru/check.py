from dilna_check import check
c = check()
c.utf8()
ns = c.load()
if ns is not None:
    def zapis(nazev, text):
        with open(nazev, "w", encoding="utf-8") as f:
            f.write(text)
    zapis("a.txt", "-4\n100\n\n  8  \n")
    zapis("b.txt", "")
    zapis("c.txt", "kratky\ndlouhy radek\nstredni\nstejna delka\n")
    zapis("d.txt", "jediny")
    zapis("e.txt", "po 5\nut -2\nst 0")
    c.returns(ns, "nacti_cisla", ("cisla.txt",), [12, 7, 30, 5])
    c.returns(ns, "nacti_cisla", ("a.txt",), [-4, 100, 8])
    c.returns(ns, "nacti_cisla", ("b.txt",), [])
    c.returns(ns, "nejdelsi_radek", ("c.txt",), "dlouhy radek")
    c.returns(ns, "nejdelsi_radek", ("d.txt",), "jediny")
    c.returns(ns, "nejdelsi_radek", ("b.txt",), "")
    c.returns(ns, "nejdelsi_radek", ("pocasi.txt",), "pondeli 18")
    c.returns(ns, "teploty", ("pocasi.txt",), {"pondeli": 18, "utery": 21, "streda": 15, "ctvrtek": 19})
    c.returns(ns, "teploty", ("e.txt",), {"po": 5, "ut": -2, "st": 0})
    c.returns(ns, "teploty", ("b.txt",), {})
c.done()
