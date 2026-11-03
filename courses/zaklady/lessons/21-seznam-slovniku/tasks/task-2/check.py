import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'nazvy', ([{'nazev': 'Les'}, {'nazev': 'Hrad'}],), ['Les', 'Hrad'])
c.returns(ns, 'nazvy', ([],), [])

c.done()
