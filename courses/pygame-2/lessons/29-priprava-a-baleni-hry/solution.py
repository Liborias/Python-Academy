# Samostatná součást předání; import nic nespouští.
import os
from pathlib import Path
import sys
import tempfile

def koren_aplikace(soubor, spustitelny, zmrazeno=False):
    zdroj = spustitelny if zmrazeno else soubor
    return Path(zdroj).resolve().parent

# Samostatné spuštění; import nic nespouští.
if __name__ == '__main__':
    print(koren_aplikace('/projekt/reseni.py', '/python/python.exe'))
