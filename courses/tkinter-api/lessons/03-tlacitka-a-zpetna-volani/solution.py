import tkinter as tk
from tkinter import ttk

okno = tk.Tk()
okno.title("Potvrzení akce")
okno.geometry("420x240")

stav = ttk.Label(okno, text="Čekám na potvrzení.")
stav.pack(padx=16, pady=12)


def potvrd():
    stav.configure(text="Akce potvrzena.")


def obnov():
    stav.configure(text="Čekám na potvrzení.")


ttk.Button(okno, text="Potvrdit", command=potvrd).pack(pady=8)
ttk.Button(okno, text="Obnovit", command=obnov).pack(pady=8)

okno.mainloop()
