# %% Knihovny a ověřené předchozí kroky
from pathlib import Path
import pandas as pd
import numpy as np
from matplotlib.figure import Figure
from predchozi import over_schema, vycisti_mereni, spoj_a_shrn


# %% Aktuální krok projektu
def napis_zpravu(cisteni, prehled):
    mereni = prehled["spojena"]
    prumer = f"{mereni['teplota'].mean():.2f}".replace(".", ",") if len(mereni) else "neurčen (žádná spárovaná měření)"
    return ("# Analytická dílna\n\n"
            f"Přijaté záznamy: {len(cisteni['cista'])}.\n"
            f"Odmítnuté záznamy: {len(cisteni['odmitnuta'])}.\n"
            f"Spárovaná měření: {len(mereni)}.\n"
            f"Nespárovaná měření: {len(prehled['nesparovana'])}.\n"
            f"Celkový průměr: {prumer} °C.\n\n"
            "Průměr počítáme ze všech spárovaných měření, nikoli průměrem průměrů stanic.\n"
            "Cvičná data popisují jen dodaná měření; neprokazují příčinu rozdílů ani dlouhodobé počasí.\n")


def vytvor_vystupy(cisteni, prehled, slozka):
    slozka = Path(slozka)
    slozka.mkdir(parents=True, exist_ok=True)
    csv = slozka / "stanice.csv"
    excel = slozka / "prehled.xlsx"
    graf = slozka / "teploty.png"
    zprava = slozka / "zprava.md"
    prehled["podle_mist"].to_csv(csv, sep=";", decimal=",", encoding="utf-8", index=False)
    with pd.ExcelWriter(excel, engine="openpyxl") as zapis:
        prehled["podle_mist"].to_excel(zapis, sheet_name="Stanice", index=False)
        prehled["podle_dnu"].to_excel(zapis, sheet_name="Dny", index=False)
        prehled["nesparovana"].to_excel(zapis, sheet_name="Nespárovaná", index=False)
        cisteni["odmitnuta"].to_excel(zapis, sheet_name="Odmítnutá", index=False)
    fig = Figure(figsize=(6, 4), layout="constrained")
    ax = fig.subplots()
    stanice = prehled["podle_mist"]
    ax.bar(stanice["kod"], stanice["prumer"])
    ax.set(title="Průměrné teploty podle stanic", xlabel="Stanice (kód)", ylabel="Teplota (°C)")
    fig.savefig(graf, dpi=120)
    zprava.write_text(napis_zpravu(cisteni, prehled), encoding="utf-8")
    return {"csv": csv, "excel": excel, "graf": graf, "zprava": zprava}


# %% Vlastní ověření nad přiloženými zdroji.
if __name__ == "__main__":
    raw = pd.read_csv("mereni.csv", sep=";", encoding="utf-8", dtype="str", keep_default_na=False)
    mista = pd.read_csv("mista.csv", sep=";", encoding="utf-8", dtype="str", keep_default_na=False)
    cisteni = vycisti_mereni(raw)
    prehled = spoj_a_shrn(cisteni["cista"], mista)
    print(napis_zpravu(cisteni, prehled))
    print("Uloženo:", vytvor_vystupy(cisteni, prehled, "vystupy"))
