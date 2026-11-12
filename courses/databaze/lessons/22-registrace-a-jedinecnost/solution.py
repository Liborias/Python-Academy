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
        jmeno = jmeno_uctu(jmeno)
        zaznam = vytvor_zaznam(heslo)
        text = json.dumps(zaznam, ensure_ascii=False, sort_keys=True)
        with self.con:
            return self.con.execute('INSERT INTO uzivatele(jmeno,overeni) VALUES(?,?)', (jmeno,text)).lastrowid

    def seznam(self):
        with self.con:
            return self.con.execute('SELECT id,jmeno FROM uzivatele ORDER BY id').fetchall()
# Nové spojení ukáže skutečné uložení; dočasná DB po ukázce zanikne.
if __name__ == '__main__':
    with TemporaryDirectory() as adresar:
        cesta = Path(adresar)/'ucty.sqlite3'
        with closing(Ucty(cesta)) as model:
            print('ID:', model.registruj('  Žofie  ', 'Cvičná fráze pro lekci!'))
        with closing(Ucty(cesta)) as model:
            print('Účty:', model.seznam())
