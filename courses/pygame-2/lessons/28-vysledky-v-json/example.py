# Samostatná součást předání; import nic nespouští.
import os
from pathlib import Path
import json
import tempfile
from vysledky_podklady import platny_vysledek, vyber_vysledky, serad_vysledky, nacti_vysledky

def platny_vysledek(zaznam):
    return (isinstance(zaznam, dict)
            and isinstance(zaznam.get('jmeno'), str)
            and 1 <= len(zaznam['jmeno'].strip()) <= 24
            and type(zaznam.get('body')) is int
            and zaznam['body'] >= 0
            and type(zaznam.get('uspech')) is bool)

# Samostatné spuštění; import nic nespouští.
if __name__ == '__main__':
    print(platny_vysledek({'jmeno': 'Žofie', 'body': 7, 'uspech': True}))
