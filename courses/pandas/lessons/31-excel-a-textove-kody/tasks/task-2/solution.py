# %% Knihovny
import pandas as pd
from pathlib import Path


# %% Funkce pro úkol
def nazvy_listu(cesta):
    with pd.ExcelFile(cesta, engine="openpyxl") as sesit:
        return sesit.sheet_names


# %% Vlastní ověření; při importu se neprovede.
if __name__ == "__main__":
    print(nazvy_listu("dilna.xlsx"))
