# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def souhrn_hodnot(serie):
    return {"soucet": serie.sum(), "prumer": serie.mean()}


# %% Vlastní ověření: tento blok se při importu neprovede.
if __name__ == "__main__":
    s = pd.Series([10, None, 20], name="hodnota", dtype="float64")
    print(souhrn_hodnot(s))
