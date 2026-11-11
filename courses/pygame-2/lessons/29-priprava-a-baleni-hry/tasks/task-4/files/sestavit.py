# Volitelná stavba; až po ověření projektu a instalaci PyInstalleru.
import subprocess
import sys
from pathlib import Path
from reseni import prikaz_baleni
if __name__ == '__main__':
    koren = Path(__file__).resolve().parent
    prikaz = prikaz_baleni(sys.executable, koren / 'hra.py', koren / 'sestaveni')
    subprocess.run(prikaz, cwd=koren, check=True)
