import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'najdi', ({'Ema': 2}, 'Ema'), 2)
c.returns(ns, 'najdi', ({}, 'Jan'), 'chybí')
c.returns(ns, 'najdi', ({'Ema': 0}, 'Ema'), 0)
c.uses(ast.Try, "Zachyťte konkrétní chybu.")
c.done()
