# %% Knihovny
import pandas as pd
from pathlib import Path


# %% Funkce pro úkol
def uloz_dva_listy(cenik, prodeje, cesta):
    cesta = Path(cesta)
    with pd.ExcelWriter(cesta, engine="openpyxl") as zapis:
        cenik.to_excel(zapis, sheet_name="Ceník", index=False)
        prodeje.to_excel(zapis, sheet_name="Prodeje", index=False)
    return cesta


# %% Vlastní ověření; při importu se neprovede.
if __name__ == "__main__":
    data = pd.read_csv("data.csv", sep=";", decimal=",", encoding="utf-8", keep_default_na=False, dtype={"kod":"str", "nazev":"str", "cena":"float64"})
    prodeje = pd.DataFrame({"kod": ["010", "001"], "kusy": [0, 2]})
    print("Uloženo:", uloz_dva_listy(data, prodeje, "prehled.xlsx"))
