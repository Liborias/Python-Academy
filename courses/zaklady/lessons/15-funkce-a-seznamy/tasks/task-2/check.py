import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'bez_nul', ([0, 2, 0, -1],), [2, -1])
c.returns(ns, 'bez_nul', ([],), [])
c.returns(ns, 'bez_nul', ([0],), [])
data = [0, 2, 0, -1]
puvodni = list(data)
c.call(ns, 'bez_nul', (data,))
c.add("Vstup se nemění", data == puvodni, "Vytvářejte nový seznam, neměňte vstup.")

c.done()
