# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def celkove_trzby(ceny, pocty):
    return (ceny * pocty).sort_index().rename("trzba")


# %% Vlastní ověření: tento blok se při importu neprovede.
if __name__ == "__main__":
    ceny = pd.Series([50, 75], index=["caj", "kava"], dtype="float64")
    pocty = pd.Series([3, 2], index=["kava", "caj"], dtype="float64")
    print(celkove_trzby(ceny, pocty))
