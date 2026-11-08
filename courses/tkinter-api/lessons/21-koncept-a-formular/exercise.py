import tkinter as tk
from tkinter import ttk


def vytvor_koncept(prijemce, predmet, text, priloha=""):
    # TODO: ověřte typy a vraťte nový slovník se všemi předanými hodnotami.
    return {"prijemce": "", "predmet": "", "text": "", "priloha": ""}


def nahled_konceptu(koncept):
    return f"Komu: {koncept['prijemce']}\nPředmět: {koncept['predmet']}\n\n{koncept['text']}"


def hlavni():
    okno = tk.Tk()
    okno.title("Korespondenční dílna: koncept")
    okno.geometry("820x560")
    okno.minsize(620, 460)
    okno.columnconfigure(1, weight=1)
    okno.rowconfigure(2, weight=1)
    okno.rowconfigure(5, weight=1)
    ttk.Label(okno, text="Příjemce").grid(row=0, column=0, padx=10, pady=6)
    prijemce = ttk.Entry(okno, name="prijemce")
    prijemce.grid(row=0, column=1, padx=10, pady=6, sticky="ew")
    ttk.Label(okno, text="Předmět").grid(row=1, column=0, padx=10, pady=6)
    predmet = ttk.Entry(okno, name="predmet")
    predmet.grid(row=1, column=1, padx=10, pady=6, sticky="ew")
    ttk.Label(okno, text="Text").grid(row=2, column=0, padx=10, pady=6)
    telo = tk.Text(okno, name="telo", height=5, width=60, wrap="word")
    telo.grid(row=2, column=1, padx=10, pady=6, sticky="nsew")
    ttk.Label(okno, text="Náhled konceptu po posledním obnovení").grid(row=4, column=0, columnspan=2, pady=6)
    nahled = tk.Text(okno, name="nahled", height=5, width=60, wrap="word", state="disabled")
    nahled.grid(row=5, column=0, columnspan=2, padx=10, pady=6, sticky="nsew")
    stav = ttk.Label(okno, text="Koncept je připravený. Nic se neodesílá.")
    stav.grid(row=6, column=0, columnspan=2, pady=8)

    def obnov():
        # Aktuální hodnoty čteme až při kliknutí, nikoli při vytvoření okna.
        koncept = vytvor_koncept(prijemce.get(), predmet.get(), telo.get("1.0", "end-1c"))
        nahled.configure(state="normal")
        nahled.delete("1.0", "end")
        nahled.insert("1.0", nahled_konceptu(koncept))
        nahled.configure(state="disabled")
        stav.configure(text="Náhled byl obnoven. Nic se neodesílá.")

    ttk.Button(okno, text="Obnovit náhled", command=obnov).grid(row=3, column=0, columnspan=2, pady=8)
    prijemce.focus_set()
    okno.mainloop()


if __name__ == "__main__":
    hlavni()
