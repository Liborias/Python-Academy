# SQLite je součást standardní knihovny; spojení nepotřebuje síťový server.
import sqlite3
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory

def verze_databaze(cesta):
    with closing(sqlite3.connect(cesta, autocommit=True)) as con:
        return con.execute('SELECT sqlite_version()').fetchone()[0]

# Při importu nic neotevíráme; ukázka pracuje jen s cvičnými daty.
if __name__ == '__main__':
    print('SQLite:', verze_databaze(':memory:'))
