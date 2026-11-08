# %% Knihovny
import pandas as pd
from pathlib import Path


# %% Funkce pro úkol
def over_excel(tabulka, cesta, list):
    try:
        nactene = pd.read_excel(cesta, sheet_name=list, engine="openpyxl", keep_default_na=False, dtype={"kod":"str", "nazev":"str", "cena":"float64"})
        pd.testing.assert_frame_equal(tabulka.reset_index(drop=True), nactene, check_exact=False, rtol=1e-12, atol=1e-12)
    except (ValueError, AssertionError):
        return False
    return True


# %% Vlastní ověření; při importu se neprovede.
if __name__ == "__main__":
    data = pd.read_csv("data.csv", sep=";", decimal=",", encoding="utf-8", keep_default_na=False, dtype={"kod":"str", "nazev":"str", "cena":"float64"})
    data.to_excel("cenik.xlsx", sheet_name="Ceník", engine="openpyxl", index=False)
    print("Obsah souhlasí:", over_excel(data, "cenik.xlsx", "Ceník"))
