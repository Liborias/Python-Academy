from dilna_check import check
c = check()
c.defines_class("Bod")
ns = c.load()
cls = (ns or {}).get("Bod")
c.add("Bod je třída", isinstance(cls, type), "Definujte class Bod.")
if ns is not None and isinstance(cls, type):
    try:
        records = []
        coordinates = [(1, 2), (1, 2), (2, 2), (1, 3), (0, 0), (-1, 2), (4, -5)]
        for x, y in coordinates:
            ok, obj = c.call(ns, "Bod", (x, y))
            c.add("Vytvoření bodu", ok and isinstance(obj, cls), "Bod přijímá dvě souřadnice.")
            if ok and isinstance(obj, cls):
                records.append((obj, (x, y)))
        if len(records) == len(coordinates):
            c.add("Rovnost není identita", records[0][0] is not records[1][0], "Každý konstruktor vytváří vlastní instanci.")
            for a, xy in records:
                for b, uv in records:
                    expected = xy == uv
                    ok, value = c.call({"eq": lambda left, right: left == right}, "eq", (a, b))
                    c.add("Rovnost obou souřadnic", ok and type(value) is bool and value == expected,
                          "Porovnejte obě souřadnice a vraťte True nebo False.")
                    ok, value = c.call({"ne": lambda left, right: left != right}, "ne", (a, b))
                    c.add("Nerovnost", ok and type(value) is bool and value == (not expected), "Operátor != musí odpovídat hodnotové rovnosti.")
            for obj, (x, y) in records:
                c.add("Porovnání nemění stav", getattr(obj, "x", None) == x and getattr(obj, "y", None) == y,
                      "Porovnání nesmí upravovat souřadnice.")
            a, b = records[0][0], records[1][0]
            a.x = 8
            ok, value = c.call({"eq": lambda left, right: left == right}, "eq", (a, b))
            c.add("Změněná souřadnice ovlivní rovnost", ok and value is False, "Čtěte aktuální stav, ne uložený starý výsledek.")
            c.add("Druhý bod se nezměnil", b.x == 1 and b.y == 2, "Dva rovné body nejsou sdílený stav.")
            for other in [None, (8, 2), {"x": 8, "y": 2}, object()]:
                ok, value = c.call({"eq": getattr(a, "__eq__", None)}, "eq", (other,))
                c.add("Neznámý typ vrací NotImplemented", ok and value is NotImplemented,
                      "Před čtením atributů ověřte isinstance a pro cizí typ vraťte NotImplemented.")
            derived = type("OdvozenyBod", (cls,), {})
            ok, other = c.call({"vytvor": derived}, "vytvor", (8, 2))
            if ok:
                ok, value = c.call({"eq": getattr(a, "__eq__", None)}, "eq", (other,))
                c.add("Podpora odvozeného bodu", ok and value is True, "Použijte isinstance, ne pouze shodu přesných typů.")
            else:
                c.add("Odvozený bod lze vytvořit", False, "Zděděné chování Bod má pracovat s předanými souřadnicemi.")
            class DruhaStrana:
                def __eq__(self, other):
                    return "převzato"
            ok, value = c.call({"eq": lambda left, right: left == right}, "eq", (a, DruhaStrana()))
            c.add("Možnost pro druhou stranu", ok and value == "převzato", "NotImplemented umožní pokračování porovnání druhým objektem.")
    except BaseException as exc:
        c.add("Porovnání bez chyby", False, f"{type(exc).__name__}: {exc}")
c.done()
