import ast
from dilna_check import check
c = check()
def _vola_funkci(a):
    return any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
               and n.func.id in ("soucet_do", "prumer_kladnych", "je_palindrom") for n in ast.walk(a.test))


_strom = c.tree
pocet_assert = sum(isinstance(n, ast.Assert) and _vola_funkci(n) for n in (_strom.body if _strom else []))
c.add("Soubor obsahuje alespoň 3 příkazy assert, které volají vaše funkce", pocet_assert >= 3,
      f"Našel jsem {pocet_assert} příkazů assert, které na úrovni souboru volají soucet_do, prumer_kladnych nebo je_palindrom. Přidejte další, např. assert soucet_do(3) == 6.")
ns = c.load()
if ns is not None:
    c.returns(ns, "soucet_do", (3,), 6)
    c.returns(ns, "soucet_do", (1,), 1)
    c.returns(ns, "soucet_do", (10,), 55)
    c.returns(ns, "soucet_do", (0,), 0)
    c.returns(ns, "prumer_kladnych", ([2, -5, 4, 0, 6],), 4.0)
    c.returns(ns, "prumer_kladnych", ([-1, -2],), 0)
    c.returns(ns, "prumer_kladnych", ([],), 0)
    c.returns(ns, "prumer_kladnych", ([5],), 5.0)
    c.returns(ns, "je_palindrom", ("kajak",), True)
    c.returns(ns, "je_palindrom", ("Anna",), True)
    c.returns(ns, "je_palindrom", ("auto",), False)
    c.returns(ns, "je_palindrom", ("",), True)
    c.returns(ns, "je_palindrom", ("ab",), False)
c.done()
