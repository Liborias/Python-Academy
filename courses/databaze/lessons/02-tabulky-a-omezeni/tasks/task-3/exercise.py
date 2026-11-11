# SQLite je součást standardní knihovny; spojení nepotřebuje síťový server.
import sqlite3
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory

def vytvor_vypujcky(con):
    # Doplňte skutečnou práci s databází podle zadání.
    raise NotImplementedError

# Při importu nic neotevíráme; ukázka pracuje jen s cvičnými daty.
if __name__ == '__main__':
    with closing(sqlite3.connect(':memory:', autocommit=True)) as con:
        vytvor_vypujcky(con)
        con.execute('INSERT INTO vypujcky (pomucka, clen) VALUES (?, ?)', ('Míč', 'Žofie'))
        print(con.execute('SELECT pomucka, clen, vraceno FROM vypujcky').fetchall())
