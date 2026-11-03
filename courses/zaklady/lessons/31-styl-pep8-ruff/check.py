import ast
import re
from dilna_check import check
c = check()
tree = c.tree
if tree is not None:
    jmena = ["secti_seznam", "nejvetsi_rozdil", "pocet_sudych"]
    funkce = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    for j in jmena:
        c.add(f"Existuje funkce {j}", j in funkce, f"Vytvořte funkci {j}(seznam).")
    c.add("Každá funkce má docstring", bool(funkce) and all(ast.get_docstring(f) for f in funkce.values()),
          "Pod řádek def přidejte popis ve třech uvozovkách.")
    spatna = [f.name for f in funkce.values() if not re.fullmatch(r"[a-z_][a-z0-9_]*", f.name)]
    spatna += [a.arg for f in funkce.values() for a in f.args.args if not re.fullmatch(r"[a-z_][a-z0-9_]*", a.arg)]
    spatna += [n.id for n in ast.walk(tree) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store)
               and not re.fullmatch(r"[a-z_][a-z0-9_]*", n.id)]
    c.add("Jména funkcí, parametrů a proměnných jsou malými písmeny s podtržítky", not spatna,
          f"Špatná jména: {spatna}.")
    radky = c.code.split("\n")
    dlouhe = [i + 1 for i, r in enumerate(radky) if len(r) > 79]
    c.add("Řádky nejsou delší než 79 znaků", not dlouhe, f"Příliš dlouhé řádky: {dlouhe}.")
    c.add("Odsazení tvoří mezery, ne tabulátory", "\t" not in c.code, "Nahraďte tabulátory čtyřmi mezerami.")
    spatne_odsazeni = [i + 1 for i, r in enumerate(radky) if r.strip() and (len(r) - len(r.lstrip(" "))) % 4]
    c.add("Odsazení je násobek čtyř mezer", not spatne_odsazeni, f"Špatné odsazení na řádcích {spatne_odsazeni}.")
    zvlnene = []
    for f in funkce.values():
        if f.lineno > 1 and f is not tree.body[0]:
            zacatek = f.lineno - 1                      # index řádku s def
            while zacatek > 0 and radky[zacatek - 1].lstrip().startswith("#"):
                zacatek -= 1                            # komentář přímo nad def patří k funkci
            predchozi = [r.strip() for r in radky[max(0, zacatek - 2):zacatek]]
            if predchozi != ["", ""]:
                zvlnene.append(f.name)
    c.add("Před funkcemi jsou dva prázdné řádky", not zvlnene,
          f"U funkcí {zvlnene} chybí dva prázdné řádky před def.")
    jednoradkove = [f.name for f in funkce.values() if f.body[0].lineno == f.lineno]
    c.add("Tělo funkce je na samostatném řádku", not jednoradkove, f"Funkce {jednoradkove} má tělo na řádku s def.")
ns = c.load()
if ns is not None:
    c.returns(ns, "secti_seznam", ([1, 2, 3],), 6)
    c.returns(ns, "secti_seznam", ([],), 0)
    c.returns(ns, "nejvetsi_rozdil", ([4, 10, 1],), 9)
    c.returns(ns, "nejvetsi_rozdil", ([5],), 0)
    c.returns(ns, "nejvetsi_rozdil", ([-3, 3],), 6)
    c.returns(ns, "pocet_sudych", ([1, 2, 3, 4, 6],), 3)
    c.returns(ns, "pocet_sudych", ([1, 3],), 0)
    c.returns(ns, "pocet_sudych", ([],), 0)
c.done()
