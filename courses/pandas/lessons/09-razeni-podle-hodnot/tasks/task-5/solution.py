# %% Knihovny
import pandas as pd


# %% Funkce pro úkol
def poradi_mereni(serie, vzestupne):
    return serie.sort_values(ascending=vzestupne, kind="stable", na_position="first")


# %% Vlastní ověření: při importu se tento blok neprovede.
if __name__ == "__main__":
    s = pd.Series([18.0, None, 15.0, 18.0], index=["B", "D", "A", "C"], name="teplota", dtype="float64")
    print(poradi_mereni(s, False))
