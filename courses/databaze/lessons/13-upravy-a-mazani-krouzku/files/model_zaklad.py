# Model vlastní spojení a každou veřejnou databázovou operaci.
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory
from priprava import otevri_krouzky, cisty_nazev, kladna_kapacita

class EvidenceKrouzku:
    def __init__(self, cesta):
        self.con = otevri_krouzky(cesta)

    def close(self):
        self.con.close()

    def pridej(self, nazev, kapacita):
        nazev = cisty_nazev(nazev)
        kladna_kapacita(kapacita)
        with self.con:
            return self.con.execute('INSERT INTO krouzky(nazev, kapacita) VALUES (?, ?)',
                                    (nazev, kapacita)).lastrowid

    def seznam(self):
        with self.con:
            return self.con.execute('SELECT id, nazev, kapacita FROM krouzky ORDER BY id').fetchall()
