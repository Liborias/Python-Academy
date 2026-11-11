# SQLite je součást standardní knihovny; spojení nepotřebuje síťový server.
import sqlite3
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory

from schema import vytvor_pomucky, vytvor_kategorie, vytvor_udalosti
from podklady import priprav_sklad, vyzaduj_transakce, kladny_pocet

def presun_kusy(con, odkud, kam, kolik):
    # Doplňte skutečnou práci s databází podle zadání.
    raise NotImplementedError

# Při importu nic neotevíráme; ukázka pracuje jen s cvičnými daty.
if __name__ == '__main__':
    with TemporaryDirectory() as adresar:
        cesta = Path(adresar) / 'sklad.sqlite3'
        with closing(sqlite3.connect(cesta, autocommit=False)) as con:
            vytvor_pomucky(con)
            vytvor_udalosti(con)
            con.commit()
            priprav_sklad(con)
            con.commit()
            presun_kusy(con, 21, 10, 2)
            print('Přesun dokončen.')
        with closing(sqlite3.connect(cesta, autocommit=True)) as pozorovatel:
            print('Jiné spojení:', pozorovatel.execute('SELECT nazev, kusy FROM pomucky ORDER BY id').fetchall())
