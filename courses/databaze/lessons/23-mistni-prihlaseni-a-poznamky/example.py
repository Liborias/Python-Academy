# Sezení drží identitu v paměti; každý dotaz poznámek má vazbu na její id.
from contextlib import closing
import sqlite3
from ucty import Ucty as ZakladniUcty
from hesla import over_heslo
from priprava import jmeno_uctu, nacti_overeni, NAHRADNI, over_poznamky

class Ucty(ZakladniUcty):
    def prihlaseni(self, jmeno, heslo):
        try:
            jmeno = jmeno_uctu(jmeno)
        except ValueError:
            return None
        with self.con:
            radek = self.con.execute('SELECT id,jmeno,overeni FROM uzivatele WHERE jmeno=?', (jmeno,)).fetchone()
        zaznam = nacti_overeni(radek[2]) if radek else NAHRADNI
        overeno = over_heslo(heslo, zaznam)
        return (radek[0],radek[1]) if radek and overeno else None

    def zapis(self, ident, texty):
        texty = over_poznamky(texty)
        with self.con:
            self.con.executemany('INSERT INTO poznamky(uzivatel_id,text) VALUES(?,?)', [(ident,text) for text in texty])
        return len(texty)

    def cti(self, ident):
        with self.con:
            return self.con.execute('SELECT id,text FROM poznamky WHERE uzivatel_id=? ORDER BY id', (ident,)).fetchall()

class Sezeni:
    def __init__(self, ucty):
        self.ucty = ucty
        self.uzivatel = None

    def prihlas(self, jmeno, heslo):
        self.uzivatel = None
        self.uzivatel = self.ucty.prihlaseni(jmeno, heslo)
        return self.uzivatel is not None

    def odhlas(self):
        self.uzivatel = None

    def importuj(self, texty):
        if self.uzivatel is None:
            raise PermissionError('Nejprve se přihlaste.')
        return self.ucty.zapis(self.uzivatel[0], texty)

    def uloz(self, text):
        return self.importuj([text])

    def seznam(self):
        if self.uzivatel is None:
            raise PermissionError('Nejprve se přihlaste.')
        return self.ucty.cti(self.uzivatel[0])
# Příklad nesbírá skutečná hesla, nová aplikace začíná bez přihlášení.
if __name__ == '__main__':
    with closing(Ucty(':memory:')) as model:
        model.registruj('Žofie', 'Cvičná fráze pro lekci!')
        sezeni = Sezeni(model)
        print('Přihlášeno:', sezeni.prihlas('ŽOFIE','Cvičná fráze pro lekci!'))
        sezeni.uloz('Moje fiktivní poznámka')
        print('Poznámky:', sezeni.seznam())
        sezeni.odhlas()
        print('Po odhlášení:', sezeni.uzivatel)
