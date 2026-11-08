# %% Knihovny
import pandas as pd
from pathlib import Path


# %% Funkce pro úkol
def zpracuj_mereni(cesta):
    data = pd.read_csv(cesta, sep=";", encoding="utf-8", keep_default_na=False, dtype="str")
    data = data[["misto", "hodnota"]].copy()
    data["misto"] = data["misto"].str.strip().replace("", pd.NA)
    text = data["hodnota"].str.strip().str.replace(",", ".", regex=False)
    data["hodnota"] = pd.to_numeric(text, errors="coerce").astype("float64")
    return data.dropna(subset=["misto", "hodnota"]).reset_index(drop=True)


# %% Vlastní ověření; při importu se neprovede.
if __name__ == "__main__":
    print(zpracuj_mereni("mereni.csv"))
