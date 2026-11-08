# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def vyber_nad_prumerem(serie):
    return serie.loc[serie > serie.mean()].copy()


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    s = pd.Series([10.0, 10.0, 12.0, 1000.0, None], name="mereni", dtype="float64")
    print(vyber_nad_prumerem(s))
