# Samostatná součást předání; import nic nespouští.
import os
from pathlib import Path
import json
import tempfile
from vysledky_podklady import platny_vysledek, vyber_vysledky, serad_vysledky, nacti_vysledky

def serad_vysledky(data, limit=5):
    if type(limit) is not int or limit < 0:
        raise ValueError('Limit musí být nezáporné celé číslo.')
    zaznamy = vyber_vysledky(data)
    return sorted(zaznamy, key=lambda z: (not z['uspech'], -z['body'], z['jmeno'].casefold()))[:limit]

# Samostatné spuštění; import nic nespouští.
if __name__ == '__main__':
    print(serad_vysledky([{'jmeno': 'Ada', 'body': 9, 'uspech': False}, {'jmeno': 'Žofie', 'body': 6, 'uspech': True}]))
