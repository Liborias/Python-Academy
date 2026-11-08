# %% Knihovny
import pandas as pd
from pathlib import Path


# %% Funkce pro úkol
def uloz_pro_excel(tabulka, cesta):
    # TODO: Doplňte podle zadání; správných postupů může být více.
    return None


# %% Vlastní ověření; při importu se neprovede.
if __name__ == "__main__":
    data = pd.read_csv("data.csv", sep=";", decimal=",", encoding="utf-8", keep_default_na=False, dtype={"kod":"str", "nazev":"str", "hodnota":"float64"})
    print("Uloženo:", uloz_pro_excel(data, "pro_excel.csv"))
