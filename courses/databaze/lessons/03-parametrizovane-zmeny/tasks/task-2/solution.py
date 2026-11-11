# SQLite je součást standardní knihovny; spojení nepotřebuje síťový server.
import sqlite3
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory

from schema import vytvor_pomucky, vytvor_kategorie, vytvor_udalosti
from podklady import priprav_sklad, vyzaduj_transakce, kladny_pocet

def pridej_vice(con, pomucky):
    con.executemany('INSERT INTO pomucky (nazev, kusy) VALUES (?, ?)', pomucky)

# Při importu nic neotevíráme; ukázka pracuje jen s cvičnými daty.
if __name__ == '__main__':
    with closing(sqlite3.connect(':memory:', autocommit=True)) as con:
        vytvor_pomucky(con)
        pridej_vice(con, ((jmeno, kusy) for jmeno, kusy in [('Šachy', 2), ('Míč', 4)]))
        print(con.execute('SELECT nazev, kusy FROM pomucky ORDER BY nazev').fetchall())
