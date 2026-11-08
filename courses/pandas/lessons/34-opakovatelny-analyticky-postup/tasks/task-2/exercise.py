# %% Knihovny
import pandas as pd
from pathlib import Path


# %% Funkce pro úkol
def souhrn_mist(tabulka):
    # TODO: Doplňte podle zadání; správných postupů může být více.
    return None


# %% Vlastní ověření; při importu se neprovede.
if __name__ == "__main__":
    data = pd.DataFrame({"misto": ["Brno", "Praha", "Brno"], "hodnota": [1.5, 0.0, 2.5]})
    print(souhrn_mist(data))
