# Samostatná součást předání; import nic nespouští.
import os
from pathlib import Path
import json
import tempfile
from vysledky_podklady import platny_vysledek, vyber_vysledky, serad_vysledky, nacti_vysledky

def uloz_vysledky(cesta, data):
    cesta = Path(cesta)
    zaznamy = vyber_vysledky(data)
    cesta.parent.mkdir(parents=True, exist_ok=True)
    docasna = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=cesta.parent,
                                         prefix=cesta.name + '.', suffix='.tmp', delete=False) as soubor:
            docasna = Path(soubor.name)
            json.dump({'verze': 1, 'vysledky': zaznamy}, soubor, ensure_ascii=False, indent=2)
            soubor.write('\n')
        os.replace(docasna, cesta)
        return len(zaznamy)
    finally:
        if docasna is not None:
            docasna.unlink(missing_ok=True)

# Samostatné spuštění; import nic nespouští.
if __name__ == '__main__':
    with tempfile.TemporaryDirectory() as adresar:
        cesta = Path(adresar) / 'data' / 'vysledky.json'
        pocet = uloz_vysledky(cesta, [{'jmeno': 'Žofie', 'body': 7, 'uspech': True}])
        print('Uloženo:', pocet, 'Načteno:', nacti_vysledky(cesta))
