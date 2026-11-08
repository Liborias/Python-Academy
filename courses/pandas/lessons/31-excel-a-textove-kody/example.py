# %% Knihovny
import pandas as pd
from pathlib import Path


# %% Funkce pro úkol
def nacti_cenik(cesta, list):
    return pd.read_excel(cesta, sheet_name=list, engine="openpyxl", keep_default_na=False, dtype={"kod":"str", "nazev":"str", "cena":"float64"})


# %% Vlastní ověření; při importu se neprovede.
if __name__ == "__main__":
    print(nacti_cenik("dilna.xlsx", "Ceník"))
