import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'zdvojnasob', ([2, -1],), [4, -2])
c.returns(ns, 'zdvojnasob', ([],), [])
c.returns(ns, 'zdvojnasob', ([0],), [0])
data = [2, -1]
puvodni = list(data)
c.call(ns, 'zdvojnasob', (data,))
c.add("Vstup se nemění", data == puvodni, "Vytvářejte nový seznam, neměňte vstup.")

c.done()
