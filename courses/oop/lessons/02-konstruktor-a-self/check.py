from dilna_check import check

c = check()
c.defines_class("Polozka")
ns = c.load()
cls = (ns or {}).get("Polozka")
c.add("Polozka je třída", isinstance(cls, type), "Definujte třídu Polozka s __init__.")
try:
    if ns is not None and isinstance(cls, type):
        records = []
        for args, expected in [
            (("Průvodce Pythonem", 250, 2), ("Průvodce Pythonem", 250, 2)),
            (("Dárkový obal", 30), ("Dárkový obal", 30, 1)),
            (("Dárek", 0, 0), ("Dárek", 0, 0)),
            (('Žlutý "sešit"', 19, 7), ('Žlutý "sešit"', 19, 7)),
            (("Průvodce Pythonem", 250, 2), ("Průvodce Pythonem", 250, 2)),
        ]:
            ok, obj = c.call(ns, "Polozka", args)
            valid = ok and isinstance(obj, cls)
            c.add("Položku lze vytvořit", valid, "Konstruktor přijímá název, cenu za kus a nepovinný počet 1.")
            c.add("Konstruktor nic nevypisuje", c.last_output == "", "Přiřaďte atributy bez výpisu.")
            if valid:
                records.append((obj, expected))
        c.add("Samostatné instance", len(records) == 5 and len({id(obj) for obj, _ in records}) == 5,
              "Každé volání třídy vytváří novou položku.")
        for obj, expected in records:
            c.add("Atributy zachovaly argumenty", (getattr(obj, "nazev", None), getattr(obj, "cena_za_kus", None), getattr(obj, "pocet", None)) == expected,
                  "Uložte hodnoty do self.nazev, self.cena_za_kus a self.pocet; ponechte i výslovnou nulu.")
        if records:
            first = records[0][0]
            first.nazev = "Jiná položka"
            first.cena_za_kus = 999
            first.pocet = 12
            for obj, expected in records[1:]:
                c.add("Změny zůstávají na instanci", (obj.nazev, obj.cena_za_kus, obj.pocet) == expected,
                      "Údaje konkrétní položky neukládejte na třídu.")
except BaseException as exc:
    c.add("Konstruktor lze ověřit", False, f"{type(exc).__name__}: {exc}")
c.done()
