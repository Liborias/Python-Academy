import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'je_cislo', ('12',), True)
c.returns(ns, 'je_cislo', ('a',), False)
c.returns(ns, 'je_cislo', ('3.5',), False)
c.returns(ns, 'je_cislo', ('-2',), True)
c.uses(ast.Try, "Použijte try/except.")
c.done()
