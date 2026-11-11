# SQLite je součást standardní knihovny; spojení nepotřebuje síťový server.
import sqlite3
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory

def vytvor_udalosti(con):
    con.execute('''
        CREATE TABLE IF NOT EXISTS udalosti (
            id INTEGER PRIMARY KEY,
            popis TEXT NOT NULL,
            poznamka TEXT
        )
    ''')

# Při importu nic neotevíráme; ukázka pracuje jen s cvičnými daty.
if __name__ == '__main__':
    with closing(sqlite3.connect(':memory:', autocommit=True)) as con:
        vytvor_udalosti(con)
        con.execute('INSERT INTO udalosti (popis) VALUES (?)', ('Otevření klubu',))
        print(con.execute('SELECT popis, poznamka FROM udalosti').fetchall())
