# %% Knihovny
import pandas as pd
from pathlib import Path


# %% Funkce pro úkol
def zachovej_kody(tabulka, cesta):
    # TODO: Doplňte podle zadání; správných postupů může být více.
    return None


# %% Vlastní ověření; při importu se neprovede.
if __name__ == "__main__":
    data = pd.DataFrame({"kod": ["001", "NA", "010"], "pocet": [2, 0, 3]})
    print("Uloženo:", zachovej_kody(data, "kody.xlsx"))
