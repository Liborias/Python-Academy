"""Spouštěč programů s modulem turtle bez okna (pro kontroly lekcí).

Spouští se jako samostatný proces: python turtlerun.py <program studenta> <spec.json> <výstup.json>

Místo skutečného modulu `turtle` se podstrčí náhrada, která si pamatuje, co želva nakreslila
(úsečky, tečky, texty, vyplněné tvary, volání funkcí) a počítá stejnou geometrii jako pravá želva
(včetně toho, že kruh je mnohoúhelník). Nic se nezobrazuje a nic se nečeká.
Spec: {"keys": ["Up", ...], "clicks": [[x, y], ...], "ticks": 5, "max_ops": 200000}
"""
import contextlib
import io
import json
import math
import os
import sys
import traceback
import types

student, spec_path, out_path = sys.argv[1:4]
with open(spec_path, encoding="utf-8") as f:
    SPEC = json.load(f)
MAX_OPS = int(SPEC.get("max_ops", 200000))

R = {"segments": [], "fills": [], "dots": [], "texts": [], "stamps": [], "calls": {}, "turtles": [], "bgcolor": None,
     "title": None, "screen": None, "handlers": {}, "ended": False, "error": None, "mainloop": False, "out": "", "ops": 0}
_buf = io.StringIO()
_state = {"colormode": 1.0, "timers": []}


class _Stop(BaseException):
    pass


def _write():
    R["out"] = _buf.getvalue()[:20000]
    for t in _turtles:
        R["turtles"].append({"x": round(t.x, 3), "y": round(t.y, 3), "heading": round(t.h % 360, 3), "pendown": t.down,
                             "visible": t.visible, "shape": t.shape_name, "pencolor": t.pencolor_, "fillcolor": t.fillcolor_,
                             "width": t.width_, "speed": t.speed_})
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(R, f, ensure_ascii=False)


def _count(name):
    R["calls"][name] = R["calls"].get(name, 0) + 1
    R["ops"] += 1
    if R["ops"] > MAX_OPS:
        raise _Stop()


class TurtleGraphicsError(Exception):
    pass


# Základní jména barev (Tk/X11). Šestnáctkový zápis téže barvy se převede na jméno, aby šlo porovnávat.
_NAMES = {"red": "#ff0000", "green": "#00ff00", "blue": "#0000ff", "yellow": "#ffff00", "black": "#000000", "white": "#ffffff",
          "orange": "#ffa500", "cyan": "#00ffff", "magenta": "#ff00ff", "brown": "#a52a2a", "gold": "#ffd700", "pink": "#ffc0cb",
          "purple": "#a020f0", "navy": "#000080", "gray": "#bebebe", "lightblue": "#add8e6"}
_BYHEX = {v: k for k, v in _NAMES.items()}


def _color(*args):
    """Barva jako text: jméno malými písmeny, nebo #rrggbb (pokud je to základní barva, tak její jméno)."""
    if len(args) == 1:
        a = args[0]
        if isinstance(a, str):
            a = a.strip().lower()
            if a.startswith("#") and len(a) == 4:
                a = "#" + "".join(ch * 2 for ch in a[1:])
            return _BYHEX.get(a, a)
        args = tuple(a)
    if len(args) == 3:
        top = 255 if _state["colormode"] == 255 else 1.0
        if any(float(v) < 0 or float(v) > top for v in args):
            raise TurtleGraphicsError("bad color sequence: %s" % (tuple(args),))
        vals = [int(round(float(v) / top * 255)) for v in args]
        h = "#%02x%02x%02x" % tuple(vals)
        return _BYHEX.get(h, h)
    return str(args)


_turtles = []


class Vec2D(tuple):
    """Dvojice jako ve skutečném turtle: umí + - * abs a vypisuje se jako (x,y) se dvěma desetinnými místy."""

    def __new__(cls, x, y):
        return tuple.__new__(cls, (x, y))

    def __add__(self, o):
        return Vec2D(self[0] + o[0], self[1] + o[1])

    def __sub__(self, o):
        return Vec2D(self[0] - o[0], self[1] - o[1])

    def __mul__(self, o):
        if isinstance(o, (int, float)):
            return Vec2D(self[0] * o, self[1] * o)
        return self[0] * o[0] + self[1] * o[1]

    def __rmul__(self, o):
        return self.__mul__(o) if isinstance(o, (int, float)) else NotImplemented

    def __neg__(self):
        return Vec2D(-self[0], -self[1])

    def __abs__(self):
        return math.hypot(self[0], self[1])

    def __repr__(self):
        return "(%.2f,%.2f)" % (self[0], self[1])


class Turtle:
    def __init__(self, *args, **kwargs):
        self.x = self.y = 0.0
        self.h = 0.0
        self.down = True
        self.visible = True
        self.pencolor_ = "black"
        self.fillcolor_ = "black"
        self.width_ = 1
        self.speed_ = 3
        self.shape_name = "classic"
        self.fill_points = None
        self.id = len(_turtles)
        self.undobuf = []
        _turtles.append(self)
        R["calls"]["Turtle()"] = R["calls"].get("Turtle()", 0) + 1

    # --- pohyb ---
    def _go(self, nx, ny, src="move"):
        if self.down and math.hypot(nx - self.x, ny - self.y) > 0.01:
            R["segments"].append([round(self.x, 3), round(self.y, 3), round(nx, 3), round(ny, 3), self.pencolor_, self.width_, self.id, src])
        self.x, self.y = nx, ny
        if self.fill_points is not None:
            self.fill_points.append((round(nx, 3), round(ny, 3)))

    def forward(self, d):
        _count("forward")
        r = math.radians(self.h)
        self._go(self.x + d * math.cos(r), self.y + d * math.sin(r))
    fd = forward

    def backward(self, d):
        _count("backward")
        r = math.radians(self.h)
        self._go(self.x - d * math.cos(r), self.y - d * math.sin(r))
    back = bk = backward

    def left(self, a):
        _count("left")
        self.h = (self.h + a) % 360
    lt = left

    def right(self, a):
        _count("right")
        self.h = (self.h - a) % 360
    rt = right

    def goto(self, x, y=None):
        _count("goto")
        if y is None:
            x, y = x
        self._go(float(x), float(y), "goto")
    setpos = setposition = goto

    def setx(self, x):
        _count("setx")
        self._go(float(x), self.y)

    def sety(self, y):
        _count("sety")
        self._go(self.x, float(y))

    def setheading(self, a):
        _count("setheading")
        self.h = float(a) % 360
    seth = setheading

    def home(self):
        _count("home")
        self._go(0.0, 0.0, "goto")
        self.h = 0.0

    def circle(self, radius, extent=None, steps=None):
        _count("circle")
        if extent is None:
            extent = 360
        frac = abs(extent) / 360.0
        if steps is None:
            steps = 1 + int(min(11 + abs(radius) / 6.0, 59.0) * frac)
        w = 1.0 * extent / steps
        w2 = 0.5 * w
        ln = 2.0 * radius * math.sin(math.radians(w2))
        if radius < 0:
            ln, w, w2 = -ln, -w, -w2
        self.h = (self.h + w2) % 360
        for _ in range(steps):
            r = math.radians(self.h)
            self._go(self.x + ln * math.cos(r), self.y + ln * math.sin(r), "circle")
            self.h = (self.h + w) % 360
        self.h = (self.h - w2) % 360

    def dot(self, size=None, *color):
        _count("dot")
        col = _color(*color) if color else self.pencolor_
        R["dots"].append([round(self.x, 3), round(self.y, 3), size if size is not None else max(self.width_ + 4, 2 * self.width_), col, self.id])

    def stamp(self):
        _count("stamp")
        R["stamps"].append([round(self.x, 3), round(self.y, 3), round(self.h, 3), self.id])
        return len(R["stamps"])

    def write(self, arg, move=False, align="left", font=("Arial", 8, "normal")):
        _count("write")
        R["texts"].append({"text": str(arg), "x": round(self.x, 3), "y": round(self.y, 3), "align": align,
                           "font": [str(v) for v in font] if isinstance(font, (tuple, list)) else [str(font)], "color": self.pencolor_, "t": self.id})

    # --- pero ---
    def penup(self):
        _count("penup")
        self.down = False
    up = pu = penup

    def pendown(self):
        _count("pendown")
        self.down = True
    pd = pendown

    def isdown(self):
        return self.down

    def pensize(self, w=None):
        _count("pensize")
        if w is None:
            return self.width_
        self.width_ = w
    width = pensize

    def pencolor(self, *args):
        _count("pencolor")
        if not args:
            return self.pencolor_
        self.pencolor_ = _color(*args)

    def fillcolor(self, *args):
        _count("fillcolor")
        if not args:
            return self.fillcolor_
        self.fillcolor_ = _color(*args)

    def color(self, *args):
        _count("color")
        if not args:
            return (self.pencolor_, self.fillcolor_)
        if len(args) == 2 and all(isinstance(a, str) or isinstance(a, tuple) for a in args):
            self.pencolor_, self.fillcolor_ = _color(args[0]), _color(args[1])
        else:
            self.pencolor_ = self.fillcolor_ = _color(*args)

    def begin_fill(self):
        _count("begin_fill")
        self.fill_points = [(round(self.x, 3), round(self.y, 3))]

    def end_fill(self):
        _count("end_fill")
        if self.fill_points is not None and len(self.fill_points) >= 3:
            R["fills"].append({"color": self.fillcolor_, "points": [list(p) for p in self.fill_points], "t": self.id})
        self.fill_points = None

    def filling(self):
        return self.fill_points is not None

    # --- vzhled ---
    def speed(self, s=None):
        _count("speed")
        if s is None:
            return self.speed_
        names = {"fastest": 0, "fast": 10, "normal": 6, "slow": 3, "slowest": 1}
        if isinstance(s, str):
            s = names.get(s, self.speed_)
        elif s > 10.5 or s < 0.5:
            s = 0
        else:
            s = int(round(s))
        self.speed_ = s

    def hideturtle(self):
        _count("hideturtle")
        self.visible = False
    ht = hideturtle

    def showturtle(self):
        _count("showturtle")
        self.visible = True
    st = showturtle

    def isvisible(self):
        return self.visible

    def shape(self, name=None):
        _count("shape")
        if name is None:
            return self.shape_name
        self.shape_name = name

    def shapesize(self, *a, **k):
        _count("shapesize")
    turtlesize = shapesize

    def _wipe(self):
        i = self.id
        R["segments"][:] = [x for x in R["segments"] if x[6] != i]
        R["fills"][:] = [x for x in R["fills"] if x["t"] != i]
        R["dots"][:] = [x for x in R["dots"] if x[4] != i]
        R["texts"][:] = [x for x in R["texts"] if x["t"] != i]
        R["stamps"][:] = [x for x in R["stamps"] if x[3] != i]

    def clear(self):
        _count("clear")
        self._wipe()

    def reset(self):
        _count("reset")
        self._wipe()
        self.x = self.y = self.h = 0.0
        self.down, self.visible, self.pencolor_, self.fillcolor_, self.width_ = True, True, "black", "black", 1

    def undo(self):
        _count("undo")

    def clone(self):
        _count("clone")
        t = Turtle()
        t.x, t.y, t.h, t.down = self.x, self.y, self.h, self.down
        t.pencolor_, t.fillcolor_, t.width_, t.shape_name = self.pencolor_, self.fillcolor_, self.width_, self.shape_name
        return t

    # --- dotazy ---
    def xcor(self):
        return self.x

    def ycor(self):
        return self.y

    def pos(self):
        return Vec2D(self.x, self.y)
    position = pos

    def heading(self):
        return self.h

    def distance(self, x, y=None):
        if y is None:
            x, y = (x.x, x.y) if isinstance(x, Turtle) else x
        return math.hypot(x - self.x, y - self.y)

    def towards(self, x, y=None):
        if y is None:
            x, y = (x.x, x.y) if isinstance(x, Turtle) else x
        return math.degrees(math.atan2(y - self.y, x - self.x)) % 360

    def degrees(self, *a):
        _count("degrees")

    def radians(self):
        _count("radians")

    def getscreen(self):
        return Screen()

    @property
    def screen(self):
        return _screen

    # --- události ---
    def _handler(self, kind, fun, key=None):
        R["handlers"].setdefault(kind, []).append(key if key is not None else True)
        _handlers.setdefault(kind, []).append((key, fun))

    def onclick(self, fun, btn=1, add=None):
        _count("onclick")
        self._handler("onclick", fun)

    def onkey(self, fun, key):
        _count("onkey")
        self._handler("onkey", fun, key)
    onkeypress = onkey

    def onkeyrelease(self, fun, key):
        _count("onkeyrelease")
        self._handler("onkeyrelease", fun, key)

    def ondrag(self, *a, **k):
        _count("ondrag")


_handlers = {}


class _Screen:
    def bgcolor(self, *args):
        _count("bgcolor")
        if not args:
            return R["bgcolor"] or "white"
        R["bgcolor"] = _color(*args)

    def title(self, t):
        _count("title")
        R["title"] = str(t)

    def setup(self, width=None, height=None, *a, **k):
        _count("setup")
        R["screen"] = [width, height]

    def screensize(self, *a, **k):
        _count("screensize")

    def tracer(self, n=None, delay=None):
        _count("tracer")

    def delay(self, d=None):
        _count("delay")

    def update(self):
        _count("update")

    def listen(self, *a, **k):
        _count("listen")

    def onkey(self, fun, key):
        _count("onkey")
        R["handlers"].setdefault("onkey", []).append(key)
        _handlers.setdefault("onkey", []).append((key, fun))
    onkeypress = onkey

    def onkeyrelease(self, fun, key):
        _count("onkeyrelease")
        _handlers.setdefault("onkeyrelease", []).append((key, fun))

    def onclick(self, fun, btn=1, add=None):
        _count("onclick")
        R["handlers"].setdefault("onclick", []).append(True)
        _handlers.setdefault("onclick", []).append((None, fun))
    onscreenclick = onclick

    def ontimer(self, fun, t=0):
        _count("ontimer")
        R["handlers"].setdefault("ontimer", []).append(t)
        _state["timers"].append(fun)

    def colormode(self, m=None):
        if m is None:
            return _state["colormode"]
        _state["colormode"] = m

    def window_width(self):
        return (R["screen"] or [None])[0] or 960

    def window_height(self):
        return (R["screen"] or [None, None])[1] or 810

    def mainloop(self):
        _count("mainloop")
        R["mainloop"] = True
        _run_events()
        raise _Stop()
    done = mainloop

    def exitonclick(self):
        _count("exitonclick")
        R["mainloop"] = True
        _run_events()
        raise _Stop()

    def bye(self):
        _count("bye")
        raise _Stop()

    def clear(self):
        _count("clearscreen")
        for t in _turtles:
            t._wipe()

    def reset(self):
        _count("resetscreen")
        for t in _turtles:
            t.reset()

    def addshape(self, *a, **k):
        _count("addshape")

    def register_shape(self, *a, **k):
        _count("register_shape")

    def textinput(self, title, prompt):
        _count("textinput")
        return ""

    def numinput(self, title, prompt, default=None, *a, **k):
        _count("numinput")
        return default


_screen = _Screen()


def Screen():
    return _screen


def _run_events():
    for key in SPEC.get("keys", []):
        for k, fun in list(_handlers.get("onkey", [])) + list(_handlers.get("onkeypress", [])):
            if k == key:
                fun()
    for pos in SPEC.get("clicks", []):
        for _, fun in list(_handlers.get("onclick", [])):
            fun(*pos)
    for _ in range(int(SPEC.get("ticks", 0))):
        timers, _state["timers"] = _state["timers"], []
        for fun in timers:
            fun()


# ----- modul turtle -----
mod = types.ModuleType("turtle")
mod.Turtle = mod.Pen = mod.RawTurtle = mod.RawPen = Turtle
mod.Screen = Screen
mod.TurtleScreen = _Screen
mod.Terminator = Exception
mod.Vec2D = Vec2D
mod.TurtleGraphicsError = TurtleGraphicsError
_default = {}


def _dt():
    if "t" not in _default:
        _default["t"] = Turtle()
        R["calls"]["Turtle()"] = R["calls"].get("Turtle()", 0) - 1
    return _default["t"]


_FUN = ["forward", "fd", "backward", "back", "bk", "left", "lt", "right", "rt", "goto", "setpos", "setposition", "setx", "sety",
        "setheading", "seth", "home", "circle", "dot", "stamp", "write", "penup", "up", "pu", "pendown", "pd", "isdown", "pensize", "width",
        "pencolor", "fillcolor", "color", "begin_fill", "end_fill", "filling", "speed", "hideturtle", "ht", "showturtle", "st",
        "isvisible", "shape", "shapesize", "turtlesize", "clear", "reset", "undo", "clone", "xcor", "ycor", "pos", "position", "heading",
        "distance", "towards", "degrees", "radians", "getscreen", "onclick", "onkey", "onkeypress", "onkeyrelease", "ondrag"]
for _n in _FUN:
    def _mk(n):
        def f(*a, **k):
            return getattr(_dt(), n)(*a, **k)
        f.__name__ = n
        return f
    setattr(mod, _n, _mk(_n))
mod.down = mod.pendown
for _n in ("bgcolor", "title", "setup", "screensize", "tracer", "delay", "update", "listen", "ontimer", "colormode", "window_width",
           "window_height", "mainloop", "done", "exitonclick", "bye", "addshape", "register_shape", "textinput", "numinput", "onscreenclick"):
    setattr(mod, _n, getattr(_screen, _n))
mod.onkey = lambda fun, key: _screen.onkey(fun, key)
mod.onkeypress = mod.onkey
mod.onclick = lambda fun, btn=1, add=None: _screen.onclick(fun, btn, add)
mod.clearscreen = _screen.clear
mod.resetscreen = _screen.reset
mod.__all__ = [n for n in dir(mod) if not n.startswith("_") and n != "Terminator"]
sys.modules["turtle"] = mod

# ----- spuštění programu studenta -----
sys.path.insert(0, os.path.dirname(os.path.abspath(student)))
ns = {"__name__": "__main__", "__file__": student, "__builtins__": __builtins__}
try:
    with open(student, encoding="utf-8") as f:
        code = compile(f.read(), student, "exec")
    with contextlib.redirect_stdout(_buf):
        exec(code, ns)
    R["ended"] = True
except (SystemExit, _Stop):
    R["ended"] = True
except BaseException as e:
    tb = traceback.extract_tb(e.__traceback__)
    mine = [t for t in tb if t.filename == student]
    R["error"] = {"type": type(e).__name__, "msg": str(e), "line": mine[-1].lineno if mine else None}
_write()
os._exit(0)
