# Samostatná součást předání; import nic nespouští.
import os
from pathlib import Path
import sys
import tempfile

def chybejici_soubory(koren, povinne):
    koren = Path(koren)
    return sorted(jmeno for jmeno in povinne if not (koren / jmeno).is_file())

# Samostatné spuštění; import nic nespouští.
if __name__ == '__main__':
    with tempfile.TemporaryDirectory() as adresar:
        koren = Path(adresar)
        (koren / 'reseni.py').write_text('# Hra', encoding='utf-8')
        print(chybejici_soubory(koren, ['reseni.py', 'NAVOD.md']))
