# Používáme skutečné SQLite ze standardní knihovny, bez síťového serveru.
import sqlite3
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory

from podklady import priprav_texty, priprav_souhrny, priprav_vazby
from relacni_schema import spojeni_s_vazbami

def presun_do_kategorie(con, pomucka_id, kategorie_id):
    # Doplňte podle zadání, SQL hodnoty patří do parametrů.
    raise NotImplementedError

# Ukázka se provede jen při spuštění souboru, nikoli při importu.
if __name__ == '__main__':
    with closing(spojeni_s_vazbami(':memory:')) as con:
        with con:
            priprav_vazby(con)
            print('Změněno:', presun_do_kategorie(con, 3, 7))
            print(con.execute('SELECT id,nazev,kategorie_id FROM pomucky ORDER BY id').fetchall())
