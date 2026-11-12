"""Půjčovna používá datovou vrstvu z lekce 10 a inventární kódy z 26."""
from pathlib import Path
from evidence import Evidence
from luhn import kontrolni_cislice, platny_kod

class Pujcovna(Evidence):
    def __init__(self,cesta):
        self.cesta = None if str(cesta)==':memory:' else Path(cesta).resolve()
        super().__init__(cesta)

    def kod(self, ident):
        if type(ident) is not int or not 1<=ident<=2**63-1:
            raise ValueError('Id musí být kladné celé číslo SQLite.')
        with self.con:
            radek = self.con.execute('SELECT id FROM pomucky WHERE id=?',(ident,)).fetchone()
        if radek is None:
            raise ValueError('Pomůcka neexistuje.')
        telo = str(ident)
        return telo + kontrolni_cislice(telo)

    def id_z_kodu(self,kod):
        if not platny_kod(kod):
            raise ValueError('Neplatná kontrolní číslice.')
        telo = kod[:-1]
        ident = int(telo)
        if not 1<=ident<=2**63-1 or str(ident)!=telo:
            raise ValueError('Kód má mít kladné id bez úvodních nul.')
        with self.con:
            radek = self.con.execute('SELECT id FROM pomucky WHERE id=?',(ident,)).fetchone()
        if radek is None:
            raise ValueError('Pomůcka neexistuje.')
        return ident

    def pujc_kod(self,kod,clen):
        return self.pujc(self.id_z_kodu(kod),clen)
