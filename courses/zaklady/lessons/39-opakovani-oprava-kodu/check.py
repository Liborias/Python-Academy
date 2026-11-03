import ast
from dilna_check import check
c = check()
tree = c.tree
if tree is not None:
    funkce = [n for n in tree.body if isinstance(n, ast.FunctionDef)]
    bez = [f.name for f in funkce if not ast.get_docstring(f)]
    c.add("Každá funkce má docstring", bool(funkce) and not bez, f"Chybí docstring u: {bez}.")
    dlouhe = [i + 1 for i, r in enumerate(c.code.split("\n")) if len(r) > 79]
    c.add("Řádky nejsou delší než 79 znaků", not dlouhe, f"Příliš dlouhé řádky: {dlouhe}.")
ns = c.load()
if ns is not None:
    c.returns(ns, "prumer", ([2, 4, 6],), 4.0)
    c.returns(ns, "prumer", ([],), 0)
    c.returns(ns, "prumer", ([5],), 5.0)
    c.returns(ns, "prumer", ([1, 2],), 1.5)
    c.returns(ns, "druha_nejvetsi", ([1, 5, 3],), 3)
    c.returns(ns, "druha_nejvetsi", ([5, 5, 2],), 2)
    c.returns(ns, "druha_nejvetsi", ([5, 5],), None)
    c.returns(ns, "druha_nejvetsi", ([7],), None)
    c.returns(ns, "druha_nejvetsi", ([],), None)
    c.returns(ns, "druha_nejvetsi", ([-1, -5, -3, -1],), -3)
    c.returns(ns, "kolik_slov", ("ahoj svete",), 2)
    c.returns(ns, "kolik_slov", ("jedno",), 1)
    c.returns(ns, "kolik_slov", ("",), 0)
    c.returns(ns, "kolik_slov", ("  mezery   navic  ",), 2)
    c.returns(ns, "bez_duplicit", ([3, 1, 3, 2, 1],), [3, 1, 2])
    c.returns(ns, "bez_duplicit", (["b", "a", "b"],), ["b", "a"])
    c.returns(ns, "bez_duplicit", ([],), [])
c.done()
