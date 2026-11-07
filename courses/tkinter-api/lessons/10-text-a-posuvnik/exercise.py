import tkinter as tk
from tkinter import ttk

okno = tk.Tk()
okno.title("Poznámkový blok")
okno.geometry("560x380")
okno.columnconfigure(0, weight=1)
okno.rowconfigure(0, weight=1)
text = tk.Text(okno, wrap="word", height=8, width=40)
text.grid(row=0, column=0, padx=(12, 0), pady=12, sticky="nsew")
# Dvě vazby: šipka posouvá text, text vrací polohu jezdce.
posuvnik = ttk.Scrollbar(okno, orient="vertical", command=None)
posuvnik.grid(row=0, column=1, padx=(0, 12), pady=12, sticky="ns")
# Připojte také zpětné hlášení polohy posuvníku.
radky = []
for cislo in range(1, 31):
    radky.append(f"Řádek {cislo}: poznámka k výuce.")
text.insert("1.0", "\n".join(radky))
zprava = ttk.Label(okno, text="Text můžete upravit.")
zprava.grid(row=2, column=0, columnspan=2, pady=8)

# Text má vlastní koncový znak nového řádku; ten do obsahu nezahrneme.
def spocitej():
    # Přečtěte aktuální obsah a vypočítejte oba počty.
    pass

ttk.Button(okno, text="Spočítat", command=spocitej).grid(row=1, column=0, columnspan=2, pady=8)
okno.mainloop()
