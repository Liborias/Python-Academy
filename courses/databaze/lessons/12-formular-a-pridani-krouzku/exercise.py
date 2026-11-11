# Widgety ukazují data; zápisy a transakce patří modelu.
import sqlite3
import tkinter as tk
from model_zaklad import EvidenceKrouzku
from priprava import cti_kapacitu
from pohled import postav
from spousteni import spust

class Aplikace:
    def __init__(self, okno, model):
        self.okno = okno
        self.model = model
        self.w = postav(okno)
        self.data = []
        self.w['pridat'].configure(command=self.pridej)
        self.w['obnovit'].configure(command=self.obnov)
        self.obnov()

    def obnov(self):
        # TODO: doplňte podle zadání a porovnejte s možným řešením.
        raise NotImplementedError('Doplňte úkol.')

    def pridej(self):
        # TODO: doplňte podle zadání a porovnejte s možným řešením.
        raise NotImplementedError('Doplňte úkol.')

# Paměťová ukázka neotevírá vlastní trvalý soubor uživatele.
if __name__ == '__main__':
    spust(Aplikace, EvidenceKrouzku, ':memory:', ukazka=True)
