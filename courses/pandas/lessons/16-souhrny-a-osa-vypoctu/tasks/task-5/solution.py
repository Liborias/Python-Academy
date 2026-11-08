# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def souhrn_mereni(serie):
    return {"zaznamy": len(serie), "dostupne": int(serie.count()), "soucet": serie.sum(min_count=1), "prumer": serie.mean()}


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    s = pd.Series([0.0, None, 12.0], name="mereni", dtype="float64")
    print(souhrn_mereni(s))
