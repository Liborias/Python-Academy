import tkinter as tk
from tkinter import ttk

okno = tk.Tk()
okno.title("Potvrzení akce")
okno.geometry("420x240")

stav = ttk.Label(okno, text="Čekám na potvrzení.")
stav.pack(padx=16, pady=12)


def potvrd():
    # Doplňte reakci podle zadání.
    pass


def obnov():
    # Doplňte reakci podle zadání.
    pass


ttk.Button(okno, text="Potvrdit", command=None).pack(pady=8)
ttk.Button(okno, text="Obnovit", command=None).pack(pady=8)

okno.mainloop()
