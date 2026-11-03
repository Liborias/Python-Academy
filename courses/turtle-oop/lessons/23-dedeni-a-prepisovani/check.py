from dilna_check import check
c = check()
ns = c.load()
classes = {name: (ns or {}).get(name) for name in ["Zvire", "Pes", "Kocka"]}
for name, cls in classes.items():
    c.defines_class(name)
    c.add(f"{name} je třída", isinstance(cls, type), f"Definujte class {name}.")
if ns is not None and all(isinstance(cls, type) for cls in classes.values()):
    try:
        base = classes["Zvire"]
        c.add("Pes i Kocka dědí ze Zvire", all(issubclass(classes[name], base) for name in ("Pes", "Kocka")),
              "U obou odvozených tříd uveďte Zvire jako základ.")
        for name in ["Pes", "Kocka"]:
            c.add(f"{name} přepisuje pozdrav", "pozdrav" in classes[name].__dict__ and callable(getattr(classes[name], "pozdrav", None)),
                  "Definujte vlastní metodu pozdrav v odvozené třídě.")
        records = []
        for name, prefix in [("Zvire", "Ahoj"), ("Pes", "Haf"), ("Kocka", "Mňau")]:
            for jmeno in ["Ema", "Žofka", ""]:
                ok, obj = c.call(ns, name, (jmeno,))
                valid = ok and isinstance(obj, classes[name])
                c.add("Vytvoření zvířete", valid, "Zvíře přijímá jméno a uloží ho na svou instanci.")
                if valid:
                    records.append((obj, jmeno, prefix))
        for obj, jmeno, prefix in records:
            c.add("Vlastní jméno", getattr(obj, "jmeno", None) == jmeno, "Zachovejte přesně jméno dané instance.")
            ok, result = c.call({"pozdrav": getattr(obj, "pozdrav", None)}, "pozdrav")
            c.add("Pozdrav podle skutečného typu", ok and result == f"{prefix}, jsem {jmeno}.",
                  f"Očekávám vrácený text {prefix}, jsem {jmeno}.")
        if len(records) == 9:
            obj = records[3][0]
            obj.jmeno = "Nové jméno"
            ok, result = c.call({"pozdrav": getattr(obj, "pozdrav", None)}, "pozdrav")
            c.add("Pozdrav používá aktuální atribut", ok and result == "Haf, jsem Nové jméno.", "Pozdrav sestavujte z aktuálního self.jmeno.")
            for other, jmeno, prefix in records:
                if other is obj:
                    continue
                ok, result = c.call({"pozdrav": getattr(other, "pozdrav", None)}, "pozdrav")
                c.add("Ostatní zvířata se nemění", ok and result == f"{prefix}, jsem {jmeno}.", "Přepsání metody ani změna jména nemění jiné instance.")
    except BaseException as exc:
        c.add("Ověření dědění bez chyby", False, f"{type(exc).__name__}: {exc}")
c.done()
