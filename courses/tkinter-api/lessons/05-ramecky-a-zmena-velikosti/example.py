import tkinter as tk
from tkinter import ttk

okno = tk.Tk()
okno.title("Příprava výpravy")
okno.geometry("480x240")
okno.minsize(360, 200)

# Okno umístí rámečky, horní rámeček pak umístí svůj vlastní obsah.
formular = ttk.Frame(okno, padding=12)
formular.pack(fill="x", padx=16, pady=12)
formular.columnconfigure(1, weight=1)
ttk.Label(formular, text="Název výpravy:").grid(row=0, column=0, padx=8)
nazev = ttk.Entry(formular)
nazev.grid(row=0, column=1, padx=8, sticky="ew")

# Pack v jiném rodiči nekoliduje s grid horního formuláře.
informace = ttk.Frame(okno, padding=12)
informace.pack(fill="x", padx=16, pady=8)
ttk.Label(informace, text="Formulář je připravený.").pack()
okno.mainloop()
