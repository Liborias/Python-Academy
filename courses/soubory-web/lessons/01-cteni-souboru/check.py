from dilna_check import check
c = check()
c.utf8()
ns = c.load()
if ns is not None:
    with open("cizi1.txt", "w", encoding="utf-8") as f:
        f.write("Příliš žluťoučký kůň\núpěl ďábelské ódy.\n")
    with open("cizi2.txt", "w", encoding="utf-8") as f:
        f.write("")
    c.returns(ns, "nacti", ("zvirata.txt",), "pes\nkocka\nkralik\nzelva\n")
    c.returns(ns, "nacti", ("cizi1.txt",), "Příliš žluťoučký kůň\núpěl ďábelské ódy.\n")
    c.returns(ns, "nacti", ("cizi2.txt",), "")
    c.returns(ns, "pocet_znaku", ("zvirata.txt",), 23)
    c.returns(ns, "pocet_znaku", ("cizi1.txt",), 40)
    c.returns(ns, "pocet_znaku", ("cizi2.txt",), 0)
    c.returns(ns, "slov_v_souboru", ("zvirata.txt",), 4)
    c.returns(ns, "slov_v_souboru", ("cizi1.txt",), 6)
    c.returns(ns, "slov_v_souboru", ("cizi2.txt",), 0)
c.done()
