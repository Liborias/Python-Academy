"""Spouštěč pygame programů bez okna (pro kontroly lekcí).

Spouští se jako samostatný proces: python pgrun.py <program studenta> <spec.json> <výstup.json>

Co dělá:
  * nastaví SDL na ovladač "dummy" (žádné okno, žádný zvuk),
  * spočítá snímky (volání display.flip / display.update) a po `frames` snímcích program ukončí,
  * podstrčí skriptované události (klávesy, myš, zavření okna) a "držené" klávesy,
  * zrychlí hodiny (Clock.tick nic nečeká a vrací 16 ms, takže pohyb je opakovatelný),
  * zaznamená barvy zadaných pixelů a počty zadaných barev v každém snímku,
  * zapíše volání pygame.draw, vykreslené texty, načtené soubory a přehrané zvuky.
"""
import contextlib
import io
import json
import os
import sys
import traceback

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

student, spec_path, out_path = sys.argv[1:4]
with open(spec_path, encoding="utf-8") as f:
    SPEC = json.load(f)
MAX_FRAMES = int(SPEC.get("frames", 3))
PIXELS = [tuple(p) for p in SPEC.get("pixels", [])]
COLORS = [tuple(c) for c in SPEC.get("colors", [])]
EVENTS = {int(k): v for k, v in SPEC.get("events", {}).items()}
HELD = sorted((int(k), v) for k, v in SPEC.get("held", {}).items())
MOUSE = sorted((int(k), v) for k, v in SPEC.get("mouse", {}).items())

import pygame  # noqa: E402

R = {"frames": 0, "ended": False, "error": None, "size": None, "caption": None, "shots": [],
     "draws": [], "texts": [], "images": [], "sounds": [], "music": [], "fps": [], "out": ""}
_state = {"flips": 0, "event_frame": -1}
_buf = io.StringIO()


def _write():
    R["out"] = _buf.getvalue()[:20000]
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(R, f, ensure_ascii=False)


def _shot():
    surf = pygame.display.get_surface()
    if surf is None:
        return
    R["size"] = list(surf.get_size())
    try:
        R["caption"] = pygame.display.get_caption()[0]
    except Exception:
        pass
    shot = {"pixels": {}, "colors": {}}
    w, h = surf.get_size()
    for (x, y) in PIXELS:
        if 0 <= x < w and 0 <= y < h:
            shot["pixels"][f"{x},{y}"] = list(surf.get_at((x, y)))[:3]
    for c in COLORS:                              # (r, g, b) nebo (r, g, b, x, y, šířka, výška) = jen část okna
        key = ",".join(map(str, c[:3])) + (("@" + ",".join(map(str, c[3:7]))) if len(c) >= 7 else "")
        try:
            plocha = surf.subsurface(pygame.Rect(c[3:7]).clip(surf.get_rect())) if len(c) >= 7 else surf
            shot["colors"][key] = pygame.mask.from_threshold(plocha, tuple(c[:3]), (1, 1, 1, 255)).count()
        except Exception:
            shot["colors"][key] = 0
    R["shots"].append(shot)


def _frame_done():
    _state["flips"] += 1
    R["frames"] = _state["flips"]
    _shot()
    if _state["flips"] >= MAX_FRAMES:
        _write()
        os._exit(0)


_orig_flip = pygame.display.flip
_orig_update = pygame.display.update


def flip():
    _orig_flip()
    _frame_done()


def update(*args, **kwargs):
    _orig_update(*args, **kwargs)
    _frame_done()


pygame.display.flip = flip
pygame.display.update = update


# ----- události -----
def _make_event(d):
    t = d["type"]
    attrs = {}
    if "key" in d:
        attrs["key"] = getattr(pygame, d["key"]) if isinstance(d["key"], str) else d["key"]
        attrs["unicode"] = d.get("unicode", "")
        attrs["mod"] = 0
    if "pos" in d:
        attrs["pos"] = tuple(d["pos"])
    if "button" in d:
        attrs["button"] = d["button"]
    if t == "MOUSEMOTION":
        attrs.setdefault("rel", (0, 0))
        attrs.setdefault("buttons", (0, 0, 0))
    return pygame.event.Event(getattr(pygame, t), **attrs)


def event_get(*args, **kwargs):
    k = _state["flips"]
    if _state["event_frame"] == k:
        return []
    _state["event_frame"] = k
    return [_make_event(d) for d in EVENTS.get(k, [])]


pygame.event.get = event_get
pygame.event.pump = lambda: None
pygame.event.poll = lambda: (event_get() or [pygame.event.Event(pygame.NOEVENT)])[0]


def _held_now():
    cur = []
    for frame, keys in HELD:
        if frame <= _state["flips"]:
            cur = keys
    return {getattr(pygame, k) for k in cur}


class _Keys:
    def __getitem__(self, key):
        return key in _held_now()


pygame.key.get_pressed = lambda: _Keys()


def mouse_get_pos():
    cur = [0, 0]
    for frame, pos in MOUSE:
        if frame <= _state["flips"]:
            cur = pos
    return tuple(cur)


pygame.mouse.get_pos = mouse_get_pos
pygame.mouse.get_pressed = lambda *a, **k: (False, False, False)


# ----- čas -----
class Clock:                      # pygame.time.Clock nejde zdědit, proto je vlastní náhrada
    def tick(self, framerate=0):
        R["fps"].append(framerate)
        return 16

    def tick_busy_loop(self, framerate=0):
        return self.tick(framerate)

    def get_fps(self):
        return float(R["fps"][-1]) if R["fps"] else 0.0

    def get_time(self):
        return 16

    def get_rawtime(self):
        return 16


pygame.time.Clock = Clock
pygame.time.delay = lambda ms: ms
pygame.time.wait = lambda ms: ms

# ----- kreslení, texty, soubory, zvuk -----


def _wrap_draw(name):
    orig = getattr(pygame.draw, name)

    def wrapper(*args, **kwargs):
        try:
            R["draws"].append({"name": name, "args": json.loads(json.dumps(args[1:], default=lambda o: list(o) if hasattr(o, "__iter__") else str(o))),
                               "frame": _state["flips"]})
        except Exception:
            R["draws"].append({"name": name, "args": [], "frame": _state["flips"]})
        return orig(*args, **kwargs)
    setattr(pygame.draw, name, wrapper)


for _n in ("rect", "circle", "line", "lines", "polygon", "ellipse", "arc", "aaline", "aalines"):
    if hasattr(pygame.draw, _n):
        _wrap_draw(_n)


class Font(pygame.font.Font):
    def render(self, text, antialias=True, color=(255, 255, 255), *args, **kwargs):
        R["texts"].append({"text": str(text), "frame": _state["flips"]})
        return super().render(text, antialias, color, *args, **kwargs)


pygame.font.Font = Font
pygame.font.SysFont = lambda name=None, size=24, *a, **k: Font(None, size)

_orig_load = pygame.image.load


def image_load(path, *args, **kwargs):
    R["images"].append(str(path))
    return _orig_load(path, *args, **kwargs)


pygame.image.load = image_load


class Sound(pygame.mixer.Sound):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._dilna_name = str(args[0]) if args else "?"

    def play(self, *args, **kwargs):
        R["sounds"].append({"file": self._dilna_name, "frame": _state["flips"]})
        return super().play(*args, **kwargs)


pygame.mixer.Sound = Sound

for _n in ("load", "play", "stop", "set_volume"):
    def _mk(n):
        orig = getattr(pygame.mixer.music, n)

        def w(*args, **kwargs):
            R["music"].append({"call": n, "args": [str(a) for a in args] + [f"{k}={v}" for k, v in kwargs.items()]})
            try:
                return orig(*args, **kwargs)
            except pygame.error:
                return None
        return w
    setattr(pygame.mixer.music, _n, _mk(_n))

# ----- spuštění programu studenta -----
sys.path.insert(0, os.path.dirname(os.path.abspath(student)))
ns = {"__name__": "__main__", "__file__": student, "__builtins__": __builtins__}
try:
    with open(student, encoding="utf-8") as f:
        code = compile(f.read(), student, "exec")
    with contextlib.redirect_stdout(_buf):
        exec(code, ns)
    R["ended"] = True
except SystemExit:
    R["ended"] = True
except BaseException as e:
    tb = traceback.extract_tb(e.__traceback__)
    mine = [t for t in tb if t.filename == student]
    R["error"] = {"type": type(e).__name__, "msg": str(e), "line": mine[-1].lineno if mine else None}
_write()
os._exit(0)
