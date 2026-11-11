# Samostatná součást předání; import nic nespouští.
import os
from pathlib import Path
import json
import tempfile
from vysledky_podklady import platny_vysledek, vyber_vysledky, serad_vysledky, nacti_vysledky

def nacti_vysledky(cesta):
    try:
        dokument = json.loads(Path(cesta).read_text(encoding='utf-8'))
    except (FileNotFoundError, json.JSONDecodeError, UnicodeDecodeError):
        return []
    if not isinstance(dokument, dict) or type(dokument.get('verze')) is not int or dokument['verze'] != 1:
        return []
    return vyber_vysledky(dokument.get('vysledky'))

# Samostatné spuštění; import nic nespouští.
if __name__ == '__main__':
    with tempfile.TemporaryDirectory() as adresar:
        cesta = Path(adresar) / 'vysledky.json'
        print('Chybějící:', nacti_vysledky(cesta))
        cesta.write_text('{rozbité', encoding='utf-8')
        print('Poškozené:', nacti_vysledky(cesta))
