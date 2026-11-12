# Datum seřazené jako ISO text odpovídá pořadí v kalendáři.
from contextlib import closing
from statistics import mean
from model import Tracker as ZakladniTracker
from priprava import over_datum
from vypocet import bmi

class Tracker(ZakladniTracker):
    def prehled(self, od=None, do=None):
        if od is not None:
            od = over_datum(od)
        if do is not None:
            do = over_datum(do)
        if od is not None and do is not None and od > do:
            raise ValueError('Začátek období nesmí být po konci.')
        podminky = []
        parametry = []
        if od is not None:
            podminky.append('den >= ?')
            parametry.append(od)
        if do is not None:
            podminky.append('den <= ?')
            parametry.append(do)
        sql = 'SELECT id,den,hmotnost,vyska_cm,poznamka FROM mereni'
        if podminky:
            sql += ' WHERE ' + ' AND '.join(podminky)
        sql += ' ORDER BY den,id'
        with self.con:
            radky = self.con.execute(sql, parametry).fetchall()
        return [(ident, den, h, v, bmi(h, v), p) for ident, den, h, v, p in radky]

    def souhrn(self, od=None, do=None):
        radky = self.prehled(od, do)
        return {
            'pocet': len(radky),
            'prvni_den': radky[0][1] if radky else None,
            'posledni_den': radky[-1][1] if radky else None,
            'prumer_bmi': mean(r[4] for r in radky) if radky else None,
            'zmena_kg': radky[-1][2] - radky[0][2] if radky else None,
        }
# Dvě měření v jednom dni jsou dva záznamy, rozhoduje i id.
if __name__ == '__main__':
    with closing(Tracker(':memory:')) as model:
        model.pridej('2026-04-05', 81, 180, 'Druhý den')
        model.pridej('2026-04-01', 80, 180, 'První den')
        model.pridej('2026-04-05', 82, 180, 'Další záznam stejného dne')
        print('Období:', model.prehled('2026-04-05', '2026-04-05'))
        print('Souhrn:', model.souhrn())
