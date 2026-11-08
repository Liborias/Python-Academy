# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def cele_pocty(serie):
    return serie.astype("Int64")


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    s = pd.Series([2.0, None, 0.0, -1.0], name="kusy", dtype="float64")
    print(cele_pocty(s))
