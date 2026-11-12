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
        radky = self.prehled(od, do)
        with bezpecny_cil(cesta, self.cesta) as (docasny, cil):
            with docasny.open('w', encoding='utf-8', newline='') as soubor:
                zapis = csv.writer(soubor, delimiter=';')
                zapis.writerow(['id','datum','hmotnost_kg','vyska_cm','bmi','poznamka'])
                zapis.writerows(radky)
        return len(radky)

    def zaloha(self, cesta):
        with bezpecny_cil(cesta, self.cesta) as (docasny, cil):
            with closing(sqlite3.connect(docasny, autocommit=True)) as target:
                self.con.backup(target)
        return cil
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
