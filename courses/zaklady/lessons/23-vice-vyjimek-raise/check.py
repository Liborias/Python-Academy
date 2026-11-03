import ast
from dilna_check import check
c = check()
for _jmeno in ("je_vek_platny", "prvek", "hodnota"):
    _f = c.function(_jmeno)
    c.add(f"Funkce {_jmeno} používá try a except", _f is not None and any(isinstance(n, ast.Try) for n in ast.walk(_f)),
          f"Ve funkci {_jmeno} použijte try a except.")
c.uses(ast.Raise, "Pro neplatný věk použijte raise ValueError(...).")
ns = c.load()
if ns is not None:
    c.returns(ns, "nacti_vek", ("25",), 25)
    c.returns(ns, "nacti_vek", ("0",), 0)
    c.returns(ns, "nacti_vek", ("150",), 150)
    c.raises(ns, "nacti_vek", ("151",), ValueError, "Věk nad 150 má vyvolat ValueError.")
    c.raises(ns, "nacti_vek", ("-1",), ValueError, "Záporný věk má vyvolat ValueError.")
    c.raises(ns, "nacti_vek", ("abc",), ValueError)
    c.returns(ns, "je_vek_platny", ("30",), True)
    c.returns(ns, "je_vek_platny", ("200",), False)
    c.returns(ns, "je_vek_platny", ("x",), False)
    c.returns(ns, "prvek", ([5, 6, 7], 1), 6)
    c.returns(ns, "prvek", ([5, 6, 7], 3), None)
    c.returns(ns, "prvek", ([], 0), None)
    c.returns(ns, "hodnota", ({"a": 1}, "a"), 1)
    c.returns(ns, "hodnota", ({"a": 1}, "b"), "?")
    c.returns(ns, "hodnota", ({"a": None}, "a"), None)
c.done()
