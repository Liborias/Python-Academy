# Ověřené kroky předchozích lekcí; zdroj se nemění.
from pathlib import Path
import pandas as pd
import numpy as np
from matplotlib.figure import Figure

def over_schema(tabulka, povinne):
    return isinstance(tabulka, pd.DataFrame) and tabulka.columns.is_unique and set(povinne).issubset(tabulka.columns)


def vycisti_mereni(tabulka):
    if not over_schema(tabulka, ["den", "kod", "teplota"]):
        raise ValueError("Nesprávné sloupce měření.")
    original = tabulka[["den", "kod", "teplota"]].copy().reset_index(drop=True)
    original.insert(0, "radek", range(1, len(original) + 1))
    data = original.copy()
    data["kod"] = data["kod"].str.strip()
    data["den"] = pd.to_datetime(data["den"].str.strip(), format="%Y-%m-%d", errors="coerce").astype("datetime64[us]")
    text = data["teplota"].str.strip().str.replace(",", ".", regex=False)
    data["teplota"] = pd.to_numeric(text, errors="coerce").astype("float64")
    duvod = pd.Series("", index=data.index, dtype="str")
    duvod.loc[data["kod"].eq("")] = "chybi_kod"
    duvod.loc[duvod.eq("") & data["den"].isna()] = "neplatne_datum"
    duvod.loc[duvod.eq("") & ~np.isfinite(data["teplota"])] = "neplatna_teplota"
    cista = data.loc[duvod.eq("")].reset_index(drop=True)
    odmitnuta = original.assign(duvod=duvod).loc[duvod.ne("")].reset_index(drop=True)
    return {"cista": cista, "odmitnuta": odmitnuta}


def spoj_a_shrn(cista, mista):
    if not over_schema(mista, ["kod", "nazev", "oblast"]):
        raise ValueError("Nesprávné sloupce katalogu.")
    spoj = cista.merge(mista[["kod", "nazev", "oblast"]], on="kod", how="left", sort=False, validate="many_to_one", indicator=True)
    spojena = spoj.loc[spoj["_merge"].eq("both"), ["radek", "den", "kod", "teplota", "nazev", "oblast"]].reset_index(drop=True)
    nesparovana = spoj.loc[spoj["_merge"].eq("left_only"), ["radek", "den", "kod", "teplota"]].reset_index(drop=True)
    podle_mist = spojena.groupby(["kod", "nazev"], as_index=False, sort=True).agg(pocet=("teplota", "size"), prumer=("teplota", "mean"))
    podle_dnu = spojena.groupby("den", as_index=False, sort=True).agg(pocet=("teplota", "size"), prumer=("teplota", "mean"))
    return {"spojena": spojena, "nesparovana": nesparovana, "podle_mist": podle_mist, "podle_dnu": podle_dnu}


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


def over_prehled(prehled, ocekavane):
    if prehled.keys() != ocekavane.keys():
        return False
    try:
        for jmeno in ocekavane:
            pd.testing.assert_frame_equal(prehled[jmeno], ocekavane[jmeno], check_exact=False, rtol=1e-12, atol=1e-12)
    except (AssertionError, TypeError, ValueError):
        return False
    return True
