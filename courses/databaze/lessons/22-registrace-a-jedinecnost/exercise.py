# Scrypt proběhne před krátkou zapisovací transakcí, UNIQUE hlídá databáze.
import json
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory
from hesla import vytvor_zaznam
from priprava import otevri_ucty, jmeno_uctu

class Ucty:
    def __init__(self, cesta):
        self.cesta = None if str(cesta)==':memory:' else Path(cesta).resolve()
        self.con = otevri_ucty(cesta)

    def close(self):
        self.con.close()

    def registruj(self, jmeno, heslo):
        # TODO: doplňte podle zadání.
        raise NotImplementedError('Doplňte úkol.')

    def seznam(self):
        # TODO: doplňte podle zadání.
        raise NotImplementedError('Doplňte úkol.')
# Nové spojení ukáže skutečné uložení; dočasná DB po ukázce zanikne.
if __name__ == '__main__':
    with TemporaryDirectory() as adresar:
        cesta = Path(adresar)/'ucty.sqlite3'
        with closing(Ucty(cesta)) as model:
            print('ID:', model.registruj('  Žofie  ', 'Cvičná fráze pro lekci!'))
        with closing(Ucty(cesta)) as model:
            print('Účty:', model.seznam())
