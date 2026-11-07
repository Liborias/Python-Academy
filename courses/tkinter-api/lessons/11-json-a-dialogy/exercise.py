import json
import tkinter as tk
from tkinter import ttk, filedialog

# Soubory používají UTF-8, aby byl český text čitelný i mimo program.
def uloz_poznamku(cesta, text):
    # Zapište objekt se skutečným textem do JSON v UTF-8.
    pass

def nacti_poznamku(cesta):
    # Načtěte a ověřte data, vraťte pouze text.
    pass


def hlavni():
    okno = tk.Tk()
    okno.title("Poznámka v JSON")
    okno.geometry("560x360")
    okno.columnconfigure(0, weight=1)
    okno.rowconfigure(0, weight=1)
    text = tk.Text(okno, wrap="word", height=8, width=40)
    text.grid(row=0, column=0, padx=12, pady=12, sticky="nsew")
    text.insert("1.0", "Moje první poznámka.\nDruhý řádek.")
    zprava = ttk.Label(okno, text="Poznámka zatím není uložená.")
    zprava.grid(row=2, column=0, pady=8)

    # Prázdná cesta znamená zrušený dialog, ne chybu souboru.
    def uloz():
        cesta = filedialog.asksaveasfilename(parent=okno, defaultextension=".json", filetypes=[("JSON", "*.json")])
        if not cesta:
            zprava.configure(text="Ukládání zrušeno.")
            return
        try:
            uloz_poznamku(cesta, text.get("1.0", "end-1c"))
        except OSError:
            zprava.configure(text="Soubor se nepodařilo uložit.")
            return
        zprava.configure(text="Poznámka uložena.")

    def nacti():
        cesta = filedialog.askopenfilename(parent=okno, filetypes=[("JSON", "*.json")])
        if not cesta:
            zprava.configure(text="Načítání zrušeno.")
            return
        try:
            novy_text = nacti_poznamku(cesta)
        except (OSError, ValueError):
            zprava.configure(text="Soubor se nepodařilo načíst.")
            return
        text.delete("1.0", "end")
        text.insert("1.0", novy_text)
        zprava.configure(text="Poznámka načtena.")

    ovladani = ttk.Frame(okno)
    ovladani.grid(row=1, column=0)
    ttk.Button(ovladani, text="Uložit JSON", command=uloz).pack(side="left", padx=8)
    ttk.Button(ovladani, text="Načíst JSON", command=nacti).pack(side="left", padx=8)
    okno.mainloop()


if __name__ == "__main__":
    hlavni()
