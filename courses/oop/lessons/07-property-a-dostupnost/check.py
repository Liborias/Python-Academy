from dilna_check import check

c = check()
c.defines_class("SkladovaKarta")
ns = c.load()
cls = (ns or {}).get("SkladovaKarta")
try:
    if ns is not None and isinstance(cls, type):
        for name in ["celkem", "rezervovano", "dostupne"]:
            c.add(f"{name} je property", isinstance(getattr(cls, name, None), property), "Definujte čtení pomocí property.")
        for bad in [-1, True, False, 2.0, "2", None]:
            c.raises(ns, "SkladovaKarta", ("Neplatná karta", bad), ValueError)
        def snapshot(card):
            return (card.nazev, card.celkem, card.rezervovano, card.dostupne)
        records = []
        for name, total in [("Kniha", 5), ("Obal", 13), ("Prázdná", 0)]:
            card = cls(name, total)
            reserved = 0
            c.add("Počáteční dostupnost", snapshot(card) == (name, total, 0, total), "Nová karta nemá rezervované kusy.")
            for attr in ["celkem", "rezervovano", "dostupne"]:
                state = snapshot(card)
                ok, error = c.call({"zapis": lambda: setattr(card, attr, 99)}, "zapis")
                c.add("Property je pouze pro čtení", not ok and isinstance(error, AttributeError) and snapshot(card) == state,
                      "Přiřazení do veřejných property se odmítá bez změn.")
            for method in ["rezervuj", "uvolni"]:
                for bad in [0, -1, 2.0, "2", True, False, None, []]:
                    state = snapshot(card)
                    ok, error = c.call({"operace": getattr(card, method)}, "operace", (bad,))
                    c.add("Chybné množství je odmítnuto", not ok and isinstance(error, ValueError) and snapshot(card) == state,
                          "Množství musí být skutečný kladný int, kontrolovaný před změnou.")
            operations = [("rezervuj", 2), ("rezervuj", 1), ("uvolni", 1), ("rezervuj", total - 2), ("uvolni", total)] if total else []
            for method, amount in operations:
                reserved += amount if method == "rezervuj" else -amount
                ok, value = c.call({"operace": getattr(card, method)}, "operace", (amount,))
                c.add("Rezervace a uvolnění vracejí dostupnost", ok and value == total - reserved
                      and snapshot(card) == (name, total, reserved, total - reserved) and c.last_output == "",
                      "Mění se rezervace, fyzický počet zůstává stejný.")
                for _ in range(2):
                    c.add("Čtení property nemění stav", snapshot(card) == (name, total, reserved, total - reserved),
                          "Dostupnost vypočítejte z aktuálních údajů.")
            for method, amount in [("rezervuj", card.dostupne + 1), ("uvolni", card.rezervovano + 1)]:
                state = snapshot(card)
                ok, error = c.call({"operace": getattr(card, method)}, "operace", (amount,))
                c.add("Nelze překročit dostupný nebo rezervovaný počet", not ok and isinstance(error, ValueError) and snapshot(card) == state,
                      "Při odmítnutí zůstávají všechny počty stejné.")
            records.append((card, snapshot(card)))
        c.add("Výchozí karta je prázdná", snapshot(cls("Výchozí")) == ("Výchozí", 0, 0, 0), "Výchozí celkový počet je nula.")
        for card, state in records:
            c.add("Karty mají samostatné počty", snapshot(card) == state, "Data různých karet se nesdílejí.")
        a, b = cls("Souběžná A", 5), cls("Souběžná B", 7)
        a.rezervuj(2)
        c.add("Rezervace jedné karty nemění druhou", snapshot(a) == ("Souběžná A", 5, 2, 3)
              and snapshot(b) == ("Souběžná B", 7, 0, 7), "Rezervované množství patří každé kartě zvlášť.")
        b.rezervuj(1)
        c.add("Dvě aktivní rezervace zůstávají nezávislé", snapshot(a) == ("Souběžná A", 5, 2, 3)
              and snapshot(b) == ("Souběžná B", 7, 1, 6), "Nepoužívejte společný třídní stav.")
    else:
        c.add("SkladovaKarta je třída", False, "Definujte SkladovaKarta.")
except BaseException as exc:
    c.add("Property a rezervace lze ověřit", False, f"{type(exc).__name__}: {exc}")
c.done()
