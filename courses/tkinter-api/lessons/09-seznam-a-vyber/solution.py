import tkinter as tk
from tkinter import ttk

okno = tk.Tk()
okno.title("Plán dne")
okno.geometry("520x360")
okno.columnconfigure(0, weight=1)
okno.rowconfigure(1, weight=1)
vstup = ttk.Entry(okno)
vstup.grid(row=0, column=0, padx=12, pady=8, sticky="ew")
seznam = tk.Listbox(okno, selectmode="browse", exportselection=False)
seznam.grid(row=1, column=0, padx=12, pady=8, sticky="nsew")
zprava = ttk.Label(okno, text="Přidejte nebo odeberte úkol.")
zprava.grid(row=3, column=0, padx=12, pady=8)
# Data jsou obyčejný seznam; Listbox je jejich zobrazení.
ukoly = ["Přečíst zadání", "Vyzkoušet ukázku", "Přečíst zadání"]

def obnov():
    seznam.delete(0, tk.END)
    for ukol in ukoly:
        seznam.insert(tk.END, ukol)

def pridej():
    text = vstup.get().strip()
    if not text:
        zprava.configure(text="Napište název úkolu.")
        return
    ukoly.append(text)
    obnov()
    vstup.delete(0, tk.END)
    zprava.configure(text=f"Přidáno: {text}.")

# Curselection vrací n-tici indexů, nikoli text vybrané položky.
def odeber():
    vyber = seznam.curselection()
    if not vyber:
        zprava.configure(text="Nejprve vyberte úkol.")
        return
    text = ukoly.pop(vyber[0])
    obnov()
    zprava.configure(text=f"Odebráno: {text}.")

ovladani = ttk.Frame(okno)
ovladani.grid(row=2, column=0)
ttk.Button(ovladani, text="Přidat", command=pridej).pack(side="left", padx=8)
ttk.Button(ovladani, text="Odebrat", command=odeber).pack(side="left", padx=8)
obnov()
okno.mainloop()
