import ast
from dilna_check import check
c = check()
for _jmeno in ("na_cislo", "bezpecne_deleni"):
    _f = c.function(_jmeno)
    c.add(f"Funkce {_jmeno} používá try a except", _f is not None and any(isinstance(n, ast.Try) for n in ast.walk(_f)),
          f"Ve funkci {_jmeno} použijte try a except.")
ns = c.load()
if ns is not None:
    c.returns(ns, "na_cislo", ("42",), 42)
    c.returns(ns, "na_cislo", ("-7",), -7)
    c.returns(ns, "na_cislo", ("abc",), None)
    c.returns(ns, "na_cislo", ("",), None)
    c.returns(ns, "na_cislo", ("3.5",), None)
    c.returns(ns, "bezpecne_deleni", (10, 4), 2.5)
    c.returns(ns, "bezpecne_deleni", (7, 0), None)
    c.returns(ns, "bezpecne_deleni", (0, 3), 0.0)
    c.returns(ns, "soucet_cisel", (["1", "2", "x", "4"],), 7)
    c.returns(ns, "soucet_cisel", (["a", "b"],), 0)
    c.returns(ns, "soucet_cisel", (["1", "2.5", "3"],), 4)
    c.returns(ns, "soucet_cisel", ([],), 0)
c.done()
