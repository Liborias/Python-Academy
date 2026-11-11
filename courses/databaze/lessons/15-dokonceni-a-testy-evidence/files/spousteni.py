"""Jedno okno a jedno spojení; ukázka v paměti, uložená aplikace se souborem."""
from contextlib import closing
from pathlib import Path
import argparse
import sqlite3
import tkinter as tk

def spust(Aplikace, Model, cesta, ukazka=False):
    with closing(Model(cesta)) as model:
        if ukazka:
            model.pridej('Robotika', 2)
            model.pridej('Šachy', 3)
        okno = tk.Tk()
        okno.title('Evidence kroužků')
        okno.geometry('880x740')
        okno.minsize(680, 600)
        try:
            Aplikace(okno, model)
            okno.mainloop()
        finally:
            try:
                okno.destroy()
            except tk.TclError:
                pass  # Zavření křížkem už mohlo okno zničit.

def konzole(Aplikace, Model, soubor):
    parser = argparse.ArgumentParser(description='Místní okenní evidence kroužků')
    parser.add_argument('--db', default=str(Path(soubor).with_name('krouzky.sqlite3')))
    args = parser.parse_args()
    try:
        spust(Aplikace, Model, args.db)
    except (sqlite3.Error, OSError, ValueError, tk.TclError) as chyba:
        parser.exit(2, f'Evidenci nelze otevřít: {chyba}\n')
