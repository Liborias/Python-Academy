import ast
import os
import sys
sys.path.insert(0, os.getcwd())
from dilna_check import check
from had_potrava import HladovyHad

c = check()
c.defines_class("BezpecnyHad")
ns = c.load()
cls = (ns or {}).get("BezpecnyHad")
valid = isinstance(cls, type) and issubclass(cls, HladovyHad)
c.add("BezpecnyHad rozšiřuje HladovyHad", valid, "Použijte připravené růstové chování.")
node = next((n for n in (c.tree.body if c.tree else []) if isinstance(n, ast.ClassDef) and n.name == "BezpecnyHad"), None)
method = next((n for n in (node.body if node else []) if isinstance(n, ast.FunctionDef) and n.name == "krok"), None)
c.add("Platný krok využívá super", method is not None and bool(c.calls_in(method, "super")), "Po kontrole jednou navažte na předchozí krok.")
calls = []
original_krok = HladovyHad.krok
def tracked(self, food=None):
    calls.append((id(self), food))
    return original_krok(self, food)
HladovyHad.krok = tracked
try:
    if ns is not None and valid:
        cases = [
            (3, 3, [(1, 1), (1, 0), (0, 0), (0, 1)], (-1, 0), None),
            (3, 3, [(1, 1), (1, 0), (0, 0), (0, 1)], (-1, 0), (0, 1)),
            (3, 3, [(1, 1), (1, 0), (0, 0), (0, 1)], (0, -1), None),
            (4, 3, [(0, 1), (3, 1), (3, 0)], (-1, 0), None),
            (3, 4, [(1, 0), (1, 3), (0, 3)], (0, -1), None),
            (6, 4, [(4, 1), (3, 1)], (1, 0), (5, 1)),
            (6, 4, [(5, 0)], (1, 0), (0, 0)),
            (1, 1, [(0, 0)], (1, 0), None),
        ]
        records = []
        for width, height, points, direction, food in cases:
            had = cls(points, width, height)
            had.smer = direction
            before = list(had.body)
            x, y = before[0]
            head = ((x + direction[0]) % width, (y + direction[1]) % height)
            occupied = before if head == food else before[:-1]
            collision = head in occupied
            calls.clear()
            ok, value = c.call({"krok": had.krok}, "krok", (food,))
            c.add("Kontrola předchází skutečnému pohybu", calls == ([] if collision else [(id(had), food)]),
                  "Při kolizi základní krok vůbec nevolejte; jinak ho využijte jednou se stejnou potravou.")
            if collision:
                c.add("Kolize je ValueError bez změny těla", not ok and isinstance(value, ValueError) and had.body == before,
                      "Kolizi odmítněte před jakoukoli změnou těla.")
            else:
                expected = [head] + (before if head == food else before[:-1])
                c.add("Platný krok respektuje ocas a růst", ok and value == head and had.body == expected,
                      "Bez růstu může hlava vstoupit do odcházejícího ocasu; růst tento ocas zachová.")
            c.add("Zachovaná pravidla a vstup", points == before and had.sirka == width and had.vyska == height and had.smer == direction,
                  "Krok nemění původní seznam, směr nebo rozměry.")
            records.append((had, list(had.body)))
        for had, state in records:
            c.add("Nezávislé modely", had.body == state, "Každý had má vlastní stav.")
except BaseException as exc:
    c.add("Kolize lze ověřit", False, f"{type(exc).__name__}: {exc}")
finally:
    HladovyHad.krok = original_krok
c.done()
