import queue
import threading
import tkinter as tk
from tkinter import ttk
import requests
from cvicne_api import cvicne_api
from kurzy import nacti_kurz


def hlavni(adresa):
    okno = tk.Tk()
    okno.title("API bez zamrznutí")
    okno.geometry("600x340")
    vysledky = queue.Queue()
    rezim = tk.StringVar(okno, value="/pomalu")
    zprava = ttk.Label(okno, text="Připraveno k načtení.")
    zprava.pack(pady=12)
    kurz_text = ttk.Label(okno, text="Kurz zatím není načtený.")
    kurz_text.pack(pady=8)
    pocitadlo = tk.IntVar(okno, value=0)
    pocet_text = ttk.Label(okno, text="Kliknutí: 0")
    pocet_text.pack(pady=8)

    def klikni():
        pocitadlo.set(pocitadlo.get() + 1)
        pocet_text.configure(text=f"Kliknutí: {pocitadlo.get()}")

    ttk.Button(okno, text="Klikni během načítání", command=klikni).pack(pady=8)
    volby = []
    for text, hodnota in [("Pomalá odpověď", "/pomalu"), ("Chyba serveru", "/chyba"), ("Běžná odpověď", "")]:
        prvek = ttk.Radiobutton(okno, text=text, variable=rezim, value=hodnota)
        prvek.pack()
        volby.append(prvek)

    # Pracovník pracuje pouze s obyčejnou adresou a frontou, nikdy s Tk.
    def pracovnik(url):
        try:
            data = nacti_kurz(url, "EUR", timeout=2)
            vysledky.put((True, data))
        except (requests.RequestException, ValueError) as chyba:
            vysledky.put((False, str(chyba)))

    def vyzvedni():
        try:
            uspech, data = vysledky.get_nowait()
        except queue.Empty:
            okno.after(25, vyzvedni)
            return
        # Po dokončení povolte nové načtení i volby.
        if uspech:
            zprava.configure(text="Kurz načten.")
            kurz_text.configure(text=f"1 EUR = {data['czk_za_jednotku']:.2f} CZK | {data['datum']} | {data['zdroj']}")
        else:
            zprava.configure(text="Kurz se nepodařilo načíst. Zkuste to znovu.")
            kurz_text.configure(text="Kurz zatím není načtený.")

    def nacti():
        # Volbu přečteme v hlavním vlákně, funkci předáme do target bez závorek.
        url = adresa + rezim.get()
        zprava.configure(text="Načítám kurz...")
        kurz_text.configure(text="Kurz zatím není načtený.")
        tlacitko.configure(state="disabled")
        for prvek in volby:
            prvek.configure(state="disabled")
        # Spusťte pracovníka s hotovou adresou a naplánujte kontrolu fronty.

    tlacitko = ttk.Button(okno, text="Načíst kurz", command=nacti)
    tlacitko.pack(pady=12)
    okno.mainloop()


if __name__ == "__main__":
    with cvicne_api() as adresa:
        hlavni(adresa)
