# Vlastní varianta propojí inventární kód, dostupné kusy a aktivní výpůjčky.
import csv
from contextlib import closing
from model import Pujcovna
from soubory import bezpecny_cil

class MojePujcovna(Pujcovna):
    def karty(self):
        with self.con:
            radky = self.con.execute("""
                SELECT p.id,p.nazev,p.kusy,COUNT(v.id)
                FROM pomucky AS p LEFT JOIN vypujcky AS v
                ON v.pomucka_id=p.id AND v.vraceno=0
                GROUP BY p.id,p.nazev,p.kusy ORDER BY p.id
            """).fetchall()
        return [{'id':ident,'nazev':nazev,'kod':self.kod(ident),'dostupne':kusy,
                 'vypujceno':pocet,'celkem':kusy+pocet} for ident,nazev,kusy,pocet in radky]

    def souhrn(self):
        karty = self.karty()
        return {'pomucky':len(karty), 'dostupne':sum(k['dostupne'] for k in karty),
                'vypujceno':sum(k['vypujceno'] for k in karty)}

    def stitky_csv(self,cesta):
        karty = self.karty()
        hlavicka = ['id','nazev','kod','dostupne','vypujceno','celkem']
        with bezpecny_cil(cesta,self.cesta) as (docasny,cil):
            with docasny.open('w',encoding='utf-8',newline='') as file:
                zapis = csv.DictWriter(file,fieldnames=hlavicka,delimiter=';')
                zapis.writeheader()
                zapis.writerows(karty)
        return len(karty)
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
