# %% Knihovny
import pandas as pd
from pathlib import Path


# %% Funkce pro úkol
def nacti_dva_listy(cesta):
    with pd.ExcelFile(cesta, engine="openpyxl") as sesit:
        cenik = pd.read_excel(sesit, sheet_name="Ceník", keep_default_na=False, dtype={"kod":"str", "nazev":"str", "cena":"float64"})
        prodeje = pd.read_excel(sesit, sheet_name="Prodeje", keep_default_na=False, dtype={"kod":"str", "kusy":"int64"})
    return {"cenik": cenik, "prodeje": prodeje}


# %% Vlastní ověření; při importu se neprovede.
if __name__ == "__main__":
    vysledek = nacti_dva_listy("dilna.xlsx")
    print(vysledek)
