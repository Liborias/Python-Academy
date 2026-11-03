from datetime import date
from dilna_check import check
c = check()
c.imports("datetime", "Na začátek souboru přidejte from datetime import date, timedelta (nebo import datetime).")
ns = c.load()
if ns is not None:
    c.returns(ns, "dnu_do", (date(2026, 10, 25), date(2026, 12, 24)), 60)
    c.returns(ns, "dnu_do", (date(2026, 1, 1), date(2026, 1, 1)), 0)
    c.returns(ns, "dnu_do", (date(2027, 1, 1), date(2026, 1, 1)), -365)
    c.returns(ns, "za_dni", (date(2026, 10, 25), 7), date(2026, 11, 1))
    c.returns(ns, "za_dni", (date(2026, 12, 30), 3), date(2027, 1, 2))
    c.returns(ns, "za_dni", (date(2026, 3, 1), -1), date(2026, 2, 28))
    c.returns(ns, "formatuj", (date(2026, 3, 5),), "05. 03. 2026")
    c.returns(ns, "formatuj", (date(2027, 11, 21),), "21. 11. 2027")
    c.returns(ns, "je_vikend", (date(2026, 10, 24),), True)
    c.returns(ns, "je_vikend", (date(2026, 10, 25),), True)
    c.returns(ns, "je_vikend", (date(2026, 10, 23),), False)
    c.returns(ns, "je_vikend", (date(2026, 10, 26),), False)
c.done()
