# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def souhrn_mereni(serie):
    # TODO: vraťte výsledek podle zadání; původní vstupy neměňte.
    return None


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    s = pd.Series([0.0, None, 12.0], name="mereni", dtype="float64")
    print(souhrn_mereni(s))
