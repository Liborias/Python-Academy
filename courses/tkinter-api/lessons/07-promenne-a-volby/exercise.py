import tkinter as tk
from tkinter import ttk

okno = tk.Tk()
okno.title("Volby expedice")
okno.geometry("440x280")
# Vytvořte propojené proměnné, zaškrtávátko a společnou skupinu přepínačů.
vysledek = ttk.Label(okno, text="Zvolte možnosti a potvrďte.")
vysledek.pack(pady=12)

def zobraz():
    # Přečtěte aktuální volby a upravte výsledek.
    pass

ttk.Button(okno, text="Zobrazit volby", command=zobraz).pack(pady=8)
okno.mainloop()
