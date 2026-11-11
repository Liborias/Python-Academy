# Samostatná součást předání; import nic nespouští.
import os
from pathlib import Path
import json
import tempfile
from vysledky_podklady import platny_vysledek, vyber_vysledky, serad_vysledky, nacti_vysledky

def uloz_vysledky(cesta, data):
    # Doplňte podle zadání; různé správné postupy jsou vítané.
    raise NotImplementedError

# Samostatné spuštění; import nic nespouští.
if __name__ == '__main__':
    with tempfile.TemporaryDirectory() as adresar:
        cesta = Path(adresar) / 'data' / 'vysledky.json'
        pocet = uloz_vysledky(cesta, [{'jmeno': 'Žofie', 'body': 7, 'uspech': True}])
        print('Uloženo:', pocet, 'Načteno:', nacti_vysledky(cesta))
