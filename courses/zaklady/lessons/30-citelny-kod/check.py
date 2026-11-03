import ast
import re
from dilna_check import check
c = check()
tree = c.tree
if tree is not None:
    konstanty = [t.id for n in tree.body if isinstance(n, ast.Assign) for t in n.targets
                 if isinstance(t, ast.Name) and re.fullmatch(r"[A-Z][A-Z0-9_]*", t.id)]
    konstanty += [n.target.id for n in tree.body if isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name)
                  and re.fullmatch(r"[A-Z][A-Z0-9_]*", n.target.id)]
    c.add("Alespoň tři konstanty velkými písmeny na úrovni souboru", len(set(konstanty)) >= 3,
          f"Našel jsem {len(set(konstanty))}. Například CENA_ZA_KM = 3.")
    fn = c.function("cena_jizdenky")
    if fn is None:
        c.add("Funkce cena_jizdenky existuje", False, "Vytvořte funkci cena_jizdenky(vek, km).")
    else:
        parametry = [a.arg for a in fn.args.args]
        c.add("Parametry mají smysluplná jména", len(parametry) == 2 and all(len(p) > 1 for p in parametry),
              "Funkce má dva parametry a jejich jména musí mít víc než jedno písmeno.")
        cisla = [n.value for n in ast.walk(fn) if isinstance(n, ast.Constant)
                 and isinstance(n.value, (int, float)) and not isinstance(n.value, bool)]
        divna = [x for x in cisla if x not in (0, 1)]
        c.add("Ve funkci nejsou magická čísla", not divna,
              f"Ve funkci jsou čísla {divna}. Přesuňte je do konstant na začátku souboru.")
ns = c.load()
if ns is not None:
    for args, ocek in (((3, 100), 0), ((5, 10), 0), ((6, 10), 15.0), ((17, 10), 15.0), ((18, 10), 30),
                       ((40, 10), 30), ((64, 7), 21), ((65, 10), 15.0), ((80, 0), 0), ((30, 25), 75)):
        c.returns(ns, "cena_jizdenky", args, ocek)
c.done()
