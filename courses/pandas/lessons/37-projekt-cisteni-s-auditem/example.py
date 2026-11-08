# %% Knihovny a ověřené předchozí kroky
from pathlib import Path
import pandas as pd
import numpy as np
from predchozi import over_schema


# %% Aktuální krok projektu
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


# %% Vlastní ověření nad přiloženými zdroji.
if __name__ == "__main__":
    raw = pd.read_csv("mereni.csv", sep=";", encoding="utf-8", dtype="str", keep_default_na=False)
    mista = pd.read_csv("mista.csv", sep=";", encoding="utf-8", dtype="str", keep_default_na=False)
    result = vycisti_mereni(raw)
    print(result)
