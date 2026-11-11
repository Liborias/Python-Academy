# Přihláška má vlastní id; kapacitu hlídá datová operace, nikoli popisek okna.
import sqlite3
import tkinter as tk
from upravy import Model as PredchoziModel, Aplikace as Upravy
from priprava import cisty_nazev
from pohled import pridej_prihlasky
from spousteni import spust

class Model(PredchoziModel):
    def prihlasky(self, ident):
        # TODO: doplňte podle zadání a porovnejte s možným řešením.
        raise NotImplementedError('Doplňte úkol.')

    def prihlas(self, ident, clen):
        # TODO: doplňte podle zadání a porovnejte s možným řešením.
        raise NotImplementedError('Doplňte úkol.')

    def odhlas(self, ident):
        # TODO: doplňte podle zadání a porovnejte s možným řešením.
        raise NotImplementedError('Doplňte úkol.')

    def souhrn(self):
        # TODO: doplňte podle zadání a porovnejte s možným řešením.
        raise NotImplementedError('Doplňte úkol.')

class Aplikace(Upravy):
    def __init__(self, okno, model):
        super().__init__(okno, model)
        pridej_prihlasky(okno, self.w)
        self.clenove = []
        self.w['prihlasit'].configure(command=self.prihlas)
        self.w['odhlasit'].configure(command=self.odhlas)

    def obnov(self):
        super().obnov()
        if 'prihlasky' in self.w:
            self.obnov_prihlasky()

    def novy(self):
        super().novy()
        self.obnov_prihlasky()

    def vyber(self, udalost=None):
        super().vyber(udalost)
        self.obnov_prihlasky()

    def obnov_prihlasky(self):
        # TODO: doplňte podle zadání a porovnejte s možným řešením.
        raise NotImplementedError('Doplňte úkol.')

    def prihlas(self):
        # TODO: doplňte podle zadání a porovnejte s možným řešením.
        raise NotImplementedError('Doplňte úkol.')

    def odhlas(self):
        # TODO: doplňte podle zadání a porovnejte s možným řešením.
        raise NotImplementedError('Doplňte úkol.')

# Paměťová ukázka neotevírá vlastní trvalý soubor uživatele.
if __name__ == '__main__':
    spust(Aplikace, Model, ':memory:', ukazka=True)
