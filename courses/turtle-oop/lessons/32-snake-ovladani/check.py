import ast
import os
import sys
sys.path.insert(0, os.getcwd())
from dilna_check import check
from had_model import Had
from had_hra import Hra

c = check()
c.defines_class("RizenaHra")
ns = c.load()
cls = (ns or {}).get("RizenaHra")
c.add("RizenaHra dědí z Hra", isinstance(cls, type) and issubclass(cls, Hra), "Rozšiřte připravenou třídu Hra.")
node = next((n for n in (c.tree.body if c.tree else []) if isinstance(n, ast.ClassDef) and n.name == "RizenaHra"), None)
method = next((n for n in (node.body if node else []) if isinstance(n, ast.FunctionDef) and n.name == "tik"), None)
c.add("Rozšířený tik používá super", method is not None and bool(c.calls_in(method, "super")), "Po zpracování směru navažte pomocí super().tik().")
trace = []
original = Hra.tik
def base_tick(self):
    trace.append((id(self), self.had.smer))
    self.had.krok()
Hra.tik = base_tick
try:
    if ns is not None and isinstance(cls, type) and issubclass(cls, Hra):
        class Okno:
            def __init__(self):
                self.bindings = {}
                self.listens = 0
            def onkey(self, callback, key):
                self.bindings[key] = callback
            def listen(self):
                self.listens += 1

        def create(direction=(1, 0)):
            had = Had([(8, 8), (7, 8), (6, 8)])
            had.smer = direction
            window = Okno()
            game = cls(window, had, object(), 95)
            return game, had, window

        for direction in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            game, had, window = create(direction)
            initial = list(had.body)
            for invalid in [direction, (-direction[0], -direction[1]), (0, 0), (1, 1), (2, 0), None, "Up"]:
                ok, value = c.call({"nastav": game.nastav_smer}, "nastav", (invalid,))
                c.add("Neplatný, stejný a opačný směr se odmítnou", ok and value is False and game.cekajici is None
                      and had.smer == direction and had.body == initial, "Odmítnutá změna nesmí obsadit čekající místo ani měnit stav.")
            accepted = (-direction[1], direction[0])
            ok, value = c.call({"nastav": game.nastav_smer}, "nastav", (accepted,))
            c.add("Kolmá změna pouze čeká", ok and value is True and game.cekajici == accepted
                  and had.smer == direction and had.body == initial, "Směr uložte do cekajici; zatím neprovádějte pohyb.")
            for second in [accepted, (-accepted[0], -accepted[1]), direction, (-direction[0], -direction[1])]:
                ok, value = c.call({"nastav": game.nastav_smer}, "nastav", (second,))
                c.add("Druhý stisk nepřepíše čekající změnu", ok and value is False and game.cekajici == accepted
                      and had.smer == direction and had.body == initial,
                      "Mezi tiky přijměte nejvýš jednu kolmou změnu; i další kolmý směr musí počkat.")
            trace.clear()
            ok, _ = c.call({"tik": game.tik}, "tik")
            x, y = initial[0]
            new_body = [((x + accepted[0]) % 20, (y + accepted[1]) % 16)] + initial[:-1]
            c.add("Tik použije změnu, uvolní ji a naváže právě jednou", ok and game.cekajici is None
                  and had.smer == accepted and had.body == new_body and trace == [(id(game), accepted)],
                  "Nejprve změňte směr, vyprázdněte cekajici a pak jednou zavolejte základní tik.")
            ok, value = c.call({"nastav": game.nastav_smer}, "nastav", ((-direction[0], -direction[1]),))
            c.add("Po tiku lze přijmout další zatáčku", ok and value is True,
                  "Po provedení kroku už je další kolmá změna dovolená.")

        for key, target in {"Up": (0, 1), "Down": (0, -1), "Left": (-1, 0), "Right": (1, 0)}.items():
            direction = (1, 0) if target[0] == 0 else (0, 1)
            game, had, window = create(direction)
            state = list(had.body)
            ok, _ = c.call({"pripoj": game.pripoj}, "pripoj")
            c.add("Čtyři šipky a listen", ok and set(window.bindings) == {"Up", "Down", "Left", "Right"} and window.listens == 1
                  and game.cekajici is None and had.smer == direction and had.body == state,
                  "Připojte čtyři metody bez závorek a zapněte listen; připojení nic neposouvá.")
            ok, _ = c.call({"key": window.bindings.get(key)}, "key")
            c.add("Šipka připraví odpovídající směr", ok and game.cekajici == target and had.smer == direction and had.body == state,
                  "Šipka pouze uloží čekající změnu a neprovádí krok.")
        a, had_a, _ = create()
        b, had_b, _ = create()
        a.nastav_smer((0, 1))
        trace.clear()
        b.tik()
        c.add("Samostatné instance a tik bez změny", a.cekajici == (0, 1) and b.cekajici is None
              and had_a.body[0] == (8, 8) and had_b.body[0] == (9, 8) and trace == [(id(b), (1, 0))],
              "I bez nové šipky proběhne běžný tik; čekající změny nejsou společné.")
except BaseException as exc:
    c.add("Ovládání lze ověřit bez chyby", False, f"{type(exc).__name__}: {exc}")
finally:
    Hra.tik = original
r = c.turtle_run(keys=["Up", "Left"], ticks=2)
if c.turtle_no_error(r):
    c.add("Ovládání je skutečně připojené", set((r.handlers or {}).get("onkey", [])) == {"Up", "Down", "Left", "Right"}
          and r.called("listen") >= 1 and r.mainloop, "Hlavní program musí připojit ovládání a spustit hru.")
    c.add("Rychlé Up a Left vedou k pohybu nahoru", [s[:2] for s in (r.stamps or [])] == [[-30, 50], [-30, 30], [-30, 10]],
          "Do prvního tiku se použije jen první platná zatáčka; další tik pokračuje nahoru.")
c.done()
