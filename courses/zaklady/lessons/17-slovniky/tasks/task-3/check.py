import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'zbozi', (10, 3), {'cena': 10, 'pocet': 3})
c.returns(ns, 'zbozi', (0, 0), {'cena': 0, 'pocet': 0})
c.returns(ns, 'zbozi', (25, 1), {'cena': 25, 'pocet': 1})

c.done()
