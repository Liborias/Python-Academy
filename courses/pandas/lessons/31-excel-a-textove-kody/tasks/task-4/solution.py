# %% Knihovny
import pandas as pd
from pathlib import Path


# %% Funkce pro úkol
def preskoc_poznamku(cesta, list):
    return pd.read_excel(cesta, sheet_name=list, skiprows=1, engine="openpyxl", keep_default_na=False, dtype={"kod":"str", "cena":"float64"})


# %% Vlastní ověření; při importu se neprovede.
if __name__ == "__main__":
    print(preskoc_poznamku("dilna.xlsx", "S poznámkou"))
