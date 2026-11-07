import tkinter as tk
from tkinter import ttk

okno = tk.Tk()
okno.title("Volby expedice")
okno.geometry("440x280")
# Proměnné vzniknou až po okně a propojí stav ovládacích prvků.
krehke = tk.IntVar(okno, value=0)
doprava = tk.StringVar(okno, value="odber")
ttk.Checkbutton(okno, text="Křehký obsah", variable=krehke, onvalue=1, offvalue=0).pack(pady=8)
ttk.Radiobutton(okno, text="Osobní odběr", variable=doprava, value="odber").pack(pady=4)
ttk.Radiobutton(okno, text="Kurýr", variable=doprava, value="kuryr").pack(pady=4)
vysledek = ttk.Label(okno, text="Zvolte možnosti a potvrďte.")
vysledek.pack(pady=12)

# Nastavení se čte teprve po potvrzení, nikoli při vytváření okna.
def zobraz():
    if doprava.get() == "odber":
        nazev = "odběr"
    else:
        nazev = "kurýr"
    if krehke.get() == 1:
        krehkost = "ano"
    else:
        krehkost = "ne"
    vysledek.configure(text=f"Doprava: {nazev}; křehké: {krehkost}.")

ttk.Button(okno, text="Zobrazit volby", command=zobraz).pack(pady=8)
okno.mainloop()
