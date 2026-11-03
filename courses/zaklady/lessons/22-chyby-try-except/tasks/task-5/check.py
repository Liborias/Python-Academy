import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'cislo_nebo', ('x', 7), 7)
c.returns(ns, 'cislo_nebo', ('42', 9), 42)
c.returns(ns, 'cislo_nebo', ('', -1), -1)
c.uses(ast.Try, "Použijte try/except.")
c.done()
