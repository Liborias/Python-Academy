# Samostatná součást předání; import nic nespouští.
import os
from pathlib import Path
import sys
import tempfile

def prikaz_testu(python, koren):
    testy = (Path(koren).resolve() / 'testy')
    if not isinstance(python, str) or not python.strip() or not testy.is_dir():
        raise ValueError('Zadejte interpreter a složku s adresářem testy.')
    return [python, '-m', 'unittest', 'discover', '-s', str(testy), '-p', 'test_*.py']

# Samostatné spuštění; import nic nespouští.
if __name__ == '__main__':
    print(prikaz_testu(sys.executable, Path(__file__).resolve().parent))
