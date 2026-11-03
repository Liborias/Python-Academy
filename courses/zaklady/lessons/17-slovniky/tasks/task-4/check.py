import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'autor', ({'autor': 'Ema'},), 'Ema')
c.returns(ns, 'autor', ({'autor': 'Jan', 'rok': 2026},), 'Jan')

c.done()
