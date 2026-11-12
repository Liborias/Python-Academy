# Každý test má vlastní dočasný soubor a zavře model před úklidem.
import sqlite3
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from contextlib import closing
from model import Pujcovna
from luhn import kontrolni_cislice

def vytvor_sadu(Pujcovna):
    # TODO: doplňte podle zadání.
    raise NotImplementedError('Doplňte úkol.')

# Sestavení sady nic nespouští, úspěch programu má návratový kód 0.
if __name__ == '__main__':
    vysledek = unittest.TextTestRunner(verbosity=2).run(vytvor_sadu(Pujcovna))
    raise SystemExit(0 if vysledek.wasSuccessful() else 1)
