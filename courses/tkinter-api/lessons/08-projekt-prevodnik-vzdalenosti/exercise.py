import math
import tkinter as tk
from tkinter import ttk

# Výpočet nezná žádné widgety, lze ho použít i bez otevření okna.
def preved_vzdalenost(hodnota, smer):
    # Vraťte převedené číslo, ne text. Neplatný vstup odmítněte ValueError.
    pass


def hlavni():
    okno = tk.Tk()
    okno.title("Převodník vzdálenosti")
    okno.geometry("480x300")
    formular = ttk.Frame(okno, padding=16)
    formular.pack(fill="x")
    formular.columnconfigure(1, weight=1)
    ttk.Label(formular, text="Vzdálenost:").grid(row=0, column=0, padx=8, pady=8)
    vstup = ttk.Entry(formular)
    vstup.grid(row=0, column=1, padx=8, pady=8, sticky="ew")
    smer = tk.StringVar(okno, value="km-m")
    ttk.Radiobutton(formular, text="Kilometry na metry", variable=smer, value="km-m").grid(row=1, column=0, columnspan=2, sticky="w")
    ttk.Radiobutton(formular, text="Metry na kilometry", variable=smer, value="m-km").grid(row=2, column=0, columnspan=2, sticky="w")
    vysledek = ttk.Label(formular, text="Zadejte nezápornou vzdálenost.")
    vysledek.grid(row=4, column=0, columnspan=2, pady=12)

    # Okno převádí text na číslo a zobrazuje buď výsledek, nebo srozumitelnou chybu.
    def preved(udalost=None):
        # Přečtěte vstup, zavolejte výpočet a zobrazte výsledek nebo chybu.
        pass

    ttk.Button(formular, text="Převést", command=preved).grid(row=3, column=0, columnspan=2, pady=12)
    vstup.bind("<Return>", preved)
    vstup.focus_set()
    okno.mainloop()


if __name__ == "__main__":
    hlavni()
