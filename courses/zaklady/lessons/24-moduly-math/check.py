import math
from dilna_check import check
c = check()
c.imports("math", "Použijte modul math: na začátek souboru přidejte import math (nebo from math import ...).")
ns = c.load()
if ns is not None:
    c.returns_close(ns, "obsah_kruhu", (1,), math.pi)
    c.returns_close(ns, "obsah_kruhu", (3,), 9 * math.pi)
    c.returns_close(ns, "obsah_kruhu", (0,), 0.0)
    c.returns_close(ns, "vzdalenost", (0, 0, 3, 4), 5.0)
    c.returns_close(ns, "vzdalenost", (1, 1, 1, 1), 0.0)
    c.returns_close(ns, "vzdalenost", (-1, -1, 2, 3), 5.0)
    c.returns(ns, "pocet_krabic", (25, 10), 3)
    c.returns(ns, "pocet_krabic", (20, 10), 2)
    c.returns(ns, "pocet_krabic", (1, 6), 1)
    c.returns(ns, "pocet_krabic", (0, 6), 0)
c.done()
