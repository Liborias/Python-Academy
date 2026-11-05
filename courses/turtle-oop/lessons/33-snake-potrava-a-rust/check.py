import ast
import os
import sys
sys.path.insert(0, os.getcwd())
from dilna_check import check
from had_model import Had

c = check()
c.defines_class("HladovyHad")
ns = c.load()
cls = (ns or {}).get("HladovyHad")
valid = isinstance(cls, type) and issubclass(cls, Had)
c.add("HladovyHad rozšiřuje Had", valid, "Použijte připravenou základní třídu Had.")
node = next((n for n in (c.tree.body if c.tree else []) if isinstance(n, ast.ClassDef) and n.name == "HladovyHad"), None)
method = next((n for n in (node.body if node else []) if isinstance(n, ast.FunctionDef) and n.name == "krok"), None)
c.add("Růst využívá super", method is not None and bool(c.calls_in(method, "super")), "Navazujte na základní krok pomocí super.")
calls = []
original_krok = Had.krok
def tracked(self):
    calls.append(id(self))
    return original_krok(self)
Had.krok = tracked
try:
    if ns is not None and valid:
        records = []
        for width, height, points, direction, food in [
            (6, 4, [(4, 1), (3, 1), (2, 1)], (1, 0), (5, 1)),
            (6, 4, [(4, 1), (3, 1), (2, 1)], (1, 0), (1, 3)),
            (6, 4, [(5, 0)], (1, 0), (0, 0)),
            (2, 3, [(1, 2)], (0, 1), (1, 0)),
            (1, 1, [(0, 0)], (1, 0), None),
        ]:
            had = cls(points, width, height)
            original_points = list(points)
            had.smer = direction
            x, y = points[0]
            head = ((x + direction[0]) % width, (y + direction[1]) % height)
            expected = [head] + (points if head == food else points[:-1])
            calls.clear()
            ok, value = c.call({"krok": had.krok}, "krok", (food,))
            c.add("Základní krok proběhl právě jednou", calls == [id(had)], "Použijte základní krok pro tentýž objekt právě jednou.")
            c.add("Pohyb a růst odpovídají potravě", ok and value == head and had.body == expected,
                  "Při snědení zachovejte původní ocas; jinak délku neměňte.")
            c.add("Pravidla i vstup zůstávají", had.smer == direction and had.sirka == width and had.vyska == height
                  and points == original_points, "Neměňte směr, rozměry nebo vstupní seznam.")
            before = list(had.body)
            x, y = before[0]
            next_head = ((x + direction[0]) % width, (y + direction[1]) % height)
            ok, value = c.call({"krok": had.krok}, "krok")
            c.add("Další krok bez potravy neroste", ok and value == next_head and had.body == [next_head] + before[:-1],
                  "Růst se týká jen kroku, ve kterém se snědla potrava.")
            records.append((had, list(had.body)))
        for had, state in records:
            c.add("Samostatné instance", had.body == state, "Těla různých hadů se nesdílejí.")
    if ns is not None:
        for width, height, points in [(3, 2, [(0, 0), (1, 0)]), (1, 1, [(0, 0)]),
                                      (2, 1, [(0, 0)]), (2, 3, [(1, 2), (0, 1)])]:
            had = Had(points, width, height)
            state = (list(had.body), had.smer, had.sirka, had.vyska)
            expected = {(x, y) for y in range(height) for x in range(width)} - set(points)
            for choose_last in [False, True]:
                offers = []
                def choose(cells):
                    offers.append(list(cells))
                    return sorted(cells)[-1 if choose_last else 0]
                ok, value = c.call(ns, "vyber_potravu", (had, choose))
                wanted = sorted(expected)[-1 if choose_last else 0] if expected else None
                c.add("Úplný výběr z volných buněk", ok and value == wanted and
                      ((not expected and offers == []) or (len(offers) == 1 and len(offers[0]) == len(expected) and set(offers[0]) == expected)),
                      "Nabídněte každou volnou buňku jednou; při plné ploše nevolejte výběr a vraťte None.")
                c.add("Výběr nemění model", (had.body, had.smer, had.sirka, had.vyska) == state,
                      "Potrava se vybírá čtením plochy, nikoli pohybem hada.")
        had = Had([(0, 0)], 4, 3)
        for _ in range(20):
            ok, value = c.call(ns, "vyber_potravu", (had,))
            c.add("Výchozí výběr vrací volnou buňku", ok and value in {(x, y) for x in range(4) for y in range(3)} - {(0, 0)},
                  "Výchozí random.choice vybírá z připravených volných míst.")
except BaseException as exc:
    c.add("Potravu a růst lze ověřit", False, f"{type(exc).__name__}: {exc}")
finally:
    Had.krok = original_krok
c.done()
