from dilna_check import check

c = check()
c.defines_class("Polozka")
ns = c.load()
cls = (ns or {}).get("Polozka")
c.add("Polozka je třída", isinstance(cls, type), "Ponechte třídu Polozka.")
try:
    if ns is not None and isinstance(cls, type):
        records = []
        for name, price, count in [("Kniha", 250, 2), ("Dárek", 0, 0), ("Řemeslný sešit", 19, 7)]:
            obj = cls(name, price, count)
            expected_count = count
            for amount in [0, 2, 5, None, 0]:
                for _ in range(2):
                    ok, value = c.call({"celkem": obj.celkem}, "celkem")
                    c.add("Cena z aktuálního stavu", ok and value == price * expected_count and c.last_output == "",
                          "Vraťte součin aktuální ceny a počtu, nikoli výpis nebo uložený starý součet.")
                    c.add("Čtení nic nemění", (obj.nazev, obj.cena_za_kus, obj.pocet) == (name, price, expected_count),
                          "Metoda celkem nesmí přidávat kusy nebo měnit cenu.")
                args = () if amount is None else (amount,)
                expected_count += 1 if amount is None else amount
                ok, value = c.call({"pridej": obj.pridej}, "pridej", args)
                c.add("Přidání vrací nový počet", ok and value == expected_count and obj.pocet == expected_count and c.last_output == "",
                      "Přičtěte kolik do atributu a vraťte výsledek; výchozí argument je 1.")
                c.add("Ostatní údaje se nemění", obj.nazev == name and obj.cena_za_kus == price, "Přidávání nemění název nebo cenu za kus.")
            obj.cena_za_kus = price + 11
            ok, value = c.call({"celkem": obj.celkem}, "celkem")
            c.add("Aktuální cena za kus se projeví", ok and value == (price + 11) * expected_count,
                  "Čtěte současné atributy i po jejich změně.")
            records.append((obj, name, price + 11, expected_count))
        for obj, name, price, count in records:
            c.add("Položky se neovlivňují", (obj.nazev, obj.cena_za_kus, obj.pocet) == (name, price, count),
                  "Každá položka mění jen svůj stav.")
except BaseException as exc:
    c.add("Metody lze ověřit", False, f"{type(exc).__name__}: {exc}")
c.done()
