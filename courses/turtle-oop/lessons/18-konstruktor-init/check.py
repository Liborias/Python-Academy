from dilna_check import check
c = check()
c.defines_class("Obdelnik")
ns = c.load()
cls = (ns or {}).get("Obdelnik")
c.add("Obdelnik je třída", isinstance(cls, type), "Definujte class Obdelnik.")
if ns is not None and isinstance(cls, type):
    try:
        objekty = []
        for sirka, vyska in [(3, 5), (0, 7), (2.5, 1.25), (81, 9)]:
            ok, obj = c.call(ns, "Obdelnik", (sirka, vyska))
            c.add("Vytvoření se dvěma argumenty", ok and isinstance(obj, cls), "__init__ přijímá self, sirka, vyska a nevrací objekt.")
            if ok:
                objekty.append((obj, sirka, vyska))
        for obj, sirka, vyska in objekty:
            c.add("Rozměry jsou uložené", getattr(obj, "sirka", None) == sirka and getattr(obj, "vyska", None) == vyska,
                  "Nastavte self.sirka a self.vyska podle parametrů.")
        if len(objekty) == 4:
            a, b = objekty[0][0], objekty[1][0]
            a.sirka = 99
            a.vyska = 100
            c.add("Nezávislé rozměry", getattr(b, "sirka", None) == 0 and getattr(b, "vyska", None) == 7, "Údaje ukládejte na instanci, nikoli na třídu.")
    except BaseException as exc:
        c.add("Práce s instancí bez chyby", False, f"{type(exc).__name__}: {exc}")

c.done()
