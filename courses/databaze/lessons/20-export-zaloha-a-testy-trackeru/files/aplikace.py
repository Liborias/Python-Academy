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
        radky = self.model.prehled(od, do)
        souhrn = self.model.souhrn(od, do)
        self.data = radky
        self.obdobi = (od, do)
        self.w['mereni'].delete(0, tk.END)
        for ident, den, h, v, hodnota, poznamka in radky:
            self.w['mereni'].insert(tk.END, f'{ident}: {den} | {h:g} kg / {v:g} cm | BMI {hodnota:.2f}')
        prumer = '—' if souhrn['prumer_bmi'] is None else f"{souhrn['prumer_bmi']:.2f}"
        self.w['souhrn'].configure(text=f"Počet: {souhrn['pocet']} | Průměr BMI: {prumer}")

    def pridej(self):
        try:
            ident = self.model.pridej(self.w['den'].get(), cti_cislo(self.w['hmotnost'].get()),
                                      cti_cislo(self.w['vyska'].get()), self.w['poznamka'].get())
        except ValueError as chyba:
            self.w['stav'].configure(text=str(chyba))
            return
        except sqlite3.Error:
            self.w['stav'].configure(text='Měření se nepodařilo uložit do databáze.')
            return
        self.w['hmotnost'].delete(0, tk.END)
        self.w['poznamka'].delete(0, tk.END)
        try:
            self.obnov(*self.obdobi)
        except sqlite3.Error:
            self.w['stav'].configure(text='Měření uloženo, přehled se nepodařilo obnovit.')
            return
        self.w['stav'].configure(text=f'Uloženo měření ID {ident}.')

    def filtruj(self):
        od = self.w['od'].get().strip() or None
        do = self.w['do'].get().strip() or None
        try:
            self.obnov(od, do)
        except ValueError as chyba:
            self.w['stav'].configure(text=str(chyba))
            return
        except sqlite3.Error:
            self.w['stav'].configure(text='Přehled se nepodařilo načíst z databáze.')
            return
        self.w['stav'].configure(text='Období použito.')

    def vse(self):
        try:
            self.obnov()
        except sqlite3.Error:
            self.w['stav'].configure(text='Přehled se nepodařilo načíst z databáze.')
            return
        self.w['od'].delete(0, tk.END)
        self.w['do'].delete(0, tk.END)
        self.w['stav'].configure(text='Zobrazuji všechna měření.')
