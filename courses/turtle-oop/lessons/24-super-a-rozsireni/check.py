import ast
from dilna_check import check
c = check()
ns = c.load()
base = (ns or {}).get("Hrac")
child = (ns or {}).get("BodovanyHrac")
for name, cls in [("Hrac", base), ("BodovanyHrac", child)]:
    c.defines_class(name)
    c.add(f"{name} je třída", isinstance(cls, type), f"Definujte class {name}.")
node = next((n for n in (c.tree.body if c.tree else []) if isinstance(n, ast.ClassDef) and n.name == "BodovanyHrac"), None)
for name in ["__init__", "popis"]:
    method = next((n for n in (node.body if node else []) if isinstance(n, ast.FunctionDef) and n.name == name), None)
    c.add(f"super uvnitř {name}", method is not None and bool(c.calls_in(method, "super")),
          f"V BodovanyHrac.{name} využijte super().")
if ns is not None and isinstance(base, type) and isinstance(child, type):
    try:
        c.add("Dědění z Hrac", issubclass(child, base), "BodovanyHrac musí dědit z Hrac.")
        ok_base, ordinary = c.call(ns, "Hrac", ("Ema",))
        if ok_base:
            ok, result = c.call({"popis": getattr(ordinary, "popis", None)}, "popis")
            c.add("Základní popis", ok and result == "Hráč: Ema", "Hrac.popis vrací základní text bez bodů.")
        else:
            c.add("Základní hráč vznikne", False, "Hrac přijímá jméno.")
        records = []
        for args, points in [(("Jan",), 0), (("Žaneta", 7), 7), (("", -3), -3)]:
            ok, obj = c.call(ns, "BodovanyHrac", args)
            valid = ok and isinstance(obj, child)
            c.add("Bodovaný hráč vznikne", valid, "Předejte jméno základu a nastavte počáteční body, výchozí jsou 0.")
            if valid:
                records.append((obj, args[0], points))
        for obj, name, points in records:
            c.add("Vlastní atributy", getattr(obj, "jmeno", None) == name and getattr(obj, "body", None) == points, "Uchovejte správné jméno a body každé instance.")
            ok, result = c.call({"popis": getattr(obj, "popis", None)}, "popis")
            c.add("Rozšířený popis", ok and result == f"Hráč: {name}, body: {points}", "Doplňte základní text o aktuální body.")
        if len(records) == 3:
            obj = records[0][0]
            for amount, expected in [(4, 4), (-2, 2), (0, 2)]:
                ok, result = c.call({"pridej": getattr(obj, "pridej_body", None)}, "pridej", (amount,))
                c.add("Body se přičítají", ok and result == expected and getattr(obj, "body", None) == expected, "Přičítejte k dosavadním bodům a vraťte nový počet.")
            obj.jmeno = "Nové jméno"
            ok, result = c.call({"popis": getattr(obj, "popis", None)}, "popis")
            c.add("Popis po změně stavu", ok and result == "Hráč: Nové jméno, body: 2", "Čtěte aktuální atributy.")
            c.add("Jiní hráči jsou nezávislí", records[1][0].body == 7 and records[2][0].body == -3, "Každý hráč má své body.")
        # Změna základní implementace prokáže skutečnou spolupráci tříd.
        original_init, original_description = base.__init__, base.popis
        calls = []
        def tracked_init(self, jmeno):
            calls.append((id(self), jmeno))
            original_init(self, jmeno)
        def new_description(self):
            return f"OVĚŘENO {self.jmeno}"
        try:
            base.__init__ = tracked_init
            base.popis = new_description
            ok, obj = c.call(ns, "BodovanyHrac", ("Kontrola", 12))
            c.add("Použije základní inicializátor pro tutéž instanci", ok and (id(obj), "Kontrola") in calls,
                  "super().__init__ musí připravit tohoto hráče, nikoli jiný objekt.")
            if ok:
                ok, result = c.call({"popis": getattr(obj, "popis", None)}, "popis")
                c.add("Rozšíří i změněný základní popis", ok and result == "OVĚŘENO Kontrola, body: 12", "Výsledek super().popis() opravdu použijte, text základu neopisujte.")
        finally:
            base.__init__, base.popis = original_init, original_description
    except BaseException as exc:
        c.add("Ověření super bez chyby", False, f"{type(exc).__name__}: {exc}")
c.done()
