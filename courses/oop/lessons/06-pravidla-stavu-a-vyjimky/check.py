from dilna_check import check

c = check()
c.defines_class("Zasoba")
ns = c.load()
cls = (ns or {}).get("Zasoba")
try:
    if ns is not None and isinstance(cls, type):
        for value in [-1, 1.5, "3", True, False, None, []]:
            c.raises(ns, "Zasoba", ("Vadný počátek", value), ValueError)
        records = []
        for name, start in [("Knihy", 5), ("Obaly", 0), ("Dárky", 12)]:
            obj = cls(name, start)
            c.add("Platný počátek", obj.stav() == start and obj.nazev == name, "Uložte zadaný nezáporný celý počet.")
            for method in ["prijmi", "vydej"]:
                for value in [0, -1, 3.0, "3", True, False, None, []]:
                    before = obj.stav()
                    ok, error = c.call({"operace": getattr(obj, method)}, "operace", (value,))
                    c.add("Neplatné množství je ValueError bez změny", not ok and isinstance(error, ValueError)
                          and obj.stav() == before and obj.nazev == name,
                          "Nejdřív ověřte skutečný kladný int, potom měňte stav.")
            before = obj.stav()
            ok, error = c.call({"vydej": obj.vydej}, "vydej", (before + 1,))
            c.add("Nedostupný výdej zachová stav", not ok and isinstance(error, ValueError) and obj.stav() == before,
                  "Při nedostatku neodebírejte nic a počet neořezávejte.")
            ok, value = c.call({"prijmi": obj.prijmi}, "prijmi", (3,))
            c.add("Platný příjem po chybě", ok and value == start + 3 and obj.stav() == start + 3 and c.last_output == "",
                  "Odmítnutí nepoškodí další operace; příjem vrací nový počet.")
            ok, value = c.call({"vydej": obj.vydej}, "vydej", (1,))
            c.add("Částečný výdej odebere právě požadované kusy", ok and value == start + 2 and obj.stav() == start + 2,
                  "Platný výdej nesmí vynulovat celou zásobu.")
            ok, value = c.call({"vydej": obj.vydej}, "vydej", (start + 2,))
            c.add("Výdej všech kusů je dovolený", ok and value == 0 and obj.stav() == 0 and c.last_output == "",
                  "Horní hranice je včetně posledního kusu.")
            ok, error = c.call({"vydej": obj.vydej}, "vydej", (1,))
            c.add("Prázdnou zásobu nelze přečerpat", not ok and isinstance(error, ValueError) and obj.stav() == 0,
                  "Prázdný stav také hlídá nedostatek.")
            obj.prijmi(start + 1)
            records.append((obj, name, start + 1))
        c.add("Výchozí nula", cls("Nová").stav() == 0, "Konstruktor má výchozí počet 0.")
        for obj, name, expected in records:
            c.add("Nezávislé zásoby", obj.nazev == name and obj.stav() == expected, "Stavy jednotlivých zásob se nesdílejí.")
    else:
        c.add("Zasoba je třída", False, "Ponechte třídu Zasoba.")
except BaseException as exc:
    c.add("Pravidla stavu lze ověřit", False, f"{type(exc).__name__}: {exc}")
c.done()
