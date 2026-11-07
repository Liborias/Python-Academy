import tkinter as tk
from tkinter import ttk

okno = tk.Tk()
okno.title("Nástěnka")
okno.geometry("420x240")

# Vytvoření widgetu a jeho umístění jsou dva samostatné kroky.
nadpis = ttk.Label(okno, text="Expediční přehled")
nadpis.pack(padx=16, pady=12)
stav = ttk.Label(okno, text="Stav: připraveno")
# Pack řadí druhý popisek pod první a přidá vnější mezery.
stav.pack(padx=16, pady=12)

okno.mainloop()
