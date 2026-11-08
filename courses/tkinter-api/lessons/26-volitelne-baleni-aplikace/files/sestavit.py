"""Ruční volitelné sestavení: python sestavit.py, až po dokončení reseni.py."""
from pathlib import Path
import subprocess
import sys
from reseni import prikaz_sestaveni


if __name__ == "__main__":
    slozka = Path(__file__).resolve().parent
    prikaz = prikaz_sestaveni(sys.executable, slozka / "dilna.py", slozka / "sestaveni")
    print("Sestavuji do:", slozka / "sestaveni")
    subprocess.run(prikaz, check=True)
