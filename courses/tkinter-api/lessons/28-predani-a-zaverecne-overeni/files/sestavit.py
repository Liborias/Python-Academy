"""Ruční volitelné sestavení: python sestavit.py, ze složky projektu."""
from pathlib import Path
import subprocess
import shutil
import sys
from baleni import prikaz_sestaveni


if __name__ == "__main__":
    slozka = Path(__file__).resolve().parent
    prikaz = prikaz_sestaveni(sys.executable, slozka / "aplikace.py", slozka / "sestaveni")
    print("Sestavuji do:", slozka / "sestaveni")
    subprocess.run(prikaz, check=True)
    # Do předávané složky přidáme také návod a praktické scénáře.
    cil = slozka / "sestaveni" / "dist" / "KorespondencniDilna"
    for nazev in ("README.md", "SCENARE.md"):
        shutil.copy2(slozka / nazev, cil / nazev)
