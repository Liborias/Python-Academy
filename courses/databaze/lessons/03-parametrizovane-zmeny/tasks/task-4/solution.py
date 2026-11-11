# SQLite je součást standardní knihovny; spojení nepotřebuje síťový server.
import sqlite3
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory

from schema import vytvor_pomucky, vytvor_kategorie, vytvor_udalosti
from podklady import priprav_sklad, vyzaduj_transakce, kladny_pocet

def smaz_pomucku(con, id_pomucky):
    return con.execute('DELETE FROM pomucky WHERE id = ?', (id_pomucky,)).rowcount

# Při importu nic neotevíráme; ukázka pracuje jen s cvičnými daty.
if __name__ == '__main__':
    with closing(sqlite3.connect(':memory:', autocommit=True)) as con:
        vytvor_pomucky(con)
        priprav_sklad(con)
        print('Smazáno:', smaz_pomucku(con, 10))
        print('Podruhé:', smaz_pomucku(con, 10))
