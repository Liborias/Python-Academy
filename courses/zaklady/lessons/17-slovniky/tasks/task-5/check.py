import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'zmen_cenu', ({'cena': 10}, 25), {'cena': 25})
c.returns(ns, 'zmen_cenu', ({'cena': 7, 'nazev': 'čaj'}, 0), {'cena': 0, 'nazev': 'čaj'})

c.done()
