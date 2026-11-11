# Používáme skutečné SQLite ze standardní knihovny, bez síťového serveru.
import sqlite3
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory


def spojeni_s_vazbami(cesta):
    con = sqlite3.connect(cesta, autocommit=True)
    try:
        con.execute('PRAGMA foreign_keys = ON')
        if con.execute('PRAGMA foreign_keys').fetchone()[0] != 1:
            raise RuntimeError('Cizí klíče se nepodařilo zapnout.')
        con.autocommit = False
        return con
    except Exception:
        con.close()
        raise

# Ukázka se provede jen při spuštění souboru, nikoli při importu.
if __name__ == '__main__':
    with closing(spojeni_s_vazbami(':memory:')) as con:
        print('Vazby:', con.execute('PRAGMA foreign_keys').fetchone()[0])
        print('Autocommit:', con.autocommit)
