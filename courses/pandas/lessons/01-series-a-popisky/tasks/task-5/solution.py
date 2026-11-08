# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def pocet_mereni(serie):
    return len(serie)


# %% Vlastní ověření: tento blok se při importu neprovede.
if __name__ == "__main__":
    s = pd.Series([5, None, 8], dtype="float64")
    print(pocet_mereni(s))
