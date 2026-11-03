import ast
from dilna_check import check
c = check()
ns = c.load()
names = ["Zaklad", "Levy", "Pravy", "Oba", "Obracene"]
classes = {name: (ns or {}).get(name) for name in names}
for name, cls in classes.items():
    c.defines_class(name)
    c.add(f"{name} je třída", isinstance(cls, type), f"Definujte class {name}.")
for name in ["Levy", "Pravy"]:
    node = next((n for n in (c.tree.body if c.tree else []) if isinstance(n, ast.ClassDef) and n.name == name), None)
    method = next((n for n in (node.body if node else []) if isinstance(n, ast.FunctionDef) and n.name == "cesta"), None)
    c.add(f"{name}.cesta používá super", method is not None and bool(c.calls_in(method, "super")), "V obou větvích skutečně volejte super().")
if ns is not None and all(isinstance(cls, type) for cls in classes.values()):
    try:
        base, left, right, both, reverse = [classes[name] for name in names]
        c.add("Společný základ", issubclass(left, base) and issubclass(right, base), "Levy a Pravy dědí ze Zaklad.")
        c.add("Správné pořadí MRO", both.__mro__[:4] == (both, left, right, base)
              and reverse.__mro__[:4] == (reverse, right, left, base), "Oba a Obracene mají různá pořadí základů.")
        expected = {"Zaklad": ["Zaklad"], "Levy": ["Levy", "Zaklad"], "Pravy": ["Pravy", "Zaklad"],
                    "Oba": ["Levy", "Pravy", "Zaklad"], "Obracene": ["Pravy", "Levy", "Zaklad"]}
        objects = {}
        for name in names:
            ok, obj = c.call(ns, name)
            c.add("Instanci lze vytvořit", ok and isinstance(obj, classes[name]), "Konstruktor zde další argumenty nepotřebuje.")
            if ok:
                objects[name] = obj
                ok, result = c.call({"cesta": getattr(obj, "cesta", None)}, "cesta")
                c.add("Cesta podle MRO", ok and isinstance(result, list) and result == expected[name], f"Očekávám {expected[name]!r}.")
                if ok and isinstance(result, list):
                    result.append("cizí změna")
                    ok, again = c.call({"cesta": getattr(obj, "cesta", None)}, "cesta")
                    c.add("Každé volání vrací nový seznam", ok and again == expected[name], "Úprava dřívějšího výsledku nemá změnit další volání.")
        original = base.cesta
        calls = []
        def changed(self):
            calls.append(id(self))
            return ["OVĚŘENO"]
        try:
            base.cesta = changed
            for name in ["Levy", "Pravy", "Oba", "Obracene"]:
                obj = objects.get(name)
                if obj is None:
                    continue
                calls.clear()
                ok, result = c.call({"cesta": getattr(obj, "cesta", None)}, "cesta")
                value = expected[name][:-1] + ["OVĚŘENO"]
                c.add("Spolupráce i po změně základu", ok and result == value, "Výsledek základní metody využijte, neopisujte její text.")
                c.add("Základ se volá jednou pro stejný objekt", calls == [id(obj)], "Použijte spolupracující řetězec super, ne samostatný průchod oběma větvemi.")
        finally:
            base.cesta = original
    except BaseException as exc:
        c.add("Ověření MRO bez chyby", False, f"{type(exc).__name__}: {exc}")
c.done()
