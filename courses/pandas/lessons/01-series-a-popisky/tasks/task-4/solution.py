# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def seznam_hodnot(serie):
    return serie.tolist()


# %% Vlastní ověření: tento blok se při importu neprovede.
if __name__ == "__main__":
    s = pd.Series([5, 0, 8], index=["A", "B", "C"], dtype="float64")
    print(seznam_hodnot(s))
