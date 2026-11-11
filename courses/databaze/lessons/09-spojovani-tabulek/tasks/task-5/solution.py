# Používáme skutečné SQLite ze standardní knihovny, bez síťového serveru.
import sqlite3
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory

from podklady import priprav_texty, priprav_souhrny, priprav_vazby
from relacni_schema import spojeni_s_vazbami
from relacni_schema import vytvor_relacni_schema

def vypujcky_clena(con, clen):
    return con.execute('''
        SELECT v.id, p.nazev FROM vypujcky AS v
        JOIN pomucky AS p ON v.pomucka_id = p.id
        WHERE v.clen = ? AND v.vraceno = 0 ORDER BY v.id
    ''', (clen,)).fetchall()

# Ukázka se provede jen při spuštění souboru, nikoli při importu.
if __name__ == '__main__':
    with closing(spojeni_s_vazbami(':memory:')) as con:
        with con:
            priprav_vazby(con)
            print(vypujcky_clena(con, 'Žofie'))
