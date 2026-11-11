# Samostatná součást předání; import nic nespouští.
import os
from pathlib import Path
import sys
import tempfile

def prikaz_baleni(python, skript, vystup, jmeno='KuryrskaSmena'):
    skript, vystup = Path(skript).resolve(), Path(vystup).resolve()
    platne_jmeno = (isinstance(jmeno, str) and 1 <= len(jmeno) <= 40 and jmeno.isascii()
                    and jmeno[0].isalpha() and all(c.isalnum() or c in '_-' for c in jmeno))
    if not isinstance(python, str) or not python.strip() or not platne_jmeno or not skript.is_file() or skript.suffix.lower() != '.py':
        raise ValueError('Neplatný interpreter, skript nebo název aplikace.')
    return [python, '-m', 'PyInstaller', '--onedir', '--console', '--clean', '--noconfirm',
            '--name', jmeno, '--distpath', str(vystup / 'dist'),
            '--workpath', str(vystup / 'build'), '--specpath', str(vystup / 'spec'), str(skript)]

# Samostatné spuštění; import nic nespouští.
if __name__ == '__main__':
    print(prikaz_baleni(sys.executable, Path(__file__), 'sestaveni'))
