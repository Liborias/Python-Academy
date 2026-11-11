# Samostatná součást předání; import nic nespouští.
import os
from pathlib import Path
import sys
import tempfile

def prikaz_testu(python, koren):
    # Doplňte podle zadání; různé správné postupy jsou vítané.
    raise NotImplementedError

# Samostatné spuštění; import nic nespouští.
if __name__ == '__main__':
    print(prikaz_testu(sys.executable, Path(__file__).resolve().parent))
