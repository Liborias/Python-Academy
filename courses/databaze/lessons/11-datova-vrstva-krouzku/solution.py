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
# Dočasný soubor ověří i znovuotevření; vaše vlastní data nemění.
if __name__ == '__main__':
    with TemporaryDirectory() as adresar:
        cesta = Path(adresar) / 'krouzky.sqlite3'
        with closing(EvidenceKrouzku(cesta)) as model:
            print('Nové ID:', model.pridej("  Robotika O'Neil  ", 2))
            print('Přehled:', model.seznam())
        with closing(EvidenceKrouzku(cesta)) as znovu:
            print('Po novém otevření:', znovu.seznam())
