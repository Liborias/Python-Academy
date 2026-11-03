import ast
from dilna_check import check
c = check()
c.uses_call("randint", "Náhodné x získáte voláním random.randint(0, 368).")
c.add("Hvězdy jsou v seznamu a procházejí se cyklem for", c.tree is not None and any(isinstance(n, ast.For) and isinstance(n.iter, ast.Name) for n in ast.walk(c.tree)),
      "Uložte hvězdy do seznamu a projděte ho cyklem for (pro pohyb i pro kreslení).")
def _je_rand(n):
    return (isinstance(n, ast.Call) and isinstance(n.func, (ast.Attribute, ast.Name)) and getattr(n.func, "attr", getattr(n.func, "id", "")) == "randint"
            and [getattr(a, "value", None) for a in n.args] == [0, 368])
c.add("Náhodné x je random.randint(0, 368)", c.tree is not None and any(_je_rand(n) for n in ast.walk(c.tree)), "Nové x hvězdy zvolte voláním random.randint(0, 368).")
Z = (255, 220, 0)
HV = [(40 + i * 80, -i * 60) for i in range(5)]
def stred(i, k):
    return (HV[i][0] + 16, HV[i][1] + 3 * k + 16)
body = {f"hvězda {i}": stred(i, 60) for i in range(4)}
body["hvězda 4 (začíná nejvýš)"] = stred(4, 100)
r = c.pygame_run(frames=145, pixels=list(body.values()), colors=[Z + (0, 60, 400, 80), Z + (0, 0, 400, 300)])
if c.pg_no_error(r):
    c.add("Titulek je „Déšť hvězd“", r.caption == "Déšť hvězd", f"Titulek je {r.caption!r}.")
    for jmeno, bod in body.items():
        k = 100 if "4" in jmeno else 60
        c.add(f"Po {k} snímcích je {jmeno} u bodu {bod}", r.pixel(bod, k) == Z, f"V bodě {bod} má být po {k} snímcích střed: {jmeno}, ale je tam {r.pixel(bod, k)}.")
    c.add("Spadlá hvězda se vrací těsně nad okno (rect.bottom = 0)", 0 < r.color_count(Z, 101, (0, 0, 400, 300)) < 1500, "Hvězda, která spadla pod okno, se má vrátit tak, aby její spodní okraj byl v 0 (rect.bottom = 0), ne celá viditelná nahoře.")
    c.add("Hvězda, která spadla, se vrátí nahoře", r.color_count(Z, 140, (0, 60, 400, 80)) > 150, "Po spadnutí pod okno se hvězda má objevit znovu nahoře (rect.bottom = 0).")
c.done()
