from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog
from koncept import vytvor_koncept
from zpravy import vytvor_zpravu, over_adresu, nahled_zpravy
from prilohy import pridej_prilohu
import os
import queue
import threading
import smtplib
from email.parser import BytesParser
from email.policy import default
from cvicna_posta import cvicna_posta
from odesilani import odesli_do_zachytu
from nastaveni import nacti_nastaveni
import json
import tempfile
from prenos import predat_zpravu
from priprava import ChybaPole, sestav_zpravu, nahled_s_prilohou


from dilna import uloz_koncept, nacti_koncept


def cesty_projektu(soubor, domov):
    # Zdroje určuje soubor programu; uživatelský cíl určuje zadaný domov.
    return {"data": Path(soubor).resolve().parent / "data",
            "koncepty": Path(domov).expanduser().resolve()}


def hlavni(posta):
    cesty = cesty_projektu(__file__, Path.home())
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

    def precti():
        return vytvor_koncept(prijemce.get(), predmet.get(), telo.get("1.0", "end-1c"), model["priloha"])

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

    def uloz():
        if model["busy"]:
            return
        cesta = filedialog.asksaveasfilename(parent=okno, title="Uložit koncept", initialdir=str(cesty["koncepty"]), defaultextension=".json")
        if not cesta:
            stav.configure(text="Ukládání zrušeno.")
            return
        try:
            uloz_koncept(cesta, precti())
        except (OSError, ValueError):
            stav.configure(text="Koncept se nepodařilo uložit.")
            return
        stav.configure(text="Koncept uložen. Nejde o potvrzení přenosu.")

    def nacti():
        if model["busy"]:
            return
        cesta = filedialog.askopenfilename(parent=okno, title="Načíst koncept", initialdir=str(cesty["koncepty"]))
        if not cesta:
            stav.configure(text="Načítání zrušeno.")
            return
        try:
            kandidat = nacti_koncept(cesta)
        except (OSError, ValueError):
            stav.configure(text="Koncept se nepodařilo načíst.")
            return
        pouzij_koncept(kandidat, "Koncept načten. Před předáním jej ověřte.")

    def pouzij_koncept(kandidat, hlaska):
        # Až po ověření celého souboru nahrazujeme všechna pole formuláře.
        prijemce.delete(0, "end")
        prijemce.insert(0, kandidat["prijemce"])
        predmet.delete(0, "end")
        predmet.insert(0, kandidat["predmet"])
        telo.delete("1.0", "end")
        telo.insert("1.0", kandidat["text"])
        model["priloha"] = kandidat["priloha"]
        soubor_text.configure(text="Příloha: " + Path(model["priloha"]).name if model["priloha"] else "Bez přílohy.")
        nastav_nahled("Načtený koncept zatím není ověřený.")
        stav.configure(text=hlaska)


    def ukazka():
        if model["busy"]:
            return
        try:
            kandidat = nacti_koncept(cesty["data"] / "vychozi-koncept.json")
        except (OSError, ValueError):
            stav.configure(text="Ukázkový koncept není dostupný. Zkontrolujte složku data.")
            return
        pouzij_koncept(kandidat, "Ukázkový koncept načten. Před předáním jej ověřte.")

    ulozit = ttk.Button(ovladani, text="Uložit koncept", command=uloz)
    ulozit.pack(side="left", padx=4)
    nacist = ttk.Button(ovladani, text="Načíst koncept", command=nacti)
    nacist.pack(side="left", padx=4)
    ukazkovy = ttk.Button(ovladani, text="Načíst ukázku", command=ukazka)
    ukazkovy.pack(side="left", padx=4)
    blokovane.extend([ulozit, nacist, ukazkovy])

    def klavesa_ulozit(udalost):
        uloz()
        return "break"

    def klavesa_nacist(udalost):
        nacti()
        return "break"

    def klavesa_overit(udalost):
        over()
        return "break"

    # Vlastní vazba na Text zachytí Ctrl+O před jeho běžnou třídní vazbou.
    for widget in (okno, prijemce, predmet, telo, nahled):
        widget.bind("<Control-s>", klavesa_ulozit)
        widget.bind("<Control-o>", klavesa_nacist)
        widget.bind("<Control-Return>", klavesa_overit)

    vysledky = queue.Queue()
    rezim = tk.StringVar(okno, value="prijmout")
    zachyt_text = ttk.Label(okno, name="zachyt", text="Zachyceno: 0", wraplength=720)
    zachyt_text.grid(row=9, column=0, columnspan=2, padx=10, pady=4)
    rezimy = ttk.Frame(okno)
    rezimy.grid(row=10, column=0, columnspan=2, pady=4)
    prenos = ttk.Frame(okno)
    prenos.grid(row=11, column=0, columnspan=2, pady=4)

    def zobraz_zachyt():
        zpravy = posta.zpravy
        popis = f"Zachyceno: {len(zpravy)}"
        if zpravy:
            posledni = BytesParser(policy=default).parsebytes(zpravy[-1].data)
            popis += f" | poslední předmět: {posledni['Subject']}"
        zachyt_text.configure(text=popis)

    def zkontroluj():
        zobraz_zachyt()
        if model["nutna_kontrola"]:
            model["nutna_kontrola"] = False
            stav.configure(text="Záchyt zkontrolován. Další pokus může vytvořit kopii zprávy.")

    def vyzvedni():
        try:
            vysledek = vysledky.get_nowait()
        except queue.Empty:
            okno.after(25, vyzvedni)
            return
        model["busy"] = False
        model["nutna_kontrola"] = vysledek == "nejiste"
        for tlacitko in blokovane:
            tlacitko.configure(state="normal")
        zpravy = {"prijato": "Zprávu převzal místní záchyt.",
                  "odmitnuto": "Příjemce byl odmítnut. Zpráva nebyla převzata.",
                  "nejiste": "Přenos není potvrzený. Před novým pokusem zkontrolujte záchyt.",
                  "chyba": "Spojení nebo SMTP služba selhaly. Ověřte nastavení."}
        stav.configure(text=zpravy[vysledek])
        zobraz_zachyt()

    def odesli():
        if model["busy"]:
            return
        if model["nutna_kontrola"]:
            stav.configure(text="Nejprve zkontrolujte záchyt před dalším pokusem.")
            return
        try:
            nastaveni = nacti_nastaveni(os.environ, posta.port)
            zprava = sestav_zpravu(precti())
        except ChybaPole as chyba:
            chyba_pole(chyba)
            return
        except ValueError:
            stav.configure(text="Neplatné SMTP nastavení. Opravte prostředí a spusťte program znovu.")
            return
        # EmailMessage už obsahuje přesné bajty přílohy; pracovník nečte cestu z disku.
        nastav_nahled(nahled_s_prilohou(zprava))
        posta.nastav_rezim(rezim.get())
        model["busy"] = True
        for tlacitko in blokovane:
            tlacitko.configure(state="disabled")
        stav.configure(text="Předávám zprávu místnímu záchytu...")
        threading.Thread(target=predat_zpravu,
                         args=(zprava, nastaveni["host"], nastaveni["port"], nastaveni["timeout"], vysledky),
                         daemon=True).start()
        okno.after(25, vyzvedni)

    for text, hodnota in [("Přijetí", "prijmout"), ("Odmítnutí příjemce", "odmitnout"), ("Opožděné potvrzení", "pomalu")]:
        volba = ttk.Radiobutton(rezimy, text=text, variable=rezim, value=hodnota)
        volba.pack(side="left", padx=4)
        blokovane.append(volba)
    odeslat = ttk.Button(prenos, text="Předat místnímu záchytu", command=odesli)
    odeslat.pack(side="left", padx=4)
    blokovane.append(odeslat)
    ttk.Button(prenos, text="Zkontrolovat záchyt", command=zkontroluj).pack(side="left", padx=4)

    nastav_nahled("Náhled zatím není ověřený.")
    prijemce.focus_set()
    okno.mainloop()


if __name__ == "__main__":
    with cvicna_posta() as posta:
        hlavni(posta)
