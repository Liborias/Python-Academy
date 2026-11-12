# Datum seřazené jako ISO text odpovídá pořadí v kalendáři.
from contextlib import closing
from statistics import mean
from model import Tracker as ZakladniTracker
from priprava import over_datum
from vypocet import bmi

class Tracker(ZakladniTracker):
    def prehled(self, od=None, do=None):
        # TODO: doplňte podle zadání.
        raise NotImplementedError('Doplňte úkol.')

    def souhrn(self, od=None, do=None):
        # TODO: doplňte podle zadání.
        raise NotImplementedError('Doplňte úkol.')
# Dvě měření v jednom dni jsou dva záznamy, rozhoduje i id.
if __name__ == '__main__':
    with closing(Tracker(':memory:')) as model:
        model.pridej('2026-04-05', 81, 180, 'Druhý den')
        model.pridej('2026-04-01', 80, 180, 'První den')
        model.pridej('2026-04-05', 82, 180, 'Další záznam stejného dne')
        print('Období:', model.prehled('2026-04-05', '2026-04-05'))
        print('Souhrn:', model.souhrn())
