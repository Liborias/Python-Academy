import os
import sys
sys.path.insert(0, os.getcwd())
from dilna_check import check
from had_model import Had

c = check()
ns = c.load()
if ns is not None:
    try:
        for width, height, point in [(6, 4, (0, 0)), (6, 4, (5, 3)), (5, 3, (2, 1)),
                                     (1, 1, (0, 0)), (7, 8, (1, 6)), (20, 16, (8, 8))]:
            x, y = point
            expected = ((x - (width - 1) / 2) * 20, (y - (height - 1) / 2) * 20)
            c.returns(ns, "na_pixely", (point, width, height), expected)

        class Pero:
            def __init__(self):
                self.calls = []
                self.stamps = [(999, 999, "starý otisk")]
                self.position = None
                self.tint = None
            def clear(self):
                self.calls.append("clear")
                self.stamps.clear()
            def goto(self, *pos):
                self.position = tuple(pos[0]) if len(pos) == 1 else tuple(pos)
                self.calls.append("goto")
            def color(self, value):
                self.tint = value
                self.calls.append("color")
            def stamp(self):
                self.stamps.append((*self.position, self.tint))
                self.calls.append("stamp")

        for points, width, height in [([(8, 8), (7, 8), (6, 8)], 20, 16),
                                      ([(0, 0)], 1, 1), ([(5, 0), (4, 0), (4, 1), (3, 1)], 7, 3)]:
            had = Had(points, width, height)
            state = (list(had.body), had.sirka, had.vyska, had.smer)
            pen = Pero()
            for _ in range(2):
                pen.calls.clear()
                expected = [((x - (width - 1) / 2) * 20, (y - (height - 1) / 2) * 20,
                             "yellow" if i == 0 else "green") for i, (x, y) in enumerate(points)]
                ok, value = c.call(ns, "vykresli", (had, pen))
                c.add("Otisky v aktuálních buňkách a správných barvách", ok and pen.stamps == expected,
                      "Převeďte každou buňku a otiskněte žlutou hlavu, pak zelené tělo.")
                c.add("Nejprve jednou smazat", bool(pen.calls) and pen.calls[0] == "clear" and pen.calls.count("clear") == 1,
                      "Před každým snímkem jednou zavolejte clear na předaném peru.")
                c.add("Kreslení nemění model", (had.body, had.sirka, had.vyska, had.smer) == state,
                      "Neprovádějte krok ani změnu uložených buněk.")
    except BaseException as exc:
        c.add("Kreslení lze ověřit bez chyby", False, f"{type(exc).__name__}: {exc}")
r = c.turtle_run()
if c.turtle_no_error(r):
    c.add("Otevřené okno s černým pozadím", r.mainloop and r.bgcolor == "black", "Ponechte přípravu a hlavní smyčku okna.")
    c.add("Tři viditelné články bez spojovacích čar", len(r.stamps or []) == 3 and not r.segments,
          "Použijte otisky čtvercového pera se zvednutým perem.")
    c.add("Hotový snímek se zobrazí", r.called("update") >= 1, "Po vykreslení proveďte okno.update().")
c.done()
