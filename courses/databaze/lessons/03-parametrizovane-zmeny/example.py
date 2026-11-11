# SQLite je součást standardní knihovny; spojení nepotřebuje síťový server.
import sqlite3
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory

from schema import vytvor_pomucky, vytvor_kategorie, vytvor_udalosti
from podklady import priprav_sklad, vyzaduj_transakce, kladny_pocet

def pridej_pomucku(con, nazev, kusy):
    kurzor = con.execute('INSERT INTO pomucky (nazev, kusy) VALUES (?, ?)', (nazev, kusy))
    return kurzor.lastrowid

# Při importu nic neotevíráme; ukázka pracuje jen s cvičnými daty.
if __name__ == '__main__':
    with closing(sqlite3.connect(':memory:', autocommit=True)) as con:
        vytvor_pomucky(con)
        print('Nové ID:', pridej_pomucku(con, "Dětská kniha O'Neil", 3))
        print(con.execute('SELECT id, nazev, kusy FROM pomucky').fetchall())
