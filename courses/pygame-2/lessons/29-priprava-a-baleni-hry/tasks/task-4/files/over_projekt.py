# Spustí jen vlastní testy modelu; herní okno se neotevře.
import subprocess
import sys
from pathlib import Path
if __name__ == '__main__':
    koren = Path(__file__).resolve().parent
    p = subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', str(koren / 'testy')],
                       cwd=koren)
    raise SystemExit(p.returncode)
