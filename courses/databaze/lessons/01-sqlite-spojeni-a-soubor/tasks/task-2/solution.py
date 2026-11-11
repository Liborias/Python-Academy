# SQLite je součást standardní knihovny; spojení nepotřebuje síťový server.
import sqlite3
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory

def pozdrav_sql(jmeno):
    with closing(sqlite3.connect(':memory:', autocommit=True)) as con:
        return con.execute("SELECT 'Ahoj, ' || ?", (jmeno,)).fetchone()[0]

# Při importu nic neotevíráme; ukázka pracuje jen s cvičnými daty.
if __name__ == '__main__':
    print(pozdrav_sql("Žofie O'Neil"))
