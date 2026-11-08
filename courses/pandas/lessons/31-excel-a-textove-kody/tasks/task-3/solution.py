# %% Knihovny
import pandas as pd
from pathlib import Path


# %% Funkce pro úkol
def nacti_vybrane_sloupce(cesta, list):
    data = pd.read_excel(cesta, sheet_name=list, usecols=["kod", "nazev"], engine="openpyxl", keep_default_na=False, dtype={"kod":"str", "nazev":"str"})
    return data[["kod", "nazev"]]


# %% Vlastní ověření; při importu se neprovede.
if __name__ == "__main__":
    print(nacti_vybrane_sloupce("dilna.xlsx", "Výběr"))
