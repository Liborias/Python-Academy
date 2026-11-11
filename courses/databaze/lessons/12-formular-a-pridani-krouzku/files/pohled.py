"""Rozložení widgetů; neprovádí SQL a nevytváří databázi při importu."""
import tkinter as tk
from tkinter import ttk

def postav(okno):
    okno.columnconfigure(0, weight=1)
    okno.rowconfigure(2, weight=1)
    w = {}
    formular = ttk.Frame(okno)
    formular.grid(row=0, column=0, sticky='ew', padx=14, pady=10)
    formular.columnconfigure(1, weight=1)
    for radek, (jmeno, popisek) in enumerate([('nazev','Název kroužku'),('kapacita','Kapacita')]):
        ttk.Label(formular, text=popisek).grid(row=radek, column=0, sticky='w', padx=(0,10), pady=4)
        w[jmeno] = ttk.Entry(formular, name=jmeno)
        w[jmeno].grid(row=radek, column=1, sticky='ew', pady=4)
    ovladani = ttk.Frame(okno)
    ovladani.grid(row=1, column=0, sticky='w', padx=14, pady=4)
    for i, (jmeno, titulek) in enumerate([('pridat','Přidat kroužek'),('obnovit','Obnovit')]):
        w[jmeno] = ttk.Button(ovladani, text=titulek)
        w[jmeno].grid(row=0, column=i, padx=(0,8))
    ramec = ttk.Frame(okno)
    ramec.grid(row=2, column=0, sticky='nsew', padx=14, pady=8)
    ramec.columnconfigure(0, weight=1)
    ramec.rowconfigure(0, weight=1)
    w['krouzky'] = tk.Listbox(ramec, name='krouzky', exportselection=False, height=6, width=50)
    w['krouzky'].grid(row=0, column=0, sticky='nsew')
    posuvnik = ttk.Scrollbar(ramec, orient='vertical', command=w['krouzky'].yview)
    posuvnik.grid(row=0, column=1, sticky='ns')
    w['krouzky'].configure(yscrollcommand=posuvnik.set)
    w['stav'] = ttk.Label(okno, name='stav', text='Evidence je připravená.', wraplength=620)
    w['stav'].grid(row=9, column=0, sticky='w', padx=14, pady=12)
    w['kapacita'].insert(0, '10')
    return w

def pridej_upravy(okno, w):
    ramec = ttk.Frame(okno)
    ramec.grid(row=3, column=0, sticky='w', padx=14, pady=4)
    for i, (jmeno, titulek) in enumerate([('novy','Nový formulář'),('upravit','Uložit změny'),('smazat','Smazat kroužek')]):
        w[jmeno] = ttk.Button(ramec, text=titulek)
        w[jmeno].grid(row=0, column=i, padx=(0,8))

def pridej_prihlasky(okno, w):
    ramec = ttk.Frame(okno)
    ramec.grid(row=4, column=0, sticky='nsew', padx=14, pady=8)
    ramec.columnconfigure(1, weight=1)
    ramec.rowconfigure(2, weight=1)
    okno.rowconfigure(4, weight=1)
    w['obsazenost'] = ttk.Label(ramec, name='obsazenost', text='Vyberte kroužek pro přihlášky.')
    w['obsazenost'].grid(row=0, column=0, columnspan=3, sticky='w', pady=4)
    ttk.Label(ramec, text='Jméno člena').grid(row=1, column=0, sticky='w', padx=(0,8))
    w['clen'] = ttk.Entry(ramec, name='clen')
    w['clen'].grid(row=1, column=1, sticky='ew')
    w['prihlasit'] = ttk.Button(ramec, text='Přihlásit člena')
    w['prihlasit'].grid(row=1, column=2, padx=(8,0))
    w['prihlasky'] = tk.Listbox(ramec, name='prihlasky', exportselection=False, height=5, width=45)
    w['prihlasky'].grid(row=2, column=0, columnspan=2, sticky='nsew', pady=8)
    posuvnik = ttk.Scrollbar(ramec, orient='vertical', command=w['prihlasky'].yview)
    posuvnik.grid(row=2, column=2, sticky='ns', pady=8)
    w['prihlasky'].configure(yscrollcommand=posuvnik.set)
    w['odhlasit'] = ttk.Button(ramec, text='Odhlásit člena')
    w['odhlasit'].grid(row=3, column=0, columnspan=2, sticky='w')
