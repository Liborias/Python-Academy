import json
import math
import queue
import threading
import tkinter as tk
from tkinter import ttk
import requests
from cvicne_api import cvicne_api
from kurzy import nacti_kurz, over_kurz

# Výpočet vrací číslo; text a zaokrouhlení patří až do okna.
def preved_castku(castka, kurz):
    for hodnota in (castka, kurz):
        if isinstance(hodnota, bool) or not isinstance(hodnota, (int, float)):
            raise ValueError("Hodnota musí být číslo.")
    try:
        castka, kurz = float(castka), float(kurz)
    except OverflowError:
        raise ValueError("Hodnota je příliš velká.") from None
    if not math.isfinite(castka) or not math.isfinite(kurz):
        raise ValueError("Hodnota musí být konečné číslo.")
    if castka < 0 or kurz <= 0:
        raise ValueError("Částka je nezáporná, kurz kladný.")
    vysledek = castka * kurz
    if not math.isfinite(vysledek):
        raise ValueError("Výsledek je příliš velký.")
    return vysledek


def nacti_kurz_soubor(cesta, mena):
    with open(cesta, encoding="utf-8") as soubor:
        data = json.load(soubor)
    symbol = mena.strip().upper()
    if not isinstance(data, dict) or symbol not in data:
        raise ValueError("Soubor nemá vybranou měnu.")
    return over_kurz(data[symbol], symbol)


def hlavni(adresa):
    okno = tk.Tk()
    okno.title("Převodník měn 2.0 – cvičná data")
    okno.geometry("680x440")
    vysledky = queue.Queue()
    mena = tk.StringVar(okno, value="EUR")
    zdroj = tk.StringVar(okno, value="api")
    nacteno = []
    castka = ttk.Entry(okno)
    castka.pack(fill="x", padx=20, pady=12)
    kurz_text = ttk.Label(okno, text="Kurz zatím není načtený.")
    kurz_text.pack(pady=8)
    vysledek_text = ttk.Label(okno, text="Výsledek: zatím nic.")
    vysledek_text.pack(pady=8)
    zprava = ttk.Label(okno, text="Vyberte zdroj a načtěte kurz.")
    zprava.pack(pady=8)

    def zmen_volbu():
        nacteno.clear()
        kurz_text.configure(text="Kurz zatím není načtený.")
        vysledek_text.configure(text="Výsledek: zatím nic.")
        prevod.configure(state="disabled")
        zprava.configure(text="Volba změněna. Načtěte nový kurz.")

    volby = []
    for text, promenna, hodnota in [("EUR", mena, "EUR"), ("USD", mena, "USD"), ("Cvičné API", zdroj, "api"), ("Cvičný soubor", zdroj, "soubor")]:
        prvek = ttk.Radiobutton(okno, text=text, variable=promenna, value=hodnota, command=zmen_volbu)
        prvek.pack()
        volby.append(prvek)

    # Všechny Tk hodnoty už byly zachycené jako obyčejné texty.
    def pracovnik(symbol, odkud):
        try:
            if odkud == "api":
                data = nacti_kurz(adresa + "/pomalu", symbol, timeout=2)
            else:
                data = nacti_kurz_soubor("kurzy.json", symbol)
            vysledky.put((True, data))
        except (requests.RequestException, OSError, ValueError) as chyba:
            vysledky.put((False, str(chyba)))

    def vyzvedni():
        try:
            uspech, data = vysledky.get_nowait()
        except queue.Empty:
            okno.after(25, vyzvedni)
            return
        nacti_tlacitko.configure(state="normal")
        for prvek in volby:
            prvek.configure(state="normal")
        if uspech:
            nacteno.append(data)
            kurz_text.configure(text=f"1 {data['mena']} = {data['czk_za_jednotku']:.2f} CZK | {data['datum']} | {data['zdroj']}")
            zprava.configure(text="Kurz načten. Převod používá zobrazená cvičná data.")
            prevod.configure(state="normal")
        else:
            zprava.configure(text="Kurz se nepodařilo načíst. Zvolte zdroj a zkuste to znovu.")

    def nacti():
        symbol, odkud = mena.get(), zdroj.get()
        nacteno.clear()
        kurz_text.configure(text="Kurz zatím není načtený.")
        vysledek_text.configure(text="Výsledek: zatím nic.")
        zprava.configure(text="Načítám kurz...")
        nacti_tlacitko.configure(state="disabled")
        prevod.configure(state="disabled")
        for prvek in volby:
            prvek.configure(state="disabled")
        threading.Thread(target=pracovnik, args=(symbol, odkud), daemon=True).start()
        okno.after(25, vyzvedni)

    def preved():
        if not nacteno:
            zprava.configure(text="Nejprve načtěte kurz.")
            return
        try:
            cislo = float(castka.get().strip().replace(",", "."))
            hodnota = preved_castku(cislo, nacteno[0]["czk_za_jednotku"])
        except ValueError:
            vysledek_text.configure(text="Výsledek: zatím nic.")
            zprava.configure(text="Zadejte platnou nezápornou částku.")
            return
        vysledek_text.configure(text=f"Výsledek: {hodnota:.2f} CZK")
        zprava.configure(text="Převod dokončen. Jde o cvičný výpočet.")

    nacti_tlacitko = ttk.Button(okno, text="Načíst kurz", command=nacti)
    nacti_tlacitko.pack(pady=10)
    prevod = ttk.Button(okno, text="Převést", command=preved, state="disabled")
    prevod.pack(pady=10)
    castka.focus_set()
    okno.mainloop()


if __name__ == "__main__":
    with cvicne_api() as adresa:
        hlavni(adresa)
