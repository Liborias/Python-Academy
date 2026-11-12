# Vlastní varianta propojí inventární kód, dostupné kusy a aktivní výpůjčky.
import csv
from contextlib import closing
from model import Pujcovna
from soubory import bezpecny_cil

class MojePujcovna(Pujcovna):
    def karty(self):
        # TODO: doplňte podle zadání.
        raise NotImplementedError('Doplňte úkol.')

    def souhrn(self):
        # TODO: doplňte podle zadání.
        raise NotImplementedError('Doplňte úkol.')

    def stitky_csv(self,cesta):
        # TODO: doplňte podle zadání.
        raise NotImplementedError('Doplňte úkol.')
# Běžný běh vytvoří pouze ukázkový CSV v dočasné pracovní kopii Akademie.
if __name__ == '__main__':
    with closing(MojePujcovna(':memory:')) as model:
        mic = model.pridej_pomucku('Míč',2)
        model.pridej_pomucku('Krabice',0)
        vypujcka = model.pujc_kod(model.kod(mic),'Žofie')
        print('Karty:',model.karty())
        print('Souhrn:',model.souhrn())
        print('Exportováno:',model.stitky_csv('stitky.csv'))
        print('Vráceno:',model.vrat(vypujcka),'podruhé:',model.vrat(vypujcka))
