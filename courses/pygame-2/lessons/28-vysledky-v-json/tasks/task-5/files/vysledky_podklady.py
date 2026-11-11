import json
import os
import tempfile
from pathlib import Path

def platny_vysledek(zaznam):
    return (isinstance(zaznam, dict)
            and isinstance(zaznam.get('jmeno'), str)
            and 1 <= len(zaznam['jmeno'].strip()) <= 24
            and type(zaznam.get('body')) is int
            and zaznam['body'] >= 0
            and type(zaznam.get('uspech')) is bool)

def vyber_vysledky(data):
    if not isinstance(data, list):
        return []
    return [{'jmeno': z['jmeno'].strip(), 'body': z['body'], 'uspech': z['uspech']}
            for z in data if platny_vysledek(z)]

def serad_vysledky(data, limit=5):
    if type(limit) is not int or limit < 0:
        raise ValueError('Limit musí být nezáporné celé číslo.')
    zaznamy = vyber_vysledky(data)
    return sorted(zaznamy, key=lambda z: (not z['uspech'], -z['body'], z['jmeno'].casefold()))[:limit]

def nacti_vysledky(cesta):
    try:
        dokument = json.loads(Path(cesta).read_text(encoding='utf-8'))
    except (FileNotFoundError, json.JSONDecodeError, UnicodeDecodeError):
        return []
    if not isinstance(dokument, dict) or type(dokument.get('verze')) is not int or dokument['verze'] != 1:
        return []
    return vyber_vysledky(dokument.get('vysledky'))

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
