#!/usr/bin/env python3
"""Diagnostika prostředí: co je nainstalováno a co chybí.   python tools/doctor.py"""
import importlib.util
import os
import shutil
import subprocess
import sys

OK, NO, WARN = "[ OK ]", "[CHYBÍ]", "[POZOR]"
rows = []


def add(state, name, detail=""):
    rows.append((state, name, detail))


def module(name, pip=None, optional=False, note=""):
    if importlib.util.find_spec(name):
        try:
            m = __import__(name)
            v = getattr(m, "__version__", "") or getattr(m, "version", "")
            if name == "pygame" and hasattr(m, "IS_CE"):
                v = f"{m.version.ver} (pygame-ce)"
            elif name == "pygame":
                return add(WARN, "pygame", "je nainstalovaný původní pygame; kurz používá pygame-ce: "
                           "pip uninstall pygame && pip install pygame-ce")
        except Exception:
            v = ""
        add(OK, name, str(v))
    else:
        add(WARN if optional else NO, name, f"pip install {pip or name}" + (f"  ({note})" if note else ""))


v = sys.version_info
add(OK if v >= (3, 12) else (WARN if v >= (3, 11) else NO), "Python",
    f"{v.major}.{v.minor}.{v.micro}" + ("" if v >= (3, 12) else "  (doporučeno 3.12 a novější, ideálně 3.14)"))
in_venv = sys.prefix != getattr(sys, "base_prefix", sys.prefix)
add(OK if in_venv else WARN, "Virtuální prostředí",
    "aktivní" if in_venv else "neaktivní; vytvořte: python -m venv .venv  a aktivujte ho")
add(OK if shutil.which("pip") or importlib.util.find_spec("pip") else NO, "pip", "")

try:
    import tkinter
    add(OK, "tkinter", f"Tk {tkinter.TkVersion}")
except Exception as e:
    add(NO, "tkinter", f"{type(e).__name__}; Linux: sudo apt install python3-tk")

module("pygame", "pygame-ce")
for mod, pip in [("pandas", None), ("matplotlib", None), ("openpyxl", None), ("requests", None),
                 ("bs4", "beautifulsoup4"), ("qrcode", "qrcode[pil]"), ("pyttsx3", None)]:
    module(mod, pip, optional=True)

for exe, label in [("codium", "VSCodium (příkaz codium)"), ("vscodium", "VSCodium (příkaz vscodium)"),
                   ("git", "Git")]:
    p = shutil.which(exe)
    if exe == "vscodium" and (shutil.which("codium") or not shutil.which("vscodium")):
        continue
    add(OK if p else (NO if exe == "git" else WARN), label,
        p or ("nenalezen v PATH" + ("; aplikace funguje i bez něj" if exe != "git" else "")))

if shutil.which("codium"):
    try:
        out = subprocess.run(["codium", "--list-extensions"], capture_output=True, text=True, timeout=20).stdout
        have = set(out.lower().split())
        for ext, why in [("ms-python.python", "Python"), ("ms-python.debugpy", "ladění"),
                         ("detachhead.basedpyright", "našeptávání (náhrada Pylance)"),
                         ("charliermarsh.ruff", "kontrola stylu"), ("ms-toolsai.jupyter", "notebooky (Pandas)")]:
            add(OK if ext in have else WARN, f"rozšíření {ext}", why if ext in have else f"codium --install-extension {ext}")
    except Exception as e:
        add(WARN, "rozšíření VSCodium", f"nepodařilo se zjistit: {e}")

if os.name == "posix" and not (os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY")) and sys.platform != "darwin":
    add(WARN, "Grafické prostředí", "není DISPLAY; okna Tkinter a Pygame se neotevřou")

w = max(len(r[1]) for r in rows)
for s, n, d in rows:
    print(f"{s} {n:<{w}}  {d}")
bad = [r for r in rows if r[0] == NO]
print(f"\nChybí {len(bad)} povinných věcí." if bad else "\nZákladní prostředí je v pořádku.")
sys.exit(1 if bad else 0)
