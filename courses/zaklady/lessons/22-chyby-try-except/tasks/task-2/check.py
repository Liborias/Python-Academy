import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'na_int', ('12',), 12)
c.returns(ns, 'na_int', ('abc',), 0)
c.returns(ns, 'na_int', ('',), 0)
c.returns(ns, 'na_int', ('-4',), -4)
c.uses(ast.Try, "Použijte try/except.")
c.done()
