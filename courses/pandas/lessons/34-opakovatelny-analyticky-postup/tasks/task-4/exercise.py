# %% Knihovny
import pandas as pd
from pathlib import Path


# %% Funkce pro úkol
def uloz_souhrn(tabulka, cesta):
    # TODO: Doplňte podle zadání; správných postupů může být více.
    return None


# %% Vlastní ověření; při importu se neprovede.
if __name__ == "__main__":
    data = pd.DataFrame({"misto": ["Brno", "Praha"], "pocet": [2, 1], "prumer": [1.5, 0.0]})
    print("Uloženo:", uloz_souhrn(data, "souhrn.csv"))
