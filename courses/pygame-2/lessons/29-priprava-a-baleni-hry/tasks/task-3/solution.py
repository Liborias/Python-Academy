# Samostatná součást předání; import nic nespouští.
import os
from pathlib import Path
import sys
import tempfile

def prikaz_spusteni(python, skript):
    skript = Path(skript).resolve()
    if not isinstance(python, str) or not python.strip() or not skript.is_file() or skript.suffix.lower() != '.py':
        raise ValueError('Zadejte interpreter a existující Python soubor.')
    return [python, '-X', 'utf8', str(skript)]

# Samostatné spuštění; import nic nespouští.
if __name__ == '__main__':
    print(prikaz_spusteni(sys.executable, Path(__file__)))
