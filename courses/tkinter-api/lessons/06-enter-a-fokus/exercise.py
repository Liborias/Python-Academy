import tkinter as tk
from tkinter import ttk

okno = tk.Tk()
okno.title("Pozdrav klávesnicí")
okno.geometry("440x220")
okno.columnconfigure(1, weight=1)
ttk.Label(okno, text="Jméno:").grid(row=0, column=0, padx=12, pady=8)
jmeno = ttk.Entry(okno)
jmeno.grid(row=0, column=1, padx=12, pady=8, sticky="ew")
vysledek = ttk.Label(okno, text="Zadejte jméno.")
vysledek.grid(row=2, column=0, columnspan=2, padx=12, pady=8)

def pozdrav():
    # Doplňte nepovinný argument a společné zpracování jména.
    pass

ttk.Button(okno, text="Pozdravit", command=pozdrav).grid(row=1, column=0, columnspan=2, pady=8)
# Připojte Enter a nastavte fokus do vstupu.
okno.mainloop()
