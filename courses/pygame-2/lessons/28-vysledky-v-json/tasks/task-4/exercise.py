# Samostatná součást předání; import nic nespouští.
import os
from pathlib import Path
import json
import tempfile
from vysledky_podklady import platny_vysledek, vyber_vysledky, serad_vysledky, nacti_vysledky

def nacti_vysledky(cesta):
    # Doplňte podle zadání; různé správné postupy jsou vítané.
    raise NotImplementedError

# Samostatné spuštění; import nic nespouští.
if __name__ == '__main__':
    with tempfile.TemporaryDirectory() as adresar:
        cesta = Path(adresar) / 'vysledky.json'
        print('Chybějící:', nacti_vysledky(cesta))
        cesta.write_text('{rozbité', encoding='utf-8')
        print('Poškozené:', nacti_vysledky(cesta))
