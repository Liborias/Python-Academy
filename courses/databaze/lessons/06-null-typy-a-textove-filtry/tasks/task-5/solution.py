# Používáme skutečné SQLite ze standardní knihovny, bez síťového serveru.
import sqlite3
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory

from podklady import priprav_texty, priprav_souhrny, priprav_vazby

def zkus_typy(hodnoty):
    with closing(sqlite3.connect(':memory:', autocommit=True)) as con:
        con.execute('CREATE TABLE hodnoty (volna, cele INTEGER)')
        con.executemany('INSERT INTO hodnoty VALUES (?, ?)', ((v, v) for v in hodnoty))
        return con.execute('SELECT typeof(volna), typeof(cele), volna, cele FROM hodnoty ORDER BY rowid').fetchall()

# Ukázka se provede jen při spuštění souboru, nikoli při importu.
if __name__ == '__main__':
    print(zkus_typy(['003', 2.0, 'ahoj', None]))
