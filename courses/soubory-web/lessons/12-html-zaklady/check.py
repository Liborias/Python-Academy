from dilna_check import check
c = check()
ns = c.load()
if ns is not None:
    with open("stranka.html", encoding="utf-8") as f:
        S = f.read()
    c.returns(ns, "nadpis", (S,), "Zvířata v ZOO")
    c.returns(ns, "nadpis", ("<h1>Ahoj</h1><p>x</p>",), "Ahoj")
    c.returns(ns, "nadpis", ("<p>bez nadpisu</p>",), "")
    c.returns(ns, "nadpis", ("<h2>jiný</h2><h1>správný</h1>",), "správný")
    c.returns(ns, "pocet_polozek", (S,), 3)
    c.returns(ns, "pocet_polozek", ("<ul><li>a</li><li>b</li></ul><li>c</li>",), 3)
    c.returns(ns, "pocet_polozek", ("<p>nic</p>",), 0)
    c.returns(ns, "pocet_polozek", ('<link rel="x"><ul><li>a</li></ul>',), 1)
    c.returns(ns, "odkazy", (S,), ["https://example.com/vstupenky", "mapa.html"])
    c.returns(ns, "odkazy", ('<a href="x">1</a> text <a href="y z">2</a>',), ["x", "y z"])
    c.returns(ns, "odkazy", ('<a href="jediny">1</a>',), ["jediny"])
    c.returns(ns, "odkazy", ("<p>bez odkazů</p>",), [])
c.done()
