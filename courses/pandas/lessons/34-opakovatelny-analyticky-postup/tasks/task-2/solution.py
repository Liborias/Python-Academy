# %% Knihovny
import pandas as pd
from pathlib import Path


# %% Funkce pro úkol
def souhrn_mist(tabulka):
    return tabulka.groupby("misto", as_index=False, sort=True).agg(pocet=("hodnota", "size"), prumer=("hodnota", "mean"))


# %% Vlastní ověření; při importu se neprovede.
if __name__ == "__main__":
    data = pd.DataFrame({"misto": ["Brno", "Praha", "Brno"], "hodnota": [1.5, 0.0, 2.5]})
    print(souhrn_mist(data))
