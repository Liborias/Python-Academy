from dilna_check import check
c = check()
c.defines_class("Trasa")
ns = c.load()
cls = (ns or {}).get("Trasa")
c.add("Trasa je třída", isinstance(cls, type), "Definujte class Trasa.")
if ns is not None and isinstance(cls, type):
    try:
        def verify(obj, name, points):
            c.add("Aktuální atributy", getattr(obj, "jmeno", None) == name and isinstance(getattr(obj, "body", None), list)
                  and obj.body == points, "Uložte jméno a vlastní seznam body.")
            for function, expected in [(len, len(points)), (str, f"Trasa {name}, bodů: {len(points)}"),
                                       (repr, f"Trasa(jmeno={name!r}, body={points!r})")]:
                ok, value = c.call({"operace": function}, "operace", (obj,))
                c.add(f"Funguje {function.__name__}", ok and value == expected, f"Očekávám {expected!r}.")
            c.add("Čtení nemění trasu", getattr(obj, "body", None) == points, "Formátování ani délka nesmí měnit body.")

        records = []
        for name, points in [("Les", [(0, 0), (2, 3)]), ("", []), ("Žofčin 'výlet'", [(4, -2)]), ('Řeka "A"', [(2, 1), (0, 0)])]:
            supplied = list(points)
            ok, obj = c.call(ns, "Trasa", (name, supplied))
            valid = ok and isinstance(obj, cls)
            c.add("Vytvoření trasy", valid, "Trasa přijímá jméno a seznam souřadnic.")
            if valid:
                c.add("Konstruktor nemění vstup", supplied == points, "Vstupní seznam nekraťte ani nepřerovnávejte.")
                supplied.append((88, 99))
                verify(obj, name, points)
                records.append((obj, name, list(points)))
        if len(records) == 4:
            obj = records[0][0]
            obj.jmeno = 'Nová "trasa"'
            obj.body.append((-7, 5))
            for _ in range(2):
                verify(obj, 'Nová "trasa"', [(0, 0), (2, 3), (-7, 5)])
            for other, name, points in records[1:]:
                verify(other, name, points)
    except BaseException as exc:
        c.add("Práce s trasou bez chyby", False, f"{type(exc).__name__}: {exc}")
c.done()
