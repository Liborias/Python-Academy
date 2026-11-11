# Používáme skutečné SQLite ze standardní knihovny, bez síťového serveru.
import sqlite3
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory

from podklady import priprav_texty, priprav_souhrny, priprav_vazby
from relacni_schema import spojeni_s_vazbami
from relacni_schema import vytvor_relacni_schema

def bez_aktivni_vypujcky(con):
    return con.execute('''
        SELECT p.id, p.nazev, p.kusy FROM pomucky AS p
        WHERE NOT EXISTS (
            SELECT 1 FROM vypujcky AS v WHERE v.pomucka_id = p.id AND v.vraceno = 0
        ) ORDER BY p.id
    ''').fetchall()

# Ukázka se provede jen při spuštění souboru, nikoli při importu.
if __name__ == '__main__':
    with closing(spojeni_s_vazbami(':memory:')) as con:
        with con:
            priprav_vazby(con)
            print(bez_aktivni_vypujcky(con))
