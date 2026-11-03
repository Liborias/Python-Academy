import ast
from dilna_check import check
c = check()
ns = c.load()
c.imports("random")
import random
random.seed(472)
hodnoty = []
for _ in range(80):
    ok, hodnota = c.call(ns, 'hod', ())
    c.add("Náhodný výsledek v rozsahu", ok and hodnota in [1, 2, 3, 4, 5, 6], "Vraťte jednu z povolených hodnot.")
    if ok:
        hodnoty.append(hodnota)
c.add("Více různých výsledků", len(set(map(repr, hodnoty))) > 1, "Nevracejte stále stejnou hodnotu ani neresetujte seed uvnitř funkce.")

c.done()
