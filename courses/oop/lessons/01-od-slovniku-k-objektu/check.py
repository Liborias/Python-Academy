from dilna_check import check

c = check()
c.defines_class("Zasilka")
ns = c.load()
cls = (ns or {}).get("Zasilka")
c.add("Zasilka je třída", isinstance(cls, type), "Ponechte třídu Zasilka.")
try:
    if ns is not None and isinstance(cls, type):
        records = []
        cases = [("Z-101", "Ema"), ("Z-102", "Jan"), ("VIP-žďár", "Žofie Nová"), ("", ""),
                 ('A "B"', "O'Neal"), (" Z-003 ", " Ema "), ("Z-101", "Ema")]
        for code, recipient in cases:
            ok, obj = c.call(ns, "vytvor_zasilku", (code, recipient))
            valid = ok and isinstance(obj, cls)
            c.add("Funkce vrací instanci", valid, "Vraťte vytvořenou Zasilka, ne slovník, třídu nebo None.")
            c.add("Funkce nic nevypisuje", c.last_output == "", "Výpis patří hlavnímu programu, zde použijte return.")
            if valid:
                records.append((obj, code, recipient))
        c.add("Každé volání má nový objekt", len(records) == len(cases) and len({id(obj) for obj, _, _ in records}) == len(cases),
              "Novou instanci vytvářejte při každém volání, i při stejných údajích.")
        for obj, code, recipient in records:
            c.add("Předané údaje a počáteční stav", getattr(obj, "kod", None) == code and getattr(obj, "prijemce", None) == recipient
                  and getattr(obj, "stav", None) == "prijata", "Uložte původní řetězce a stav prijata.")
        if records:
            obj = records[0][0]
            obj.prijemce = "Změněný příjemce"
            obj.stav = "odeslana"
            for other, code, recipient in records[1:]:
                c.add("Změna první neovlivní ostatní", other.kod == code and other.prijemce == recipient and other.stav == "prijata",
                      "Každá zásilka má samostatný stav.")
except BaseException as exc:
    c.add("Zásilky lze ověřit", False, f"{type(exc).__name__}: {exc}")
c.done()
