# Rozšiřujeme model i formulář z předchozích lekcí, neměníme jejich definice.
import sqlite3
import tkinter as tk
from model_zaklad import EvidenceKrouzku
from formular import Aplikace as Formular
from priprava import cisty_nazev, kladna_kapacita, cti_kapacitu
from pohled import pridej_upravy
from spousteni import spust

class Model(EvidenceKrouzku):
    def uprav(self, ident, nazev, kapacita):
        # TODO: doplňte podle zadání a porovnejte s možným řešením.
        raise NotImplementedError('Doplňte úkol.')

    def smaz(self, ident):
        # TODO: doplňte podle zadání a porovnejte s možným řešením.
        raise NotImplementedError('Doplňte úkol.')

class Aplikace(Formular):
    def __init__(self, okno, model):
        super().__init__(okno, model)
        pridej_upravy(okno, self.w)
        self.w['novy'].configure(command=self.novy)
        self.w['upravit'].configure(command=self.uprav)
        self.w['smazat'].configure(command=self.smaz)
        self.w['krouzky'].bind('<<ListboxSelect>>', self.vyber)

    def vybrane_id(self):
        # TODO: doplňte podle zadání a porovnejte s možným řešením.
        raise NotImplementedError('Doplňte úkol.')

    def vyber(self, udalost=None):
        # TODO: doplňte podle zadání a porovnejte s možným řešením.
        raise NotImplementedError('Doplňte úkol.')

    def novy(self):
        self.w['krouzky'].selection_clear(0, tk.END)
        self.w['nazev'].delete(0, tk.END)
        self.w['kapacita'].delete(0, tk.END)
        self.w['kapacita'].insert(0, '10')

    def uprav(self):
        # TODO: doplňte podle zadání a porovnejte s možným řešením.
        raise NotImplementedError('Doplňte úkol.')

    def smaz(self):
        # TODO: doplňte podle zadání a porovnejte s možným řešením.
        raise NotImplementedError('Doplňte úkol.')

# Paměťová ukázka neotevírá vlastní trvalý soubor uživatele.
if __name__ == '__main__':
    spust(Aplikace, Model, ':memory:', ukazka=True)
