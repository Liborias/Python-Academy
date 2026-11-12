"""Připraví soubor ve stejné složce a cíl nahradí až po úplném úspěchu."""
from contextlib import contextmanager
import os
from pathlib import Path
import tempfile

@contextmanager
def bezpecny_cil(cesta, zdroj=None):
    cil = Path(cesta).resolve()
    if zdroj is not None:
        zdroj = Path(zdroj).resolve()
        if cil == zdroj or (cil.exists() and zdroj.exists() and cil.samefile(zdroj)):
            raise ValueError('Cíl nesmí přepsat právě otevřenou databázi.')
    fd, jmeno = tempfile.mkstemp(prefix='.bmi-', suffix='.tmp', dir=cil.parent)
    os.close(fd)
    docasny = Path(jmeno)
    try:
        yield docasny, cil
        os.replace(docasny, cil)
    finally:
        docasny.unlink(missing_ok=True)
