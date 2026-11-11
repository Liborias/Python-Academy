# SQLite je součást standardní knihovny; spojení nepotřebuje síťový server.
import sqlite3
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory

def otevri_databazi(cesta):
    # Doplňte skutečnou práci s databází podle zadání.
    raise NotImplementedError

# Při importu nic neotevíráme; ukázka pracuje jen s cvičnými daty.
if __name__ == '__main__':
    with closing(otevri_databazi(':memory:')) as con:
        print('Spojení používá SQLite:', con.execute('SELECT 2 + 3').fetchone()[0])
