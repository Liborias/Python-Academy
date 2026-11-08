# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def serad_podle_popisku(serie):
    return serie.sort_index()


# %% Vlastní ověření: tento blok se při importu neprovede.
if __name__ == "__main__":
    s = pd.Series([4, 7, 1], index=["B", "C", "A"], name="hodnota", dtype="float64")
    print(serad_podle_popisku(s))
