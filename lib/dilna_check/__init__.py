"""dilna_check: pomocná knihovna pro kontrolu cvičení.

Použití v lekci (check.py):

    from dilna_check import check
    c = check()
    r = c.run(stdin="Eva\\n")                      # spustí studentův program v podprocesu
    c.no_error(r)
    c.output_contains(r, "Ahoj Eva", "Program má pozdravit zadané jméno.")
    c.uses_call("input")                           # kontrola struktury kódu (AST)
    ns = c.load()                                  # načte kód jako modul (bez bloku __main__)
    c.returns(ns, "secti", (2, 3), 5)              # zavolá studentovu funkci
    c.done()                                       # zapíše výsledek (vždy na konec)

Kontroly nikdy neshodí celý běh: každá vloží do výsledku řádek {name, ok, msg}.
Pygame bez okna: c.pygame_run(frames=5, pixels=[(10, 10)], events={2: [{"type": "QUIT"}]}) spustí program
s ovladačem "dummy" a vrátí PgResult (barvy pixelů, volání pygame.draw, texty, zvuky, skončil-li program).
Úvodní Tkinter: c.tk_run(actions=[{"action": "click", "text": "Potvrdit"}]) vrátí
TkResult se stavy widgetů před akcemi a po nich. Náhrada podporuje pouze části
Tkinteru potřebné v úvodních lekcích; skutečný vzhled se ověřuje zvlášť s Tk.
load() spouští kód s __name__ == "student", takže blok `if __name__ == "__main__":`
se přeskočí. Kód vytvářející okno mimo tento blok se při load() provede také.
"""
import ast
import builtins
import contextlib
import io
import json
import math
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

__all__ = ["check", "Checker", "RunResult", "PgResult", "TurtleResult", "TkResult"]


@dataclass
class TkResult:
    """Stav widgetů před akcemi a po nich; nejde o snímek skutečného Tk."""
    snapshots: list | None = None
    mainloops: int = 0
    error: dict | None = None
    timed_out: bool = False
    crashed: str = ""
    out: str = ""
    err: str = ""

    def widgets(self, kind=None, index=0):
        states = self.snapshots or []
        if not states or not -len(states) <= index < len(states):
            return []
        return [w for w in states[index] if kind is None or w["kind"] == kind]


@dataclass
class RunResult:
    out: str
    err: str
    exit: int | None
    timed_out: bool = False


@dataclass
class PgResult:
    """Výsledek c.pygame_run(): co program studenta s pygame udělal během několika snímků."""
    frames: int = 0
    ended: bool = False
    error: dict | None = None
    timed_out: bool = False
    crashed: str = ""
    size: list | None = None
    caption: str | None = None
    shots: list | None = None
    draws: list | None = None
    texts: list | None = None
    images: list | None = None
    sounds: list | None = None
    music: list | None = None
    fps: list | None = None
    out: str = ""

    def pixel(self, pos, frame: int = -1):
        """Barva (r, g, b) pixelu pos ve snímku frame (výchozí poslední). Pozice musela být zadána v pygame_run."""
        if not self.shots:
            return None
        v = self.shots[frame]["pixels"].get(f"{pos[0]},{pos[1]}")
        return tuple(v) if v else None

    def color_count(self, color, frame: int = -1, region=None) -> int:
        """Počet pixelů dané barvy ve snímku (celé okno, nebo jen region = (x, y, šířka, výška)).
        Barva (a případně region) musela být zadána v pygame_run: colors=[(r, g, b)] nebo [(r, g, b, x, y, š, v)]."""
        if not self.shots:
            return 0
        key = ",".join(map(str, color)) + (("@" + ",".join(map(str, region))) if region else "")
        return self.shots[frame]["colors"].get(key, 0)

    def drew(self, name: str | None = None) -> list:
        return [d for d in (self.draws or []) if name is None or d["name"] == name]

    def rendered(self, text: str) -> bool:
        return any(text in t["text"] for t in (self.texts or []))


@dataclass
class TurtleResult:
    """Výsledek c.turtle_run(): co želva nakreslila. Souřadnice jako v turtle: střed okna (0, 0), osa y nahoru."""
    segments: list | None = None     # [x1, y1, x2, y2, barva, tloušťka, číslo želvy, zdroj ("move", "goto", "circle")]
    fills: list | None = None        # [{"color", "points", "t"}]
    dots: list | None = None         # [x, y, velikost, barva, želva]
    texts: list | None = None        # [{"text", "x", "y", "align", "font", "color", "t"}]
    stamps: list | None = None
    calls: dict | None = None        # počet volání jednotlivých funkcí
    turtles: list | None = None      # konečný stav každé želvy (x, y, heading, pendown, visible, shape, pencolor, fillcolor, width, speed)
    bgcolor: str | None = None
    title: str | None = None
    screen: list | None = None
    handlers: dict | None = None
    ended: bool = False
    mainloop: bool = False
    error: dict | None = None
    timed_out: bool = False
    crashed: str = ""
    out: str = ""
    ops: int = 0

    def called(self, name: str) -> int:
        return (self.calls or {}).get(name, 0)

    def length(self, color=None) -> float:
        """Celková délka nakreslených čar (volitelně jen dané barvy)."""
        return sum(math.hypot(s[2] - s[0], s[3] - s[1]) for s in (self.segments or []) if color is None or s[4] == color)

    def colors(self) -> set:
        return {s[4] for s in (self.segments or [])}

    def widths(self) -> set:
        return {s[5] for s in (self.segments or [])}

    def covers(self, point, tol: float = 1.5, color=None) -> bool:
        """Prochází nakreslená čára do vzdálenosti tol od bodu (volitelně jen dané barvy)?"""
        px, py = point
        for x1, y1, x2, y2, col, *_ in (self.segments or []):
            if color is not None and col != color:
                continue
            dx, dy = x2 - x1, y2 - y1
            ln = dx * dx + dy * dy
            t = 0 if ln == 0 else max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / ln))
            if math.hypot(px - (x1 + t * dx), py - (y1 + t * dy)) <= tol:
                return True
        return False

    def bbox(self):
        """(xmin, ymin, xmax, ymax) všech nakreslených čar, nebo None."""
        pts = [(s[0], s[1]) for s in (self.segments or [])] + [(s[2], s[3]) for s in (self.segments or [])]
        if not pts:
            return None
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        return (min(xs), min(ys), max(xs), max(ys))

    def corners(self, min_turn: float = 1.0, src=("move", "goto")) -> list:
        """Rohy: body, kde na sebe navazují dvě úsečky a směr se změní o víc než min_turn stupňů (kruhy se ve výchozím stavu přeskočí)."""
        segs = [s for s in (self.segments or []) if src is None or s[7] in src]
        out = []
        for a, b in zip(segs, segs[1:]):
            if math.hypot(a[2] - b[0], a[3] - b[1]) > 0.01:
                continue
            a1, a2 = math.atan2(a[3] - a[1], a[2] - a[0]), math.atan2(b[3] - b[1], b[2] - b[0])
            if abs((math.degrees(a2 - a1) + 180) % 360 - 180) > min_turn:
                out.append((round(a[2], 2), round(a[3], 2)))
        return out

    def fill_area(self, color=None) -> float:
        """Součet ploch vyplněných mnohoúhelníků (volitelně jen dané barvy)."""
        tot = 0.0
        for f in (self.fills or []):
            if color is not None and f["color"] != color:
                continue
            p = f["points"]
            tot += abs(sum(p[i][0] * p[(i + 1) % len(p)][1] - p[(i + 1) % len(p)][0] * p[i][1] for i in range(len(p)))) / 2
        return tot


class _NoInput:
    """Náhrada input(): bere řádky z předem zadaného vstupu, po vyčerpání vyhodí EOFError."""

    def __init__(self, text: str):
        self.lines = text.splitlines()

    def __call__(self, prompt=""):
        print(prompt, end="")
        if not self.lines:
            raise EOFError("Program chce další vstup, který kontrola nezadala.")
        return self.lines.pop(0)


class Checker:
    def __init__(self):
        self.student = Path(os.environ["DILNA_STUDENT"])
        self.result_path = Path(os.environ["DILNA_RESULT"])
        self.data_dir = Path(os.environ.get("DILNA_DATA", "."))
        self.results: list[dict] = []
        self._code: str | None = None
        self._tree: ast.AST | None = None
        self.last_output = ""

    # ---------- zápis výsledků ----------
    def add(self, name: str, ok: bool, msg: str = "") -> bool:
        self.results.append({"name": name, "ok": bool(ok), "msg": "" if ok else msg})
        return bool(ok)

    def done(self):
        ok = bool(self.results) and all(r["ok"] for r in self.results)
        self.result_path.write_text(json.dumps({"ok": ok, "results": self.results}, ensure_ascii=False),
                                    encoding="utf-8")

    # ---------- kód ----------
    @property
    def code(self) -> str:
        if self._code is None:
            self._code = self.student.read_text(encoding="utf-8")
        return self._code

    @property
    def tree(self) -> ast.AST | None:
        if self._tree is None:
            try:
                self._tree = ast.parse(self.code)
            except SyntaxError as e:
                self.add("Syntaxe", False, f"Chyba v zápisu kódu na řádku {e.lineno}: {e.msg}")
                return None
        return self._tree

    # ---------- spuštění jako program ----------
    def run(self, stdin: str = "", timeout: float = 5, args: list[str] | None = None) -> RunResult:
        env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8",
                   SDL_VIDEODRIVER="dummy", SDL_AUDIODRIVER="dummy")
        try:
            p = subprocess.run([sys.executable, "-u", "-X", "utf8", str(self.student), *(args or [])],
                               input=stdin.encode("utf-8"), capture_output=True, timeout=timeout,
                               cwd=self.student.parent, env=env)
            return RunResult(p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace"), p.returncode)
        except subprocess.TimeoutExpired as e:
            return RunResult((e.stdout or b"").decode("utf-8", "replace"),
                             (e.stderr or b"").decode("utf-8", "replace"), None, True)

    # ---------- pygame bez okna ----------
    def pygame_run(self, frames: int = 3, pixels=(), colors=(), events: dict | None = None, held: dict | None = None,
                   mouse: dict | None = None, timeout: float = 15) -> PgResult:
        """Spustí program studenta s pygame bez okna a po `frames` snímcích (volání flip/update) ho ukončí.

        pixels  seznam (x, y), jejichž barvu zapisovat v každém snímku;
        colors  seznam (r, g, b) nebo (r, g, b, x, y, šířka, výška): počet pixelů barvy (v části okna) v každém snímku;
        events  {číslo snímku: [{"type": "KEYDOWN", "key": "K_LEFT"}, {"type": "QUIT"}, ...]};
        held    {od snímku: ["K_LEFT"]}: klávesy držené pro pygame.key.get_pressed();
        mouse   {od snímku: [x, y]}: poloha myši pro pygame.mouse.get_pos().
        Snímky se číslují od 0 (událost ve snímku 2 dostane program při třetím průchodu smyčkou).
        """
        import tempfile
        spec = {"frames": frames, "pixels": [list(p) for p in pixels], "colors": [list(c) for c in colors],
                "events": {str(k): v for k, v in (events or {}).items()},
                "held": {str(k): v for k, v in (held or {}).items()},
                "mouse": {str(k): list(v) for k, v in (mouse or {}).items()}}
        tmp = Path(tempfile.mkdtemp(prefix="pg-"))
        (tmp / "spec.json").write_text(json.dumps(spec), encoding="utf-8")
        out = tmp / "out.json"
        env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8", SDL_VIDEODRIVER="dummy",
                   SDL_AUDIODRIVER="dummy", PYGAME_HIDE_SUPPORT_PROMPT="1")
        try:
            p = subprocess.run([sys.executable, "-u", "-X", "utf8", str(Path(__file__).with_name("pgrun.py")),
                                str(self.student), str(tmp / "spec.json"), str(out)],
                               capture_output=True, timeout=timeout, cwd=self.student.parent, env=env)
        except subprocess.TimeoutExpired:
            return PgResult(timed_out=True)
        if not out.is_file():
            err = p.stderr.decode("utf-8", "replace").strip().splitlines()
            return PgResult(crashed=err[-1] if err else "program nespustil")
        return PgResult(**json.loads(out.read_text(encoding="utf-8")))

    def tk_run(self, actions=(), timeout: float = 10, max_steps: int = 100000) -> TkResult:
        """Spustí úvodní Tkinter bez okna a provede fill/click akce."""
        import tempfile
        with tempfile.TemporaryDirectory(prefix="tk-") as temp:
            tmp = Path(temp)
            (tmp / "spec.json").write_text(json.dumps({"actions": list(actions), "max_steps": max_steps}), encoding="utf-8")
            out = tmp / "out.json"
            env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
            try:
                p = subprocess.run([sys.executable, "-u", "-X", "utf8", str(Path(__file__).with_name("tkrun.py")),
                                    str(self.student), str(tmp / "spec.json"), str(out)], capture_output=True,
                                   timeout=timeout, cwd=self.student.parent, env=env)
            except subprocess.TimeoutExpired:
                return TkResult(timed_out=True)
            if not out.is_file():
                lines = p.stderr.decode("utf-8", "replace").strip().splitlines()
                return TkResult(crashed=lines[-1] if lines else "program nespustil")
            return TkResult(**json.loads(out.read_text(encoding="utf-8")))

    def tk_no_error(self, r: TkResult, name="Program Tkinter běží bez chyby") -> bool:
        if r.timed_out:
            return self.add(name, False, "Program běžel příliš dlouho. Zkontrolujte cykly a čekání.")
        if r.crashed:
            return self.add(name, False, f"Kontrola Tkinteru se nespustila: {r.crashed}")
        if r.error:
            return self.add(name, False, f"{r.error['type']}: {r.error['msg']} (řádek {r.error.get('line')})")
        return self.add(name, True)

    def turtle_run(self, keys=(), clicks=(), ticks: int = 0, timeout: float = 15, max_ops: int = 200000) -> TurtleResult:
        """Spustí program studenta s modulem turtle bez okna a zaznamená, co želva nakreslila.

        keys    klávesy ("Up", "space", ...), které se po dosažení mainloop()/done() pošlou funkcím z onkey;
        clicks  kliknutí [(x, y), ...] pro onclick; ticks  kolikrát se zavolají funkce naplánované přes ontimer.
        """
        import tempfile
        spec = {"keys": list(keys), "clicks": [list(c) for c in clicks], "ticks": ticks, "max_ops": max_ops}
        tmp = Path(tempfile.mkdtemp(prefix="tt-"))
        (tmp / "spec.json").write_text(json.dumps(spec), encoding="utf-8")
        out = tmp / "out.json"
        env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
        try:
            p = subprocess.run([sys.executable, "-u", "-X", "utf8", str(Path(__file__).with_name("turtlerun.py")),
                                str(self.student), str(tmp / "spec.json"), str(out)],
                               capture_output=True, timeout=timeout, cwd=self.student.parent, env=env)
        except subprocess.TimeoutExpired:
            return TurtleResult(timed_out=True)
        if not out.is_file():
            err = p.stderr.decode("utf-8", "replace").strip().splitlines()
            return TurtleResult(crashed=err[-1] if err else "program nespustil")
        return TurtleResult(**json.loads(out.read_text(encoding="utf-8")))

    def turtle_no_error(self, r: TurtleResult, name: str = "Program běží bez chyby") -> bool:
        """Zapíše výsledek: program doběhl (nebo došel k done()/mainloop()) bez chyby."""
        if r.timed_out:
            return self.add(name, False, "Program běžel příliš dlouho. Nemáte nekonečný cyklus bez konce?")
        if r.crashed:
            return self.add(name, False, f"Program se nepodařilo spustit: {r.crashed}")
        if r.error:
            return self.add(name, False, f"Program skončil chybou {r.error['type']}: {r.error['msg']}"
                            + (f" (řádek {r.error['line']})" if r.error.get("line") else ""))
        return self.add(name, True)

    def pg_no_error(self, r: PgResult, name: str = "Program běží bez chyby") -> bool:
        """Zapíše výsledek: program doběhl nebo se zastavil po zadaném počtu snímků bez chyby."""
        if r.timed_out:
            return self.add(name, False, "Program běžel příliš dlouho bez nakreslení snímku. Chybí v herní smyčce pygame.display.flip()?")
        if r.crashed:
            return self.add(name, False, f"Program se nepodařilo spustit: {r.crashed}")
        if r.error:
            return self.add(name, False, f"Program skončil chybou {r.error['type']}: {r.error['msg']}"
                            + (f" (řádek {r.error['line']})" if r.error.get("line") else ""))
        if r.frames == 0 and not r.ended:
            return self.add(name, False, "Program nic nenakreslil.")
        return self.add(name, True)

    def no_error(self, r: RunResult, name: str = "Program doběhl bez chyby") -> bool:
        if r.timed_out:
            return self.add(name, False, "Program běžel příliš dlouho. Neběží někde nekonečný cyklus, nebo nečeká na vstup?")
        if r.exit != 0:
            last = r.err.strip().splitlines()[-1] if r.err.strip() else "neznámá chyba"
            return self.add(name, False, f"Program skončil chybou: {last}")
        return self.add(name, True)

    def output_contains(self, r: RunResult, text: str, hint: str = "", ignore_case: bool = False) -> bool:
        a, b = (r.out.lower(), text.lower()) if ignore_case else (r.out, text)
        return self.add(f"Výstup obsahuje „{text}“", b in a,
                        hint or f"Ve výstupu chybí text „{text}“. Váš výstup: {self._short(r.out)}")

    def output_equals(self, r: RunResult, text: str, hint: str = "") -> bool:
        ok = r.out.strip().replace("\r\n", "\n") == text.strip()
        return self.add("Výstup se shoduje", ok,
                        hint or f"Očekáváno: {self._short(text)} | Máte: {self._short(r.out)}")

    @staticmethod
    def _short(s: str, n: int = 160) -> str:
        s = s.strip().replace("\n", " ⏎ ")
        return (s[:n] + "…") if len(s) > n else (s or "(nic)")

    # ---------- načtení jako modul ----------
    def load(self, stdin: str = "", name: str = "student") -> dict | None:
        """Provede kód s __name__ == 'student'. Vrací jmenný prostor, nebo None při chybě."""
        if self.tree is None:
            return None
        ns: dict = {"__name__": name, "__file__": str(self.student)}
        buf = io.StringIO()
        old_input = builtins.input
        builtins.input = _NoInput(stdin)
        try:
            with contextlib.redirect_stdout(buf):
                exec(compile(self.code, str(self.student), "exec"), ns)
        except BaseException as e:  # včetně SystemExit
            builtins.input = old_input
            self.add("Kód se dá načíst", False, f"Při načtení kódu vznikla chyba {type(e).__name__}: {e}")
            return None
        finally:
            builtins.input = old_input
        ns["__output__"] = buf.getvalue()
        self.add("Kód se dá načíst", True)
        return ns

    def returns(self, ns: dict | None, func: str, args: tuple = (), expected=None, kwargs: dict | None = None,
                hint: str = "", stdin: str = "") -> bool:
        label = f"{func}({', '.join(map(repr, args))})"
        if ns is None:
            return self.add(label, False, "Kód se nepodařilo načíst.")
        f = ns.get(func)
        if not callable(f):
            return self.add(label, False, f"Chybí funkce {func}. Vytvořte ji pomocí def {func}(...):")
        old_input = builtins.input
        builtins.input = _NoInput(stdin)
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                got = f(*args, **(kwargs or {}))
        except BaseException as e:
            return self.add(label, False, f"Volání skončilo chybou {type(e).__name__}: {e}")
        finally:
            builtins.input = old_input
        return self.add(f"{label} == {expected!r}", got == expected,
                        hint or f"Funkce vrátila {got!r}, ale má vrátit {expected!r}.")

    def call(self, ns: dict | None, func: str, args: tuple = (), kwargs: dict | None = None, stdin: str = ""):
        """Zavolá funkci studenta se zadaným vstupem. Vrací (ok, hodnota nebo výjimka).
        Vypsaný text je potom v self.last_output."""
        self.last_output = ""
        f = (ns or {}).get(func)
        if not callable(f):
            return False, NameError(func)
        buf = io.StringIO()
        old_input = builtins.input
        builtins.input = _NoInput(stdin)
        try:
            with contextlib.redirect_stdout(buf):
                return True, f(*args, **(kwargs or {}))
        except BaseException as e:
            return False, e
        finally:
            builtins.input = old_input
            self.last_output = buf.getvalue()

    def returns_close(self, ns: dict | None, func: str, args: tuple = (), expected: float = 0.0,
                      tol: float = 1e-6, hint: str = "") -> bool:
        """Jako returns, ale desetinná čísla se porovnávají s tolerancí."""
        label = f"{func}({', '.join(map(repr, args))})"
        if ns is None or not callable(ns.get(func)):
            return self.add(label, False, f"Chybí funkce {func}. Vytvořte ji pomocí def {func}(...):")
        ok, got = self.call(ns, func, args)
        if not ok:
            return self.add(label, False, f"Volání skončilo chybou {type(got).__name__}: {got}")
        good = isinstance(got, (int, float)) and not isinstance(got, bool) and abs(got - expected) <= tol
        return self.add(f"{label} ≈ {expected!r}", good, hint or f"Funkce vrátila {got!r}, ale má vrátit přibližně {expected!r}.")

    def raises(self, ns: dict | None, func: str, args: tuple, exc: type, hint: str = "") -> bool:
        """Volání musí skončit výjimkou typu exc."""
        label = f"{func}({', '.join(map(repr, args))}) vyvolá {exc.__name__}"
        if ns is None or not callable(ns.get(func)):
            return self.add(label, False, f"Chybí funkce {func}. Vytvořte ji pomocí def {func}(...):")
        ok, got = self.call(ns, func, args)
        if ok:
            return self.add(label, False, hint or f"Funkce vrátila {got!r}, ale měla vyvolat {exc.__name__}.")
        return self.add(label, isinstance(got, exc), hint or f"Vznikla {type(got).__name__}, ale má vzniknout {exc.__name__}.")

    def utf8(self, hint: str = "") -> bool:
        """Každé textové open(), read_text() a write_text() má parametr encoding (a aspoň jedno takové volání existuje)."""
        volani, bez = 0, 0
        for n in self._walk():
            if not isinstance(n, ast.Call):
                continue
            f = n.func
            jmeno = f.id if isinstance(f, ast.Name) else f.attr if isinstance(f, ast.Attribute) else ""
            if jmeno == "open" and isinstance(f, ast.Attribute) and not (isinstance(f.value, ast.Name) and f.value.id in ("io", "codecs")):
                pass                                  # Path.open(...) se počítá stejně jako open(...)
            if jmeno not in ("open", "read_text", "write_text"):
                continue
            rezim = ""
            if jmeno == "open":
                pozice = 1 if isinstance(f, ast.Name) else 0
                if len(n.args) > pozice and isinstance(n.args[pozice], ast.Constant):
                    rezim = str(n.args[pozice].value)
                for k in n.keywords:
                    if k.arg == "mode" and isinstance(k.value, ast.Constant):
                        rezim = str(k.value.value)
                if "b" in rezim:
                    continue
            volani += 1
            if not any(k.arg == "encoding" for k in n.keywords):
                bez += 1
        return self.add("Soubory se otevírají s encoding=\"utf-8\"", volani > 0 and bez == 0,
                        hint or "Při otevírání textového souboru vždy přidejte encoding=\"utf-8\".")

    def output_has_line(self, r: RunResult, text: str, hint: str = "") -> bool:
        """Některý řádek výstupu KONČÍ textem (Součet: 8 nepustí Součet: 80). Výzvy input() bez nového řádku
        se do výstupu dostanou před text, proto se neporovnává celý řádek."""
        ok = any(l.strip().endswith(text) for l in r.out.splitlines())
        return self.add(f"Výstup má řádek „{text}“", ok, hint or f"Ve výstupu chybí řádek „{text}“. Váš výstup: {self._short(r.out)}")

    # ---------- kontroly struktury (AST) ----------
    def function(self, name: str):
        """Uzel FunctionDef podle jména, nebo None."""
        return next((n for n in self._walk() if isinstance(n, ast.FunctionDef) and n.name == name), None)

    @staticmethod
    def calls_in(node, name: str) -> list:
        """Volání funkce nebo metody `name` uvnitř uzlu."""
        out = []
        for n in ast.walk(node):
            if isinstance(n, ast.Call):
                f = n.func
                if (isinstance(f, ast.Name) and f.id == name) or (isinstance(f, ast.Attribute) and f.attr == name):
                    out.append(n)
        return out

    def _walk(self):
        t = self.tree
        return ast.walk(t) if t is not None else iter(())

    def uses(self, node_type, hint: str, label: str | None = None) -> bool:
        ok = any(isinstance(n, node_type) for n in self._walk())
        return self.add(label or f"Kód používá {node_type.__name__}", ok, hint)

    def uses_call(self, name: str, hint: str = "") -> bool:
        """Kód volá funkci nebo metodu `name`. Alternativy se zadají přes "|", např. "forward|fd"."""
        names = name.split("|")

        def called(n):
            if not isinstance(n, ast.Call):
                return False
            f = n.func
            return (isinstance(f, ast.Name) and f.id in names) or (isinstance(f, ast.Attribute) and f.attr in names)
        ok = any(called(n) for n in self._walk())
        return self.add(f"Kód volá {names[0]}()", ok, hint or f"V kódu chybí volání {names[0]}().")

    def defines_function(self, name: str, nargs: int | None = None, hint: str = "") -> bool:
        for n in self._walk():
            if isinstance(n, ast.FunctionDef) and n.name == name:
                if nargs is None or len(n.args.args) == nargs:
                    return self.add(f"Funkce {name}", True)
                return self.add(f"Funkce {name}", False, hint or f"Funkce {name} má mít {nargs} parametrů.")
        return self.add(f"Funkce {name}", False, hint or f"Chybí funkce {name}.")

    def defines_class(self, name: str, hint: str = "") -> bool:
        ok = any(isinstance(n, ast.ClassDef) and n.name == name for n in self._walk())
        return self.add(f"Třída {name}", ok, hint or f"Chybí třída {name}.")

    def imports(self, module: str, hint: str = "") -> bool:
        ok = False
        for n in self._walk():
            if isinstance(n, ast.Import) and any(a.name.split(".")[0] == module for a in n.names):
                ok = True
            if isinstance(n, ast.ImportFrom) and (n.module or "").split(".")[0] == module:
                ok = True
        return self.add(f"Import {module}", ok, hint or f"Je potřeba importovat {module}.")

    def not_uses_call(self, name: str, hint: str) -> bool:
        ok = not any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == name
                     for n in self._walk())
        return self.add(f"Kód nepoužívá {name}()", ok, hint)

    def no_hardcoded(self, text: str, hint: str) -> bool:
        """Zadání nesmí být jen vypsané natvrdo."""
        ok = not any(isinstance(n, ast.Constant) and isinstance(n.value, str) and text in n.value
                     for n in self._walk())
        return self.add("Výsledek se počítá, není vypsaný natvrdo", ok, hint)


def check() -> Checker:
    return Checker()
