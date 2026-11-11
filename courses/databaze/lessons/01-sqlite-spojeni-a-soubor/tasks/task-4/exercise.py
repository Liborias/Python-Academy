# SQLite je součást standardní knihovny; spojení nepotřebuje síťový server.
import sqlite3
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory

def pocet_tabulek(cesta):
    # Doplňte skutečnou práci s databází podle zadání.
    raise NotImplementedError

# Při importu nic neotevíráme; ukázka pracuje jen s cvičnými daty.
if __name__ == '__main__':
    with TemporaryDirectory() as adresar:
        cesta = Path(adresar) / 'pokus.sqlite3'
        with closing(sqlite3.connect(cesta, autocommit=True)) as con:
            con.execute('CREATE TABLE hraci (id INTEGER PRIMARY KEY)')
        print('Vlastní tabulky:', pocet_tabulek(cesta))
