from dilna_check import check
c = check()
c.imports("bs4", "Použijte BeautifulSoup: from bs4 import BeautifulSoup.")
for _jmeno in ("nazvy", "ceny", "odkaz_produktu"):
    _f = c.function(_jmeno)
    c.add(f"Funkce {_jmeno} používá select nebo select_one", _f is not None and bool(c.calls_in(_f, "select") or c.calls_in(_f, "select_one")),
          f"Ve funkci {_jmeno} použijte select(...) nebo select_one(...) s CSS selektorem.")
ns = c.load()
if ns is not None:
    with open("produkty.html", encoding="utf-8") as f:
        S = f.read()
    c.returns(ns, "nazvy", (S,), ["Tužka", "Sešit", "Guma"])
    c.returns(ns, "nazvy", ("<p>nic</p>",), [])
    c.returns(ns, "ceny", (S,), [12, 25, 8])
    _ok, _v = c.call(ns, "ceny", (S,))
    c.add("ceny jsou celá čísla", _ok and isinstance(_v, list) and all(type(x) is int for x in _v), "Převeďte text na celé číslo pomocí int().")
    c.returns(ns, "ceny", ('<div class="produkt"><span class="cena">1999 Kč</span></div><span class="cena">99 Kč</span>',), [1999])
    c.returns(ns, "skladem", (S,), ["Tužka", "Sešit"])
    c.returns(ns, "skladem", ('<div class="produkt vyprodano"><h3>A</h3></div><div class="produkt"><h3>B</h3></div>',), ["B"])
    c.returns(ns, "skladem", ('<div class="vyprodano"><h3>Mimo</h3></div>',), [])
    c.returns(ns, "odkaz_produktu", (S, "p2"), "/sesit")
    c.returns(ns, "odkaz_produktu", (S, "p3"), "/guma")
    c.returns(ns, "odkaz_produktu", (S, "p9"), None)
    c.returns(ns, "odkaz_produktu", ('<div id="x"><h3>bez odkazu</h3></div>', "x"), None)
c.done()
