import os
import sys
sys.path.insert(0, os.getcwd())
from dilna_check import check
from had_model import Had
import had_pohled

c = check()
c.defines_class("Hra")
trace = []
original = had_pohled.vykresli
def draw(had, pen):
    trace.append(("draw", id(had), id(pen), list(had.body)))
had_pohled.vykresli = draw
ns = c.load()
cls = (ns or {}).get("Hra")
c.add("Hra je třída", isinstance(cls, type), "Ponechte třídu Hra.")
try:
    if ns is not None and isinstance(cls, type):
        class Okno:
            def __init__(self):
                self.queue = []
            def update(self):
                trace.append(("update",))
            def ontimer(self, callback, delay):
                trace.append(("timer", delay))
                self.queue.append((callback, delay))

        games = []
        for interval, width, height in [(160, 20, 16), (75, 7, 5)]:
            had = Had([(2, 2), (1, 2), (0, 2)], width, height)
            pen, window = object(), Okno()
            ok, game = c.call(ns, "Hra", (window, had, pen, interval))
            c.add("Vytvoření hry", ok and isinstance(game, cls), "Uložte vlastní okno, model, pero a interval.")
            if not ok:
                continue
            trace.clear()
            start = list(had.body)
            ok, _ = c.call({"spust": getattr(game, "spust", None)}, "spust")
            expected = [("draw", id(had), id(pen), start), ("update",), ("timer", interval)]
            c.add("Start zobrazí počáteční stav a založí jeden časovač", ok and trace == expected
                  and had.body == start and len(window.queue) == 1, "Start nekoná krok; kreslí, provede update a naplánuje tik.")
            trace.clear()
            ok, _ = c.call({"spust": getattr(game, "spust", None)}, "spust")
            c.add("Opakovaný start nic nepřidá", ok and trace == [] and len(window.queue) == 1 and had.body == start,
                  "Použijte příznak spusteno, aby nevzniklo více řetězců časovače.")
            expected_body = start
            for _ in range(5):
                if len(window.queue) != 1:
                    c.add("Právě jeden čekající tik", False, "Každý tik plánuje právě jedno pokračování.")
                    break
                callback, delay = window.queue.pop(0)
                x, y = expected_body[0]
                expected_body = [((x + 1) % width, y)] + expected_body[:-1]
                trace.clear()
                ok, _ = c.call({"callback": callback}, "callback")
                expected = [("draw", id(had), id(pen), expected_body), ("update",), ("timer", interval)]
                c.add("Tik: krok, kreslení, update, jeden časovač", ok and had.body == expected_body
                      and trace == expected and len(window.queue) == 1, "Předejte volatelný tik a využijte aktuální model i interval instance.")
            games.append((had, list(had.body), window, pen, interval))
        if len(games) == 2 and len(games[0][2].queue) == 1:
            had, state, window, pen, interval = games[0]
            callback, _ = window.queue.pop(0)
            x, y = state[0]
            expected_body = [((x + 1) % had.sirka, y)] + state[:-1]
            trace.clear()
            ok, _ = c.call({"callback": callback}, "callback")
            expected = [("draw", id(had), id(pen), expected_body), ("update",), ("timer", interval)]
            c.add("První hra funguje i po vytvoření druhé", ok and had.body == expected_body and trace == expected
                  and len(window.queue) == 1 and games[1][0].body == games[1][1],
                  "Model, pero, okno i interval patří konkrétní instanci.")
except BaseException as exc:
    c.add("Časovač lze ověřit bez chyby", False, f"{type(exc).__name__}: {exc}")
finally:
    had_pohled.vykresli = original
r = c.turtle_run(ticks=3)
if c.turtle_no_error(r):
    c.add("Běží smyčka a opakovaný časovač", r.mainloop and r.called("ontimer") == 4,
          "Spusťte hru a v každém tiku naplánujte právě jeden další.")
    c.add("Model se opravdu překreslil po třech krocích", [s[:2] for s in (r.stamps or [])] == [[30, 10], [10, 10], [-10, 10]],
          "Ponechte výchozí tělo a propojte pohyb s vykreslením.")
c.done()
