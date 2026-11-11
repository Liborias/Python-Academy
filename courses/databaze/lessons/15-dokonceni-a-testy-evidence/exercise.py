# Testy používají skutečný model a pro každý případ vlastní dočasný soubor.
import sqlite3
import unittest
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory
from prihlasky import Model

def vytvor_sadu(Model):
    # TODO: doplňte podle zadání a porovnejte s možným řešením.
    raise NotImplementedError('Doplňte úkol.')

# Vytvoření sady samo nic nespouští; výsledek překládáme na návratový kód.
if __name__ == '__main__':
    vysledek = unittest.TextTestRunner(verbosity=2).run(vytvor_sadu(Model))
    raise SystemExit(0 if vysledek.wasSuccessful() else 1)
