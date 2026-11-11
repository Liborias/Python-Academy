# Samostatná součást předání; import nic nespouští.
import os
from pathlib import Path
import sys
import tempfile

def prikaz_spusteni(python, skript):
    # Doplňte podle zadání; různé správné postupy jsou vítané.
    raise NotImplementedError

# Samostatné spuštění; import nic nespouští.
if __name__ == '__main__':
    print(prikaz_spusteni(sys.executable, Path(__file__)))
