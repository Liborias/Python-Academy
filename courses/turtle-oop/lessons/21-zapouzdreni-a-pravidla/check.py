from dilna_check import check
c = check()
c.defines_class("Ucet")
ns = c.load()
cls = (ns or {}).get("Ucet")
c.add("Ucet je třída", isinstance(cls, type), "Definujte class Ucet.")
if ns is not None and isinstance(cls, type):
    try:
        for value in [-1, -100]:
            c.raises(ns, "Ucet", (value,), ValueError)
        ok_a, a = c.call(ns, "Ucet")
        ok_b, b = c.call(ns, "Ucet", (10,))
        valid = ok_a and ok_b and isinstance(a, cls) and isinstance(b, cls)
        c.add("Vytvoření účtů", valid, "Konstruktor má mít výchozí zůstatek 0 a přijímat nezáporný začátek.")
        if valid:
            def stav(obj, expected):
                ok, value = c.call({"metoda": getattr(obj, "stav", None)}, "metoda")
                c.add("Aktuální zůstatek", ok and value == expected, f"Metoda stav() má vrátit {expected} jako číslo.")

            stav(a, 0)
            stav(b, 10)
            cases = [("vloz", 8, 8, False), ("vloz", 5, 13, False), ("vyber", 3, 10, False),
                     ("vloz", 0, 10, True), ("vloz", -5, 10, True), ("vyber", 0, 10, True),
                     ("vyber", -2, 10, True), ("vyber", 11, 10, True), ("vyber", 10, 0, False),
                     ("vyber", 1, 0, True), ("vloz", 2, 2, False)]
            for method, amount, expected, rejected in cases:
                ok, value = c.call({"metoda": getattr(a, method, None)}, "metoda", (amount,))
                if rejected:
                    c.add("Neplatná operace vyvolá ValueError", not ok and isinstance(value, ValueError),
                          "Neplatnou částku odmítněte pomocí raise ValueError ještě před změnou stavu.")
                else:
                    c.add("Operace vrací nový zůstatek", ok and value == expected,
                          f"Pro {method}({amount}) očekávám nový zůstatek {expected}.")
                stav(a, expected)
                stav(a, expected)  # Samotné čtení nesmí měnit stav.
                stav(b, 10)
            ok, value = c.call({"metoda": getattr(b, "vyber", None)}, "metoda", (4,))
            c.add("Druhý účet funguje samostatně", ok and value == 6, "Účty musí mít vlastní zůstatek.")
            stav(a, 2)
            stav(b, 6)
            ok_d, d = c.call(ns, "Ucet", (250,))
            c.add("Další účet", ok_d and isinstance(d, cls), "Počáteční částku nezapisujte natvrdo.")
            if ok_d:
                stav(d, 250)
                stav(a, 2)
    except BaseException as exc:
        c.add("Ověření účtu bez chyby", False, f"{type(exc).__name__}: {exc}")
c.done()
