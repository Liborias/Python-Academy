"""Pouze rozložení widgetů, bez SQL či otevření okna při importu."""
from datetime import date
import tkinter as tk
from tkinter import ttk

def postav(okno):
    okno.columnconfigure(0, weight=1)
    okno.rowconfigure(3, weight=1)
    w = {}
    formular = ttk.Frame(okno)
    formular.grid(row=0, column=0, sticky='ew', padx=14, pady=8)
    formular.columnconfigure(1, weight=1)
    for radek, (jmeno,popis) in enumerate([('den','Datum (RRRR-MM-DD)'),('hmotnost','Hmotnost (kg)'),('vyska','Výška (cm)'),('poznamka','Poznámka')]):
        ttk.Label(formular, text=popis).grid(row=radek, column=0, sticky='w', padx=(0,10), pady=4)
        w[jmeno] = ttk.Entry(formular, name=jmeno)
        w[jmeno].grid(row=radek, column=1, sticky='ew', pady=4)
    w['den'].insert(0, date.today().isoformat())
    w['vyska'].insert(0, '180')
    w['pridat'] = ttk.Button(formular, text='Uložit měření')
    w['pridat'].grid(row=4, column=1, sticky='w', pady=6)
    filtr = ttk.Frame(okno)
    filtr.grid(row=1, column=0, sticky='ew', padx=14, pady=8)
    for sloupec, (jmeno,popis) in enumerate([('od','Od'),('do','Do')]):
        ttk.Label(filtr, text=popis).grid(row=0, column=2*sloupec, padx=(0,5))
        w[jmeno] = ttk.Entry(filtr, name=jmeno, width=13)
        w[jmeno].grid(row=0, column=2*sloupec+1, padx=(0,10))
    w['filtrovat'] = ttk.Button(filtr, text='Použít období')
    w['filtrovat'].grid(row=1, column=0, columnspan=2, sticky='w', pady=6)
    w['vse'] = ttk.Button(filtr, text='Všechna měření')
    w['vse'].grid(row=1, column=2, columnspan=2, sticky='w', pady=6)
    w['souhrn'] = ttk.Label(okno, name='souhrn', text='', wraplength=610)
    w['souhrn'].grid(row=2, column=0, sticky='w', padx=14, pady=6)
    ramec = ttk.Frame(okno)
    ramec.grid(row=3, column=0, sticky='nsew', padx=14, pady=8)
    ramec.columnconfigure(0, weight=1)
    ramec.rowconfigure(0, weight=1)
    w['mereni'] = tk.Listbox(ramec, name='mereni', height=8, width=55, exportselection=False)
    w['mereni'].grid(row=0, column=0, sticky='nsew')
    posuvnik = ttk.Scrollbar(ramec, orient='vertical', command=w['mereni'].yview)
    posuvnik.grid(row=0, column=1, sticky='ns')
    w['mereni'].configure(yscrollcommand=posuvnik.set)
    ttk.Label(okno, text='BMI je orientační ukazatel pro dospělé, ne posouzení zdraví.', wraplength=610).grid(row=4, column=0, sticky='w', padx=14)
    w['stav'] = ttk.Label(okno, name='stav', text='Tracker je připravený.', wraplength=610)
    w['stav'].grid(row=5, column=0, sticky='w', padx=14, pady=10)
    return w
