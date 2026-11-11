# Přihláška má vlastní id; kapacitu hlídá datová operace, nikoli popisek okna.
import sqlite3
import tkinter as tk
from upravy import Model as PredchoziModel, Aplikace as Upravy
from priprava import cisty_nazev
from pohled import pridej_prihlasky
from spousteni import spust

class Model(PredchoziModel):
    def prihlasky(self, ident):
        with self.con:
            return self.con.execute('SELECT id, clen FROM prihlasky WHERE krouzek_id = ? ORDER BY id', (ident,)).fetchall()

    def prihlas(self, ident, clen):
        clen = cisty_nazev(clen)
        with self.con:
            radek = self.con.execute('SELECT kapacita FROM krouzky WHERE id = ?', (ident,)).fetchone()
            if radek is None:
                raise ValueError('Kroužek už neexistuje.')
            pocet = self.con.execute('SELECT COUNT(*) FROM prihlasky WHERE krouzek_id = ?', (ident,)).fetchone()[0]
            if pocet >= radek[0]:
                raise ValueError('Kroužek je plný.')
            return self.con.execute('INSERT INTO prihlasky(krouzek_id, clen) VALUES (?, ?)', (ident, clen)).lastrowid

    def odhlas(self, ident):
        with self.con:
            return self.con.execute('DELETE FROM prihlasky WHERE id = ?', (ident,)).rowcount == 1

    def souhrn(self):
        with self.con:
            return self.con.execute('''SELECT k.id, k.nazev, k.kapacita, COUNT(p.id)
                FROM krouzky AS k LEFT JOIN prihlasky AS p ON p.krouzek_id = k.id
                GROUP BY k.id, k.nazev, k.kapacita ORDER BY k.id''').fetchall()

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
        ident = self.vybrane_id()
        self.clenove = self.model.prihlasky(ident) if ident is not None else []
        self.w['prihlasky'].delete(0, tk.END)
        for klic, clen in self.clenove:
            self.w['prihlasky'].insert(tk.END, f'{klic}: {clen}')
        souhrn = next((r for r in self.model.souhrn() if r[0] == ident), None)
        popis = f'Obsazeno {souhrn[3]} / {souhrn[2]}' if souhrn else 'Vyberte kroužek pro přihlášky.'
        self.w['obsazenost'].configure(text=popis)

    def prihlas(self):
        ident = self.vybrane_id()
        if ident is None:
            self.w['stav'].configure(text='Nejprve vyberte kroužek.')
            return
        try:
            self.model.prihlas(ident, self.w['clen'].get())
        except ValueError as chyba:
            self.w['stav'].configure(text=str(chyba))
            return
        except sqlite3.IntegrityError:
            self.w['stav'].configure(text='Člen už je v tomto kroužku přihlášený.')
            return
        self.obnov_prihlasky()
        self.w['clen'].delete(0, tk.END)
        self.w['stav'].configure(text='Člen přihlášen.')

    def odhlas(self):
        vyber = self.w['prihlasky'].curselection()
        if not vyber:
            self.w['stav'].configure(text='Nejprve vyberte přihlášku.')
            return
        ident = self.clenove[vyber[0]][0]
        uspech = self.model.odhlas(ident)
        self.obnov_prihlasky()
        self.w['stav'].configure(text='Člen odhlášen.' if uspech else 'Přihláška už neexistuje.')

# Paměťová ukázka neotevírá vlastní trvalý soubor uživatele.
if __name__ == '__main__':
    spust(Aplikace, Model, ':memory:', ukazka=True)
