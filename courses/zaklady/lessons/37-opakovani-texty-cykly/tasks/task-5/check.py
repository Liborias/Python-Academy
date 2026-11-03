import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'pocet_dlouhych', ('pes kočka les', 4), 1)
c.returns(ns, 'pocet_dlouhych', ('', 1), 0)
c.returns(ns, 'pocet_dlouhych', ('a bb ccc', 2), 2)

c.done()
