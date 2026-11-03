import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'levne', ([{'nazev': 'čaj', 'cena': 30}, {'nazev': 'káva', 'cena': 50}], 30), ['čaj'])
c.returns(ns, 'levne', ([], 50), [])
c.returns(ns, 'levne', ([{'nazev': 'x', 'cena': 10}], 0), [])

c.done()
