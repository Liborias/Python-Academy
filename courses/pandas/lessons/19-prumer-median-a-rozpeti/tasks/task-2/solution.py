# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def rozpeti_hodnot(serie):
    return serie.max() - serie.min()


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    s = pd.Series([10.0, 12.0, 1000.0, None], dtype="float64")
    print(rozpeti_hodnot(s))
