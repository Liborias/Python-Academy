# Samostatná součást předání; import nic nespouští.
import os
from pathlib import Path
import json
import tempfile
from vysledky_podklady import platny_vysledek, vyber_vysledky, serad_vysledky, nacti_vysledky

def vyber_vysledky(data):
    # Doplňte podle zadání; různé správné postupy jsou vítané.
    raise NotImplementedError

# Samostatné spuštění; import nic nespouští.
if __name__ == '__main__':
    print(vyber_vysledky([{'jmeno': '  Žofie ', 'body': 7, 'uspech': True}, {'jmeno': '', 'body': -1, 'uspech': False}]))
