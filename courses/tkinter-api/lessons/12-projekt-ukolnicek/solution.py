import json
import tkinter as tk
from tkinter import ttk, filedialog

# Souborové funkce neznají okno. Nejdřív se ověří celý nový model.
def uloz_ukoly(cesta, ukoly):
    with open(cesta, "w", encoding="utf-8") as soubor:
        json.dump(ukoly, soubor, ensure_ascii=False, indent=2)

def nacti_ukoly(cesta):
    with open(cesta, encoding="utf-8") as soubor:
        data = json.load(soubor)
    if not isinstance(data, list):
        raise ValueError("Očekávám seznam úkolů.")
    vysledek = []
    for zaznam in data:
        if not isinstance(zaznam, dict):
            raise ValueError("Úkol musí být objekt.")
        if not isinstance(zaznam.get("nazev"), str) or not zaznam["nazev"].strip():
            raise ValueError("Úkol potřebuje neprázdný název.")
        if not isinstance(zaznam.get("hotovo"), bool):
            raise ValueError("Hotovo musí být true nebo false.")
        vysledek.append({"nazev": zaznam["nazev"], "hotovo": zaznam["hotovo"]})
    return vysledek


def hlavni():
    okno = tk.Tk()
    okno.title("Můj úkolníček")
    okno.geometry("640x540")
    okno.minsize(520, 440)
    okno.columnconfigure(0, weight=1)
    okno.rowconfigure(1, weight=1)
    ukoly = []
    vstup = ttk.Entry(okno)
    vstup.grid(row=0, column=0, padx=12, pady=8, sticky="ew")
    seznam = tk.Listbox(okno, selectmode="browse", exportselection=False, height=8)
    seznam.grid(row=1, column=0, padx=(12, 0), pady=8, sticky="nsew")
    posuvnik = ttk.Scrollbar(okno, orient="vertical", command=seznam.yview)
    posuvnik.grid(row=1, column=1, padx=(0, 12), pady=8, sticky="ns")
    seznam.configure(yscrollcommand=posuvnik.set)
    detail = tk.Text(okno, height=3, width=40, wrap="word")
    detail.grid(row=2, column=0, columnspan=2, padx=12, pady=8, sticky="ew")
    zprava = ttk.Label(okno, text="Úkolníček je připravený.")
    zprava.grid(row=4, column=0, columnspan=2, pady=8)

    def nastav_detail(obsah):
        detail.configure(state="normal")
        detail.delete("1.0", "end")
        detail.insert("1.0", obsah)
        detail.configure(state="disabled")

    def zobraz_detail(udalost=None):
        vyber = seznam.curselection()
        if not vyber:
            nastav_detail("Vyberte úkol pro podrobnosti.")
            return
        ukol = ukoly[vyber[0]]
        if ukol["hotovo"]:
            stav = "hotovo"
        else:
            stav = "čeká"
        nastav_detail(f"Úkol: {ukol['nazev']}\nStav: {stav}")

    def obnov():
        seznam.delete(0, tk.END)
        for ukol in ukoly:
            if ukol["hotovo"]:
                znacka = "[hotovo] "
            else:
                znacka = "[ ] "
            seznam.insert(tk.END, znacka + ukol["nazev"])
        zobraz_detail()

    def pridej():
        nazev = vstup.get().strip()
        if not nazev:
            zprava.configure(text="Napište název úkolu.")
            return
        ukoly.append({"nazev": nazev, "hotovo": False})
        obnov()
        vstup.delete(0, tk.END)
        zprava.configure(text=f"Přidáno: {nazev}.")

    # Dokončení nastaví True, opakované potvrzení už stav nepřepne zpět.
    def dokonci():
        vyber = seznam.curselection()
        if not vyber:
            zprava.configure(text="Nejprve vyberte úkol.")
            return
        index = vyber[0]
        ukoly[index]["hotovo"] = True
        nazev = ukoly[index]["nazev"]
        obnov()
        seznam.selection_set(index)
        seznam.see(index)
        zobraz_detail()
        zprava.configure(text=f"Dokončeno: {nazev}.")

    def odstran():
        vyber = seznam.curselection()
        if not vyber:
            zprava.configure(text="Nejprve vyberte úkol.")
            return
        ukol = ukoly.pop(vyber[0])
        obnov()
        zprava.configure(text=f"Odstraněno: {ukol['nazev']}.")

    def uloz():
        cesta = filedialog.asksaveasfilename(parent=okno, defaultextension=".json", filetypes=[("JSON", "*.json")])
        if not cesta:
            zprava.configure(text="Ukládání zrušeno.")
            return
        try:
            uloz_ukoly(cesta, ukoly)
        except OSError:
            zprava.configure(text="Soubor se nepodařilo uložit.")
            return
        zprava.configure(text="Úkoly uloženy.")

    def nacti():
        cesta = filedialog.askopenfilename(parent=okno, filetypes=[("JSON", "*.json")])
        if not cesta:
            zprava.configure(text="Načítání zrušeno.")
            return
        try:
            nactene = nacti_ukoly(cesta)
        except (OSError, ValueError):
            zprava.configure(text="Soubor se nepodařilo načíst.")
            return
        ukoly[:] = nactene
        obnov()
        zprava.configure(text="Úkoly načteny.")

    ovladani = ttk.Frame(okno)
    ovladani.grid(row=3, column=0, columnspan=2, pady=8)
    for sloupec, (nazev, funkce) in enumerate([("Přidat", pridej), ("Dokončit", dokonci), ("Odstranit", odstran), ("Uložit JSON", uloz), ("Načíst JSON", nacti)]):
        ttk.Button(ovladani, text=nazev, command=funkce).grid(row=0, column=sloupec, padx=4)
    seznam.bind("<<ListboxSelect>>", zobraz_detail)
    vstup.focus_set()
    obnov()
    okno.mainloop()


if __name__ == "__main__":
    hlavni()
