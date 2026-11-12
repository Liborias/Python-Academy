# CSV je přenos tabulky, záloha SQLite zachová celou databázi.
import csv
from contextlib import closing
from pathlib import Path
import sqlite3
from tempfile import TemporaryDirectory
from prehledy import Tracker as PredchoziTracker
from soubory import bezpecny_cil

class Tracker(PredchoziTracker):
    def export_csv(self, cesta, od=None, do=None):
        # TODO: doplňte podle zadání.
        raise NotImplementedError('Doplňte úkol.')

    def zaloha(self, cesta):
        # TODO: doplňte podle zadání.
        raise NotImplementedError('Doplňte úkol.')
# Zkouška používá jen TemporaryDirectory; vlastní evidenci nemění.
if __name__ == '__main__':
    with TemporaryDirectory() as adresar:
        slozka = Path(adresar)
        with closing(Tracker(':memory:')) as model:
            model.pridej('2026-04-01', 81, 180, 'Ukázka; český text')
            print('Exportováno řádků:', model.export_csv(slozka / 'mereni.csv'))
            kopie = model.zaloha(slozka / 'kopie.sqlite3')
        with closing(Tracker(kopie)) as znovu:
            print('Ze zálohy:', znovu.prehled())
