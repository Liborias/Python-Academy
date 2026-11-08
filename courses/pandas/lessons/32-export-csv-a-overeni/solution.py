# %% Knihovny
import pandas as pd
from pathlib import Path


# %% Funkce pro úkol
def uloz_csv(tabulka, cesta):
    cesta = Path(cesta)
    tabulka.to_csv(cesta, sep=";", decimal=",", encoding="utf-8", index=False)
    return cesta


# %% Vlastní ověření; při importu se neprovede.
if __name__ == "__main__":
    data = pd.read_csv("data.csv", sep=";", decimal=",", encoding="utf-8", keep_default_na=False, dtype={"kod":"str", "nazev":"str", "hodnota":"float64"})
    print("Uloženo:", uloz_csv(data, "vystup.csv"))
