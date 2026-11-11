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
        nazev = cisty_nazev(nazev)
        kladna_kapacita(kapacita)
        with self.con:
            pocet = self.con.execute('SELECT COUNT(*) FROM prihlasky WHERE krouzek_id = ?', (ident,)).fetchone()[0]
            if kapacita < pocet:
                raise ValueError('Kapacita nesmí být menší než počet přihlášek.')
            return self.con.execute('UPDATE krouzky SET nazev = ?, kapacita = ? WHERE id = ?',
                                    (nazev, kapacita, ident)).rowcount == 1

    def smaz(self, ident):
        with self.con:
            return self.con.execute('DELETE FROM krouzky WHERE id = ?', (ident,)).rowcount == 1

class Aplikace(Formular):
    def __init__(self, okno, model):
        super().__init__(okno, model)
        pridej_upravy(okno, self.w)
        self.w['novy'].configure(command=self.novy)
        self.w['upravit'].configure(command=self.uprav)
        self.w['smazat'].configure(command=self.smaz)
        self.w['krouzky'].bind('<<ListboxSelect>>', self.vyber)

    def vybrane_id(self):
        vyber = self.w['krouzky'].curselection()
        return self.data[vyber[0]][0] if vyber else None

    def vyber(self, udalost=None):
        vyber = self.w['krouzky'].curselection()
        if not vyber:
            return
        _, nazev, kapacita = self.data[vyber[0]]
        for klic, hodnota in [('nazev', nazev), ('kapacita', str(kapacita))]:
            self.w[klic].delete(0, tk.END)
            self.w[klic].insert(0, hodnota)

    def novy(self):
        self.w['krouzky'].selection_clear(0, tk.END)
        self.w['nazev'].delete(0, tk.END)
        self.w['kapacita'].delete(0, tk.END)
        self.w['kapacita'].insert(0, '10')

    def uprav(self):
        ident = self.vybrane_id()
        if ident is None:
            self.w['stav'].configure(text='Nejprve vyberte kroužek.')
            return
        try:
            uspech = self.model.uprav(ident, self.w['nazev'].get(), cti_kapacitu(self.w['kapacita'].get()))
        except ValueError as chyba:
            self.w['stav'].configure(text=str(chyba))
            return
        except sqlite3.IntegrityError:
            self.w['stav'].configure(text='Název kroužku už existuje.')
            return
        if not uspech:
            self.w['stav'].configure(text='Kroužek už neexistuje. Obnovte seznam.')
            return
        self.obnov()
        self.novy()
        self.w['stav'].configure(text='Změny uloženy.')

    def smaz(self):
        ident = self.vybrane_id()
        if ident is None:
            self.w['stav'].configure(text='Nejprve vyberte kroužek.')
            return
        try:
            uspech = self.model.smaz(ident)
        except sqlite3.IntegrityError:
            self.w['stav'].configure(text='Kroužek nelze smazat: odhlaste členy.')
            return
        self.obnov()
        self.novy()
        self.w['stav'].configure(text='Kroužek smazán.' if uspech else 'Kroužek už neexistuje.')

# Paměťová ukázka neotevírá vlastní trvalý soubor uživatele.
if __name__ == '__main__':
    spust(Aplikace, Model, ':memory:', ukazka=True)
