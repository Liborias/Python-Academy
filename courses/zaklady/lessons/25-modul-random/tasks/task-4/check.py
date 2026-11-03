import ast
from dilna_check import check
c = check()
ns = c.load()
c.imports("random")
import random
random.seed(472)
hodnoty = []
for _ in range(80):
    ok, hodnota = c.call(ns, 'vyber', (['A', 'B', 'C'],))
    c.add("Náhodný výsledek v rozsahu", ok and hodnota in ['A', 'B', 'C'], "Vraťte jednu z povolených hodnot.")
    if ok:
        hodnoty.append(hodnota)
c.add("Více různých výsledků", len(set(map(repr, hodnoty))) > 1, "Nevracejte stále stejnou hodnotu ani neresetujte seed uvnitř funkce.")
data = ["A", "B", "C"]
c.call(ns, 'vyber', (data,))
c.add("Vstup se nemění", data == ["A", "B", "C"], "Neměňte vstup.")

c.done()
