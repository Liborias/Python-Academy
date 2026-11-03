import ast
from dilna_check import check
c = check()
c.imports("bs4", "Použijte BeautifulSoup: from bs4 import BeautifulSoup.")
for _jmeno in ("nadpis", "prvni_odstavec", "prvni_odkaz", "text_s_id", "text_s_tridou"):
    _f = c.function(_jmeno)
    c.add(f"Funkce {_jmeno} používá find", _f is not None and bool(c.calls_in(_f, "find")),
          f"Ve funkci {_jmeno} použijte soup.find(...).")
ns = c.load()
if ns is not None:
    with open("stranka.html", encoding="utf-8") as f:
        S = f.read()
    c.returns(ns, "nadpis", (S,), "Zvířata v ZOO")
    c.returns(ns, "nadpis", ("<h1>  Ahoj \n</h1>",), "Ahoj")
    c.returns(ns, "nadpis", ("<p>x</p>",), None)
    c.returns(ns, "nadpis", ('<h2>jiný</h2><h1 class="velky">správný</h1>',), "správný")
    c.returns(ns, "prvni_odstavec", (S,), "Vítejte v naší malé ZOO.")
    c.returns(ns, "prvni_odstavec", ("<h1>x</h1>",), None)
    c.returns(ns, "prvni_odstavec", ("<p> mezery </p>",), "mezery")
    c.returns(ns, "prvni_odkaz", (S,), ("Vstupenky", "https://example.com/vstupenky"))
    c.returns(ns, "prvni_odkaz", ('<a name="x">bez href</a><a href="y">y</a>',), ("bez href", None))
    c.returns(ns, "prvni_odkaz", ('<a href="y"> text \n</a>',), ("text", "y"))
    c.returns(ns, "prvni_odkaz", ("<p>nic</p>",), None)
    c.returns(ns, "text_s_id", (S, "uvod"), "Vítejte v naší malé ZOO.")
    c.returns(ns, "text_s_id", (S, "neni"), None)
    c.returns(ns, "text_s_id", ('<div id="a"><b>x</b></div>', "a"), "x")
    c.returns(ns, "text_s_tridou", (S, "info"), "Otevřeno denně od 9 do 17 hodin.")
    c.returns(ns, "text_s_tridou", (S, "jina"), None)
    c.returns(ns, "text_s_tridou", ('<span class="zluta">s</span>', "zluta"), "s")
    c.returns(ns, "text_s_tridou", ('<p class="a b">dva</p>', "b"), "dva")
c.done()
