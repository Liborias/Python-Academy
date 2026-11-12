# Model ukládá původní hodnoty, nikoli zaokrouhlený BMI.
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory
from priprava import otevri_tracker, over_mereni

class Tracker:
    def __init__(self, cesta):
        self.cesta = None if str(cesta) == ':memory:' else Path(cesta).resolve()
        self.con = otevri_tracker(cesta)

    def close(self):
        self.con.close()

    def pridej(self, den, hmotnost, vyska_cm, poznamka=''):
        hodnoty = over_mereni(den, hmotnost, vyska_cm, poznamka)
        with self.con:
            return self.con.execute('INSERT INTO mereni(den,hmotnost,vyska_cm,poznamka) VALUES(?,?,?,?)', hodnoty).lastrowid

    def seznam(self):
        with self.con:
            return self.con.execute('SELECT id,den,hmotnost,vyska_cm,poznamka FROM mereni ORDER BY den,id').fetchall()
# Nové spojení ověří, že měření bylo skutečně potvrzené.
if __name__ == '__main__':
    with TemporaryDirectory() as adresar:
        cesta = Path(adresar) / 'bmi.sqlite3'
        with closing(Tracker(cesta)) as model:
            print('ID:', model.pridej('2026-04-05', 81, 180, 'Ukázkové měření'))
        with closing(Tracker(cesta)) as znovu:
            print('Po novém otevření:', znovu.seznam())
