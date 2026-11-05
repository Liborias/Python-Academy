import os
import sys
sys.path.insert(0, os.getcwd())
from dilna_check import check
from had_ovladani import RizenaHra
import had_panel

c = check()
c.defines_class("SnakeHra")
trace = []
original_draw = had_panel.vykresli_partii
def draw(partie, pen, food, text):
    trace.append(("draw", id(partie), partie.stav, partie.skore, list(partie.had.body), id(pen), id(food), id(text)))
had_panel.vykresli_partii = draw
ns = c.load()
cls = (ns or {}).get("SnakeHra")
valid = isinstance(cls, type) and issubclass(cls, RizenaHra)
c.add("SnakeHra využívá ovládání RizenaHra", valid, "Ponechte připravený konstruktor a základ ovládání.")
try:
    if ns is not None and valid:
        class Okno:
            def __init__(self):
                self.queue = []
                self.bindings = {}
                self.hook = None
            def update(self):
                trace.append(("update",))
                if self.hook is not None:
                    hook, self.hook = self.hook, None
                    hook()
            def ontimer(self, callback, delay):
                trace.append(("timer", delay))
                self.queue.append(callback)
            def onkey(self, callback, key):
                self.bindings[key] = callback
            def listen(self):
                pass

        def first(cells):
            return sorted(cells, key=lambda p: (p[1], p[0]))[0]
        def create(points, width=4, height=2, interval=75):
            window = Okno()
            pens = (object(), object(), object())
            game = cls(window, *pens, points, width, height, interval, first)
            return game, window
        def snapshot(game):
            p = game.partie
            return (id(p), list(p.had.body), p.had.smer, p.skore, p.potrava, p.stav, game.cekajici, game.generace)
        def fire(window):
            c.add("Právě jeden aktuální časovač", len(window.queue) == 1, "Každý platný tik plánuje právě jedno pokračování.")
            callback = window.queue.pop(0) if window.queue else None
            ok, _ = c.call({"callback": callback}, "callback")
            c.add("Callback lze zavolat", ok, "Časovači předejte volatelnou funkci bez okamžitého spuštění.")

        supplied = [(1, 0), (0, 0)]
        game, window = create(supplied)
        game.pripoj()
        c.add("Šipky a Enter jsou připojené", set(window.bindings) == {"Up", "Down", "Left", "Right", "Return"},
              "Zachovejte směrové metody a připojte restart na Return.")
        trace.clear()
        game.spust()
        c.add("První snímek nové partie", game.generace == 1 and game.spusteno and game.had is game.partie.had
              and game.had.body == supplied and game.partie.skore == 0 and game.cekajici is None and len(window.queue) == 1
              and [x[0] for x in trace] == ["draw", "update", "timer"] and trace[-1] == ("timer", 75),
              "Start vytvoří a zobrazí partii bez pohybu, pak založí jeden časovač instance.")
        supplied.append((99, 99))
        trace.clear()
        game.spust()
        c.add("Opakovaný start nezrychlí hru", trace == [] and len(window.queue) == 1, "Opakované spust se ihned vrátí.")
        trace.clear()
        fire(window)
        c.add("Tik využívá pravidla partie", game.partie.skore == 10 and game.had.body == [(2, 0), (1, 0), (0, 0)]
              and len(window.queue) == 1 and [x[0] for x in trace] == ["draw", "update", "timer"],
              "Proveďte jeden krok Partie, ne dodatečný krok starého časovače.")
        game.nastav_smer((0, 1))
        game.partie.skore = 50
        old = window.queue.pop(0)
        previous = game.partie
        generation = game.generace
        game.restart()
        c.add("Restart obnoví celý stav", game.generace == generation + 1 and game.partie is not previous
              and game.had is game.partie.had and game.had.body == [(1, 0), (0, 0)] and game.had.smer == (1, 0)
              and game.partie.skore == 0 and game.cekajici is None and len(window.queue) == 1,
              "Vytvořte novou partii z vlastní kopie počátku, vyprázdněte zatáčku a zvyšte generaci.")
        state = snapshot(game)
        trace.clear()
        ok, _ = c.call({"old": old}, "old")
        c.add("Starý tik už nezasáhne novou partii", ok and snapshot(game) == state and trace == [] and len(window.queue) == 1,
              "Callback musí nést tehdejší generaci a při nesouladu nic nedělat.")
        game.restart()
        game.restart()
        callbacks, window.queue = window.queue, []
        state = snapshot(game)
        for callback in callbacks[:-1]:
            trace.clear()
            ok, _ = c.call({"old": callback}, "old")
            c.add("Více rychlých restartů nezaloží více her", ok and snapshot(game) == state and trace == [] and not window.queue,
                  "Všechna dřívější volání se po novém restartu zneplatní.")
        ok, _ = c.call({"current": callbacks[-1] if callbacks else None}, "current")
        c.add("Nejnovější generace normálně pokračuje", ok and game.partie.skore == 10 and len(window.queue) == 1,
              "Z posledního platného tiku vznikne právě jedno pokračování.")

        for target in ["konec", "vyhra"]:
            points = [(1, 1), (1, 0), (0, 0), (0, 1)] if target == "konec" else [(0, 0)]
            ended, end_window = create(points, 3 if target == "konec" else 2, 3 if target == "konec" else 1)
            ended.spust()
            if target == "konec":
                ended.had.smer = (0, -1)
                ended.partie.potrava = (2, 2)
            trace.clear()
            fire(end_window)
            c.add("Konec i výhra zastaví plánování", ended.partie.stav == target and not end_window.queue
                  and [x[0] for x in trace] == ["draw", "update"], "Zobrazte konečný snímek bez dalšího časovače.")
            state = snapshot(ended)
            trace.clear()
            ended.tik()
            c.add("Ukončená hra nepřijímá pohyb", snapshot(ended) == state and trace == [] and ended.nastav_smer((0, 1)) is False,
                  "Po ukončení se další tik i šipka odmítnou.")
            ended.restart()
            c.add("Restart je možný i po konci", ended.partie.stav == "hra" and ended.partie.skore == 0 and len(end_window.queue) == 1,
                  "Enter obnovuje partii také po prohře nebo výhře.")
        full, full_window = create([(0, 0)], 1, 1)
        full.spust()
        c.add("Plná plocha se jen zobrazí", full.partie.stav == "vyhra" and not full_window.queue,
              "Naplanuj nezakládá časovač pro ukončenou partii.")

        reentrant, re_window = create([(1, 0), (0, 0)])
        reentrant.spust()
        re_window.hook = reentrant.restart
        fire(re_window)
        c.add("Restart během překreslení má jediný časovač", len(re_window.queue) == 1 and reentrant.partie.skore == 0
              and reentrant.had.body == [(1, 0), (0, 0)], "Po update plánujte jen při nezměněné generaci.")
        re_window.queue.clear()
        re_window.hook = reentrant.restart
        reentrant.restart()
        c.add("Vnořený restart se nezduplikuje", len(re_window.queue) == 1,
              "I restart ověří generaci po obnovení obrázku.")
        other, other_window = create([(2, 2)], 5, 4, 310)
        state = snapshot(game)
        trace.clear()
        other.spust()
        c.add("Dvě hry jsou nezávislé", snapshot(game) == state and trace[-1] == ("timer", 310) and len(other_window.queue) == 1,
              "Stav, rozměry, interval a časovače patří konkrétní hře.")
except BaseException as exc:
    c.add("Hotovou hru lze ověřit", False, f"{type(exc).__name__}: {exc}")
finally:
    had_panel.vykresli_partii = original_draw
r = c.turtle_run(keys=["Return", "Return", "Up", "Down"], ticks=2)
if c.turtle_no_error(r):
    c.add("Hotová hra má ovládání a jeden běžící řetězec", r.mainloop and set((r.handlers or {}).get("onkey", []))
          == {"Up", "Down", "Left", "Right", "Return"} and r.called("ontimer") == 5,
          "Připojte Enter a šipky; staré generace už nic neplánují.")
    c.add("Hlava po rychlých restartech zatáčí jednou", bool(r.stamps) and r.stamps[0][:2] == [-30, 50],
          "Po dvojím restartu a Up/Down se přijme jen Up a proběhnou dva kroky.")
    c.add("Viditelné skóre a nápověda", any(t["text"].startswith("Skóre: ") for t in (r.texts or []))
          and any("Enter" in t["text"] for t in (r.texts or [])), "Ponechte grafický panel partie.")
c.done()
