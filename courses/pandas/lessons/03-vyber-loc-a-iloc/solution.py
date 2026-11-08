# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def vyber_podle_popisku(serie, popisky):
    return serie.loc[popisky].copy()


# %% Vlastní ověření: tento blok se při importu neprovede.
if __name__ == "__main__":
    s = pd.Series([18, 21, 16], index=["Brno", "Praha", "Zlin"], name="teplota", dtype="float64")
    print(vyber_podle_popisku(s, ["Zlin", "Brno"]))
