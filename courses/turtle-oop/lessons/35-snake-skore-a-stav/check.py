import os
import sys
sys.path.insert(0, os.getcwd())
from dilna_check import check

c = check()
c.defines_class("Partie")
ns = c.load()
cls = (ns or {}).get("Partie")
c.add("Partie je třída", isinstance(cls, type), "Ponechte třídu Partie s připraveným konstruktorem.")
try:
    if ns is not None and isinstance(cls, type):
        offers = []
        def first(cells):
            offers.append(list(cells))
            return sorted(cells, key=lambda p: (p[1], p[0]))[0]

        def snapshot(game):
            return (list(game.had.body), game.had.smer, game.skore, game.potrava, game.stav)

        records = []
        game = cls([(1, 0), (0, 0)], 4, 2, first)
        c.add("Počáteční stav", game.skore == 0 and game.stav == "hra" and game.potrava == (2, 0),
              "Partie má vlastní skóre nula a první volnou potravu.")
        for score, head, food, body in [
            (10, (2, 0), (3, 0), [(2, 0), (1, 0), (0, 0)]),
            (20, (3, 0), (0, 1), [(3, 0), (2, 0), (1, 0), (0, 0)]),
            (20, (0, 0), (0, 1), [(0, 0), (3, 0), (2, 0), (1, 0)]),
        ]:
            count = len(offers)
            eaten = game.potrava == head
            ok, value = c.call({"krok": game.krok}, "krok")
            c.add("Body, růst a průběh partie", ok and value == "hra" and game.stav == "hra" and game.skore == score
                  and game.had.body == body and game.potrava == food,
                  "Přidejte 10 bodů pouze po snědení a pokračujte nad aktuálním tělem.")
            c.add("Výběr potravy jen po snědení", len(offers) == count + int(eaten), "Při běžném pohybu potravu znovu nelosujte.")
            if eaten and len(offers) > count:
                c.add("Nové tělo už je obsazené", not set(game.had.body) & set(offers[-1]),
                      "Potravu vybírejte po růstu, ne ze starých buněk.")
        records.append((game, snapshot(game)))

        for width, height, points, direction, food, score, expected in [
            (2, 1, [(0, 0)], (1, 0), (1, 0), 10, "vyhra"),
            (3, 2, [(2, 0)], (1, 0), (0, 0), 10, "hra"),
            (3, 3, [(1, 1), (1, 0), (0, 0), (0, 1)], (0, -1), (2, 2), 0, "konec"),
        ]:
            game = cls(points, width, height, first)
            game.had.smer = direction
            game.potrava = food
            before = list(game.had.body)
            count = len(offers)
            ok, value = c.call({"krok": game.krok}, "krok")
            c.add("Krajní případy a ukončení", ok and value == expected and game.stav == expected and game.skore == score,
                  "Rozlište potravu (0, 0), poslední volnou buňku a kolizi.")
            if expected == "konec":
                c.add("Kolize zachová data", game.had.body == before and game.potrava == food and len(offers) == count,
                      "Po kolizi neprovádějte další krok, bodování nebo výběr.")
            if expected == "vyhra":
                c.add("Poslední potrava se započítala", game.potrava is None and len(game.had.body) == width * height,
                      "Nejprve započítejte růst a 10 bodů, pak oznamte plnou plochu.")
            if expected != "hra":
                state = snapshot(game)
                count = len(offers)
                for _ in range(3):
                    ok, value = c.call({"krok": game.krok}, "krok")
                    c.add("Ukončená partie už nic nemění", ok and value == expected and snapshot(game) == state and len(offers) == count,
                          "Konec a výhra se vracejí ihned, bez pohybu nebo nového bodování.")
            records.append((game, snapshot(game)))
        game = cls([(0, 0)], 1, 1, first)
        count = len(offers)
        ok, value = c.call({"krok": game.krok}, "krok")
        c.add("Plná plocha už při startu", ok and value == "vyhra" and game.skore == 0 and game.potrava is None
              and game.had.body == [(0, 0)] and len(offers) == count, "Plná počáteční plocha je výhra bez snědení potravy.")
        for other, state in records:
            c.add("Nezávislé partie", snapshot(other) == state, "Každá partie uchovává vlastní model, skóre, potravu a stav.")
except BaseException as exc:
    c.add("Pravidla partie lze ověřit", False, f"{type(exc).__name__}: {exc}")
c.done()
