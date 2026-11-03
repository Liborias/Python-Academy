from dilna_check import check
c = check()
c.imports("bs4", "Použijte BeautifulSoup: from bs4 import BeautifulSoup.")
for _jmeno in ("polozky", "odkazy", "tabulka"):
    _f = c.function(_jmeno)
    c.add(f"Funkce {_jmeno} používá find_all", _f is not None and bool(c.calls_in(_f, "find_all")),
          f"Ve funkci {_jmeno} použijte find_all(...).")
ns = c.load()
if ns is not None:
    with open("obchod.html", encoding="utf-8") as f:
        S = f.read()
    c.returns(ns, "polozky", (S,), ["Jablka", "Hrušky", "Mrkev"])
    c.returns(ns, "polozky", (S, "ovoce"), ["Jablka", "Hrušky"])
    c.returns(ns, "polozky", (S, "zelenina"), ["Mrkev"])
    c.returns(ns, "polozky", (S, "maso"), [])
    c.returns(ns, "polozky", ("<p>nic</p>",), [])
    c.returns(ns, "odkazy", (S,), [("Jablka", "/jablka"), ("Hrušky", "/hrusky")])
    c.returns(ns, "odkazy", ('<a href="a">A</a><a>B</a><a href="">C</a>',), [("A", "a"), ("C", "")])
    c.returns(ns, "odkazy", ("<p>nic</p>",), [])
    c.returns(ns, "tabulka", (S,), [["Jablka", "25"], ["Hrušky", "30"], ["Mrkev", "18"]])
    c.returns(ns, "tabulka", ("<table><tr><th>a</th></tr></table>",), [])
    c.returns(ns, "tabulka", ("<table><tr><td> 1 </td><td>2</td></tr></table>",), [["1", "2"]])
    c.returns(ns, "ceny", (S,), {"Jablka": 25, "Hrušky": 30, "Mrkev": 18})
    c.returns(ns, "ceny", ("<table><tr><td>Čaj</td><td>99</td></tr></table>",), {"Čaj": 99})
    c.returns(ns, "ceny", ("<p>nic</p>",), {})
c.done()
