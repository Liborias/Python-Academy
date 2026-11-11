# SQLite je součást standardní knihovny; spojení nepotřebuje síťový server.
import sqlite3
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory

from schema import vytvor_pomucky, vytvor_kategorie, vytvor_udalosti
from podklady import priprav_sklad, vyzaduj_transakce, kladny_pocet

def malo_na_sklade(con, minimum):
    return con.execute('''
        SELECT id, nazev, kusy FROM pomucky WHERE kusy < ?
        ORDER BY kusy, nazev, id
    ''', (minimum,)).fetchall()

# Při importu nic neotevíráme; ukázka pracuje jen s cvičnými daty.
if __name__ == '__main__':
    with closing(sqlite3.connect(':memory:', autocommit=True)) as con:
        priprav_sklad(con)
        print(malo_na_sklade(con, 3))
