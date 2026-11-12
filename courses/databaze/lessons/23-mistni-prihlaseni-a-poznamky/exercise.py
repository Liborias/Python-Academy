# Sezení drží identitu v paměti; každý dotaz poznámek má vazbu na její id.
from contextlib import closing
import sqlite3
from ucty import Ucty as ZakladniUcty
from hesla import over_heslo
from priprava import jmeno_uctu, nacti_overeni, NAHRADNI, over_poznamky

class Ucty(ZakladniUcty):
    def prihlaseni(self, jmeno, heslo):
        # TODO: doplňte podle zadání.
        raise NotImplementedError('Doplňte úkol.')

    def zapis(self, ident, texty):
        # TODO: doplňte podle zadání.
        raise NotImplementedError('Doplňte úkol.')

    def cti(self, ident):
        # TODO: doplňte podle zadání.
        raise NotImplementedError('Doplňte úkol.')

class Sezeni:
    def __init__(self, ucty):
        self.ucty = ucty
        self.uzivatel = None

    def prihlas(self, jmeno, heslo):
        # TODO: doplňte podle zadání.
        raise NotImplementedError('Doplňte úkol.')

    def odhlas(self):
        self.uzivatel = None

    def importuj(self, texty):
        # TODO: doplňte podle zadání.
        raise NotImplementedError('Doplňte úkol.')

    def uloz(self, text):
        return self.importuj([text])

    def seznam(self):
        # TODO: doplňte podle zadání.
        raise NotImplementedError('Doplňte úkol.')
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
