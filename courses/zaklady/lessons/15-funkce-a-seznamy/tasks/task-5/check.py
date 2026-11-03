import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'kladne', ([-1, 0, 3, 2],), [3, 2])
c.returns(ns, 'kladne', ([],), [])
c.returns(ns, 'kladne', ([-4],), [])
data = [-1, 0, 3, 2]
puvodni = list(data)
c.call(ns, 'kladne', (data,))
c.add("Vstup se nemění", data == puvodni, "Vytvářejte nový seznam, neměňte vstup.")

c.done()
