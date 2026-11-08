# %% Knihovny a ověřené předchozí kroky
from pathlib import Path
import pandas as pd
import numpy as np
from predchozi import over_schema, vycisti_mereni


# %% Aktuální krok projektu
def spoj_a_shrn(cista, mista):
    if not over_schema(mista, ["kod", "nazev", "oblast"]):
        raise ValueError("Nesprávné sloupce katalogu.")
    spoj = cista.merge(mista[["kod", "nazev", "oblast"]], on="kod", how="left", sort=False, validate="many_to_one", indicator=True)
    spojena = spoj.loc[spoj["_merge"].eq("both"), ["radek", "den", "kod", "teplota", "nazev", "oblast"]].reset_index(drop=True)
    nesparovana = spoj.loc[spoj["_merge"].eq("left_only"), ["radek", "den", "kod", "teplota"]].reset_index(drop=True)
    podle_mist = spojena.groupby(["kod", "nazev"], as_index=False, sort=True).agg(pocet=("teplota", "size"), prumer=("teplota", "mean"))
    podle_dnu = spojena.groupby("den", as_index=False, sort=True).agg(pocet=("teplota", "size"), prumer=("teplota", "mean"))
    return {"spojena": spojena, "nesparovana": nesparovana, "podle_mist": podle_mist, "podle_dnu": podle_dnu}


# %% Vlastní ověření nad přiloženými zdroji.
if __name__ == "__main__":
    raw = pd.read_csv("mereni.csv", sep=";", encoding="utf-8", dtype="str", keep_default_na=False)
    mista = pd.read_csv("mista.csv", sep=";", encoding="utf-8", dtype="str", keep_default_na=False)
    cisteni = vycisti_mereni(raw)
    print(spoj_a_shrn(cisteni["cista"], mista))
