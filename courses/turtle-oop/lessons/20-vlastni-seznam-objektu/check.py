from dilna_check import check
c = check()
c.defines_class("Batoh")
ns = c.load()
cls = (ns or {}).get("Batoh")
c.add("Batoh je třída", isinstance(cls, type), "Definujte class Batoh.")
if ns is not None and isinstance(cls, type):
    try:
        ok_a, a = c.call(ns, "Batoh")
        ok_b, b = c.call(ns, "Batoh")
        valid = ok_a and ok_b and isinstance(a, cls) and isinstance(b, cls)
        c.add("Dva batohy", valid, "Batoh() má vytvořit novou instanci bez dalších argumentů.")
        if valid:
            c.add("Každá instance vlastní seznam", isinstance(getattr(a, "veci", None), list)
                  and isinstance(getattr(b, "veci", None), list) and a.veci is not b.veci,
                  "V __init__ vytvořte self.veci = [] pro každou instanci zvlášť.")
            def obsah(obj, expected, label):
                ok, value = c.call({"metoda": getattr(obj, "obsah", None)}, "metoda")
                c.add(label, ok and isinstance(value, list) and value == expected,
                      "Vraťte nový seznam aktuálních věcí ve správném pořadí.")
                return value if ok and isinstance(value, list) else []

            obsah(a, [], "První batoh je prázdný")
            obsah(b, [], "Druhý batoh je prázdný")
            expected = []
            for predmet in ["mapa", "voda", "mapa", "", "čelovka"]:
                expected.append(predmet)
                ok, value = c.call({"metoda": getattr(a, "pridej", None)}, "metoda", (predmet,))
                c.add("Přidání vrací nový počet", ok and type(value) is int and value == len(expected), "Přidejte i opakující se předmět a vraťte délku seznamu.")
                obsah(a, expected, "Věci se postupně uchovávají")
            obsah(b, [], "Věci se nesdílejí")
            snapshot = obsah(a, expected, "Vrácená kopie má aktuální obsah")
            snapshot.append("cizí věc")
            obsah(a, expected, "Změna kopie neovlivní batoh")
            snapshot.clear()
            obsah(a, expected, "Ani vymazání kopie neovlivní batoh")
            before = obsah(a, expected, "Snímek před dalším přidáním")
            ok, _ = c.call({"metoda": getattr(a, "pridej", None)}, "metoda", ("kompas",))
            c.add("Starší kopie se sama nemění", ok and before == expected, "Každý obsah() vrací samostatný seznam.")
            expected.append("kompas")
            ok, d = c.call(ns, "Batoh")
            c.add("Další instance vznikne", ok, "Další konstruktor nesmí poškodit starší batohy.")
            obsah(a, expected, "Nový batoh nemaže existující")
            c.add("Uložený seznam věcí", getattr(a, "veci", None) == expected, "Seznam uchovávejte v atributu veci.")
    except BaseException as exc:
        c.add("Práce s batohy bez chyby", False, f"Při ověření metod vznikla chyba {type(exc).__name__}: {exc}")
c.done()
