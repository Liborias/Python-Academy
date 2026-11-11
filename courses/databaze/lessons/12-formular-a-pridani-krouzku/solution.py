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
        self.data = self.model.seznam()
        self.w['krouzky'].delete(0, tk.END)
        for ident, nazev, kapacita in self.data:
            self.w['krouzky'].insert(tk.END, f'{ident}: {nazev} (kapacita {kapacita})')

    def pridej(self):
        try:
            kapacita = cti_kapacitu(self.w['kapacita'].get())
            ident = self.model.pridej(self.w['nazev'].get(), kapacita)
        except ValueError as chyba:
            self.w['stav'].configure(text=str(chyba))
            return
        except sqlite3.IntegrityError:
            self.w['stav'].configure(text='Název kroužku už existuje.')
            return
        self.obnov()
        self.w['nazev'].delete(0, tk.END)
        self.w['kapacita'].delete(0, tk.END)
        self.w['kapacita'].insert(0, '10')
        self.w['stav'].configure(text=f'Přidán kroužek ID {ident}.')

# Paměťová ukázka neotevírá vlastní trvalý soubor uživatele.
if __name__ == '__main__':
    spust(Aplikace, EvidenceKrouzku, ':memory:', ukazka=True)
