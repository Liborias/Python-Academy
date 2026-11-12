# Formulář převádí text, model vlastní SQL a transakce.
import sqlite3
import tkinter as tk
from prehledy import Tracker
from validace import cti_cislo
from pohled import postav
from spousteni import spust

class Aplikace:
    def __init__(self, okno, model):
        self.model = model
        self.w = postav(okno)
        self.obdobi = (None, None)
        self.data = []
        self.w['pridat'].configure(command=self.pridej)
        self.w['filtrovat'].configure(command=self.filtruj)
        self.w['vse'].configure(command=self.vse)
        self.obnov()

    def obnov(self, od=None, do=None):
        # TODO: doplňte podle zadání.
        raise NotImplementedError('Doplňte úkol.')

    def pridej(self):
        # TODO: doplňte podle zadání.
        raise NotImplementedError('Doplňte úkol.')

    def filtruj(self):
        # TODO: doplňte podle zadání.
        raise NotImplementedError('Doplňte úkol.')

    def vse(self):
        # TODO: doplňte podle zadání.
        raise NotImplementedError('Doplňte úkol.')
# Krátká paměťová evidence ukáže okno, vlastní soubor řeší uložený spouštěč.
if __name__ == '__main__':
    spust(Aplikace, Tracker, ':memory:', ukazka=True)
