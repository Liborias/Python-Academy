from dilna_check import check

c = check()
c.defines_class("Had")
ns = c.load()
cls = (ns or {}).get("Had")
c.add("Had je třída", isinstance(cls, type), "Ponechte definici třídy Had.")
if ns is not None and isinstance(cls, type):
    try:
        records = []
        cases = [(6, 4, [(4, 1), (3, 1), (2, 1)]), (7, 5, [(0, 0)]),
                 (3, 8, [(1, 7), (1, 6)]), (1, 1, [(0, 0)])]
        for width, height, points in cases:
            supplied = list(points)
            ok, had = c.call(ns, "Had", (supplied, width, height))
            c.add("Lze vytvořit model", ok and isinstance(had, cls), "Konstruktor přijímá tělo, šířku a výšku.")
            if not ok:
                continue
            c.add("Rozměry a počáteční směr", had.sirka == width and had.vyska == height and had.smer == (1, 0),
                  "Uchovejte rozměry instance; počáteční směr je doprava.")
            c.add("Vstupní seznam zůstává zachovaný", supplied == points, "Konstruktor vstupní seznam nemění.")
            supplied.append((99, 99))
            expected = list(points)
            c.add("Had má vlastní seznam", isinstance(had.body, list) and had.body == expected,
                  "Vytvořte vlastní seznam pomocí list(body).")
            for direction in [(1, 0)] * 4 + [(0, 1)] * 3 + [(-1, 0)] * 4 + [(0, -1)] * 3:
                had.smer = direction
                x, y = expected[0]
                dx, dy = direction
                head = ((x + dx) % width, (y + dy) % height)
                expected = [head] + expected[:-1]
                ok, result = c.call({"krok": getattr(had, "krok", None)}, "krok")
                c.add("Krok vrací novou hlavu", ok and isinstance(result, tuple) and result == head,
                      f"Vraťte dvojici nové hlavy; očekávám {head!r}.")
                c.add("Tělo následuje hlavu a zachová délku", had.body == expected,
                      f"Přidejte novou hlavu a odeberte poslední článek; očekávám {expected!r}.")
                c.add("Krok nemění směr ani rozměry", had.smer == direction and had.sirka == width and had.vyska == height,
                      "Krok mění tělo, ne pravidla nebo rozměry modelu.")
            records.append((had, list(expected)))
        for had, expected in records:
            c.add("Jiní hadi tento stav nezměnili", had.body == expected, "Každá instance má vlastní seznam těla.")
        ok, default = c.call(ns, "Had", ([(2, 3)],))
        c.add("Výchozí rozměry", ok and default.sirka == 20 and default.vyska == 16,
              "Ponechte výchozí šířku 20 a výšku 16.")
    except BaseException as exc:
        c.add("Model lze ověřit bez chyby", False, f"{type(exc).__name__}: {exc}")
c.done()
