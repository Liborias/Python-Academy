# %% Knihovny
import pandas as pd
from pathlib import Path


# %% Funkce pro úkol
def uloz_excel(tabulka, cesta, list):
    cesta = Path(cesta)
    tabulka.to_excel(cesta, sheet_name=list, engine="openpyxl", index=False)
    return cesta


# %% Vlastní ověření; při importu se neprovede.
if __name__ == "__main__":
    data = pd.read_csv("data.csv", sep=";", decimal=",", encoding="utf-8", keep_default_na=False, dtype={"kod":"str", "nazev":"str", "cena":"float64"})
    print("Uloženo:", uloz_excel(data, "cenik.xlsx", "Ceník"))
