# SQLite je součást standardní knihovny; spojení nepotřebuje síťový server.
import sqlite3
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory

def vytvor_vypujcky(con):
    con.execute('''
        CREATE TABLE IF NOT EXISTS vypujcky (
            id INTEGER PRIMARY KEY,
            pomucka TEXT NOT NULL,
            clen TEXT NOT NULL,
            vraceno INTEGER NOT NULL DEFAULT 0 CHECK (vraceno IN (0, 1))
        )
    ''')

# Při importu nic neotevíráme; ukázka pracuje jen s cvičnými daty.
if __name__ == '__main__':
    with closing(sqlite3.connect(':memory:', autocommit=True)) as con:
        vytvor_vypujcky(con)
        con.execute('INSERT INTO vypujcky (pomucka, clen) VALUES (?, ?)', ('Míč', 'Žofie'))
        print(con.execute('SELECT pomucka, clen, vraceno FROM vypujcky').fetchall())
