#!/usr/bin/env python3
"""Vytvoří virtuální prostředí .venv a nainstaluje balíčky pro vybrané podkurzy.

  python tools/setup_env.py                 # základ + všechny podkurzy
  python tools/setup_env.py --courses pandas,pygame-1
  python tools/setup_env.py --dry-run       # jen vypíše, co by udělal
"""
import argparse
import os
import subprocess
import sys
import venv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# Balíčky podle podkurzů. Pygame: používáme pygame-ce (import pygame zůstává).
PACKAGES = {
    "priprava": [],
    "zaklady": [],
    "oop": [],
    "soubory-web": ["requests", "beautifulsoup4"],
    "pygame-1": ["pygame-ce"],
    "turtle-oop": ["requests"],
    "pandas": ["pandas>=3,<4", "matplotlib", "openpyxl", "ipykernel"],
    "tkinter-api": ["requests", "aiosmtpd>=1.4.6,<2"],
    "pygame-2": ["pygame-ce"],
    "databaze": [],
}


OPTIONAL_PACKAGES = {"tkinter-api": ["pyinstaller"], "databaze": ["qrcode[pil]>=8.2,<9", "psycopg[binary,pool]>=3.2,<4"]}


def venv_python(root: Path, venv_dir: str = ".venv") -> Path:
    d = root / venv_dir
    return d / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def wanted(courses: str, extras: bool = False) -> list[str]:
    ids = list(PACKAGES) if courses in ("", "all") else [c.strip() for c in courses.split(",") if c.strip()]
    bad = [c for c in ids if c not in PACKAGES]
    if bad:
        raise SystemExit(f"Neznámý podkurz: {', '.join(bad)}. Platné: {', '.join(PACKAGES)}")
    pk: list[str] = []
    for c in ids:
        for p in PACKAGES[c] + (OPTIONAL_PACKAGES.get(c, []) if extras else []):
            if p not in pk:
                pk.append(p)
    return pk


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--courses", default="all")
    ap.add_argument("--venv", default=".venv")
    ap.add_argument("--extras", action="store_true", help="také volitelné balíčky pro pozdější projekty")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-install", action="store_true", help="jen vytvořit prostředí")
    a = ap.parse_args()
    if sys.version_info < (3, 11):
        print("Je potřeba Python 3.11 nebo novější."); return 1
    pk = wanted(a.courses, a.extras)
    py = venv_python(ROOT, a.venv)
    print(f"Prostředí: {ROOT / a.venv}\nBalíčky: {', '.join(pk) or '(žádné)'}")
    if a.dry_run:
        print("(dry-run: nic se nevytvořilo)"); return 0
    if not py.exists():
        print("Vytvářím virtuální prostředí…")
        venv.EnvBuilder(with_pip=True, clear=False).create(ROOT / a.venv)
    if not a.no_install and pk:
        print("Instaluji balíčky (potřebuje internet)…")
        r = subprocess.run([str(py), "-m", "pip", "install", "--upgrade", "pip", *pk])
        if r.returncode:
            print("Instalace selhala. Zkontrolujte připojení; tkinter se instaluje zvlášť (viz docs/instalace.md)."); return r.returncode
    act = r".venv\Scripts\activate" if os.name == "nt" else "source .venv/bin/activate"
    print(f"\nHotovo. Aktivace v terminálu: {act}\nDále: python tools/install_extensions.py  a  python tools/doctor.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
