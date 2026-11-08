from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog
from koncept import vytvor_koncept
from zpravy import vytvor_zpravu, over_adresu, nahled_zpravy
from prilohy import pridej_prilohu


class ChybaPole(ValueError):
    def __init__(self, pole, zprava):
        super().__init__(zprava)
        self.pole = pole


def sestav_zpravu(koncept):
    if not isinstance(koncept, dict) or any(k not in koncept for k in ("prijemce", "predmet", "text", "priloha")):
        raise ChybaPole("koncept", "Koncept nemá všechna pole.")
    try:
        kandidat = vytvor_koncept(koncept["prijemce"], koncept["predmet"], koncept["text"], koncept["priloha"])
    except ValueError:
        raise ChybaPole("koncept", "Pole konceptu musí být texty.") from None
    try:
        prijemce = over_adresu(kandidat["prijemce"])
    except ValueError:
        raise ChybaPole("prijemce", "Příjemce: zadejte jednu platnou adresu.") from None
    predmet = kandidat["predmet"]
    if not predmet.strip() or "\r" in predmet or "\n" in predmet:
        raise ChybaPole("predmet", "Předmět: napište neprázdný text bez nového řádku.")
    if not kandidat["text"].strip():
        raise ChybaPole("text", "Text: napište tělo zprávy.")
    zprava = vytvor_zpravu("eva@example.test", prijemce, predmet, kandidat["text"])
    if kandidat["priloha"]:
        try:
            pridej_prilohu(zprava, kandidat["priloha"])
        except (OSError, ValueError):
            raise ChybaPole("priloha", "Příloha: soubor nelze načíst nebo překračuje 1 000 000 B.") from None
    return zprava


def nahled_s_prilohou(zprava):
    text = nahled_zpravy(zprava)
    for priloha in zprava.iter_attachments():
        text += f"\nPříloha: {priloha.get_filename()} | {priloha.get_content_type()} | {len(priloha.get_payload(decode=True))} B\n"
    return text


def hlavni():
    okno = tk.Tk()
    okno.title("Korespondenční dílna")
    okno.geometry("940x740")
    okno.minsize(760, 620)
    okno.columnconfigure(1, weight=1)
    okno.rowconfigure(2, weight=1)
    okno.rowconfigure(7, weight=1)
    model = {"priloha": "", "busy": False, "nutna_kontrola": False}
    ttk.Label(okno, text="Příjemce").grid(row=0, column=0, padx=10, pady=4)
    prijemce = ttk.Entry(okno, name="prijemce")
    prijemce.grid(row=0, column=1, padx=10, pady=4, sticky="ew")
    ttk.Label(okno, text="Předmět").grid(row=1, column=0, padx=10, pady=4)
    predmet = ttk.Entry(okno, name="predmet")
    predmet.grid(row=1, column=1, padx=10, pady=4, sticky="ew")
    ttk.Label(okno, text="Text").grid(row=2, column=0, padx=10, pady=4)
    telo = tk.Text(okno, name="telo", height=5, width=70, wrap="word")
    telo.grid(row=2, column=1, padx=10, pady=4, sticky="nsew")
    soubor_text = ttk.Label(okno, name="soubor", text="Bez přílohy.")
    soubor_text.grid(row=3, column=0, columnspan=2, padx=10, pady=4)
    soubory = ttk.Frame(okno)
    soubory.grid(row=4, column=0, columnspan=2, pady=4)
    ovladani = ttk.Frame(okno)
    ovladani.grid(row=5, column=0, columnspan=2, pady=4)
    ttk.Label(okno, text="Náhled po posledním ověření nebo zahájení přenosu").grid(row=6, column=0, columnspan=2, pady=4)
    nahled = tk.Text(okno, name="nahled", height=6, width=70, wrap="word", state="disabled")
    nahled.grid(row=7, column=0, columnspan=2, padx=10, pady=4, sticky="nsew")
    stav = ttk.Label(okno, name="stav", text="Koncept zatím není ověřený.", wraplength=720, justify="left")
    stav.grid(row=8, column=0, columnspan=2, padx=10, pady=5)

    # Vstup zůstává ve widgetech; nový koncept sestavíme pro každou operaci.
    def precti():
        return vytvor_koncept(prijemce.get(), predmet.get(), telo.get("1.0", "end-1c"), model["priloha"])

    # Náhled krátce odemkneme pouze pro výměnu obsahu.
    def nastav_nahled(text):
        nahled.configure(state="normal")
        nahled.delete("1.0", "end")
        nahled.insert("1.0", text)
        nahled.configure(state="disabled")

    def chyba_pole(chyba):
        stav.configure(text=str(chyba))
        nastav_nahled("Zpráva zatím není připravená.")
        pole = {"prijemce": prijemce, "predmet": predmet, "text": telo, "priloha": vybrat}
        pole.get(chyba.pole, prijemce).focus_set()

    def over():
        if model["busy"]:
            return
        try:
            zprava = sestav_zpravu(precti())
        except ChybaPole as chyba:
            chyba_pole(chyba)
            return
        nastav_nahled(nahled_s_prilohou(zprava))
        stav.configure(text="Zpráva je připravená. Nic se neodeslalo.")

    def vyber():
        if model["busy"]:
            return
        cesta = filedialog.askopenfilename(parent=okno, title="Vyberte cvičnou přílohu")
        if not cesta:
            stav.configure(text="Výběr přílohy zrušen.")
            return
        try:
            kandidat = vytvor_zpravu("eva@example.test", "jan@example.test", "Ověření přílohy", "Zkouška")
            pridej_prilohu(kandidat, cesta)
        except (OSError, ValueError):
            stav.configure(text="Příloha: soubor nelze načíst nebo překračuje 1 000 000 B.")
            return
        model["priloha"] = str(Path(cesta).resolve())
        soubor_text.configure(text="Příloha: " + Path(cesta).name)
        nastav_nahled("Náhled obnovte po změně přílohy.")
        stav.configure(text="Příloha vybrána. Obnovte náhled.")

    def odeber():
        if model["busy"]:
            return
        model["priloha"] = ""
        soubor_text.configure(text="Bez přílohy.")
        nastav_nahled("Náhled obnovte po změně přílohy.")
        stav.configure(text="Příloha odebrána. Obnovte náhled.")

    vybrat = ttk.Button(soubory, text="Vybrat přílohu", command=vyber)
    vybrat.pack(side="left", padx=4)
    odebrat = ttk.Button(soubory, text="Odebrat přílohu", command=odeber)
    odebrat.pack(side="left", padx=4)
    overit = ttk.Button(ovladani, text="Ověřit a zobrazit", command=over)
    overit.pack(side="left", padx=4)
    blokovane = [vybrat, odebrat, overit]

    nastav_nahled("Náhled zatím není ověřený.")
    prijemce.focus_set()
    okno.mainloop()


if __name__ == "__main__":
    hlavni()
