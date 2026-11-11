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
        # TODO: doplňte podle zadání a porovnejte s možným řešením.
        raise NotImplementedError('Doplňte úkol.')

    def seznam(self):
        # TODO: doplňte podle zadání a porovnejte s možným řešením.
        raise NotImplementedError('Doplňte úkol.')
# Dočasný soubor ověří i znovuotevření; vaše vlastní data nemění.
if __name__ == '__main__':
    with TemporaryDirectory() as adresar:
        cesta = Path(adresar) / 'krouzky.sqlite3'
        with closing(EvidenceKrouzku(cesta)) as model:
            print('Nové ID:', model.pridej("  Robotika O'Neil  ", 2))
            print('Přehled:', model.seznam())
        with closing(EvidenceKrouzku(cesta)) as znovu:
            print('Po novém otevření:', znovu.seznam())
