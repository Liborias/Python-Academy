from dilna_check import check
c = check()
c.defines_class("Hrac")
ns = c.load()
cls = (ns or {}).get("Hrac")
c.add("Hrac je třída", isinstance(cls, type), "Definujte třídu Hrac pomocí class.")
if ns is not None and isinstance(cls, type):
    try:
        objekty = []
        for jmeno, body in [("Ema", 4), ("Žaneta", 0), ("", -3), ("Jan", 257)]:
            ok, hrac = c.call(ns, "vytvor_hrace", (jmeno, body))
            spravny = ok and isinstance(hrac, cls)
            c.add("Funkce vrací instanci Hrac", spravny, "Vytvořte Hrac(), nastavte atributy a objekt vraťte.")
            if spravny:
                objekty.append((hrac, jmeno, body))
        # Čteme je až po všech voláních: odhalí i sdílený objekt nebo přepsání třídy.
        for hrac, jmeno, body in objekty:
            c.add("Vlastní jméno a body", getattr(hrac, "jmeno", None) == jmeno and getattr(hrac, "body", None) == body,
                  "Atributy každého hráče mají zachovat jeho argumenty.")
        if len(objekty) == 4:
            a, b = objekty[0][0], objekty[1][0]
            c.add("Nové instance", len({id(x[0]) for x in objekty}) == 4, "Při každém volání vytvořte nového hráče.")
            a.body = 99
            c.add("Změna se nesdílí", getattr(b, "body", None) == 0, "Změna bodů jednoho hráče nesmí ovlivnit druhého.")
    except BaseException as exc:
        c.add("Práce s instancí bez chyby", False, f"{type(exc).__name__}: {exc}")

c.done()
