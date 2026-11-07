import tkinter as tk
from tkinter import ttk

okno = tk.Tk()
okno.title("Pozdrav z formuláře")
okno.geometry("440x220")
okno.columnconfigure(1, weight=1)

ttk.Label(okno, text="Vaše jméno:").grid(row=0, column=0, padx=12, pady=8, sticky="w")
jmeno = ttk.Entry(okno)
jmeno.grid(row=0, column=1, padx=12, pady=8, sticky="ew")
vysledek = ttk.Label(okno, text="Zadejte jméno a klikněte.")
vysledek.grid(row=2, column=0, columnspan=2, padx=12, pady=8)


def pozdrav():
    text = jmeno.get().strip()
    if not text:
        vysledek.configure(text="Zadejte jméno.")
    else:
        vysledek.configure(text=f"Ahoj, {text}!")


ttk.Button(okno, text="Pozdravit", command=pozdrav).grid(row=1, column=0, columnspan=2, padx=12, pady=8)

okno.mainloop()
